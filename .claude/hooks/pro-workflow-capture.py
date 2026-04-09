#!/usr/bin/env python3
"""
pro-workflow-capture.py — Pro-Workflow SQLite session memory for BANXE UI
IL-063 | Developer Plane | developer-core

Inspired by: rohitg00/pro-workflow (Claude Code plugin)
This lightweight implementation captures:
  - Patterns: recurring code patterns Claude uses for BANXE
  - Fixes: corrections made (what broke + what fixed it)
  - Conventions: BANXE-specific rules discovered in session

Runs as PostToolUse hook (after Write/Edit) and Stop hook (session end).

Storage: ~/.developer/.claude/hooks/pro-workflow.db (SQLite)
"""

import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path.home() / "developer" / ".claude" / "hooks" / "pro-workflow.db"

# ── Schema ────────────────────────────────────────────────────────────────────

SCHEMA = """
CREATE TABLE IF NOT EXISTS patterns (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    type     TEXT NOT NULL,        -- 'pattern' | 'fix' | 'convention'
    summary  TEXT NOT NULL,        -- human-readable one-liner
    detail   TEXT,                 -- extended notes
    file_pat TEXT,                 -- file path pattern where this applies
    count    INTEGER DEFAULT 1,    -- how many times seen
    last_seen TEXT NOT NULL        -- ISO timestamp
);

CREATE TABLE IF NOT EXISTS session_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    ts         TEXT NOT NULL,
    tool       TEXT,
    file_path  TEXT,
    action     TEXT              -- brief description
);
"""

# ── Heuristic pattern detection ──────────────────────────────────────────────

PATTERN_RULES = [
    # (regex_on_new_string, type, summary, file_pattern)
    (r'font-mono', 'convention', 'Amounts/IBAN use font-mono (I-05 invariant)', '*.tsx'),
    (r'TransactionRowSkeleton|BalanceWidgetSkeleton', 'pattern', 'Skeleton components used for loading states', '*.tsx'),
    (r'aria-label|aria-live|role=', 'convention', 'ARIA labels added to interactive/dynamic elements', '*.tsx'),
    (r'text-ai-accent|✦ AI|ai-badge', 'convention', 'AI badge (text-ai-accent) mandatory on AI responses', '*.tsx'),
    (r'ComplianceFlag', 'pattern', 'ComplianceFlag used for BLOCKED/REVIEW transactions', '*.tsx'),
    (r'useState.*loading|loading.*useState', 'pattern', 'useState loading pattern in screen components', '*.tsx'),
]


def get_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def log_action(conn: sqlite3.Connection, tool: str, file_path: str, action: str) -> None:
    conn.execute(
        "INSERT INTO session_log (ts, tool, file_path, action) VALUES (?, ?, ?, ?)",
        (datetime.now(timezone.utc).isoformat(), tool, file_path, action),
    )
    conn.commit()


def capture_patterns(conn: sqlite3.Connection, content: str, file_path: str) -> None:
    for regex, ptype, summary, file_pat in PATTERN_RULES:
        if re.search(regex, content):
            existing = conn.execute(
                "SELECT id, count FROM patterns WHERE summary = ?", (summary,)
            ).fetchone()
            if existing:
                conn.execute(
                    "UPDATE patterns SET count = count + 1, last_seen = ? WHERE id = ?",
                    (datetime.now(timezone.utc).isoformat(), existing[0]),
                )
            else:
                conn.execute(
                    "INSERT INTO patterns (type, summary, file_pat, last_seen) VALUES (?, ?, ?, ?)",
                    (ptype, summary, file_path, datetime.now(timezone.utc).isoformat()),
                )
    conn.commit()


def session_end_summary(conn: sqlite3.Connection) -> None:
    """Print session summary to stdout (captured in Claude Code output)."""
    recent = conn.execute(
        "SELECT tool, file_path, action FROM session_log ORDER BY id DESC LIMIT 10"
    ).fetchall()
    top_patterns = conn.execute(
        "SELECT type, summary, count FROM patterns ORDER BY count DESC LIMIT 5"
    ).fetchall()

    if not recent:
        return

    print("\n🧠 Pro-Workflow session summary:")
    print(f"   Files modified this session: {len(recent)}")
    if top_patterns:
        print("   Top patterns (cumulative):")
        for ptype, summary, count in top_patterns:
            print(f"     [{ptype}] {summary} (×{count})")
    print("")


def main() -> None:
    is_session_end = "--session-end" in sys.argv

    if is_session_end:
        conn = get_db()
        session_end_summary(conn)
        conn.close()
        return

    # PostToolUse: read tool input from stdin
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    tool_name  = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name not in ("Write", "Edit", "MultiEdit"):
        return

    file_path = tool_input.get("file_path", "")
    content   = ""
    if tool_name == "Write":
        content = tool_input.get("content", "")
    elif tool_name == "Edit":
        content = tool_input.get("new_string", "")
    elif tool_name == "MultiEdit":
        for edit in tool_input.get("edits", []):
            content += edit.get("new_string", "")

    if not content or not file_path:
        return

    conn = get_db()
    log_action(conn, tool_name, file_path, f"wrote {len(content)} chars")
    capture_patterns(conn, content, file_path)
    conn.close()


if __name__ == "__main__":
    main()
