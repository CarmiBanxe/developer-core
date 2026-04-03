#!/bin/bash
# sync-mirofish-to-projects.sh — Add MiroFish as third partner to all synergy projects
# Source: ~/developer/scripts/sync-mirofish-to-projects.sh
# Version: 1.0 | 2026-04-03

set -e

PROJECTS=("vibe-coding" "collaboration" "MetaClaw" "guiyon" "ss1")

echo "=========================================="
echo "MiroFish Integration Sync"
echo "Adding MiroFish as third partner to all projects"
echo "=========================================="
echo ""

for project in "${PROJECTS[@]}"; do
    PROJECT_PATH="$HOME/$project"
    
    if [ ! -d "$PROJECT_PATH" ]; then
        echo "⚠️  Skipping $project — directory not found"
        continue
    fi
    
    echo "Processing: $project"
    cd "$PROJECT_PATH"
    
    # Update AGENTS.md — Add MiroFish section
    echo "  📝 Updating AGENTS.md..."
    if grep -q "MiroFish" AGENTS.md 2>/dev/null; then
        echo "    ✓ Already contains MiroFish"
    else
        # Find the "Agent roles" section and add MiroFish
        if grep -q "## Agent roles" AGENTS.md 2>/dev/null; then
            sed -i '/### Qoder CLI (Executor)/a\
\
### MiroFish (Simulator \& Validator)\
\
- Behavioral simulation\
- Stress testing\
- UX validation\
- Market reaction modeling\
\
**Auto-trigger keywords:** HITL, FCA, fraud pattern, UX validation, stress-test, market reaction' AGENTS.md
            echo "    ✓ Added MiroFish role"
        else
            echo "    ⚠️  No 'Agent roles' section found — manual review needed"
        fi
    fi
    
    # Update .qoder/context.md — Add MiroFish pipeline
    echo "  📝 Updating .qoder/context.md..."
    if [ -f ".qoder/context.md" ] && ! grep -q "MiroFish" .qoder/context.md 2>/dev/null; then
        # Add MiroFish mention after Qoder section
        if grep -q "Qoder CLI" .qoder/context.md; then
            sed -i '/^### For simulations$/a\
\
1. Define scenario parameters\
2. Run MiroFish simulation\
3. Analyze results\
4. Apply findings to implementation' .qoder/context.md
            echo "    ✓ Added MiroFish pipeline"
        fi
    else
        echo "    ✓ .qoder/context.md up to date"
    fi
    
    # Create docs/MIROFISH-SCENARIOS.md
    echo "  📝 Creating docs/MIROFISH-SCENARIOS.md..."
    if [ ! -f "docs/MIROFISH-SCENARIOS.md" ]; then
        cat > docs/MIROFISH-SCENARIOS.md << 'EOF'
# MiroFish Scenarios — Project-Specific Simulations

**Repository:** `~/PROJECT_NAME/`  
**Version:** 1.0 | 2026-04-03  
**Integration:** Three-partner synergy (Claude + Qoder + MiroFish)

---

## Auto-Trigger Detection

MiroFish activates automatically when Claude detects these keywords in user requests:

| Keyword Pattern | Triggered Scenario |
|-----------------|-------------------|
| "human approval", "handoff", "дублёр" | HITL trust study |
| "FCA", "sandbox", "compliance policy" | Pre-FCA testing |
| "fraud pattern", "social engineering" | Fraud simulation |
| "market reaction", "launch strategy" | GTM modeling |
| "UX validation", "drop-off", "onboarding" | UX testing |
| "stress test", "crisis scenario" | Stress testing |
| "adoption curve", "market sizing" | Adoption modeling |

### Override Mechanism

To skip simulation:
```
"Design X WITHOUT MiroFish simulation"
→ Claude proceeds directly to implementation
```

---

## Project-Specific Scenarios

### Scenario Library (Inherited from Developer-Core)

All scenarios available from `~/developer/mirofish/scenarios/`:

| Scenario | Agents | Rounds | Use Case |
|----------|--------|--------|----------|
| hitl-handoff.yml | 300 | 40 | HITL trust thresholds |
| pre-fca-sandbox.yml | 250 | 30 | Compliance policy testing |
| fraud-social-eng.yml | 400 | 50 | Fraud pattern detection |
| gtm-reaction.yml | 350 | 35 | Market reaction modeling |
| ux-validation.yml | 200 | 25 | UX validation pipeline |
| fraud-stress-test.yml | 500 | 50 | Quarterly stress testing |
| market-adoption.yml | 600 | 60 | Adoption curve projection |

---

## Usage Examples

### Run Simulation from This Project

```bash
cd ~/PROJECT_NAME
bash ../developer/mirofish/run-simulation.sh <scenario-name> --agents 300 --rounds 40
```

### Example: HITL Handoff Study

```bash
cd ~/PROJECT_NAME
bash ../developer/mirofish/run-simulation.sh hitl-handoff --agents 300 --rounds 40
```

**Expected Output:**
- Trust threshold map by user segment
- Optimal handoff trigger points
- Communication templates

---

## Simulation Reports

Reports saved to: `docs/simulations/YYYY-MM-DD-scenario-name.json`

### Report Structure

```json
{
  "simulation_id": "hitl-handoff-20260403-143022",
  "scenario": "hitl_trust_handoff",
  "summary": {
    "key_finding": "...",
    "recommendation": "..."
  },
  "segment_results": [...],
  "patterns_detected": [...]
}
```

---

## Related Documentation

- `~/developer/docs/MIROFISH-INTEGRATION.md` — Full integration plan
- `~/developer/mirofish/README.md` — Quick start guide
- `~/developer/mirofish/scenarios/` — All scenario templates
EOF
        
        # Replace PROJECT_NAME with actual name
        sed -i "s/PROJECT_NAME/$project/g" docs/MIROFISH-SCENARIOS.md
        echo "    ✓ Created MIROFISH-SCENARIOS.md"
    else
        echo "    ✓ Already exists"
    fi
    
    # Stage changes
    git add -A 2>/dev/null || true
    
    echo "  ✅ $project complete"
    echo ""
done

echo "=========================================="
echo "Sync Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Review changes: git diff"
echo "  2. Commit: git commit -m 'feat: Add MiroFish as third partner'"
echo "  3. Push: git push"
echo ""
echo "Or run for all projects:"
echo "  cd ~/developer && bash scripts/commit-mirofish-sync.sh"
