#!/usr/bin/env bash
# banxe-ui-session-start.sh — SessionStart hook for banxe-ui
# IL-063 | Developer Plane
#
# Автоматически инжектирует в контекст Claude Code:
# - Текущую git ветку + последние коммиты
# - Статус незавершённых IL
# - Напоминание о дизайн-системе BANXE
# - Статус компонентов @banxe/ui
# - Известные паттерны из Pro-Workflow SQLite

set -euo pipefail

BANXE_UI="$HOME/banxe-ui"
ARCH="$HOME/banxe-architecture"
PRO_WF_DB="$HOME/developer/.claude/hooks/pro-workflow.db"

echo ""
echo "═══ BANXE AI BANK — UI Session Context ════════════════"
echo ""

# ── 1. Git status ────────────────────────────────────────────
cd "$BANXE_UI" 2>/dev/null || true
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
echo "📦 Repo:   banxe-ui @ $BRANCH"
echo "📝 Recent commits:"
git log --oneline -5 2>/dev/null | sed 's/^/   /' || echo "   (git not available)"
echo ""

# ── 2. Component inventory ───────────────────────────────────
echo "🧩 @banxe/ui components:"
FINANCIALS=$(ls "$BANXE_UI/packages/ui/src/financial/" 2>/dev/null | tr '\n' ' ')
PRIMITIVES=$(ls "$BANXE_UI/packages/ui/src/primitives/" 2>/dev/null | tr '\n' ' ')
echo "   Financial: ${FINANCIALS:-none}"
echo "   Primitives: ${PRIMITIVES:-none}"
echo ""

# ── 3. Web screens status ────────────────────────────────────
echo "🖥  Web screens:"
for S in Dashboard Transactions Wallets Send AIAssistant Profile; do
    if [[ -f "$BANXE_UI/apps/web/src/screens/$S/index.tsx" ]]; then
        echo "   ✅ W-$S"
    else
        echo "   ⬜ W-$S — MISSING"
    fi
done
echo ""

# ── 4. Active ILs from INSTRUCTION-LEDGER ────────────────────
if [[ -f "$ARCH/INSTRUCTION-LEDGER.md" ]]; then
    PENDING=$(grep "IN_PROGRESS\|PENDING" "$ARCH/INSTRUCTION-LEDGER.md" 2>/dev/null | grep "^###" | head -3 || true)
    if [[ -n "$PENDING" ]]; then
        echo "⚠️  Незавершённые IL:"
        echo "$PENDING" | sed 's/^/   /'
        echo ""
    fi
fi

# ── 5. Design rules reminder ─────────────────────────────────
echo "📐 Design rules (always active):"
echo "   • Amounts → font-mono (I-05: no parseFloat)"
echo "   • Loading → skeleton (not spinner-only)"
echo "   • AI content → ✦ badge + confidence (HIGH|MEDIUM|UNCERTAIN)"
echo "   • Colors → Tailwind classes only (no hardcoded hex)"
echo "   • ARIA labels → ALL interactive elements"
echo ""

# ── 6. Pro-Workflow — recalled patterns ──────────────────────
if command -v python3 &>/dev/null && [[ -f "$PRO_WF_DB" ]]; then
    PATTERNS=$(python3 -c "
import sqlite3, sys
try:
    conn = sqlite3.connect('$PRO_WF_DB')
    rows = conn.execute('''
        SELECT type, summary FROM patterns
        ORDER BY count DESC LIMIT 5
    ''').fetchall()
    for r in rows:
        print(f'   [{r[0]}] {r[1]}')
    conn.close()
except: pass
" 2>/dev/null || true)
    if [[ -n "$PATTERNS" ]]; then
        echo "🧠 Pro-Workflow (top patterns from past sessions):"
        echo "$PATTERNS"
        echo ""
    fi
fi

echo "───────────────────────────────────────────────────────"
echo "  MCP: context7 ✓  figma ✓  storybook ✓"
echo "  Commands: /new-screen  /gsd-health  /gsd-quick"
echo "═══════════════════════════════════════════════════════"
echo ""
