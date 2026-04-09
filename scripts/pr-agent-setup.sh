#!/usr/bin/env bash
# pr-agent-setup.sh — Install & configure Qodo PR-Agent for BANXE UI
# IL-064 | Developer Plane
#
# PR-Agent анализирует git diff и оставляет inline-комментарии с severity.
# Запускается локально — код не уходит в облако (используем Ollama).
#
# Usage:
#   bash ~/developer/scripts/pr-agent-setup.sh          # install
#   bash ~/developer/scripts/pr-agent-setup.sh --review # review current branch
#   bash ~/developer/scripts/pr-agent-setup.sh --improve # suggest improvements

set -euo pipefail

MODE="${1:---install}"
VENV="$HOME/.pr-agent-venv"
OLLAMA_URL="${OLLAMA_BASE_URL:-http://gmktec:11434}"

RED="\033[0;31m" GREEN="\033[0;32m" YELLOW="\033[1;33m" BOLD="\033[1m" RESET="\033[0m"

echo ""
echo -e "${BOLD}═══ PR-Agent (Qodo) — BANXE UI ══════════════════════${RESET}"

# ── Install ───────────────────────────────────────────────────────────────────
if [[ "$MODE" == "--install" ]]; then
  echo -e "  Installing PR-Agent..."

  if [[ ! -d "$VENV" ]]; then
    python3 -m venv "$VENV"
  fi
  source "$VENV/bin/activate"
  pip install pr-agent -q
  echo -e "  ${GREEN}✅ pr-agent installed${RESET}"

  # Config file for local Ollama usage
  mkdir -p "$HOME/.pr_agent"
  cat > "$HOME/.pr_agent/configuration.toml" << TOML
[config]
model = "ollama/llama3.1:8b"
fallback_models = ["ollama/qwen2.5:7b"]

[ollama]
api_base = "$OLLAMA_URL"

[pr_reviewer]
require_score_label = false
require_tests_review = true
require_security_review = true

[pr_code_suggestions]
num_code_suggestions = 5
summarize_code_changes = true

[github]
# Not used — running locally against local git
user_token = ""
TOML

  echo -e "  ${GREEN}✅ Config: ~/.pr_agent/configuration.toml${RESET}"
  echo ""
  echo -e "  ${BOLD}Usage:${RESET}"
  echo -e "    bash ~/developer/scripts/pr-agent-setup.sh --review    # review diff"
  echo -e "    bash ~/developer/scripts/pr-agent-setup.sh --improve   # suggest improvements"
  echo ""
  echo -e "${BOLD}═══════════════════════════════════════════════════════${RESET}"
  exit 0
fi

# ── Review / Improve ──────────────────────────────────────────────────────────
if [[ ! -d "$VENV" ]]; then
  echo -e "${RED}PR-Agent not installed. Run: bash ~/developer/scripts/pr-agent-setup.sh${RESET}"
  exit 1
fi

source "$VENV/bin/activate"

REPO_DIR="${2:-$HOME/banxe-ui}"
cd "$REPO_DIR"

# Get diff against main
DIFF=$(git diff main...HEAD --stat 2>/dev/null | head -20 || git diff HEAD~1 --stat | head -20)
echo -e "  Diff:\n$DIFF"
echo ""

if [[ "$MODE" == "--review" ]]; then
  echo -e "  ${YELLOW}Running PR review...${RESET}"
  DIFF_FULL=$(git diff main...HEAD 2>/dev/null || git diff HEAD~1)
  echo "$DIFF_FULL" | python3 -m pr_agent.cli \
    --pr_description "" \
    review 2>&1 | head -80
elif [[ "$MODE" == "--improve" ]]; then
  echo -e "  ${YELLOW}Running code improvement suggestions...${RESET}"
  DIFF_FULL=$(git diff main...HEAD 2>/dev/null || git diff HEAD~1)
  echo "$DIFF_FULL" | python3 -m pr_agent.cli \
    --pr_description "" \
    improve 2>&1 | head -80
fi

echo ""
echo -e "${BOLD}═══════════════════════════════════════════════════════${RESET}"
