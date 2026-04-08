#!/usr/bin/env python3
"""
spec_first_auditor.py — Enforcement script for IL-045 Spec-First Methodology.

Usage:
  python3 spec_first_auditor.py        # audit ALL blocks
  python3 spec_first_auditor.py 3      # audit specific block

Exit codes:
  0 = PASS — all files present, no territory violations
  1 = FAIL — missing files or territory violation detected
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
DEV  = HOME / "developer"
EMI  = HOME / "banxe-emi-stack"
ARCH = HOME / "banxe-architecture"
LOG  = DEV / "spec-first" / "audit" / "audit_log.jsonl"

BLOCK_CHECKS: dict = {
    0: {
        "must_exist": [
            ARCH / "agents/passports/spec_first_auditor.yaml",
            DEV  / "spec-first/audit/spec_first_auditor.py",
        ],
        "must_not_exist": [],
        "must_contain": {},
    },
    1: {
        "must_exist": [DEV / "spec-first/PROJECTIDEA.md"],
        "must_not_exist": [
            ARCH / "PROJECTIDEA.md",
            EMI  / "PROJECTIDEA.md",
        ],
        "must_contain": {
            DEV / "spec-first/PROJECTIDEA.md": [
                "Проблема", "Стек", "MVP scope", "Метрики", "AI-специфика",
            ],
        },
        "min_lines": {DEV / "spec-first/PROJECTIDEA.md": 40},
    },
    2: {
        "must_exist": [DEV / "spec-first/SPEC-TEMPLATE.md"],
        "must_not_exist": [
            EMI  / "SPEC-TEMPLATE.md",
            ARCH / "SPEC-TEMPLATE.md",
        ],
        "must_contain": {
            DEV / "spec-first/SPEC-TEMPLATE.md": [
                "User Stories", "Database Schema", "API Endpoints",
            ],
        },
        "min_lines": {DEV / "spec-first/SPEC-TEMPLATE.md": 80},
    },
    3: {
        "must_exist": [
            DEV / "rules/quality.md",
            DEV / "rules/compliance.md",
            DEV / "rules/testing.md",
        ],
        "must_not_exist": [
            EMI / ".claude/rules/quality.md",
            EMI / ".claude/rules/compliance.md",
            EMI / ".claude/rules/testing.md",
        ],
        "must_contain": {},
    },
    4: {
        "must_exist": [
            DEV / "skills/implement-feature.md",
            DEV / "skills/create-migration.md",
            DEV / "skills/deploy-gmktec.md",
        ],
        "must_not_exist": [
            EMI / ".claude/skills/implement-feature.md",
            EMI / ".claude/skills/create-migration.md",
            EMI / ".claude/skills/deploy-gmktec.md",
        ],
        "must_contain": {},
    },
    5: {
        "must_exist": [
            DEV / "agents/database-architect.md",
            DEV / "agents/backend-engineer.md",
            DEV / "agents/compliance-specialist.md",
            DEV / "agents/qa-reviewer.md",
            DEV / "agents/devops-engineer.md",
        ],
        "must_not_exist": [
            EMI / ".claude/agents/database-architect.md",
            EMI / ".claude/agents/backend-engineer.md",
        ],
        "must_contain": {},
    },
    6: {
        "must_exist": [DEV / ".claude/CLAUDE.md"],
        "must_not_exist": [],
        "must_contain": {
            DEV / ".claude/CLAUDE.md": [
                "Spec-First",
                "EXECUTION ORDER",
                "spec-first-auditor",
            ],
        },
    },
}


def audit_block(block: int) -> bool:
    checks = BLOCK_CHECKS.get(block)
    if checks is None:
        print(f"⛔ Unknown block: {block}")
        return False

    errors: list[str] = []

    for f in checks.get("must_exist", []):
        if not Path(f).exists():
            errors.append(f"MISSING: {f}")

    for f in checks.get("must_not_exist", []):
        if Path(f).exists():
            errors.append(f"TERRITORY VIOLATION: {f} — должен быть в ~/developer/, не здесь!")

    for f, keywords in checks.get("must_contain", {}).items():
        fp = Path(f)
        if fp.exists():
            content = fp.read_text()
            for kw in keywords:
                if kw not in content:
                    errors.append(f"CONTENT MISSING: '{kw}' not in {f}")

    for f, min_ln in checks.get("min_lines", {}).items():
        fp = Path(f)
        if fp.exists():
            lines = len(fp.read_text().splitlines())
            if lines < min_ln:
                errors.append(f"TOO SHORT: {f} has {lines} lines (minimum {min_ln})")

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "block": block,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
    }

    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as log_fh:
        log_fh.write(json.dumps(result) + "\n")

    if errors:
        print(f"⛔ BLOCK {block} FAILED:")
        for e in errors:
            print(f"  - {e}")
        return False

    print(f"✅ BLOCK {block} PASS — all files verified, no territory violations")
    return True


def main() -> int:
    if len(sys.argv) > 1:
        try:
            block = int(sys.argv[1])
        except ValueError:
            print(f"⛔ Invalid block number: {sys.argv[1]}")
            return 1
        return 0 if audit_block(block) else 1

    # Audit ALL blocks
    all_pass = True
    for b in range(7):
        if not audit_block(b):
            all_pass = False
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
