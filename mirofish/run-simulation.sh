#!/bin/bash
# run-simulation.sh — MiroFish Simulation Runner
# Source: ~/developer/mirofish/run-simulation.sh
# Version: 1.0 | 2026-04-03

set -e

# Configuration
MIROFISH_API="http://localhost:3000/api"
SCENARIOS_DIR="$HOME/developer/mirofish/scenarios"
OUTPUT_DIR="$PWD/docs/simulations"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

usage() {
    cat << EOF
Usage: $(basename "$0") <scenario> [options]

MiroFish Simulation Runner

Arguments:
  scenario              Name of scenario to run (or 'test' for quick test)
                        Available scenarios:
                          - hitl-handoff
                          - pre-fca-sandbox
                          - fraud-social-eng
                          - gtm-reaction
                          - ux-validation
                          - fraud-stress-test
                          - market-adoption
                          - test (quick 50-agent validation)

Options:
  -a, --agents N        Override default agent count
  -r, --rounds N        Override default round count
  -o, --output DIR      Output directory (default: ./docs/simulations/)
  -s, --seed N          Random seed for reproducibility
  --dry-run             Validate scenario without executing
  --help                Show this help message

Examples:
  $(basename "$0") test
  $(basename "$0") hitl-handoff --agents 300 --rounds 40
  $(basename "$0") pre-fca-sandbox -o /tmp/simulations
  $(basename "$0") fraud-stress-test --seed 42

EOF
    exit 1
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse arguments
SCENARIO=""
AGENTS_OVERRIDE=""
ROUNDS_OVERRIDE=""
SEED=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -a|--agents)
            AGENTS_OVERRIDE="$2"
            shift 2
            ;;
        -r|--rounds)
            ROUNDS_OVERRIDE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -s|--seed)
            SEED="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            if [ -z "$SCENARIO" ]; then
                SCENARIO="$1"
                shift
            else
                log_error "Unknown argument: $1"
                usage
            fi
            ;;
    esac
done

if [ -z "$SCENARIO" ]; then
    log_error "Scenario name required"
    usage
fi

# Check MiroFish API health
check_api() {
    log_info "Checking MiroFish API health..."
    if ! curl -s "$MIROFISH_API/health" > /dev/null 2>&1; then
        log_error "MiroFish API not responding at $MIROFISH_API"
        echo ""
        echo "Start MiroFish services:"
        echo "  cd ~/mirofish-engine && docker compose up -d"
        exit 1
    fi
    log_success "API healthy"
}

# Load scenario configuration
load_scenario() {
    local scenario_file="$SCENARIOS_DIR/${SCENARIO}.yml"
    
    if [ ! -f "$scenario_file" ]; then
        log_error "Scenario not found: $SCENARIO"
        echo ""
        echo "Available scenarios:"
        ls -1 "$SCENARIOS_DIR"/*.yml 2>/dev/null | xargs -n1 basename | sed 's/.yml//'
        exit 1
    fi
    
    log_info "Loading scenario: $SCENARIO"
    cat "$scenario_file"
}

# Run simulation via API
run_simulation() {
    local scenario_file="$SCENARIOS_DIR/${SCENARIO}.yml"
    local timestamp=$(date +%Y%m%d-%H%M%S)
    local simulation_id="${SCENARIO}-${timestamp}"
    local output_file="$OUTPUT_DIR/${simulation_id}.json"
    
    # Create output directory
    mkdir -p "$OUTPUT_DIR"
    
    log_info "Starting simulation: $simulation_id"
    
    if [ "$DRY_RUN" = true ]; then
        log_info "Dry run mode - validating scenario only"
        # Validate YAML syntax
        if command -v python3 &> /dev/null; then
            python3 -c "import yaml; yaml.safe_load(open('$scenario_file'))" && \
                log_success "Scenario YAML valid" || \
                log_error "Invalid YAML syntax"
        fi
        return 0
    fi
    
    # Apply overrides
    local agents_json=""
    local rounds_json=""
    local seed_json=""
    
    [ -n "$AGENTS_OVERRIDE" ] && agents_json=", \"agents\": $AGENTS_OVERRIDE"
    [ -n "$ROUNDS_OVERRIDE" ] && rounds_json=", \"rounds\": $ROUNDS_OVERRIDE"
    [ -n "$SEED" ] && seed_json=", \"seed\": $SEED"
    
    # Build API request
    local request_body=$(cat << EOF
{
    "scenario": "$SCENARIO",
    "simulation_id": "$simulation_id"$agents_json$rounds_json$seed_json,
    "config_file": "$scenario_file"
}
EOF
)
    
    log_info "Sending request to MiroFish API..."
    
    # Execute simulation
    local response=$(curl -s -X POST "$MIROFISH_API/simulations" \
        -H "Content-Type: application/json" \
        -d "$request_body")
    
    # Extract job ID
    local job_id=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('job_id', 'unknown'))" 2>/dev/null || echo "unknown")
    
    log_info "Simulation started (job_id: $job_id)"
    log_info "Polling for results..."
    
    # Poll for completion
    local status="running"
    local progress=0
    
    while [ "$status" = "running" ] || [ "$status" = "pending" ]; do
        sleep 5
        
        local status_response=$(curl -s "$MIROFISH_API/simulations/$job_id/status")
        status=$(echo "$status_response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', 'unknown'))" 2>/dev/null || echo "error")
        progress=$(echo "$status_response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('progress', 0))" 2>/dev/null || echo "?")
        
        printf "\r  Progress: %s%% - Status: %s" "$progress" "$status"
    done
    
    echo ""
    
    if [ "$status" = "completed" ]; then
        log_success "Simulation completed!"
        
        # Fetch results
        log_info "Fetching results..."
        curl -s "$MIROFISH_API/simulations/$job_id/results" > "$output_file"
        
        log_success "Results saved to: $output_file"
        
        # Display summary
        echo ""
        echo "=== Simulation Summary ==="
        python3 -c "
import json
with open('$output_file') as f:
    data = json.load(f)
    print(f\"Scenario: {data.get('scenario', 'N/A')}\")
    print(f\"Agents: {data.get('parameters', {}).get('agents', 'N/A')}\")
    print(f\"Rounds: {data.get('parameters', {}).get('rounds', 'N/A')}\")
    print(f\"Key Finding: {data.get('summary', {}).get('key_finding', 'N/A')}\")
"
        echo ""
        
    elif [ "$status" = "failed" ]; then
        log_error "Simulation failed"
        
        # Fetch error details
        curl -s "$MIROFISH_API/simulations/$job_id/error" | python3 -m json.tool
        exit 1
    else
        log_error "Unexpected status: $status"
        exit 1
    fi
}

# Main execution
main() {
    echo "=========================================="
    echo "MiroFish Simulation Runner"
    echo "Scenario: $SCENARIO"
    echo "=========================================="
    echo ""
    
    check_api
    
    if [ "$DRY_RUN" = true ]; then
        load_scenario
    fi
    
    run_simulation
    
    log_success "Done!"
}

main
