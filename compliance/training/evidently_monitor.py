"""
Evidently AI — Drift Monitor for BANXE Agent Training Corpus
Tracks behavioral drift across training interactions over time.

Usage:
    python3 -m compliance.training.evidently_monitor
    python3 -m compliance.training.evidently_monitor --report html
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from datetime import datetime

import pandas as pd

try:
    from evidently import Dataset, DataDefinition
    from evidently.presets import DataDriftPreset, DataQualityPreset
    from evidently import Report
    EVIDENTLY_V2 = True
except ImportError:
    EVIDENTLY_V2 = False

CORPUS_DIR = Path("compliance/training/corpus")
REPORTS_DIR = Path("compliance/training/results/evidently")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Production thresholds (from methodology)
DRIFT_THRESHOLD = 0.15
ROLE_VIOLATION_THRESHOLD = 0
HALLUCINATION_THRESHOLD = 0.05


def load_corpus_as_dataframe() -> pd.DataFrame:
    """Load all JSONL corpus files into a DataFrame."""
    records = []
    for f in sorted(CORPUS_DIR.glob("corpus_*.jsonl")):
        with open(f) as fp:
            for line in fp:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except Exception:
                        pass
    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["consensus_binary"] = (df["consensus"] == "CONFIRMED").astype(int)
    df["drift_score"] = df["drift_score"].astype(float)
    df["role_violation"] = df["role_boundary_violated"].astype(int)
    df["escalation_error"] = (~df["escalation_correct"]).astype(int)
    df["hitl_flag"] = df["hitl_required"].astype(int)
    return df


def run_drift_report(df: pd.DataFrame, output_format: str = "text") -> dict:
    """Generate Evidently drift report."""
    if df.empty:
        print("[Evidently] No corpus data found.")
        return {}

    # Split into reference (first half) vs current (second half)
    mid = len(df) // 2
    if mid < 5:
        print(f"[Evidently] Too few records ({len(df)}) for drift comparison — need ≥10")
        return _simple_stats(df)

    reference = df.iloc[:mid]
    current = df.iloc[mid:]

    metrics_cols = ["drift_score", "consensus_binary", "role_violation",
                    "escalation_error", "hitl_flag"]

    if EVIDENTLY_V2 and output_format == "html":
        try:
            definition = DataDefinition(
                numerical_columns=["drift_score", "consensus_binary",
                                   "role_violation", "escalation_error", "hitl_flag"]
            )
            ref_dataset = Dataset.from_pandas(reference[metrics_cols], data_definition=definition)
            cur_dataset = Dataset.from_pandas(current[metrics_cols], data_definition=definition)

            report = Report(presets=[DataDriftPreset(), DataQualityPreset()])
            report.run(reference_data=ref_dataset, current_data=cur_dataset)

            out_path = REPORTS_DIR / f"drift_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
            report.save_html(str(out_path))
            print(f"[Evidently] HTML report saved: {out_path}")
        except Exception as e:
            print(f"[Evidently] HTML report failed: {e} — falling back to text")

    return _simple_stats(df, reference, current)


def _simple_stats(df: pd.DataFrame,
                  reference: pd.DataFrame | None = None,
                  current: pd.DataFrame | None = None) -> dict:
    """Text-based drift statistics."""
    total = len(df)
    avg_drift = df["drift_score"].mean()
    confirmed_rate = df["consensus_binary"].mean()
    role_violations = df["role_violation"].sum()
    escalation_errors = df["escalation_error"].sum()
    hitl_flags = df["hitl_flag"].sum()
    hallucination_rate = 1 - confirmed_rate  # approx

    sep = "=" * 60
    print(f"\n{sep}")
    print("  EVIDENTLY AI — BANXE DRIFT MONITOR")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(sep)
    print(f"  Total corpus records:  {total}")
    print()

    def _chk(val, threshold, low_is_good=True):
        ok = val <= threshold if low_is_good else val >= threshold
        return "✅" if ok else "❌"

    print("  Behavioral Metrics:")
    print(f"    {_chk(avg_drift, DRIFT_THRESHOLD)} Avg drift score:     {avg_drift:.4f}  (threshold: <{DRIFT_THRESHOLD})")
    print(f"    {_chk(confirmed_rate, 0.95, False)} Confirmed rate:      {confirmed_rate:.1%}  (threshold: ≥95%)")
    print(f"    {_chk(role_violations, 0)} Role violations:     {role_violations}       (threshold: 0)")
    print(f"    {_chk(escalation_errors, 0)} Escalation errors:   {escalation_errors}       (threshold: 0)")
    print(f"    {_chk(hallucination_rate, HALLUCINATION_THRESHOLD)} Hallucination rate:  {hallucination_rate:.1%}  (threshold: <5%)")

    if current is not None and reference is not None:
        drift_delta = current["drift_score"].mean() - reference["drift_score"].mean()
        direction = "↑ INCREASING" if drift_delta > 0.02 else "↓ decreasing" if drift_delta < -0.02 else "→ stable"
        print()
        print(f"  Drift trend: {direction} (Δ{drift_delta:+.4f})")
        print(f"    Reference period avg: {reference['drift_score'].mean():.4f}")
        print(f"    Current period avg:   {current['drift_score'].mean():.4f}")

    # Overall status
    prod_ready = (avg_drift < DRIFT_THRESHOLD and role_violations == 0
                  and escalation_errors == 0 and confirmed_rate >= 0.95)
    print()
    print(f"  {'🟢 PRODUCTION READY' if prod_ready else '🔴 NOT PRODUCTION READY'}")
    print(sep)

    return {
        "total": total,
        "avg_drift": float(avg_drift),
        "confirmed_rate": float(confirmed_rate),
        "role_violations": int(role_violations),
        "escalation_errors": int(escalation_errors),
        "hallucination_rate": float(hallucination_rate),
        "production_ready": prod_ready,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evidently drift monitor for BANXE training corpus")
    parser.add_argument("--report", choices=["text", "html"], default="text")
    args = parser.parse_args()

    df = load_corpus_as_dataframe()
    run_drift_report(df, output_format=args.report)
