#!/usr/bin/env python3
"""
GSD + Spec-First Auditor v2 — territory, existence & content enforcement.
IL-060 | Developer Plane | banxe-architecture/agents/passports/spec_first_auditor.yaml

Usage:
  python3 spec_first_auditor.py          # audit ALL blocks
  python3 spec_first_auditor.py 3        # audit specific block
  python3 spec_first_auditor.py --full   # explicit full audit
  python3 spec_first_auditor.py --strict # content violations also block (default)
  python3 spec_first_auditor.py --warn-only  # content violations warn but don't fail

Exit: 0 = ALL PASS | 1 = FAIL (missing file, territory violation, or content violation)

v2 changes (IL-060):
  - Content validation: required sections checked per file
  - Blocks 8-11: Obsidian vault, Infrastructure, API layer, Quality gate
  - Pre-commit hook support: --pre-commit mode
  - Configurable roots for testability (AuditorConfig)
"""
import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ── Configuration (injectable for tests) ─────────────────────────────────────

@dataclass
class AuditorConfig:
    """Root paths — override in tests by passing different home."""
    home: Path = field(default_factory=Path.home)

    @property
    def dev(self) -> Path:
        return self.home / "developer"

    @property
    def emi(self) -> Path:
        return self.home / "banxe-emi-stack"

    @property
    def arch(self) -> Path:
        return self.home / "banxe-architecture"

    @property
    def obsidian(self) -> Path:
        return self.home / "obsidian-vault"

    @property
    def log(self) -> Path:
        return self.dev / "spec-first" / "audit" / "audit_log.jsonl"


# ── Content requirements ──────────────────────────────────────────────────────
# Maps relative path (from dev root) → list of required substrings.
# For agents/* and skills/* the key is a glob pattern.

def _build_content_checks(cfg: AuditorConfig) -> dict[Path, list[str]]:
    """Return dict of {absolute_path: [required_substrings]}."""
    return {
        cfg.dev / ".claude/rules/quality.md":     ["Type Annotations", "Docstrings", "Запреты"],
        cfg.dev / ".claude/rules/compliance.md":   ["FCA", "CASS", "AML"],
        cfg.dev / ".claude/rules/testing.md":      ["Coverage", "Минимальный объём", "Изоляция"],
        cfg.dev / ".claude/CLAUDE.md":             ["EXECUTION ORDER", "Territory Rules", "GSD Framework"],
        cfg.dev / "spec-first/PROJECTIDEA.md":     ["## Stack", "## Metrics"],
        cfg.dev / "spec-first/SPEC-TEMPLATE.md":   ["## User Stories", "## DB Schema"],
    }


# Required substrings for all agent and skill files (checked dynamically).
AGENT_REQUIRED = ["## Role", "## Rules"]
SKILL_REQUIRED = ["## Steps"]


# ── Territory violations ──────────────────────────────────────────────────────

def _build_territory_violations(cfg: AuditorConfig) -> list[Path]:
    return [
        cfg.emi / ".claude" / "rules" / "quality.md",
        cfg.emi / ".claude" / "rules" / "compliance.md",
        cfg.emi / ".claude" / "rules" / "testing.md",
        cfg.emi / ".claude" / "skills" / "implement-feature.md",
        cfg.emi / ".claude" / "skills" / "create-migration.md",
        cfg.emi / ".claude" / "skills" / "deploy-gmktec.md",
        cfg.emi / ".claude" / "agents" / "database-architect.md",
        cfg.emi / ".claude" / "agents" / "backend-engineer.md",
        cfg.emi / ".claude" / "agents" / "qa-reviewer.md",
        cfg.arch / "PROJECTIDEA.md",
        cfg.arch / "SPEC-TEMPLATE.md",
        cfg.emi / "PROJECTIDEA.md",
        cfg.emi / "SPEC-TEMPLATE.md",
    ]


# ── Block checks ──────────────────────────────────────────────────────────────

def _build_block_checks(cfg: AuditorConfig) -> dict[int, list[Path]]:
    return {
        0: [
            cfg.arch / "agents/passports/spec_first_auditor.yaml",
            cfg.dev  / "spec-first/audit/spec_first_auditor.py",
        ],
        1: [cfg.dev / "spec-first/PROJECTIDEA.md"],
        2: [cfg.dev / "spec-first/SPEC-TEMPLATE.md"],
        3: [
            cfg.dev / ".claude/rules/quality.md",
            cfg.dev / ".claude/rules/compliance.md",
            cfg.dev / ".claude/rules/testing.md",
        ],
        4: [
            cfg.dev / ".claude/skills/implement-feature.md",
            cfg.dev / ".claude/skills/create-migration.md",
            cfg.dev / ".claude/skills/deploy-gmktec.md",
        ],
        5: [
            cfg.dev / ".claude/agents/gsd-planner.md",
            cfg.dev / ".claude/agents/gsd-executor.md",
            cfg.dev / ".claude/agents/gsd-verifier.md",
            cfg.dev / ".claude/agents/database-architect.md",
            cfg.dev / ".claude/agents/backend-engineer.md",
            cfg.dev / ".claude/agents/compliance-specialist.md",
            cfg.dev / ".claude/agents/qa-reviewer.md",
            cfg.dev / ".claude/agents/devops-engineer.md",
        ],
        6: [
            cfg.dev / ".claude/commands/gsd-new-project.md",
            cfg.dev / ".claude/commands/gsd-plan-phase.md",
            cfg.dev / ".claude/commands/gsd-execute-plan.md",
            cfg.dev / ".claude/commands/gsd-quick.md",
            cfg.dev / ".claude/commands/gsd-health.md",
            cfg.dev / ".claude/commands/gsd-help.md",
        ],
        7: [
            cfg.dev / ".claude/CLAUDE.md",
            cfg.dev / ".planning/PROJECT.md",
            cfg.dev / ".planning/STATE.md",
            cfg.dev / ".planning/REQUIREMENTS.md",
            cfg.dev / ".planning/roadmap/ROADMAP.md",
        ],
        # ── New blocks (IL-060) ──────────────────────────────────────────────
        8: [
            # Obsidian Knowledge Vault
            cfg.obsidian / "00-home/index.md",
            cfg.obsidian / "sessions",
            cfg.obsidian / "knowledge",
        ],
        9: [
            # Infrastructure
            cfg.emi / "infra/ballerine/docker-compose.yml",
            cfg.emi / "config/n8n",
        ],
        10: [
            # API layer
            cfg.emi / "api/main.py",
            cfg.emi / "api/deps.py",
            cfg.emi / "api/routers",
            cfg.emi / "api/models",
        ],
        11: [
            # Quality gate
            cfg.emi / "scripts/quality-gate.sh",
            cfg.emi / ".env.example",
        ],
    }


# ── Content validation ────────────────────────────────────────────────────────

def check_content(path: Path, required: list[str]) -> list[str]:
    """
    Return list of missing required substrings in path's content.
    Returns [] if file doesn't exist (missing file is caught by existence check).
    """
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return [f"UNREADABLE: {path}"]
    return [s for s in required if s not in text]


def check_agent_content(agents_dir: Path) -> list[str]:
    """Check all *.md in agents_dir contain AGENT_REQUIRED strings."""
    violations: list[str] = []
    if not agents_dir.is_dir():
        return violations
    for md in sorted(agents_dir.glob("*.md")):
        missing = check_content(md, AGENT_REQUIRED)
        for s in missing:
            violations.append(f"CONTENT: {md.name} missing '{s}'")
    return violations


def check_skill_content(skills_dir: Path) -> list[str]:
    """Check all *.md in skills_dir contain SKILL_REQUIRED strings."""
    violations: list[str] = []
    if not skills_dir.is_dir():
        return violations
    for md in sorted(skills_dir.glob("*.md")):
        missing = check_content(md, SKILL_REQUIRED)
        for s in missing:
            violations.append(f"CONTENT: {md.name} missing '{s}'")
    return violations


# ── Core audit logic ──────────────────────────────────────────────────────────

def audit_block(
    block: int,
    cfg: AuditorConfig,
    strict: bool = True,
) -> bool:
    """
    Audit a single block. Returns True = PASS, False = FAIL.

    strict=True  → content violations count as FAIL (exit 1)
    strict=False → content violations are WARN (exit 0)
    """
    block_checks = _build_block_checks(cfg)
    if block not in block_checks:
        print(f"⛔ Unknown block: {block}")
        return False

    exist_errors: list[str] = []
    territory_errors: list[str] = []
    content_errors: list[str] = []
    content_checks = _build_content_checks(cfg)
    territory_violations = _build_territory_violations(cfg)

    # 1. Existence check
    for p in block_checks[block]:
        if not Path(p).exists():
            exist_errors.append(f"MISSING: {p}")

    # 2. Territory violation check (always run for every block)
    for p in territory_violations:
        if Path(p).exists():
            territory_errors.append(f"TERRITORY VIOLATION: {p}")

    # 3. Content checks for files in this block
    for p in block_checks[block]:
        path = Path(p)
        if path in content_checks:
            missing = check_content(path, content_checks[path])
            for s in missing:
                content_errors.append(f"CONTENT: {path.name} missing '{s}'")

    # 4. Agent content checks (block 5)
    if block == 5:
        content_errors.extend(
            check_agent_content(cfg.dev / ".claude/agents")
        )

    # 5. Skill content checks (block 4)
    if block == 4:
        content_errors.extend(
            check_skill_content(cfg.dev / ".claude/skills")
        )

    # Determine pass/fail
    hard_errors = exist_errors + territory_errors
    fail = bool(hard_errors) or (strict and bool(content_errors))

    # Log
    result = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "block": block,
        "ok": not fail,
        "exist_errors": exist_errors,
        "territory_errors": territory_errors,
        "content_errors": content_errors,
    }
    cfg.log.parent.mkdir(parents=True, exist_ok=True)
    with open(cfg.log, "a") as fh:
        fh.write(json.dumps(result) + "\n")

    # Print
    if not hard_errors and not content_errors:
        print(f"✅ BLOCK {block} PASS — all files verified, no violations")
        return True

    for e in exist_errors:
        print(f"  ⛔ {e}")
    for e in territory_errors:
        print(f"  ⛔ {e}")

    if content_errors:
        prefix = "  ⛔" if strict else "  ⚠️"
        for e in content_errors:
            print(f"{prefix} {e}")

    if fail:
        print(f"⛔ BLOCK {block} FAIL")
        return False
    else:
        print(f"⚠️  BLOCK {block} PASS (with content warnings)")
        return True


def audit_full(cfg: AuditorConfig, strict: bool = True) -> bool:
    all_pass = True
    block_checks = _build_block_checks(cfg)
    print("")
    print("═══ SPEC-FIRST AUDITOR v2 ═══════════════════════════════")
    print(f"  Home: {cfg.home}  |  strict={strict}")
    print(f"  Date: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print("═══════════════════════════════════════════════════════════")
    for b in sorted(block_checks):
        if not audit_block(b, cfg, strict=strict):
            all_pass = False
    print("───────────────────────────────────────────────────────────")
    result_str = "✅ PASS" if all_pass else "❌ FAIL"
    print(f"  RESULT: {result_str}")
    print("═══════════════════════════════════════════════════════════")
    print("")
    return all_pass


# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description="GSD + Spec-First Auditor v2")
    p.add_argument("block", nargs="?", type=int, default=None,
                   help="Block number (0-11). Omit for full audit.")
    p.add_argument("--full", action="store_true", help="Audit all blocks.")
    p.add_argument("--warn-only", action="store_true",
                   help="Content violations produce warnings, not errors.")
    p.add_argument("--pre-commit", action="store_true",
                   help="Pre-commit mode: strict, terse output.")
    args = p.parse_args(argv)

    strict = not args.warn_only
    cfg = AuditorConfig()

    if args.full or args.block is None:
        return 0 if audit_full(cfg, strict=strict) else 1
    return 0 if audit_block(args.block, cfg, strict=strict) else 1


if __name__ == "__main__":
    sys.exit(main())
