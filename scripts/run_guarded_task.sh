#!/usr/bin/env bash
set -euo pipefail

TASK_TEXT="${1:-}"
ROOT_DIR="$(pwd)"
SUPERVISOR_DIR="$ROOT_DIR/.claude-supervisor"
STATE_DIR="$SUPERVISOR_DIR/state"
LOGS_DIR="$SUPERVISOR_DIR/logs"
TEMPLATE="$SUPERVISOR_DIR/contract_template.json"
ACTIVE="$STATE_DIR/active_contract.json"

if [[ -z "$TASK_TEXT" ]]; then
  echo "Usage: ./run_guarded_task.sh \"your task\""
  exit 1
fi

if [[ ! -f "$TEMPLATE" ]]; then
  echo "Missing $TEMPLATE"
  exit 2
fi

mkdir -p "$STATE_DIR" "$LOGS_DIR"
TASK_ID="task-$(date +%Y%m%d-%H%M%S)"

python3 - <<PY
import json
from pathlib import Path

template = json.loads(Path("$TEMPLATE").read_text(encoding="utf-8"))
template["task_id"] = "$TASK_ID"
template["source_instruction"] = """$TASK_TEXT"""
Path("$ACTIVE").write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")
PY

cat > "$ROOT_DIR/CLAUDE.md" <<EOF
# Guarded execution rules

You must obey the active contract at .claude-supervisor/state/active_contract.json.

Mandatory rules:
1. Work only inside files_in_scope.
2. Never modify .env, secrets, credentials, tokens, keys, or git internals.
3. Use only tools and shell commands allowed by the contract.
4. If blocked by policy, stop and explain the reason in plain language.
5. Do not ask the user to manually enable permissions or disable safeguards.
6. Your task instruction is:

$TASK_TEXT
EOF

echo "Guarded task prepared: $TASK_ID"
echo "Contract written to: $ACTIVE"
echo "Run Claude Code with: claude --permission-mode dontAsk"
echo "After completion check: .claude-supervisor/logs/verifier_summary.json"
