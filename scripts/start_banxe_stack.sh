#!/bin/bash
set -euo pipefail

# start_banxe_stack.sh — Master startup check for BANXE AI Stack v2.0
# Verifies all components before starting a work session.
# Usage: bash scripts/start_banxe_stack.sh [--strict]
#
# --strict: exit 1 if ANY component is unavailable (default: warnings only)

STRICT="${1:-}"
PASS=0
WARN=0
FAIL=0

check_pass() { echo "  ✅ $1"; PASS=$((PASS+1)); }
check_warn() { echo "  ⚠️  $1"; WARN=$((WARN+1)); }
check_fail() { echo "  ❌ $1"; FAIL=$((FAIL+1)); }

echo "════════════ BANXE AI Stack v2.0 — Startup Check ════════════"
echo ""

# ── Infrastructure ──────────────────────────────────────────────────────────

echo "── Infrastructure ──"

# LiteLLM :4000 (required for Aider CLI and parallel-verify.sh)
if curl -sf http://localhost:4000/v1/models > /dev/null 2>&1; then
  check_pass "LiteLLM :4000 — OK"
else
  check_fail "LiteLLM :4000 — NOT RESPONDING (Aider and parallel-verify will fail)"
fi

# Ollama :11434
if curl -sf http://192.168.0.72:11434/api/tags > /dev/null 2>&1; then
  check_pass "Ollama :11434 — OK"
else
  check_warn "Ollama :11434 — not responding (using LiteLLM cache fallback)"
fi

echo ""

# ── Platform (OpenClaw bots) ─────────────────────────────────────────────────

echo "── Platform (OpenClaw) ──"

for PORT in 18789 18791 18793; do
  if curl -sf "http://localhost:${PORT}/api/health" > /dev/null 2>&1; then
    check_pass "OpenClaw Bot :${PORT} — OK"
  else
    check_warn "OpenClaw Bot :${PORT} — OFFLINE"
  fi
done

echo ""

# ── Partners ─────────────────────────────────────────────────────────────────

echo "── Partners ──"

# Aider CLI
if which aider > /dev/null 2>&1; then
  AIDER_VER=$(aider --version 2>/dev/null || echo "version unknown")
  check_pass "Aider CLI — found ($AIDER_VER)"
else
  check_fail "Aider CLI — NOT FOUND (install: pip install aider-chat)"
fi

# Ruflo config
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUFLO_CONFIG="${SCRIPT_DIR}/../ruflo/config.yaml"
if [ -f "$RUFLO_CONFIG" ]; then
  check_pass "Ruflo config — found ($RUFLO_CONFIG)"
else
  check_warn "Ruflo config — not found at $RUFLO_CONFIG"
fi

# MiroFish :3000
if curl -sf http://localhost:3000/api/health > /dev/null 2>&1; then
  check_pass "MiroFish :3000 — OK"
else
  check_warn "MiroFish :3000 — not deployed (run mirofish/install-mirofish.sh)"
fi

echo ""

# ── CANON ────────────────────────────────────────────────────────────────────

echo "── CANON ──"

CANON_DIR="${SCRIPT_DIR}/../canon/modules"
for MOD in CORE.md DEV.md DECISION.md; do
  if [ -f "${CANON_DIR}/${MOD}" ]; then
    check_pass "CANON/${MOD}"
  else
    check_warn "CANON/${MOD} — missing"
  fi
done

echo ""

# ── Verification utility ──────────────────────────────────────────────────────

echo "── Verification ──"

if [ -f "${SCRIPT_DIR}/parallel-verify.sh" ]; then
  check_pass "parallel-verify.sh — found"
else
  check_warn "parallel-verify.sh — missing"
fi

if [ -f "${SCRIPT_DIR}/aider-banxe.sh" ]; then
  check_pass "aider-banxe.sh — found"
else
  check_fail "aider-banxe.sh — missing"
fi

echo ""

# ── Summary ──────────────────────────────────────────────────────────────────

echo "════════════ Summary ════════════"
echo "  PASS: ${PASS}  |  WARN: ${WARN}  |  FAIL: ${FAIL}"
echo ""

if [ "${FAIL}" -gt 0 ]; then
  echo "🔴 Stack NOT ready — ${FAIL} critical component(s) missing."
  echo "   Fix FAIL items before starting work."
  [ "${STRICT}" = "--strict" ] && exit 1 || exit 0
elif [ "${WARN}" -gt 0 ]; then
  echo "🟡 Stack PARTIALLY ready — ${WARN} warning(s). Core features available."
  exit 0
else
  echo "🟢 Stack READY — all components nominal."
  exit 0
fi
