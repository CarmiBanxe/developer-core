# ROADMAP.md — Banxe AI Bank

**Updated:** 2026-04-08 | **Deadline P0:** 7 May 2026

---

## Phase 0: Foundation (COMPLETE ✅)
- ✅ IL-001..IL-011: CASS 15 + FA-01..FA-07 deployed
- ✅ IL-012..IL-016: Sprint P1 (75/75 tests, 80% coverage)
- ✅ IL-039: BT-011 Keycloak 26.2.5 deploy
- ✅ IL-041: Dual-entity AML thresholds
- ✅ IL-044: Skills Orchestration model
- ✅ IL-045: Spec-First + GSD infrastructure

---

## Phase 1: Core API + Services (P0 — deadline 7 May 2026)

| # | Feature | IL | Status | Priority |
|---|---------|-----|--------|----------|
| 1 | Safeguarding Deploy (GMKtec) | IL-043 | IN_PROGRESS | P0 |
| 2 | FastAPI REST API Layer | IL-046 | PENDING | P0 |
| 3 | Notification Service S17-03 | IL-047 | PENDING | P0 |
| 4 | Redis VelocityTracker | TBD | PENDING | P0 |
| 5 | Fraud + AML Pipeline S9-05 | TBD | PENDING | P0 |
| 6 | Consumer Duty S9-06 FCA PS22/9 | TBD | PENDING | P0 |

---

## Phase 2: Integrations (P1 — pending Modulr API key)

| # | Feature | Blocker | Notes |
|---|---------|---------|-------|
| 7 | Modulr Payment Rails | BT-001: API key | Register at modulrfinance.com/developer |
| 8 | Companies House KYB | BT-002: API key | Corporate KYC verification |
| 9 | OpenCorporates | BT-003: API key | Company ownership data |
| 10 | HITL Feedback Loop | - | AI learns from CTIO Oleg's actions |

---

## Phase 3: Compliance Reporting (P2)

| # | Feature | FCA Rule | Notes |
|---|---------|---------|-------|
| 11 | FIN060 Report | CASS 15.12.4R | Monthly safeguarding return |
| 12 | SAR Auto-Filing | POCA 2002 s.330 | With MLRO approval gate |
| 13 | Consumer Duty Annual Report | PS22/9 | 4 outcomes assessment |

---

## Key Milestones

| Date | Milestone |
|------|-----------|
| 2026-04-15 | FastAPI Layer live on GMKtec |
| 2026-04-22 | Notification + Redis complete |
| 2026-04-30 | Fraud + AML wired end-to-end |
| 2026-05-07 | **P0 COMPLETE** — Consumer Duty |
| TBD | Modulr sandbox integration |
| TBD | FIN060 first submission |
