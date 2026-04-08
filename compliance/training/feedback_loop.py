"""
Feedback Loop — corpus corrections → SOUL.md / AGENTS.md / verifier patches.

Reads REFUTED entries from training corpus JSONL files, groups corrections by type,
and generates concrete diffs that can be applied to improve the agents.

Usage:
    python3 compliance/training/feedback_loop.py --report     # show what would be patched
    python3 compliance/training/feedback_loop.py --apply      # apply all patches (CLASS_A only)
    python3 compliance/training/feedback_loop.py --apply --source compliance_validator  # apply one source
    python3 compliance/training/feedback_loop.py --apply \\
        --approver mark-001 --approver-role DEVELOPER \\
        --reason "quarterly SOUL update from corpus"   # also apply CLASS_B (SOUL.md)

G-05 Governance Gate:
    SOUL.md and other CLASS_B files require --approver + --approver-role + --reason.
    Without these flags, soul_patches are skipped (not blocked — just bypassed).
    Pass --strict to abort with error instead of skipping when approver missing.

Called by: scripts/train-agent.sh --feedback / --deploy
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


# ─────────────────────────────────────────────
# Paths (can be overridden via env)
# ─────────────────────────────────────────────
DEVELOPER_DIR = Path(os.environ.get("DEVELOPER_DIR", Path.home() / "developer"))

# ── G-05: Governance gate import (optional — degrades gracefully if missing) ──
_GOVERNANCE_AVAILABLE = False
try:
    _VIBE_SRC = Path(os.environ.get("VIBE_DIR", Path.home() / "vibe-coding")) / "src"
    if str(_VIBE_SRC) not in sys.path:
        sys.path.insert(0, str(_VIBE_SRC))
    from compliance.governance.soul_governance import (  # type: ignore[import]
        ChangeRequest,
        GovernanceError,
        GovernanceGate,
    )
    _GOVERNANCE_AVAILABLE = True
except ImportError:
    pass
CORPUS_DIR    = DEVELOPER_DIR / "compliance" / "training" / "corpus"
VIBE_DIR      = Path(os.environ.get("VIBE_DIR", Path.home() / "vibe-coding"))
SOUL_MD       = VIBE_DIR / "docs" / "SOUL.md"
AGENTS_MD     = VIBE_DIR / "agents" / "workspace-moa" / "AGENTS.md"  # canonical — deployed to GMKtec

CV_PATH = DEVELOPER_DIR / "compliance" / "verification" / "compliance_validator.py"
PA_PATH = DEVELOPER_DIR / "compliance" / "verification" / "policy_agent.py"
WA_PATH = DEVELOPER_DIR / "compliance" / "verification" / "workflow_agent.py"


# ─────────────────────────────────────────────
# Data types
# ─────────────────────────────────────────────

class Correction:
    def __init__(self, entry: dict):
        self.statement       = entry.get("statement", "")
        self.agent_id        = entry.get("agent_id", "unknown")
        self.agent_role      = entry.get("agent_role", "unknown")
        self.consensus       = entry.get("consensus", "")
        self.correction      = entry.get("correction", "")
        self.source          = entry.get("correction_source", "")
        self.rule            = entry.get("compliance_rule") or entry.get("workflow_rule") or entry.get("policy_rule") or ""
        self.reason          = entry.get("compliance_reason") or entry.get("workflow_reason") or entry.get("policy_reason") or ""
        self.timestamp       = entry.get("timestamp", "")
        self.drift_score     = entry.get("drift_score", 0)

    @property
    def patch_type(self) -> str:
        """Classify what kind of patch this correction suggests."""
        src = self.source.lower()
        rule = self.rule.lower()
        reason = self.reason.lower()

        if "compliance validator" in src or "fca mlr" in rule or "aml red line" in rule:
            return "forbidden_pattern"
        if "policy agent" in src or "emi authorisation" in rule or "transfer limits" in rule:
            return "policy_violation"
        if "workflow agent" in src or "mlro authority" in rule or "role boundaries" in rule:
            return "workflow_violation"
        if "soul" in reason or "step" in reason:
            return "soul_update"
        # Default: try to infer from the correction text
        if any(k in self.correction.lower() for k in ["pep", "edd", "mlro", "sanctions", "kyc"]):
            return "soul_update"
        return "agents_update"


# ─────────────────────────────────────────────
# Corpus reading
# ─────────────────────────────────────────────

def load_corpus(since_date: str | None = None) -> list[Correction]:
    """Load all REFUTED entries with corrections from corpus JSONL files."""
    corrections: list[Correction] = []
    if not CORPUS_DIR.exists():
        print(f"[feedback_loop] WARN: corpus dir not found: {CORPUS_DIR}", file=sys.stderr)
        return []

    for path in sorted(CORPUS_DIR.glob("corpus_*.jsonl")):
        # Optional date filter (e.g. "2026-04-04")
        if since_date and path.stem.replace("corpus_", "") < since_date.replace("-", ""):
            continue
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if entry.get("consensus") == "REFUTED" and entry.get("correction"):
                    corrections.append(Correction(entry))

    return corrections


# ─────────────────────────────────────────────
# Deduplication
# ─────────────────────────────────────────────

def _already_present(text: str, file_path: Path) -> bool:
    """Return True if key phrase from text already exists in target file."""
    if not file_path.exists():
        return False
    # Extract key 4-word phrase from middle of text
    words = text.split()
    if len(words) >= 4:
        key = " ".join(words[max(0, len(words)//2 - 2):len(words)//2 + 2]).lower()
    else:
        key = text[:40].lower()
    try:
        return key in file_path.read_text().lower()
    except Exception:
        return False


def _pattern_already_in_cv(pattern: str) -> bool:
    """Check if a pattern string already exists in compliance_validator.py."""
    if not CV_PATH.exists():
        return False
    try:
        return pattern.lower() in CV_PATH.read_text().lower()
    except Exception:
        return False


# ─────────────────────────────────────────────
# Patch generators
# ─────────────────────────────────────────────

def _extract_forbidden_pattern(correction: Correction) -> str | None:
    """Extract a regex pattern from a REFUTED compliance_validator correction."""
    reason = correction.reason.lower()
    # Pattern: "Statement contains forbidden pattern: 'pattern'"
    m = re.search(r"forbidden pattern:\s*['\"]([^'\"]+)['\"]", correction.reason, re.IGNORECASE)
    if m:
        return m.group(1)
    # Fallback: extract key words from statement
    stmt_words = [w for w in correction.statement.lower().split() if len(w) > 4]
    if len(stmt_words) >= 2:
        return rf"{re.escape(stmt_words[0])}\s+.*{re.escape(stmt_words[1])}"
    return None


def generate_forbidden_pattern_patch(corrections: list[Correction]) -> list[dict]:
    """Generate patches for compliance_validator.py _FORBIDDEN_PATTERNS."""
    patches = []
    seen_patterns: set[str] = set()

    for c in corrections:
        pattern = _extract_forbidden_pattern(c)
        if not pattern or pattern in seen_patterns:
            continue
        if _pattern_already_in_cv(pattern):
            continue
        seen_patterns.add(pattern)
        patches.append({
            "type": "forbidden_pattern",
            "file": str(CV_PATH),
            "pattern": pattern,
            "example_statement": c.statement[:120],
            "reason": c.reason,
            "insert_after": "_FORBIDDEN_PATTERNS = [",
            "line_to_add": f'    r"{pattern}",  # auto: {c.rule or "REFUTED"} {datetime.now().strftime("%Y-%m-%d")}',
        })

    return patches


def generate_soul_patch(corrections: list[Correction]) -> list[dict]:
    """Generate additions to SOUL.md from workflow/policy corrections."""
    patches = []
    seen: set[str] = set()

    for c in corrections:
        # Extract the core compliance rule from the correction
        rule_hint = c.correction[:150].strip()
        if len(rule_hint) < 10:
            continue
        key = rule_hint[:40].lower()
        if key in seen:
            continue
        if _already_present(rule_hint, SOUL_MD):
            continue
        seen.add(key)

        # Generate a concise soul instruction
        soul_line = _correction_to_soul_line(c)
        if soul_line:
            patches.append({
                "type": "soul_update",
                "file": str(SOUL_MD),
                "soul_line": soul_line,
                "insert_after": "СТРОГО ЗАПРЕЩЕНО:",
                "reason": c.reason,
                "example_statement": c.statement[:120],
                "rule": c.rule,
            })

    return patches


def _correction_to_soul_line(c: Correction) -> str | None:
    """Convert a correction into a concise SOUL.md instruction line."""
    rule = (c.rule or "").lower()
    reason = (c.reason or "").lower()
    stmt = c.statement.lower()

    # Map known rule patterns to SOUL instructions
    if "forbidden pattern" in reason:
        m = re.search(r"forbidden pattern:\s*['\"]([^'\"]+)['\"]", c.reason, re.IGNORECASE)
        if m:
            pattern = m.group(1).replace("\\s+", " ").replace("\\s", " ")
            return f"- ЗАПРЕЩЕНО: '{pattern}' в любом ответе — немедленный REFUTED"

    if "pep" in stmt and ("without edd" in stmt or "skip edd" in stmt):
        return "- PEP всегда требует EDD и MLRO одобрение — нет исключений"

    if "mlro" in rule and "sar" in stmt:
        return "- SAR только через MLRO — самостоятельная отправка в NCA запрещена"

    if "role boundaries" in rule:
        role = c.agent_role.lower()
        action = re.search(r"attempting '([^']+)'", c.reason)
        if action:
            return f"- {c.agent_role}: '{action.group(1)}' вне границ роли — эскалировать"

    if "emi authorisation scope" in rule:
        product = re.search(r"does not offer '([^']+)'", c.reason)
        if product:
            return f"- BANXE не предлагает '{product.group(1)}' — EMI scope только"

    if "hitl" in rule and "hitl" not in stmt:
        return "- При триггере HITL (PEP, sanctions, ≥£10,000) всегда указывать human review"

    return None


def generate_agents_patch(corrections: list[Correction]) -> list[dict]:
    """Generate patches for AGENTS.md (workflow routing rules)."""
    patches = []
    seen: set[str] = set()

    for c in corrections:
        if "workflow" not in c.source.lower():
            continue
        rule_key = c.rule[:50].lower() if c.rule else c.reason[:50].lower()
        if rule_key in seen:
            continue
        seen.add(rule_key)

        patch_line = None
        if "mlro authority" in c.rule.lower():
            patch_line = f"- {c.agent_role}: MLRO required for '{c.reason[:60]}'"
        elif "role boundaries" in c.rule.lower():
            action = re.search(r"attempting '([^']+)'", c.reason)
            if action:
                patch_line = f"- {c.agent_role}: cannot '{action.group(1)}' — escalate to higher role"
        elif "hitl" in c.rule.lower():
            patch_line = f"- Trigger HITL and mention human review when: {c.reason[:80]}"

        if patch_line:
            patches.append({
                "type": "agents_update",
                "file": "AGENTS.md (GMKtec workspace)",
                "line_to_add": patch_line,
                "reason": c.reason,
                "rule": c.rule,
            })

    return patches


# ─────────────────────────────────────────────
# Report generation
# ─────────────────────────────────────────────

def generate_report(corrections: list[Correction]) -> dict:
    """Group corrections and generate all patches."""
    by_type: dict[str, list[Correction]] = defaultdict(list)
    for c in corrections:
        by_type[c.patch_type].append(c)

    forbidden_patches = generate_forbidden_pattern_patch(by_type.get("forbidden_pattern", []))
    soul_patches       = generate_soul_patch(corrections)  # all types contribute
    agents_patches     = generate_agents_patch(by_type.get("workflow_violation", []))

    return {
        "corpus_entries":   len(corrections),
        "by_type":          {k: len(v) for k, v in by_type.items()},
        "forbidden_patches": forbidden_patches,
        "soul_patches":      soul_patches,
        "agents_patches":    agents_patches,
        "timestamp":         datetime.utcnow().isoformat(),
    }


def print_report(report: dict) -> None:
    """Print human-readable report."""
    RULE  = "─" * 50
    DLINE = "═" * 50

    print(f"\n{DLINE}")
    print(f"  FEEDBACK LOOP REPORT  {report['timestamp'][:10]}")
    print(DLINE)
    print(f"  Corpus entries (REFUTED): {report['corpus_entries']}")
    print(f"  By type: {report['by_type']}")
    print()

    if report["forbidden_patches"]:
        print(f"{RULE}")
        print(f"  compliance_validator.py — NEW FORBIDDEN PATTERNS ({len(report['forbidden_patches'])})")
        print(RULE)
        for p in report["forbidden_patches"]:
            print(f"  + {p['line_to_add']}")
            print(f"    Example: {p['example_statement'][:80]}")
        print()

    if report["soul_patches"]:
        print(f"{RULE}")
        print(f"  SOUL.md — NEW INSTRUCTIONS ({len(report['soul_patches'])})")
        print(f"  Insert after 'СТРОГО ЗАПРЕЩЕНО:'")
        print(RULE)
        for p in report["soul_patches"]:
            print(f"  + {p['soul_line']}")
            print(f"    Rule: {p['rule'] or 'N/A'}")
        print()

    if report["agents_patches"]:
        print(f"{RULE}")
        print(f"  AGENTS.md — NEW ROUTING RULES ({len(report['agents_patches'])})")
        print(RULE)
        for p in report["agents_patches"]:
            print(f"  + {p['line_to_add']}")
        print()

    total = (len(report["forbidden_patches"]) +
             len(report["soul_patches"]) +
             len(report["agents_patches"]))
    print(DLINE)
    print(f"  Total patches: {total}")
    print(f"  To apply: python3 feedback_loop.py --apply")
    print(DLINE + "\n")


# ─────────────────────────────────────────────
# Apply patches
# ─────────────────────────────────────────────

def apply_forbidden_patches(patches: list[dict]) -> int:
    """Add new patterns to compliance_validator.py _FORBIDDEN_PATTERNS list."""
    if not patches or not CV_PATH.exists():
        return 0

    content = CV_PATH.read_text()
    applied = 0

    for p in patches:
        line = p["line_to_add"] + "\n"
        if p["pattern"] in content:
            print(f"  [SKIP] pattern already present: {p['pattern'][:50]}")
            continue
        # Insert after _FORBIDDEN_PATTERNS = [
        content = content.replace(
            "_FORBIDDEN_PATTERNS = [\n",
            "_FORBIDDEN_PATTERNS = [\n" + "    " + line,
            1
        )
        applied += 1
        print(f"  [APPLY] compliance_validator.py: + {p['pattern'][:60]}")

    if applied:
        CV_PATH.write_text(content)
    return applied


def apply_soul_patches(patches: list[dict]) -> int:
    """Add new instructions to SOUL.md via local file edit (caller must run protect-soul.sh)."""
    if not patches or not SOUL_MD.exists():
        print(f"  [SKIP] SOUL.md not found at {SOUL_MD}")
        return 0

    content = SOUL_MD.read_text()
    applied = 0

    for p in patches:
        line = p["soul_line"]
        if line.lower() in content.lower():
            print(f"  [SKIP] already in SOUL.md: {line[:60]}")
            continue
        # Insert after "СТРОГО ЗАПРЕЩЕНО:"
        content = content.replace(
            "СТРОГО ЗАПРЕЩЕНО:\n",
            "СТРОГО ЗАПРЕЩЕНО:\n" + line + "\n",
            1
        )
        applied += 1
        print(f"  [APPLY] SOUL.md: + {line[:80]}")

    if applied:
        SOUL_MD.write_text(content)
    return applied


_AGENTS_AUTO_SECTION = "## Auto-Generated Routing Rules"


def apply_agents_patches(patches: list[dict]) -> int:
    """Apply workflow routing rule patches to local agents/workspace-moa/AGENTS.md."""
    if not patches:
        return 0

    if not AGENTS_MD.exists():
        print(f"  [SKIP] AGENTS.md not found at {AGENTS_MD}")
        return 0

    content = AGENTS_MD.read_text()
    applied = 0

    # Ensure the auto-generated section exists
    if _AGENTS_AUTO_SECTION not in content:
        content = content.rstrip("\n") + f"\n\n---\n\n{_AGENTS_AUTO_SECTION}\n\n"
        print(f"  [INIT] Added '{_AGENTS_AUTO_SECTION}' section to AGENTS.md")

    for p in patches:
        line = p["line_to_add"].strip()
        if not line:
            continue
        if line.lower() in content.lower():
            print(f"  [SKIP] already in AGENTS.md: {line[:60]}")
            continue
        # Insert after the auto-generated section header
        content = content.replace(
            _AGENTS_AUTO_SECTION + "\n\n",
            _AGENTS_AUTO_SECTION + "\n\n" + line + "\n",
            1
        )
        applied += 1
        print(f"  [APPLY] AGENTS.md: + {line[:80]}")

    if applied:
        AGENTS_MD.write_text(content)

    return applied


def _git_commit_push(repo_dir: Path, files: list[Path], message: str) -> bool:
    """Stage specific files, commit, pull --rebase, push. Returns True on success."""
    try:
        # Only stage files that exist and have changes
        changed = [str(f) for f in files if f.exists()]
        if not changed:
            return True
        subprocess.run(["git", "-C", str(repo_dir), "add"] + changed, check=True)
        # Check if anything staged
        result = subprocess.run(
            ["git", "-C", str(repo_dir), "diff", "--cached", "--name-only"],
            capture_output=True, text=True
        )
        if not result.stdout.strip():
            return True
        subprocess.run(["git", "-C", str(repo_dir), "commit", "-m", message], check=True)
        subprocess.run(
            ["git", "-C", str(repo_dir), "pull", "--rebase", "origin", "main", "--quiet"],
            check=True
        )
        subprocess.run(["git", "-C", str(repo_dir), "push"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [WARN] Git operation failed: {e}", file=sys.stderr)
        return False


def commit_developer_changes(applied: int) -> None:
    """Commit compliance_validator.py changes to developer-core."""
    if applied == 0:
        return
    date_str = datetime.now().strftime("%Y-%m-%d")
    msg = f"feat(feedback): apply {applied} corrections from corpus [{date_str}]"
    ok = _git_commit_push(DEVELOPER_DIR, [CV_PATH, PA_PATH, WA_PATH], msg)
    if ok:
        print(f"  [GIT] developer-core: committed and pushed {applied} changes")


def commit_vibe_changes(soul_applied: int, agents_applied: int) -> None:
    """Commit SOUL.md and AGENTS.md changes to vibe-coding."""
    total = soul_applied + agents_applied
    if total == 0:
        return
    parts = []
    if soul_applied:
        parts.append(f"SOUL.md ({soul_applied} rules)")
    if agents_applied:
        parts.append(f"AGENTS.md ({agents_applied} routing rules)")
    date_str = datetime.now().strftime("%Y-%m-%d")
    msg = f"feat(feedback): auto-patch {', '.join(parts)} from corpus [{date_str}]"
    ok = _git_commit_push(VIBE_DIR, [SOUL_MD, AGENTS_MD], msg)
    if ok:
        print(f"  [GIT] vibe-coding: committed and pushed SOUL.md + AGENTS.md")


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

def _governance_check_soul(
    approver_id:   str | None,
    approver_role: str | None,
    reason:        str,
    soul_patches:  list[dict],
    strict:        bool = False,
) -> bool:
    """
    G-05: Run governance gate before applying SOUL.md patches.

    Returns True if patches should be applied, False if they should be skipped.
    Raises SystemExit(1) in --strict mode when gate blocks.

    Without governance module (fallback): always returns True (legacy behaviour).
    """
    if not soul_patches:
        return True

    if not _GOVERNANCE_AVAILABLE:
        print("  [G-05] Governance module not available — SOUL.md patches applied without gate")
        return True

    # Build diff summary for audit log
    diff_lines = [p.get("soul_line", "")[:80] for p in soul_patches[:5]]
    diff_summary = "; ".join(diff_lines)

    gate = GovernanceGate()
    req  = ChangeRequest(
        target_file   = "docs/SOUL.md",
        change_type   = "soul_update",
        proposed_by   = "feedback_loop",
        content_diff  = diff_summary,
        approver_id   = approver_id,
        approver_role = approver_role,
        reason        = reason,
    )

    try:
        decision = gate.evaluate(req)
        print(
            f"  [G-05] SOUL.md governance APPROVED "
            f"[CLASS_{decision.change_class}] "
            f"approver={decision.approver_id} role={decision.approver_role}"
        )
        return True
    except GovernanceError as e:
        if strict:
            print(f"\n[G-05] SOUL.md governance BLOCKED:\n  {e}", file=sys.stderr)
            sys.exit(1)
        print(
            f"  [G-05] SOUL.md governance gate: no approver provided — "
            f"skipping {len(soul_patches)} soul_patch(es).\n"
            f"  To apply SOUL.md changes, pass: "
            f"--approver <id> --approver-role DEVELOPER|CTIO|CEO --reason '<text>'"
        )
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="BANXE Feedback Loop — corpus → patches")
    parser.add_argument("--report",       action="store_true", help="Show what would be patched (no changes)")
    parser.add_argument("--apply",        action="store_true", help="Apply all patches")
    parser.add_argument("--source",       default=None,        help="Filter by source: compliance_validator, policy_agent, workflow_agent")
    parser.add_argument("--since",        default=None,        help="Only process corpus from this date YYYY-MM-DD")
    parser.add_argument("--json",         action="store_true", help="Output JSON report")
    # G-05 governance gate arguments
    parser.add_argument("--approver",       default=None, help="[G-05] Approver ID for CLASS_B changes (SOUL.md)")
    parser.add_argument("--approver-role",  default=None, help="[G-05] Approver role: DEVELOPER | CTIO | CEO")
    parser.add_argument("--reason",         default="",   help="[G-05] Reason for CLASS_B change")
    parser.add_argument("--strict",         action="store_true",
                        help="[G-05] Abort with error if governance gate blocks (default: skip)")
    args = parser.parse_args()

    if not args.report and not args.apply:
        parser.print_help()
        sys.exit(0)

    print(f"[feedback_loop] Loading corpus from {CORPUS_DIR} ...")
    corrections = load_corpus(since_date=args.since)

    if args.source:
        corrections = [c for c in corrections if args.source.lower() in c.source.lower()]

    if not corrections:
        print("[feedback_loop] No REFUTED corrections found in corpus.")
        return

    print(f"[feedback_loop] Found {len(corrections)} REFUTED entries with corrections")

    report = generate_report(corrections)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return

    print_report(report)

    if args.apply:
        print("Applying patches...\n")
        cv_applied     = apply_forbidden_patches(report["forbidden_patches"])
        agents_applied = apply_agents_patches(report["agents_patches"])

        # ── G-05: Governance gate for SOUL.md (CLASS_B) ──────────────────────
        soul_allowed = _governance_check_soul(
            approver_id   = args.approver,
            approver_role = getattr(args, "approver_role", None),
            reason        = args.reason,
            soul_patches  = report["soul_patches"],
            strict        = args.strict,
        )
        soul_applied = apply_soul_patches(report["soul_patches"]) if soul_allowed else 0

        total_applied = cv_applied + soul_applied + agents_applied
        commit_developer_changes(cv_applied)
        commit_vibe_changes(soul_applied, agents_applied)
        print(f"\n[feedback_loop] Done — {total_applied} patches applied")
        print(f"  compliance_validator.py: {cv_applied}")
        print(f"  SOUL.md:                 {soul_applied}")
        print(f"  AGENTS.md:               {agents_applied}")
        if soul_applied or agents_applied:
            print("\n[feedback_loop] vibe-coding committed — train-agent.sh --deploy will auto-deploy to GMKtec")


if __name__ == "__main__":
    main()
