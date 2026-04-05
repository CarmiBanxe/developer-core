"""
registry_loader.py — BANXE scenario registry loader + validator.

Invariants enforced (ADR-007):
  I-1  source ∈ {amltrix, hybrid, internal}
  I-2  source amltrix/hybrid → tactic_id + technique_id + amltrix_version required
  I-3  source internal → amltrix_pending_review required (boolean)
  I-4  fail-fast: ValueError on any violation; no partial registry returned
  I-5  filters operate only on a fully-validated registry
  I-8  engine.id ∈ closed enum
  I-9  engine.mode ∈ {rule, ml, hybrid}
  I-10 (scenario_id, engine.id, rule_id) triple must be unique

Usage:
    from compliance.training.scenarios.registry_loader import load_registry, pending_review

    scenarios = load_registry()
    for s in pending_review(scenarios):
        print(s["id"], s["name"])
    for s in by_engine(scenarios, "tx_monitor"):
        print(s["id"], [e["rule_id"] for e in s.get("engines", [])
                        if e["id"] == "tx_monitor"])
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

_REGISTRY_PATH = Path(__file__).parent / "scenario_registry.yaml"

_VALID_SOURCES = frozenset({"amltrix", "hybrid", "internal"})

_VALID_ENGINE_IDS = frozenset({
    "tx_monitor",
    "sanctions_check",
    "crypto_aml",
    "compliance_validator",
    "workflow_agent",
    "banxe_aml_orchestrator",
    "case_orchestrator",
})

_VALID_ENGINE_MODES = frozenset({"rule", "ml", "hybrid"})


def load_registry(path: Path | None = None) -> list[dict[str, Any]]:
    """
    Load and validate scenario_registry.yaml.

    Raises ValueError (I-4: fail-fast) on any invariant violation.
    Returns fully-validated list of scenario dicts.
    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML required: pip install pyyaml") from e

    registry_path = path or _REGISTRY_PATH
    with open(registry_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    scenarios = data.get("scenarios", [])
    errors: list[str] = []

    # I-4 / I-6: duplicate scenario id check
    seen_ids: set[str] = set()
    for s in scenarios:
        sid = s.get("id", "?")
        if sid in seen_ids:
            errors.append(f"{sid}: duplicate scenario id (I-6)")
        seen_ids.add(sid)

    # I-1..I-3: source + AMLTRIX invariants
    for s in scenarios:
        sid = s.get("id", "?")
        source = s.get("source", "")

        # I-1: valid source
        if source not in _VALID_SOURCES:
            errors.append(f"{sid}: unknown source '{source}' (I-1) — must be amltrix/hybrid/internal")
            continue

        # I-2: AMLTRIX required for amltrix/hybrid
        if source in ("amltrix", "hybrid"):
            amltrix = s.get("amltrix")
            if not amltrix:
                errors.append(f"{sid}: source='{source}' requires non-null amltrix block (I-2)")
            else:
                for field in ("tactic_id", "technique_id", "amltrix_version"):
                    if not amltrix.get(field):
                        errors.append(f"{sid}: source='{source}' requires amltrix.{field} (I-2)")

        # I-3: pending_review required for internal
        elif source == "internal":
            if "amltrix_pending_review" not in s:
                errors.append(f"{sid}: source='internal' requires amltrix_pending_review boolean (I-3)")
            elif not isinstance(s["amltrix_pending_review"], bool):
                errors.append(f"{sid}: amltrix_pending_review must be boolean (I-3)")

        # I-8..I-10: engine binding invariants
        engines = s.get("engines", [])
        seen_triples: set[tuple[str, str]] = set()   # (engine_id, rule_id)
        for eng in engines:
            eng_id   = eng.get("id", "")
            eng_mode = eng.get("mode", "")
            rule_id  = eng.get("rule_id", "")

            # I-8: engine id must be from closed enum
            if eng_id not in _VALID_ENGINE_IDS:
                errors.append(
                    f"{sid}: engine.id '{eng_id}' not in valid set (I-8): {sorted(_VALID_ENGINE_IDS)}"
                )

            # I-9: mode must be rule | ml | hybrid
            if eng_mode not in _VALID_ENGINE_MODES:
                errors.append(
                    f"{sid}: engine.mode '{eng_mode}' invalid (I-9) — must be rule/ml/hybrid"
                )

            # I-10: (engine_id, rule_id) must be unique within scenario
            triple = (eng_id, rule_id)
            if triple in seen_triples:
                errors.append(
                    f"{sid}: duplicate (engine_id={eng_id}, rule_id={rule_id}) within scenario (I-10)"
                )
            seen_triples.add(triple)

            # enabled must be boolean
            if "enabled" in eng and not isinstance(eng["enabled"], bool):
                errors.append(f"{sid}: engine '{eng_id}' enabled must be boolean")

    if errors:
        raise ValueError(
            "scenario_registry.yaml validation failed:\n"
            + "\n".join(f"  - {e}" for e in errors)
        )

    return scenarios


def pending_review(scenarios: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return scenarios with amltrix_pending_review: true (open AMLTRIX mapping backlog)."""
    return [s for s in scenarios if s.get("amltrix_pending_review") is True]


def by_category(
    scenarios: list[dict[str, Any]],
    category: str,
) -> list[dict[str, Any]]:
    """Filter scenarios by category (A/B/C/D/E)."""
    return [s for s in scenarios if s.get("category") == category]


def by_engine(
    scenarios: list[dict[str, Any]],
    engine: str,
) -> list[dict[str, Any]]:
    """
    Filter scenarios that have at least one binding for the given engine id.
    Uses structured engines[] list (I-8). Falls back to linked_engines[] for
    legacy scenarios that predate the engines block.
    """
    result = []
    for s in scenarios:
        engines = s.get("engines")
        if engines is not None:
            # structured binding (preferred)
            if any(e.get("id") == engine for e in engines):
                result.append(s)
        else:
            # legacy fallback
            if engine in s.get("linked_engines", []):
                result.append(s)
    return result


def engine_rules(
    scenarios: list[dict[str, Any]],
    engine: str,
) -> list[dict[str, Any]]:
    """
    Return all engine bindings for a specific engine across all scenarios.
    Each item: {scenario_id, scenario_name, rule_id, mode, enabled}.
    """
    result = []
    for s in scenarios:
        for eng in s.get("engines", []):
            if eng.get("id") == engine:
                result.append({
                    "scenario_id":   s["id"],
                    "scenario_name": s["name"],
                    "rule_id":       eng["rule_id"],
                    "mode":          eng["mode"],
                    "enabled":       eng.get("enabled", True),
                })
    return result


if __name__ == "__main__":
    scenarios = load_registry()
    print(f"Loaded {len(scenarios)} scenarios from {_REGISTRY_PATH.name}")
    print()

    # Pending AMLTRIX review backlog
    backlog = pending_review(scenarios)
    if backlog:
        print(f"AMLTRIX pending review ({len(backlog)}):")
        for s in backlog:
            print(f"  {s['id']} [{s['category']}] {s['name']}")
    else:
        print("No pending AMLTRIX reviews.")
    print()

    # By category
    for cat in ("A", "B", "C", "D", "E"):
        group = by_category(scenarios, cat)
        label = {"A": "hard rules", "B": "edge cases", "C": "red lines",
                 "D": "routing", "E": "uncertainty"}[cat]
        print(f"  Cat {cat} ({label:10s}): {len(group)} scenarios")
    print()

    # Engine coverage map
    print("Engine coverage:")
    for eng in sorted(_VALID_ENGINE_IDS):
        bound = by_engine(scenarios, eng)
        rules = engine_rules(scenarios, eng)
        enabled = sum(1 for r in rules if r["enabled"])
        print(f"  {eng:30s}: {len(bound)} scenarios, {enabled} active rules")
