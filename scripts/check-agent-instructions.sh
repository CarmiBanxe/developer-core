#!/bin/bash
# Check active agent instructions in current project
# Usage: bash scripts/check-agent-instructions.sh

set -e

echo "════════════════════════════════════════════"
echo "  Active Agent Instructions Checker"
echo "════════════════════════════════════════════"
echo ""

# Detect git root
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")
echo "Repository root: $GIT_ROOT"
echo ""

echo "=== GLOBAL INSTRUCTIONS ==="
if [ -f ~/.claude/CLAUDE.md ]; then
    echo "✓ ~/.claude/CLAUDE.md exists"
    echo "  Lines: $(wc -l < ~/.claude/CLAUDE.md)"
    echo "  Key rules:"
    grep -E "^### (Core rule|Project isolation|Collaboration behavior)" ~/.claude/CLAUDE.md | head -3
else
    echo "✗ ~/.claude/CLAUDE.md NOT FOUND"
fi
echo ""

echo "=== PROJECT INSTRUCTIONS ==="
for file in "CLAUDE.md" "AGENTS.md" "docs/COLLAB.md" "COLLAB.md"; do
    if [ -f "$GIT_ROOT/$file" ]; then
        echo "✓ $file exists"
        echo "  Lines: $(wc -l < $GIT_ROOT/$file)"
    fi
done
echo ""

echo "=== QODER CONTEXT ==="
if [ -f "$GIT_ROOT/.qoder/context.md" ]; then
    echo "✓ .qoder/context.md exists"
    echo "  Lines: $(wc -l < $GIT_ROOT/.qoder/context.md)"
    echo "  Core rule:"
    grep -A1 "^## Core rule" $GIT_ROOT/.qoder/context.md | tail -1
else
    echo "✗ .qoder/context.md NOT FOUND"
fi
echo ""

echo "=== COMPLIANCE ARCH (if applicable) ==="
if [ -f "$GIT_ROOT/src/compliance/COMPLIANCE_ARCH.md" ]; then
    echo "✓ src/compliance/COMPLIANCE_ARCH.md exists"
    echo "  Invariants:"
    grep -E "^[0-9]+\." $GIT_ROOT/src/compliance/COMPLIANCE_ARCH.md | head -6
else
    echo "○ Compliance arch not found (not a compliance project?)"
fi
echo ""

echo "=== MCP CONFIG ==="
if [ -f ~/.claude/settings.json ]; then
    echo "✓ ~/.claude/settings.json exists"
    if grep -q "qoder" ~/.claude/settings.json; then
        echo "  Qoder MCP server: configured"
    else
        echo "  Qoder MCP server: NOT configured"
    fi
else
    echo "✗ ~/.claude/settings.json NOT FOUND"
fi
echo ""

echo "=== QODER CONFIG ==="
if [ -f ~/.qoder/config.yml ]; then
    echo "✓ ~/.qoder/config.yml exists"
    echo "  Context paths:"
    grep -A5 "contextPaths:" ~/.qoder/config.yml | tail -n+2 | head -5
else
    echo "○ ~/.qoder/config.yml not found"
fi
echo ""

echo "════════════════════════════════════════════"
echo "  Instruction hierarchy is COMPLETE"
echo "════════════════════════════════════════════"
