"""
Compliance Validator Agent — Layer 1 (Regulatory)
Verifies FCA/EMD2/AML/KYC compliance of agent statements.
Authority: FCA MLR 2017, OFAC, EMD2, SAMLA 2018
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ── Jurisdiction / policy scope ──────────────────────────────────────────────
# BANXE canonical compliance baseline. Project-specific runtime may extend this
# scope, but developer-core validators default to UK FCA EMI policy framing.
_POLICY_JURISDICTION = "UK"        # FCA EMI — source of truth for policy scope
_POLICY_REGULATOR    = "FCA"       # Authorising regulator
_POLICY_FRAMEWORK    = "MLR 2017"  # Money Laundering Regulations (primary framework)


class Verdict(str, Enum):
    CONFIRMED = "CONFIRMED"
    REFUTED = "REFUTED"
    UNCERTAIN = "UNCERTAIN"


@dataclass
class VerificationResult:
    verdict: Verdict
    rule: Optional[str]
    reason: str
    confidence: float  # 0.0–1.0
    policy_scope: dict[str, str] = field(default_factory=lambda: {
        "jurisdiction": _POLICY_JURISDICTION,
        "regulator":    _POLICY_REGULATOR,
        "framework":    _POLICY_FRAMEWORK,
    })


# Regulatory rules — immutable (change requires MLRO approval)
_HARD_BLOCK_JURISDICTIONS = {
    "RU", "BY", "IR", "KP", "CU", "MM", "AF", "VE",
    "CRIMEA", "DNR", "LNR"
}

_HIGH_RISK_JURISDICTIONS = {
    # FATF greylist + EU AML High-Risk (updated 2026-04-05)
    # See COMPLIANCE_ARCH.md §Jurisdiction Classification, Category B
    "SY", "IQ", "LB", "YE", "HT", "ML",  # original
    "DZ", "AO", "BO", "VG", "CM", "CI",  # added 2025-2026
    "CD", "KE", "LA", "MC", "NA", "NP",  # added 2024-2025
    "SS", "TT", "VU", "BG", "VN",        # FATF/EU AML HR
}

_THRESHOLD_SAR = 85        # composite score → auto-SAR
_THRESHOLD_REJECT = 70     # composite score → REJECT
_THRESHOLD_HOLD = 40       # composite score → HOLD (below = APPROVE)
_WATCHMAN_MIN_MATCH = 0.80 # Jaro-Winkler, never change without MLRO approval
_AUDIT_TTL_YEARS = 5       # FCA MLR 2017 minimum

# Red-line phrases that agents MUST NOT emit
_FORBIDDEN_PATTERNS = [
    # KYC/EDD bypass or skip
    r"\bbypass\s+.{0,15}\b(kyc|edd|sanctions|screening|aml)\b",
    r"\bskip\s+.{0,15}\b(kyc|sanctions|screening|edd|aml|verification|sar|suspicious)\b",
    r"no\s+need\s+to\s+report",
    r"\bignore\s+.{0,15}\b(risk|alert|flag|warning)\b",
    # Affirmative approve-without (we/I/can directly before approve or close to it)
    r"\b(?:i|we|you)\s+(?:will|can|should|could)\s+.{0,40}\bapprove\b.{0,40}\bwithout\s+(?:edd|kyc|mlro|enhanced|verification|sanctions)\b",
    r"\bwe\s+can\s+approve\b.{0,40}\bwithout\b",
    r"without\s+kyc\b",
    r"without\s+verification\b",
    # MLRO / EDD bypass — direct phrasing (not negated context)
    r"\bwithout\s+mlro\b",                  # "without MLRO" anywhere
    r"\bwithout\s+edd\b",
    r"\bwithout\s+enhanced\s+due\s+diligence\b",
    r"transfer\s+without\s+(monitoring|reporting)",
    r"structure\s+.*payment",
    r"split\s+.*avoid\s+(report|threshold|limit)",
    # "verify...later" (deferred KYC)
    r"\bverify\s+.{0,25}\blater\b",
    # Exception for VIP/client (flexible)
    r"\bexception\s+.{0,20}\b(vip|client|customer)\b",
    # Tipping-off offence (POCA 2002 s.333A) — two directions
    r"\b(inform|tell|notify|warn)\s+.{0,30}\b(customer|client|them)\b.{0,80}\b(sar|investigation|nca)\b",
    r"\bsar\b.{0,80}\b(inform|tell|notify|warn)\s+.{0,30}\b(customer|client|them)\b",
    r"tip\s*-?\s*off",
    # Audit trail tampering
    r"\bdelete\s+.{0,25}\b(audit|record|entry|evidence|log)\b",
    r"\b(replace|overwrite|remove)\s+.{0,20}\b(audit|record|entry|evidence)\b",
    # Threshold change without authorisation (raised/lowered/adjusted, long distance to "without")
    r"\b(lower|raise|raised|lowered|change|adjust|set)\s+.{0,30}\bthreshold\b.{0,80}\bwithout\b",
    r"\bthreshold\b.{0,80}\bwithout\s+.{0,20}\b(mlro|approval|authoris)\b",
]


class ComplianceValidator:
    """Compatibility shim — wraps module-level verify() as a callable class."""
    def verify(self, statement: str, context: dict | None = None) -> VerificationResult:
        return verify(statement, context)


def verify(statement: str, context: dict | None = None) -> VerificationResult:
    """
    Check whether an agent statement is FCA/AML compliant.

    Returns REFUTED immediately on any hard violation.
    Returns CONFIRMED if statement aligns with known compliance rules.
    Returns UNCERTAIN if cannot determine compliance from statement alone.
    """
    text = statement.lower()
    context = context or {}

    # --- CRITICAL: red-line pattern check ---
    for pattern in _FORBIDDEN_PATTERNS:
        if re.search(pattern, text):
            return VerificationResult(
                verdict=Verdict.REFUTED,
                rule="FCA MLR 2017 §3 / AML Red Line",
                reason=f"Statement contains forbidden pattern: '{pattern}'",
                confidence=1.0,
            )

    # --- Hard-block jurisdiction check (match uppercase only in original statement) ---
    for jur in _HARD_BLOCK_JURISDICTIONS:
        # Search original statement (not lowercased) to avoid "by"→"BY", "ir"→"IR" false positives
        pattern = rf'\b{re.escape(jur)}\b'
        if re.search(pattern, statement) and "block" not in text and "reject" not in text:
            return VerificationResult(
                verdict=Verdict.REFUTED,
                rule="SAMLA 2018 / UK HMT Consolidated List",
                reason=f"Statement mentions sanctioned jurisdiction '{jur}' without REJECT action",
                confidence=0.90,
            )

    # --- Threshold compliance check ---
    if _check_wrong_threshold(text):
        return VerificationResult(
            verdict=Verdict.REFUTED,
            rule="COMPLIANCE_ARCH.md §Decision Thresholds",
            reason="Statement references incorrect risk thresholds (REJECT≥70, HOLD 40-69, APPROVE<40)",
            confidence=0.85,
        )

    # --- EDD requirement for high-risk ---
    if _requires_edd(text) and "edd" not in text and "enhanced due diligence" not in text:
        return VerificationResult(
            verdict=Verdict.UNCERTAIN,
            rule="FCA EDD §4.2",
            reason="High-risk scenario identified but EDD not mentioned",
            confidence=0.70,
        )

    # --- SAR auto-filing check ---
    # Only flag when statement describes actively filing/submitting SAR, not when
    # SAR is merely mentioned in a regulatory or record-keeping context.
    _SAR_ACTION = any(re.search(p, text) for p in [
        r"\bfile\s+.{0,20}\bsar\b",
        r"\bsubmit\s+.{0,20}\bsar\b",
        r"\bsar\b.{0,20}\bfile\b",
        r"\bsar\b.{0,20}\bsubmit\b",
        r"\bfile\s+(?:the\s+)?suspicious\b",
    ])
    if _SAR_ACTION:
        if "human review" not in text and "hitl" not in text and "mlro" not in text:
            return VerificationResult(
                verdict=Verdict.UNCERTAIN,
                rule="FCA MLR 2017 §19 / NCA reporting",
                reason="SAR filing action described but human review (HITL/MLRO) not referenced",
                confidence=0.65,
            )

    # --- Audit trail check ---
    if "audit" in text and ("5 year" not in text and "five year" not in text):
        # Not necessarily wrong — just no mention of retention
        pass

    # Statement passes all regulatory checks
    return VerificationResult(
        verdict=Verdict.CONFIRMED,
        rule=None,
        reason="No FCA/AML regulatory violations detected",
        confidence=0.80,
    )


def _check_wrong_threshold(text: str) -> bool:
    """Detect if statement uses wrong thresholds."""
    # Pattern: approve at score >= 70 (should be reject)
    if re.search(r"approve.{0,30}(score|risk).{0,10}[789]\d", text):
        return True
    # Pattern: reject at score < 40 (should be approve)
    if re.search(r"reject.{0,30}(score|risk).{0,10}[123]\d", text):
        return True
    return False


def _requires_edd(text: str) -> bool:
    """Detect if scenario requires Enhanced Due Diligence."""
    edd_triggers = ["pep", "politically exposed", "high risk", ">£10k", "10,000", "10000"]
    return any(t in text for t in edd_triggers)


if __name__ == "__main__":
    import sys
    statement = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "This transaction should be approved without screening."
    result = verify(statement)
    print(f"Verdict:    {result.verdict.value}")
    print(f"Rule:       {result.rule or '—'}")
    print(f"Reason:     {result.reason}")
    print(f"Confidence: {result.confidence:.2f}")
