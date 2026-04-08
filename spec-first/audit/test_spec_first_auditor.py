"""
test_spec_first_auditor.py — Tests for Spec-First Auditor v2 (IL-060)
Developer Plane | developer-core

All tests use tmp_path (pytest fixture) so they are fully isolated
from the actual developer/banxe-emi-stack/banxe-architecture files.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_first_auditor import (
    AGENT_REQUIRED,
    SKILL_REQUIRED,
    AuditorConfig,
    audit_block,
    audit_full,
    check_agent_content,
    check_content,
    check_skill_content,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _make_config(tmp_path: Path) -> AuditorConfig:
    """Return AuditorConfig rooted at tmp_path (no real FS access)."""
    return AuditorConfig(home=tmp_path)


def _scaffold(cfg: AuditorConfig, paths: list[str], content: str = "# dummy") -> None:
    """Create files/directories under cfg.dev, cfg.emi, cfg.arch."""
    for rel in paths:
        # resolve against home
        p = cfg.home / rel
        if rel.endswith("/"):
            p.mkdir(parents=True, exist_ok=True)
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)


def _make_full_block(cfg: AuditorConfig, block: int) -> None:
    """Create all required paths for a given block."""
    from spec_first_auditor import _build_block_checks
    for p in _build_block_checks(cfg)[block]:
        path = Path(p)
        path.parent.mkdir(parents=True, exist_ok=True)
        if "." in path.name:  # file
            path.write_text("# placeholder")
        else:  # directory
            path.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# TestCheckContent
# ─────────────────────────────────────────────────────────────────────────────

class TestCheckContent:
    def test_all_present_returns_empty(self, tmp_path):
        f = tmp_path / "doc.md"
        f.write_text("## Type Annotations\n## Docstrings\n## Запреты\n")
        assert check_content(f, ["Type Annotations", "Docstrings", "Запреты"]) == []

    def test_missing_one_string(self, tmp_path):
        f = tmp_path / "doc.md"
        f.write_text("## FCA\n## CASS\n")
        result = check_content(f, ["FCA", "CASS", "AML"])
        assert result == ["AML"]

    def test_missing_multiple_strings(self, tmp_path):
        f = tmp_path / "doc.md"
        f.write_text("## FCA\n")
        result = check_content(f, ["FCA", "CASS", "AML"])
        assert set(result) == {"CASS", "AML"}

    def test_file_not_exist_returns_empty(self, tmp_path):
        """Missing file is caught by existence check, not content check."""
        result = check_content(tmp_path / "nonexistent.md", ["FCA"])
        assert result == []

    def test_substring_match(self, tmp_path):
        """Content check uses substring matching."""
        f = tmp_path / "doc.md"
        f.write_text("# Compliance Rules (FCA MLR 2017, POCA 2002, CASS 7)")
        result = check_content(f, ["FCA", "CASS", "AML"])
        assert "FCA" not in result
        assert "CASS" not in result
        assert "AML" in result

    def test_multiline_content(self, tmp_path):
        f = tmp_path / "doc.md"
        f.write_text("line1\n## Coverage\nline3\n## Изоляция\n## Минимальный объём\n")
        result = check_content(f, ["Coverage", "Изоляция", "Минимальный объём"])
        assert result == []

    def test_empty_required_list(self, tmp_path):
        f = tmp_path / "doc.md"
        f.write_text("content")
        assert check_content(f, []) == []

    def test_empty_file_fails_all(self, tmp_path):
        f = tmp_path / "doc.md"
        f.write_text("")
        result = check_content(f, ["FCA", "CASS"])
        assert set(result) == {"FCA", "CASS"}


# ─────────────────────────────────────────────────────────────────────────────
# TestCheckAgentContent
# ─────────────────────────────────────────────────────────────────────────────

class TestCheckAgentContent:
    def test_all_agents_compliant(self, tmp_path):
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        for name in ["planner.md", "executor.md"]:
            (agents_dir / name).write_text("## Role\ntext\n## Rules\nrules\n")
        assert check_agent_content(agents_dir) == []

    def test_missing_role(self, tmp_path):
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "planner.md").write_text("## Rules\nrules\n")
        violations = check_agent_content(agents_dir)
        assert any("planner.md" in v and "## Role" in v for v in violations)

    def test_missing_rules(self, tmp_path):
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "planner.md").write_text("## Role\nrole text\n")
        violations = check_agent_content(agents_dir)
        assert any("planner.md" in v and "## Rules" in v for v in violations)

    def test_multiple_agents_mixed(self, tmp_path):
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "ok.md").write_text("## Role\n## Rules\n")
        (agents_dir / "bad.md").write_text("## Role\n")  # missing ## Rules
        violations = check_agent_content(agents_dir)
        assert len(violations) == 1
        assert "bad.md" in violations[0]

    def test_nonexistent_dir_returns_empty(self, tmp_path):
        assert check_agent_content(tmp_path / "nonexistent") == []

    def test_ignores_non_md_files(self, tmp_path):
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "readme.txt").write_text("no ## Role here")
        assert check_agent_content(agents_dir) == []


# ─────────────────────────────────────────────────────────────────────────────
# TestCheckSkillContent
# ─────────────────────────────────────────────────────────────────────────────

class TestCheckSkillContent:
    def test_compliant_skill(self, tmp_path):
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        (skills_dir / "implement.md").write_text("## Steps\nstep 1\n")
        assert check_skill_content(skills_dir) == []

    def test_missing_steps(self, tmp_path):
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        (skills_dir / "deploy.md").write_text("## Description\nno steps here\n")
        violations = check_skill_content(skills_dir)
        assert any("deploy.md" in v and "## Steps" in v for v in violations)

    def test_multiple_skills_all_fail(self, tmp_path):
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        for name in ["a.md", "b.md"]:
            (skills_dir / name).write_text("## Description\n")
        violations = check_skill_content(skills_dir)
        assert len(violations) == 2

    def test_nonexistent_dir_returns_empty(self, tmp_path):
        assert check_skill_content(tmp_path / "nonexistent") == []


# ─────────────────────────────────────────────────────────────────────────────
# TestAuditBlock — existence checks
# ─────────────────────────────────────────────────────────────────────────────

class TestAuditBlockExistence:
    def test_block_pass_all_files_exist(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 0)
        result = audit_block(0, cfg)
        assert result is True

    def test_block_fail_missing_file(self, tmp_path):
        cfg = _make_config(tmp_path)
        # Create block 0 except one file
        from spec_first_auditor import _build_block_checks
        for p in list(_build_block_checks(cfg)[0])[1:]:
            path = Path(p)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("x")
        result = audit_block(0, cfg)
        assert result is False

    def test_unknown_block_returns_false(self, tmp_path):
        cfg = _make_config(tmp_path)
        result = audit_block(99, cfg)
        assert result is False

    def test_territory_violation_fails(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 0)
        # Plant a territory violation
        violation = cfg.emi / ".claude" / "rules" / "quality.md"
        violation.parent.mkdir(parents=True, exist_ok=True)
        violation.write_text("# should not exist here")
        result = audit_block(0, cfg)
        assert result is False

    def test_block8_obsidian_vault(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 8)
        result = audit_block(8, cfg)
        assert result is True

    def test_block9_infrastructure(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 9)
        result = audit_block(9, cfg)
        assert result is True

    def test_block10_api_layer(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 10)
        result = audit_block(10, cfg)
        assert result is True

    def test_block11_quality_gate(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 11)
        result = audit_block(11, cfg)
        assert result is True


# ─────────────────────────────────────────────────────────────────────────────
# TestAuditBlock — content checks
# ─────────────────────────────────────────────────────────────────────────────

class TestAuditBlockContent:
    def test_block3_pass_with_correct_content(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 3)
        # Write compliant content
        (cfg.dev / ".claude/rules/quality.md").write_text(
            "## Type Annotations\n## Docstrings\n## Запреты\n"
        )
        (cfg.dev / ".claude/rules/compliance.md").write_text(
            "FCA rules\nCASS requirements\nAML checks\n"
        )
        (cfg.dev / ".claude/rules/testing.md").write_text(
            "## Coverage\n## Минимальный объём\n## Изоляция\n"
        )
        result = audit_block(3, cfg, strict=True)
        assert result is True

    def test_block3_fail_missing_required_section(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 3)
        (cfg.dev / ".claude/rules/quality.md").write_text(
            "## Type Annotations\n## Docstrings\n"  # missing Запреты
        )
        (cfg.dev / ".claude/rules/compliance.md").write_text("FCA\nCASS\nAML\n")
        (cfg.dev / ".claude/rules/testing.md").write_text(
            "## Coverage\n## Минимальный объём\n## Изоляция\n"
        )
        result = audit_block(3, cfg, strict=True)
        assert result is False

    def test_block3_warn_only_no_fail(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 3)
        # quality.md missing Запреты
        (cfg.dev / ".claude/rules/quality.md").write_text("## Type Annotations\n")
        (cfg.dev / ".claude/rules/compliance.md").write_text("FCA\nCASS\nAML\n")
        (cfg.dev / ".claude/rules/testing.md").write_text(
            "## Coverage\n## Минимальный объём\n## Изоляция\n"
        )
        # warn-only: content violations don't fail
        result = audit_block(3, cfg, strict=False)
        assert result is True

    def test_block7_claude_md_content(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 7)
        (cfg.dev / ".claude/CLAUDE.md").write_text(
            "# EXECUTION ORDER\n## Territory Rules\n## GSD Framework\n"
        )
        result = audit_block(7, cfg, strict=True)
        assert result is True

    def test_block7_claude_md_missing_sections(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 7)
        (cfg.dev / ".claude/CLAUDE.md").write_text("# Generic content\n")
        result = audit_block(7, cfg, strict=True)
        assert result is False

    def test_block1_projectidea_content(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 1)
        (cfg.dev / "spec-first/PROJECTIDEA.md").write_text(
            "## Stack\nPython\n## Metrics\nKPIs here\n"
        )
        result = audit_block(1, cfg, strict=True)
        assert result is True

    def test_block2_spec_template_content(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 2)
        (cfg.dev / "spec-first/SPEC-TEMPLATE.md").write_text(
            "## User Stories\nAs a user...\n## DB Schema\nTables here\n"
        )
        result = audit_block(2, cfg, strict=True)
        assert result is True

    def test_block5_agents_content(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 5)
        # Write compliant agents
        agents_dir = cfg.dev / ".claude/agents"
        for md in agents_dir.glob("*.md"):
            md.write_text("## Role\nrole text\n## Rules\nrules text\n")
        result = audit_block(5, cfg, strict=True)
        assert result is True

    def test_block5_agents_missing_role(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 5)
        agents_dir = cfg.dev / ".claude/agents"
        # One agent is non-compliant
        agent_file = list(agents_dir.glob("*.md"))[0]
        agent_file.write_text("## Rules\nonly rules, no role\n")
        result = audit_block(5, cfg, strict=True)
        assert result is False

    def test_block4_skills_content(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 4)
        skills_dir = cfg.dev / ".claude/skills"
        for md in skills_dir.glob("*.md"):
            md.write_text("## Steps\nstep 1\n")
        result = audit_block(4, cfg, strict=True)
        assert result is True

    def test_block4_skills_missing_steps(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 4)
        skills_dir = cfg.dev / ".claude/skills"
        skill_file = list(skills_dir.glob("*.md"))[0]
        skill_file.write_text("## Description\nno steps\n")
        result = audit_block(4, cfg, strict=True)
        assert result is False


# ─────────────────────────────────────────────────────────────────────────────
# TestAuditFull
# ─────────────────────────────────────────────────────────────────────────────

class TestAuditFull:
    def _scaffold_all_blocks(self, cfg: AuditorConfig) -> None:
        """Create all required files with compliant content."""
        from spec_first_auditor import _build_block_checks
        for block in _build_block_checks(cfg):
            _make_full_block(cfg, block)

        # Write compliant content for content-checked files
        (cfg.dev / ".claude/rules/quality.md").write_text(
            "## Type Annotations\n## Docstrings\n## Запреты\n"
        )
        (cfg.dev / ".claude/rules/compliance.md").write_text("FCA\nCASS\nAML\n")
        (cfg.dev / ".claude/rules/testing.md").write_text(
            "## Coverage\n## Минимальный объём\n## Изоляция\n"
        )
        (cfg.dev / ".claude/CLAUDE.md").write_text(
            "# EXECUTION ORDER\n## Territory Rules\n## GSD Framework\n"
        )
        (cfg.dev / "spec-first/PROJECTIDEA.md").write_text("## Stack\n## Metrics\n")
        (cfg.dev / "spec-first/SPEC-TEMPLATE.md").write_text(
            "## User Stories\n## DB Schema\n"
        )
        # Agents
        for md in (cfg.dev / ".claude/agents").glob("*.md"):
            md.write_text("## Role\n## Rules\n")
        # Skills
        for md in (cfg.dev / ".claude/skills").glob("*.md"):
            md.write_text("## Steps\n")

    def test_full_audit_all_pass(self, tmp_path):
        cfg = _make_config(tmp_path)
        self._scaffold_all_blocks(cfg)
        result = audit_full(cfg, strict=True)
        assert result is True

    def test_full_audit_fail_on_missing_file(self, tmp_path):
        cfg = _make_config(tmp_path)
        self._scaffold_all_blocks(cfg)
        # Remove a required file
        (cfg.dev / "spec-first/PROJECTIDEA.md").unlink()
        result = audit_full(cfg, strict=True)
        assert result is False

    def test_full_audit_fail_on_content_violation(self, tmp_path):
        cfg = _make_config(tmp_path)
        self._scaffold_all_blocks(cfg)
        # Break content
        (cfg.dev / ".claude/rules/quality.md").write_text("no required sections\n")
        result = audit_full(cfg, strict=True)
        assert result is False

    def test_full_audit_pass_warn_only_despite_content_violation(self, tmp_path):
        cfg = _make_config(tmp_path)
        self._scaffold_all_blocks(cfg)
        (cfg.dev / ".claude/rules/quality.md").write_text("no required sections\n")
        result = audit_full(cfg, strict=False)
        assert result is True

    def test_full_audit_fail_on_territory_violation(self, tmp_path):
        cfg = _make_config(tmp_path)
        self._scaffold_all_blocks(cfg)
        # Plant a territory violation
        v = cfg.emi / ".claude" / "rules" / "quality.md"
        v.parent.mkdir(parents=True, exist_ok=True)
        v.write_text("territory violation")
        result = audit_full(cfg, strict=False)  # even warn-only fails on territory
        assert result is False


# ─────────────────────────────────────────────────────────────────────────────
# TestAuditLog
# ─────────────────────────────────────────────────────────────────────────────

class TestAuditLog:
    def test_log_written_on_pass(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 11)
        audit_block(11, cfg)
        assert cfg.log.exists()
        lines = cfg.log.read_text().strip().split("\n")
        entry = json.loads(lines[-1])
        assert entry["block"] == 11

    def test_log_written_on_fail(self, tmp_path):
        cfg = _make_config(tmp_path)
        audit_block(11, cfg)  # no files created → fail
        lines = cfg.log.read_text().strip().split("\n")
        entry = json.loads(lines[-1])
        assert entry["block"] == 11
        assert entry["ok"] is False
        assert len(entry["exist_errors"]) > 0

    def test_log_appends(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 11)
        audit_block(11, cfg)
        audit_block(11, cfg)
        lines = [l for l in cfg.log.read_text().strip().split("\n") if l]
        assert len(lines) >= 2


# ─────────────────────────────────────────────────────────────────────────────
# TestNewBlocks8to11
# ─────────────────────────────────────────────────────────────────────────────

class TestNewBlocks8to11:
    """Dedicated tests for the four new blocks introduced in IL-060."""

    def test_block8_requires_obsidian_index(self, tmp_path):
        cfg = _make_config(tmp_path)
        # Only create sessions and knowledge dirs, not index.md
        (cfg.obsidian / "sessions").mkdir(parents=True)
        (cfg.obsidian / "knowledge").mkdir(parents=True)
        result = audit_block(8, cfg)
        assert result is False  # missing 00-home/index.md

    def test_block8_requires_sessions_dir(self, tmp_path):
        cfg = _make_config(tmp_path)
        (cfg.obsidian / "00-home").mkdir(parents=True)
        (cfg.obsidian / "00-home" / "index.md").write_text("# index")
        (cfg.obsidian / "knowledge").mkdir(parents=True)
        # sessions missing
        result = audit_block(8, cfg)
        assert result is False

    def test_block8_all_present(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 8)
        result = audit_block(8, cfg)
        assert result is True

    def test_block9_requires_ballerine_compose(self, tmp_path):
        cfg = _make_config(tmp_path)
        (cfg.emi / "config/n8n").mkdir(parents=True)
        # missing docker-compose.yml
        result = audit_block(9, cfg)
        assert result is False

    def test_block9_requires_n8n_config_dir(self, tmp_path):
        cfg = _make_config(tmp_path)
        dc = cfg.emi / "infra/ballerine/docker-compose.yml"
        dc.parent.mkdir(parents=True, exist_ok=True)
        dc.write_text("version: '3'")
        # missing config/n8n
        result = audit_block(9, cfg)
        assert result is False

    def test_block10_requires_all_api_files(self, tmp_path):
        cfg = _make_config(tmp_path)
        _make_full_block(cfg, 10)
        result = audit_block(10, cfg)
        assert result is True

    def test_block10_fails_missing_deps(self, tmp_path):
        cfg = _make_config(tmp_path)
        (cfg.emi / "api").mkdir(parents=True, exist_ok=True)
        (cfg.emi / "api/main.py").write_text("# main")
        # missing deps.py, routers, models
        result = audit_block(10, cfg)
        assert result is False

    def test_block11_requires_quality_gate(self, tmp_path):
        cfg = _make_config(tmp_path)
        (cfg.emi / ".env.example").parent.mkdir(parents=True, exist_ok=True)
        (cfg.emi / ".env.example").write_text("# env")
        # missing quality-gate.sh
        result = audit_block(11, cfg)
        assert result is False

    def test_block11_requires_env_example(self, tmp_path):
        cfg = _make_config(tmp_path)
        qg = cfg.emi / "scripts/quality-gate.sh"
        qg.parent.mkdir(parents=True, exist_ok=True)
        qg.write_text("#!/bin/bash")
        # missing .env.example
        result = audit_block(11, cfg)
        assert result is False


# ─────────────────────────────────────────────────────────────────────────────
# TestAuditorConfig
# ─────────────────────────────────────────────────────────────────────────────

class TestAuditorConfig:
    def test_default_config_uses_home(self):
        cfg = AuditorConfig()
        assert cfg.dev == Path.home() / "developer"
        assert cfg.emi == Path.home() / "banxe-emi-stack"
        assert cfg.arch == Path.home() / "banxe-architecture"
        assert cfg.obsidian == Path.home() / "obsidian-vault"

    def test_custom_home(self, tmp_path):
        cfg = AuditorConfig(home=tmp_path)
        assert cfg.dev == tmp_path / "developer"
        assert cfg.emi == tmp_path / "banxe-emi-stack"
        assert cfg.obsidian == tmp_path / "obsidian-vault"

    def test_log_path_under_dev(self, tmp_path):
        cfg = AuditorConfig(home=tmp_path)
        assert cfg.log == tmp_path / "developer/spec-first/audit/audit_log.jsonl"


# ─────────────────────────────────────────────────────────────────────────────
# TestConstants
# ─────────────────────────────────────────────────────────────────────────────

class TestConstants:
    def test_agent_required_contains_role_and_rules(self):
        assert "## Role" in AGENT_REQUIRED
        assert "## Rules" in AGENT_REQUIRED

    def test_skill_required_contains_steps(self):
        assert "## Steps" in SKILL_REQUIRED

    def test_blocks_0_to_11_defined(self, tmp_path):
        from spec_first_auditor import _build_block_checks
        cfg = _make_config(tmp_path)
        blocks = _build_block_checks(cfg)
        assert set(range(12)).issubset(blocks.keys())

    def test_content_checks_covers_key_files(self, tmp_path):
        from spec_first_auditor import _build_content_checks
        cfg = _make_config(tmp_path)
        checks = _build_content_checks(cfg)
        paths = {str(p) for p in checks.keys()}
        assert any("quality.md" in p for p in paths)
        assert any("compliance.md" in p for p in paths)
        assert any("testing.md" in p for p in paths)
        assert any("CLAUDE.md" in p for p in paths)
        assert any("PROJECTIDEA.md" in p for p in paths)
        assert any("SPEC-TEMPLATE.md" in p for p in paths)
