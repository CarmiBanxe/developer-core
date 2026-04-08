#!/usr/bin/env python3
"""
GSD + Spec-First Auditor — territory & completeness enforcement.
IL-045 | Developer Plane | banxe-architecture/agents/passports/spec_first_auditor.yaml

Usage:
  python3 spec_first_auditor.py          # audit ALL blocks
  python3 spec_first_auditor.py 3        # audit specific block
  python3 spec_first_auditor.py --full   # explicit full audit

Exit: 0 = ALL PASS | 1 = FAIL (missing file or territory violation)
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
DEV  = HOME / "developer"
EMI  = HOME / "banxe-emi-stack"
ARCH = HOME / "banxe-architecture"
LOG  = DEV / "spec-first" / "audit" / "audit_log.jsonl"

# Territory violations — files that MUST NOT exist in these locations
TERRITORY_VIOLATIONS = [
    EMI / ".claude" / "rules" / "quality.md",
    EMI / ".claude" / "rules" / "compliance.md",
    EMI / ".claude" / "rules" / "testing.md",
    EMI / ".claude" / "skills" / "implement-feature.md",
    EMI / ".claude" / "skills" / "create-migration.md",
    EMI / ".claude" / "skills" / "deploy-gmktec.md",
    EMI / ".claude" / "agents" / "database-architect.md",
    EMI / ".claude" / "agents" / "backend-engineer.md",
    EMI / ".claude" / "agents" / "qa-reviewer.md",
    ARCH / "PROJECTIDEA.md",
    ARCH / "SPEC-TEMPLATE.md",
    EMI / "PROJECTIDEA.md",
    EMI / "SPEC-TEMPLATE.md",
]

# Block checks — files that MUST exist in correct locations
BLOCK_CHECKS: dict[int, list[Path]] = {
    0: [
        ARCH / "agents/passports/spec_first_auditor.yaml",
        DEV  / "spec-first/audit/spec_first_auditor.py",
    ],
    1: [DEV / "spec-first/PROJECTIDEA.md"],
    2: [DEV / "spec-first/SPEC-TEMPLATE.md"],
    3: [
        DEV / ".claude/rules/quality.md",
        DEV / ".claude/rules/compliance.md",
        DEV / ".claude/rules/testing.md",
    ],
    4: [
        DEV / ".claude/skills/implement-feature.md",
        DEV / ".claude/skills/create-migration.md",
        DEV / ".claude/skills/deploy-gmktec.md",
    ],
    5: [
        DEV / ".claude/agents/gsd-planner.md",
        DEV / ".claude/agents/gsd-executor.md",
        DEV / ".claude/agents/gsd-verifier.md",
        DEV / ".claude/agents/database-architect.md",
        DEV / ".claude/agents/backend-engineer.md",
        DEV / ".claude/agents/compliance-specialist.md",
        DEV / ".claude/agents/qa-reviewer.md",
        DEV / ".claude/agents/devops-engineer.md",
    ],
    6: [
        DEV / ".claude/commands/gsd-new-project.md",
        DEV / ".claude/commands/gsd-plan-phase.md",
        DEV / ".claude/commands/gsd-execute-plan.md",
        DEV / ".claude/commands/gsd-quick.md",
        DEV / ".claude/commands/gsd-health.md",
        DEV / ".claude/commands/gsd-help.md",
    ],
    7: [
        DEV / ".claude/CLAUDE.md",
        DEV / ".planning/PROJECT.md",
        DEV / ".planning/STATE.md",
        DEV / ".planning/REQUIREMENTS.md",
        DEV / ".planning/roadmap/ROADMAP.md",
    ],
}


def audit_block(block: int) -> bool:
    checks = BLOCK_CHECKS.get(block)
    if checks is None:
        print(f"⛔ Unknown block: {block}")
        return False

    errors: list[str] = []

    # Check required files exist
    for f in checks:
        if not Path(f).exists():
            errors.append(f"MISSING: {f}")

    # Check territory violations
    for f in TERRITORY_VIOLATIONS:
        if Path(f).exists():
            errors.append(f"TERRITORY VIOLATION: {f}")

    result = {
        "ts":     datetime.now(timezone.utc).isoformat(),
        "block":  block,
        "ok":     not errors,
        "errors": errors,
    }
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as fh:
        fh.write(json.dumps(result) + "\n")

    if errors:
        print(f"⛔ BLOCK {block} FAILED:")
        for e in errors:
            print(f"  - {e}")
        return False

    print(f"✅ BLOCK {block} PASS — all files verified, no territory violations")
    return True


def audit_full() -> bool:
    all_pass = True
    for b in sorted(BLOCK_CHECKS):
        if not audit_block(b):
            all_pass = False
    return all_pass


def main() -> int:
    p = argparse.ArgumentParser(description="GSD + Spec-First Auditor")
    p.add_argument("block", nargs="?", type=int, default=None,
                   help="Block number (0-7). Omit for full audit.")
    p.add_argument("--full", action="store_true", help="Audit all blocks.")
    args = p.parse_args()

    if args.full or args.block is None:
        return 0 if audit_full() else 1
    return 0 if audit_block(args.block) else 1


if __name__ == "__main__":
    sys.exit(main())
