#!/bin/bash
# install-mirofish.sh — MiroFish Offline Installation Script
# Source: ~/developer/mirofish/install-mirofish.sh
# Version: 1.0 | 2026-04-03

set -e

echo "=========================================="
echo "MiroFish Offline Installation"
echo "Version 1.0 | 2026-04-03"
echo "=========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Docker check
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker not found. Please install Docker Desktop first."
    exit 1
fi

# Docker Compose check
if ! docker compose version &> /dev/null; then
    echo "ERROR: Docker Compose not found. Please install Docker Desktop."
    exit 1
fi

# Ollama check (optional but recommended)
if command -v ollama &> /dev/null; then
    echo "✓ Ollama found: $(ollama --version)"
else
    echo "WARNING: Ollama not found. Will use API-based LLM (higher cost)."
    read -p "Continue without local LLM? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Memory check (recommend 32GB+ for large simulations)
TOTAL_MEM_GB=$(free -g | awk '/^Mem:/{print $2}')
if [ "$TOTAL_MEM_GB" -lt 16 ]; then
    echo "WARNING: Less than 16GB RAM detected. Large simulations may be slow."
fi
echo "✓ Memory: ${TOTAL_MEM_GB}GB available"

echo ""
echo "Installing MiroFish..."

# Clone repository
MIROFISH_DIR=~/mirofish-engine
if [ -d "$MIROFISH_DIR" ]; then
    echo "MiroFish already installed at $MIROFISH_DIR"
    read -p "Reinstall? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$MIROFISH_DIR"
    else
        echo "Skipping installation."
        exit 0
    fi
fi

echo "Cloning MiroFish-Offline repository..."
git clone https://github.com/nikmcfly/MiroFish-Offline.git "$MIROFISH_DIR"
cd "$MIROFISH_DIR"

# Configure environment
echo "Configuring environment..."
cp .env.example .env

cat >> .env << EOF

# Custom configuration (added by install script)
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL_NAME=qwen2.5:32b
NEO4J_URI=bolt://localhost:7687
EMBEDDING_MODEL=nomic-embed-text
NEO4J_PASSWORD=${NEO4J_PASSWORD:-changeme}
EOF

echo "✓ Environment configured"

# Start services
echo "Starting Docker services (Neo4j + Ollama + MiroFish app)..."
docker compose up -d

echo "Waiting for services to be ready..."
sleep 10

# Check service health
echo "Checking service health..."
docker compose ps

# Pull Ollama models
if command -v ollama &> /dev/null; then
    echo "Pulling Ollama models (this may take a few minutes)..."
    ollama pull qwen2.5:32b || echo "Warning: Failed to pull qwen2.5:32b"
    ollama pull nomic-embed-text || echo "Warning: Failed to pull nomic-embed-text"
    echo "✓ Models pulled"
fi

# Test API
echo "Testing MiroFish API..."
MAX_RETRIES=30
RETRY_COUNT=0
until curl -s http://localhost:3000/api/health > /dev/null 2>&1 || [ $RETRY_COUNT -eq $MAX_RETRIES ]; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "  Waiting for API... ($RETRY_COUNT/$MAX_RETRIES)"
    sleep 2
done

if curl -s http://localhost:3000/api/health > /dev/null 2>&1; then
    HEALTH_RESPONSE=$(curl -s http://localhost:3000/api/health)
    echo "✓ API healthy: $HEALTH_RESPONSE"
else
    echo "ERROR: API not responding after $MAX_RETRIES attempts"
    echo "Troubleshooting:"
    echo "  docker compose logs mirofish-app"
    exit 1
fi

# Copy configuration template
echo "Copying configuration template..."
mkdir -p ~/.mirofish
cp ~/developer/mirofish/config-template.yml ~/.mirofish/config.yml

echo ""
echo "=========================================="
echo "MiroFish Installation Complete!"
echo "=========================================="
echo ""
echo "Access UI: http://localhost:3000"
echo "API: http://localhost:3000/api/health"
echo "Config: ~/.mirofish/config.yml"
echo ""
echo "Next steps:"
echo "  1. Run first test simulation:"
echo "     bash ~/developer/mirofish/run-simulation.sh test"
echo ""
echo "  2. Review scenario library:"
echo "     ls ~/developer/mirofish/scenarios/"
echo ""
echo "  3. Integrate with Banxe workflow:"
echo "     cd ~/vibe-coding && claude"
echo "     'Run HITL handoff simulation'"
echo ""
