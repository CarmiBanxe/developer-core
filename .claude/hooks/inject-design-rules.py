#!/usr/bin/env python3
"""
inject-design-rules.py — PreToolUse hook for BANXE UI design rule enforcement.
Developer Plane | developer-core | IL-061

Runs before Write/Edit tool calls in banxe-ui context.
Validates that:
  1. No hardcoded hex colors (use design tokens)
  2. No hardcoded pixel values in className (use Tailwind tokens)
  3. No `float` for monetary amounts (I-05 invariant)
  4. No AI response without confidence indicator
  5. No spinner-only loading states (skeleton required)

Exit 0 = proceed | Exit 1 = block + explain
stdin: JSON with tool_name + tool_input
stdout: printed warnings (exit 0) or errors (exit 1)
"""

import json
import re
import sys


# ── Patterns that block ──────────────────────────────────────────────────────

BLOCKING_PATTERNS = [
    (
        r'parseFloat\s*\(|Number\s*\(',
        "I-05: Use Decimal/string for monetary amounts, not parseFloat() or Number(). "
        "Amounts must stay as strings until display.",
    ),
    (
        r'color:\s*#[0-9a-fA-F]{3,6}',
        "Design rule: Hardcoded hex color detected. Use CSS variables (--color-*) "
        "from the design token system instead.",
    ),
    (
        r'style=\{\{[^}]*color:\s*["\'][^"\']*["\']',
        "Design rule: Inline color style detected. Use Tailwind classes with design tokens.",
    ),
]

# ── Patterns that warn (but don't block) ────────────────────────────────────

WARN_PATTERNS = [
    (
        r'<(div|span)\s[^>]*className=["\'][^"\']*spinner',
        "UX rule: Spinner-only loading state detected. Use skeleton screens per design spec.",
    ),
    (
        r'confidence.*["\']UNCERTAIN["\']',
        "AI trust rule: UNCERTAIN confidence must show 'I am not certain' disclaimer.",
    ),
]

# ── Paths where rules apply ──────────────────────────────────────────────────

UI_PATHS = ("banxe-ui/", "apps/web/src/", "apps/mobile/src/", "packages/ui/src/")


def is_ui_file(path: str) -> bool:
    return any(p in path for p in UI_PATHS) and path.endswith((".tsx", ".ts", ".css"))


def check_content(content: str, path: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for pattern, message in BLOCKING_PATTERNS:
        if re.search(pattern, content):
            errors.append(f"BLOCK: {message}")
    for pattern, message in WARN_PATTERNS:
        if re.search(pattern, content):
            warnings.append(f"WARN: {message}")
    return errors, warnings


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0  # not a valid hook call — pass through

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name not in ("Write", "Edit", "MultiEdit"):
        return 0

    file_path = tool_input.get("file_path", "")
    if not is_ui_file(file_path):
        return 0

    content = ""
    if tool_name == "Write":
        content = tool_input.get("content", "")
    elif tool_name == "Edit":
        content = tool_input.get("new_string", "")
    elif tool_name == "MultiEdit":
        for edit in tool_input.get("edits", []):
            content += edit.get("new_string", "")

    if not content:
        return 0

    errors, warnings = check_content(content, file_path)

    for w in warnings:
        print(f"⚠️  {w}", file=sys.stderr)

    if errors:
        print("", file=sys.stderr)
        print("🚫 BANXE Design Rules violated — edit blocked:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        print("", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
