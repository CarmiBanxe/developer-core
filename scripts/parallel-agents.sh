#!/usr/bin/env bash
# parallel-agents.sh — Run parallel Claude Code agent teams for BANXE
# IL-063 | Developer Plane
#
# Three concurrent agent teams:
#   Agent 1 (Frontend)  → banxe-ui screens/components
#   Agent 2 (Backend)   → banxe-emi-stack API/services
#   Agent 3 (QA)        → tests, a11y, quality gate
#
# Usage:
#   bash ~/developer/scripts/parallel-agents.sh "implement Send screen W-04"
#   bash ~/developer/scripts/parallel-agents.sh --frontend-only "fix Wallets screen"
#   bash ~/developer/scripts/parallel-agents.sh --status
#
# Requires: Claude Code CLI (claude) installed and authenticated
# Each agent runs as a tmux pane (requires tmux)

set -euo pipefail

TASK="${1:-}"
FLAG="${1:---all}"

RED="\033[0;31m" GREEN="\033[0;32m" YELLOW="\033[1;33m" BOLD="\033[1m" RESET="\033[0m"
SESSION="banxe-agents"

usage() {
  echo ""
  echo -e "${BOLD}parallel-agents.sh — BANXE AI BANK Parallel Agent Teams${RESET}"
  echo ""
  echo "Usage:"
  echo "  bash parallel-agents.sh \"<task description>\"    # all 3 agents"
  echo "  bash parallel-agents.sh --frontend \"<task>\"     # frontend only"
  echo "  bash parallel-agents.sh --backend  \"<task>\"     # backend only"
  echo "  bash parallel-agents.sh --qa                    # QA + a11y only"
  echo "  bash parallel-agents.sh --status               # show agent status"
  echo "  bash parallel-agents.sh --kill                 # kill all agents"
  echo ""
}

require_tmux() {
  if ! command -v tmux &>/dev/null; then
    echo -e "${RED}ERROR: tmux required. Install: sudo apt install tmux${RESET}"
    exit 1
  fi
}

require_claude() {
  if ! command -v claude &>/dev/null; then
    echo -e "${RED}ERROR: claude CLI not found. Install Claude Code first.${RESET}"
    exit 1
  fi
}

# ── Agent definitions ─────────────────────────────────────────────────────────

frontend_prompt() {
  local task="$1"
  cat << PROMPT
You are the Frontend Agent for BANXE AI BANK (IL-063).
Working directory: ~/banxe-ui
Task: $task

Before starting:
1. Read ~/banxe-ui/.claude/CLAUDE.md
2. Read ~/banxe-architecture/docs/BANXE-SCREEN-INVENTORY.md
3. Check ~/banxe-ui/packages/ui/src/index.ts (existing components)

Rules:
- Use only Tailwind classes from tailwind.config.ts
- All amounts → font-mono, no parseFloat (I-05)
- Loading states → Skeleton, not spinner
- AI content → ✦ badge + confidence mandatory
- Write Storybook story for any new component
- Run typecheck after: cd ~/banxe-ui && npx tsc --noEmit

When done: commit with "feat(ui): [Frontend Agent] $task"
PROMPT
}

backend_prompt() {
  local task="$1"
  cat << PROMPT
You are the Backend Agent for BANXE AI BANK (IL-063).
Working directory: ~/banxe-emi-stack
Task: $task (API/services side)

Before starting:
1. Read ~/banxe-emi-stack/.claude/CLAUDE.md
2. Check ~/banxe-emi-stack/api/routers/ (existing endpoints)
3. Check ~/banxe-emi-stack/services/ (existing services)

Rules:
- Python + FastAPI + SQLAlchemy (async)
- All monetary amounts: Decimal (I-05 invariant)
- 100% type annotations
- Tests required (pytest, ≥80% coverage)
- No float() for money
- FCA audit trail: all financial ops logged

When done: commit with "feat(api): [Backend Agent] $task"
PROMPT
}

qa_prompt() {
  local task="${1:-Run full quality gate}"
  cat << PROMPT
You are the QA Agent for BANXE AI BANK (IL-063).
Task: $task

Run in sequence:
1. cd ~/banxe-ui && npm -w @banxe/ui run test 2>&1 | tail -20
2. cd ~/banxe-ui && npx tsc --noEmit 2>&1 | head -30
3. cd ~/banxe-emi-stack && python -m pytest --tb=short -q 2>&1 | tail -20
4. cd ~/banxe-emi-stack && ruff check . 2>&1 | head -20
5. bash ~/banxe-emi-stack/scripts/quality-gate.sh 2>&1 | tail -30

For any failures:
- Identify root cause
- Apply minimal fix
- Re-run the failing check
- Commit: "fix(qa): [QA Agent] <description>"

Report format:
  Frontend tests: PASS/FAIL (N tests)
  TypeScript: PASS/FAIL
  Backend tests: PASS/FAIL (N/N)
  Ruff: PASS/FAIL
  Quality gate: PASS/FAIL
PROMPT
}

# ── Launch functions ──────────────────────────────────────────────────────────

launch_agent() {
  local pane_name="$1"
  local dir="$2"
  local prompt_text="$3"

  tmux new-window -t "$SESSION" -n "$pane_name" 2>/dev/null || true
  tmux send-keys -t "$SESSION:$pane_name" "cd $dir" Enter
  # Write prompt to temp file to avoid quoting issues
  local tmp=$(mktemp /tmp/agent-prompt-XXXXXX.txt)
  echo "$prompt_text" > "$tmp"
  tmux send-keys -t "$SESSION:$pane_name" "claude --print < $tmp" Enter
}

show_status() {
  if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo -e "${GREEN}Active tmux session: $SESSION${RESET}"
    tmux list-windows -t "$SESSION"
  else
    echo -e "${YELLOW}No active agent session${RESET}"
  fi
}

kill_agents() {
  tmux kill-session -t "$SESSION" 2>/dev/null && \
    echo -e "${GREEN}Agents terminated${RESET}" || \
    echo -e "${YELLOW}No agents running${RESET}"
}

# ── Main ──────────────────────────────────────────────────────────────────────

case "${1:-}" in
  --status) show_status; exit 0 ;;
  --kill)   kill_agents; exit 0 ;;
  --help|-h) usage; exit 0 ;;
esac

TASK="${2:-${1:-Review and improve current state}}"
MODE="${1:---all}"

if [[ "$MODE" != --* ]] || [[ "$MODE" == "--all" ]]; then
  TASK="${1:-Review and improve current state}"
  MODE="--all"
fi

require_tmux
require_claude

echo ""
echo -e "${BOLD}═══ BANXE Parallel Agents ════════════════════════════${RESET}"
echo -e "  Task: ${YELLOW}$TASK${RESET}"
echo -e "  Mode: $MODE"
echo ""

# Create tmux session
tmux new-session -d -s "$SESSION" -n "coordinator" 2>/dev/null || true

START_TS=$(date +%s)

case "$MODE" in
  --all)
    echo -e "  ${GREEN}Launching 3 agents in parallel...${RESET}"
    launch_agent "frontend" "$HOME/banxe-ui"          "$(frontend_prompt "$TASK")"
    launch_agent "backend"  "$HOME/banxe-emi-stack"   "$(backend_prompt  "$TASK")"
    launch_agent "qa"       "$HOME/banxe-emi-stack"   "$(qa_prompt       "$TASK")"
    echo -e "  ${GREEN}✅ Frontend Agent${RESET} → tmux: $SESSION:frontend"
    echo -e "  ${GREEN}✅ Backend Agent${RESET}  → tmux: $SESSION:backend"
    echo -e "  ${GREEN}✅ QA Agent${RESET}       → tmux: $SESSION:qa"
    ;;
  --frontend)
    launch_agent "frontend" "$HOME/banxe-ui"        "$(frontend_prompt "$TASK")"
    echo -e "  ${GREEN}✅ Frontend Agent started${RESET}"
    ;;
  --backend)
    launch_agent "backend" "$HOME/banxe-emi-stack"  "$(backend_prompt "$TASK")"
    echo -e "  ${GREEN}✅ Backend Agent started${RESET}"
    ;;
  --qa)
    launch_agent "qa" "$HOME/banxe-emi-stack"       "$(qa_prompt "$TASK")"
    echo -e "  ${GREEN}✅ QA Agent started${RESET}"
    ;;
  *)
    echo -e "${RED}Unknown mode: $MODE${RESET}"
    usage; exit 1
    ;;
esac

echo ""
echo -e "${BOLD}Monitor agents:${RESET}"
echo -e "  tmux attach -t $SESSION"
echo -e "  tmux select-window -t $SESSION:frontend"
echo -e "  tmux select-window -t $SESSION:backend"
echo -e "  tmux select-window -t $SESSION:qa"
echo ""
echo -e "${BOLD}Stop all:${RESET}"
echo -e "  bash ~/developer/scripts/parallel-agents.sh --kill"
echo ""
echo -e "${BOLD}═══════════════════════════════════════════════════════${RESET}"
echo ""
