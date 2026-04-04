#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(pwd)}"
PROJECT_CLAUDE_DIR="$ROOT_DIR/.claude"
SUPERVISOR_DIR="$ROOT_DIR/.claude-supervisor"
HOOKS_DIR="$SUPERVISOR_DIR/hooks"
STATE_DIR="$SUPERVISOR_DIR/state"
LOGS_DIR="$SUPERVISOR_DIR/logs"

mkdir -p "$PROJECT_CLAUDE_DIR" "$HOOKS_DIR" "$STATE_DIR" "$LOGS_DIR"

echo "Supervisor directories prepared in $ROOT_DIR"
echo "Now copy the provided files into:"
echo "  $PROJECT_CLAUDE_DIR"
echo "  $SUPERVISOR_DIR"
