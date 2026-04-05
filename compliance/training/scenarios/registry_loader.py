"""
registry_loader.py — BANXE scenario registry loader + validator.

Loads scenario_registry.yaml, validates AMLTRIX contract:
  source amltrix/hybrid  → tactic_id + technique_id + amltrix_version required
  source internal        → amltrix_pending_review required

Usage:
    from compliance.training.scenarios.registry_loader import load_registry, pending_review

    scenarios = load_registry()
    for s in pending_review(scenarios):
        print(s["id"], s["name"])
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

_REGISTRY_PATH = Path(__file__).parent / "scenario_registry.yaml"


def load_registry(path: Path | None = None) -> list[dict[str, Any]]:
    """
    Load and validate scenario_registry.yaml.

    Raises ValueError on any AMLTRIX contract violation.
    Returns list of scenario dicts (active only by default).
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

    for s in scenarios:
        sid = s.get("id", "?")
        source = s.get("source", "")

        if source in ("amltrix", "hybrid"):
            amltrix = s.get("amltrix")
            if not amltrix:
                errors.append(f"{sid}: source='{source}' requires amltrix block (not null)")
                continue
            for field in ("tactic_id", "technique_id", "amltrix_version"):
                if not amltrix.get(field):
                    errors.append(f"{sid}: source='{source}' requires amltrix.{field}")

        elif source == "internal":
            if "amltrix_pending_review" not in s:
                errors.append(
                    f"{sid}: source='internal' requires amltrix_pending_review (true/false)"
                )

        else:
            errors.append(f"{sid}: unknown source '{source}' (must be amltrix/hybrid/internal)")

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
    """Filter scenarios linked to a specific AML engine."""
    return [s for s in scenarios if engine in s.get("linked_engines", [])]


if __name__ == "__main__":
    scenarios = load_registry()
    meta_path = _REGISTRY_PATH
    print(f"Loaded {len(scenarios)} scenarios from {meta_path.name}")
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
        print(f"  Cat {cat} ({label}): {len(group)} scenarios")
