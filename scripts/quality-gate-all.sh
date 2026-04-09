#!/bin/bash
# quality-gate-all.sh — Run full quality gate across all BANXE repos
# IL-068 | Developer Plane | BANXE AI BANK
# Usage: bash ~/developer/scripts/quality-gate-all.sh

EMI_DIR="$HOME/banxe-emi-stack"
UI_DIR="$HOME/banxe-ui"
PASS=0
FAIL=0
RESULTS=()

_pass() { PASS=$((PASS+1)); RESULTS+=("  ✅ $1"); }
_fail() { FAIL=$((FAIL+1)); RESULTS+=("  ❌ $1 — $2"); }

echo ""
echo "═══ BANXE Quality Gate — ALL REPOS ═══════════════════"
echo ""

# ── banxe-emi-stack ──────────────────────────────────────
echo "── banxe-emi-stack ──"
cd "$EMI_DIR"

if ruff check . --quiet 2>&1; then
    _pass "Ruff lint (banxe-emi-stack)"
else
    _fail "Ruff lint (banxe-emi-stack)" "lint errors"
fi

if ruff format --check . --quiet 2>&1; then
    _pass "Ruff format (banxe-emi-stack)"
else
    _fail "Ruff format (banxe-emi-stack)" "format errors"
fi

PYTEST_OUT=$(python3 -m pytest tests/ --no-cov --tb=no 2>&1)
PYTEST_SUMMARY=$(echo "$PYTEST_OUT" | grep -oE "[0-9]+ passed" | head -1)
if [ -n "$PYTEST_SUMMARY" ]; then
    _pass "Pytest: $PYTEST_SUMMARY (banxe-emi-stack)"
else
    PYTEST_ERR=$(echo "$PYTEST_OUT" | grep -E "FAILED|ERROR|error" | head -2)
    _fail "Pytest (banxe-emi-stack)" "${PYTEST_ERR:-no tests found}"
fi

COV_OUT=$(python3 -m pytest tests/ -q --cov=services --cov=api --cov-report=term-missing --no-header 2>&1)
COV_PCT=$(echo "$COV_OUT" | grep "^TOTAL" | awk '{print $NF}')
if echo "$COV_PCT" | grep -qE "^[89][0-9]%$|^100%$"; then
    _pass "Coverage: $COV_PCT (banxe-emi-stack)"
else
    _fail "Coverage (banxe-emi-stack)" "${COV_PCT:-below 80%}"
fi

if semgrep --config .semgrep/banxe-rules.yml --error --quiet 2>&1; then
    _pass "Semgrep (banxe-emi-stack)"
else
    _fail "Semgrep (banxe-emi-stack)" "violations found"
fi

echo ""

# ── banxe-ui ──────────────────────────────────────────────
echo "── banxe-ui ──"
cd "$UI_DIR"

if npx tsc --noEmit --pretty false 2>&1 | grep -qE "error TS"; then
    _fail "TypeScript (banxe-ui)" "type errors"
else
    _pass "TypeScript (banxe-ui)"
fi

if npx eslint packages/ui/src apps/web/src --ext .ts,.tsx --max-warnings 0 --quiet 2>&1; then
    _pass "ESLint (banxe-ui)"
else
    _fail "ESLint (banxe-ui)" "lint errors"
fi

VT_OUT=$(npx vitest run --reporter=dot 2>&1)
VT_SUMMARY=$(echo "$VT_OUT" | grep -oE "Tests[[:space:]]+[0-9]+ passed" | head -1)
if [ -n "$VT_SUMMARY" ]; then
    _pass "Vitest: $VT_SUMMARY (banxe-ui)"
else
    VT_ERR=$(echo "$VT_OUT" | grep -E "FAIL|failed|error" | head -2)
    _fail "Vitest (banxe-ui)" "${VT_ERR:-check output}"
fi

if semgrep --config .semgrep/banxe-ui-rules.yaml apps/web/src packages/ui/src --error --quiet 2>&1; then
    _pass "Semgrep (banxe-ui)"
else
    _fail "Semgrep (banxe-ui)" "violations found"
fi

echo ""

# ── Summary ───────────────────────────────────────────────
echo "═══ RESULTS ════════════════════════════════════════════"
for r in "${RESULTS[@]}"; do echo "$r"; done
echo ""
echo "═══ SUMMARY: $PASS passed, $FAIL failed ════════════════"

if [ "$FAIL" -gt 0 ]; then
    echo "GATE: ❌ FAILED"
    exit 1
else
    echo "GATE: ✅ ALL PASS"
    exit 0
fi
