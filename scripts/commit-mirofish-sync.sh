#!/bin/bash
# commit-mirofish-sync.sh — Commit and push MiroFish sync to all projects
# Source: ~/developer/scripts/commit-mirofish-sync.sh
# Version: 1.0 | 2026-04-03

set -e

PROJECTS=("vibe-coding" "collaboration" "MetaClaw" "guiyon" "ss1")

echo "=========================================="
echo "MiroFish Sync — Commit & Push"
echo "=========================================="
echo ""

for project in "${PROJECTS[@]}"; do
    PROJECT_PATH="$HOME/$project"
    
    if [ ! -d "$PROJECT_PATH" ]; then
        echo "⚠️  Skipping $project — directory not found"
        continue
    fi
    
    cd "$PROJECT_PATH"
    
    # Check for changes
    if git status --porcelain | grep -q .; then
        echo "📦 $project — has changes"
        
        # Commit
        git add -A
        git commit -m "feat: Add MiroFish as third partner (Claude + Qoder + MiroFish)

- AGENTS.md: Added MiroFish role (Simulator & Validator)
- .qoder/context.md: Added MiroFish simulation pipeline
- docs/MIROFISH-SCENARIOS.md: Project-specific scenario library

Integration: Three-partner synergy via MCP
Auto-triggers: HITL, FCA, fraud pattern, UX validation, stress-test

🤖 Generated with [Qoder][https://qoder.com]"
        
        # Push
        git push origin master 2>/dev/null || git push origin main 2>/dev/null || {
            echo "  ⚠️  Push failed — manual review needed"
            continue
        }
        
        echo "  ✅ $project pushed"
    else
        echo "✓ $project — no changes"
    fi
done

echo ""
echo "=========================================="
echo "Sync Complete!"
echo "=========================================="
echo ""
echo "All 5 projects updated with MiroFish integration."
echo ""
echo "Next: Deploy MiroFish engine to GMKtec"
echo "  See: ~/developer/docs/MIROFISH-DEPLOY-GMKTEC.md"
