#!/usr/bin/env bash
# hooks/spec-first-pre-commit.sh — Spec-First Auditor pre-commit hook
# IL-060 | Developer Plane | banxe-architecture
#
# Installed by: bash ~/developer/scripts/install-auditor-hooks.sh
# Runs on: developer-core, banxe-emi-stack, banxe-architecture
#
# Exit 0 = commit allowed | Exit 1 = commit BLOCKED

AUDITOR="$HOME/developer/spec-first/audit/spec_first_auditor.py"

if [[ ! -f "$AUDITOR" ]]; then
    echo "⚠️  spec_first_auditor.py not found at $AUDITOR — skipping audit"
    exit 0
fi

echo ""
echo "🔍 Running Spec-First Auditor (pre-commit)..."
echo ""

python3 "$AUDITOR" --full
EXIT_CODE=$?

if [[ $EXIT_CODE -ne 0 ]]; then
    echo ""
    echo "❌ COMMIT BLOCKED by Spec-First Auditor."
    echo "   Fix the violations above, then commit again."
    echo "   To skip (emergency only): git commit --no-verify"
    echo ""
    exit 1
fi

exit 0
