#!/usr/bin/env bash
# scripts/install-auditor-hooks.sh — Install Spec-First Auditor pre-commit hook
# IL-060 | Developer Plane
#
# Installs the hook to:
#   ~/developer           (developer-core)
#   ~/banxe-emi-stack     (Product Plane)
#   ~/banxe-architecture  (Architecture)
#
# Usage (run from Legion):
#   bash ~/developer/scripts/install-auditor-hooks.sh
#
# The hook is a symlink to ~/developer/hooks/spec-first-pre-commit.sh
# so updates to the hook source are reflected immediately in all repos.

set -euo pipefail

HOOK_SRC="$HOME/developer/hooks/spec-first-pre-commit.sh"
REPOS=(
    "$HOME/developer"
    "$HOME/banxe-emi-stack"
    "$HOME/banxe-architecture"
)

RED="\033[0;31m" GREEN="\033[0;32m" YELLOW="\033[1;33m" BOLD="\033[1m" RESET="\033[0m"

echo ""
echo -e "${BOLD}═══ Install Spec-First Auditor Pre-commit Hook ════════${RESET}"
echo ""

if [[ ! -f "$HOOK_SRC" ]]; then
    echo -e "${RED}ERROR: Hook source not found: $HOOK_SRC${RESET}"
    exit 1
fi

chmod +x "$HOOK_SRC"

FAIL=0
for REPO in "${REPOS[@]}"; do
    HOOK_DST="$REPO/.git/hooks/pre-commit"
    REPO_NAME=$(basename "$REPO")

    if [[ ! -d "$REPO/.git" ]]; then
        echo -e "  ${YELLOW}SKIP${RESET}  $REPO_NAME (not a git repo)"
        continue
    fi

    # Remove existing hook if it's not our symlink
    if [[ -f "$HOOK_DST" && ! -L "$HOOK_DST" ]]; then
        BACKUP="${HOOK_DST}.bak.$(date +%s)"
        mv "$HOOK_DST" "$BACKUP"
        echo -e "  ${YELLOW}BACKUP${RESET} existing hook → $BACKUP"
    fi

    # Create symlink
    ln -sf "$HOOK_SRC" "$HOOK_DST"

    if [[ -L "$HOOK_DST" && -f "$HOOK_DST" ]]; then
        echo -e "  ${GREEN}OK${RESET}    $REPO_NAME → $HOOK_DST"
    else
        echo -e "  ${RED}FAIL${RESET}  $REPO_NAME — could not install hook"
        FAIL=1
    fi
done

echo ""
echo -e "${BOLD}───────────────────────────────────────────────────────${RESET}"
if [[ $FAIL -eq 0 ]]; then
    echo -e "  ${BOLD}RESULT: ${GREEN}✅ Hooks installed in all repos${RESET}"
else
    echo -e "  ${BOLD}RESULT: ${RED}❌ Some repos failed${RESET}"
fi
echo -e "${BOLD}═══════════════════════════════════════════════════════${RESET}"
echo ""

exit $FAIL
