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

| # | Feature | IL | Status | Tests |
|---|---------|-----|--------|-------|
| 1 | Safeguarding Deploy (GMKtec) | IL-043 | DONE ✅ | 13/13 |
| 2 | FastAPI REST API Layer | IL-046 | DONE ✅ | 80/80 |
| 3 | Notification Service S17-03 | IL-047 | DONE ✅ | 38/38 |
| 4 | Redis VelocityTracker | IL-048 | DONE ✅ | 22/22 |
| 5 | Fraud + AML Pipeline S9-05 | IL-049 | DONE ✅ | 27/27 |
| 6 | Consumer Duty S9-06 FCA PS22/9 | IL-050 | DONE ✅ | 33/33 |

**Phase 1 COMPLETE ✅ — 680/680 tests PASS (2026-04-08)**

---

## Phase 2: Integrations (P1 — pending API keys)

| # | Feature | Blocker | Notes |
|---|---------|---------|-------|
| 7 | Modulr Payment Rails | BT-001: API key | Register at modulrfinance.com/developer |
| 8 | Companies House KYB | BT-002: API key | Corporate KYC verification |
| 9 | OpenCorporates | BT-003: API key | Company ownership data |
| 10 | Sardine.ai Fraud Scoring | BT-004: API key | Contact sales@sardine.ai |
| 11 | HITL Feedback Loop | - | AI learns from CTIO Oleg's actions |

---

## Phase 3: Compliance Reporting (P2)

| # | Feature | FCA Rule | Notes |
|---|---------|---------|-------|
| 12 | FIN060 Report | CASS 15.12.4R | Monthly safeguarding return |
| 13 | SAR Auto-Filing | POCA 2002 s.330 | With MLRO approval gate |
| 14 | n8n Shortfall Alert Workflow | CASS 7.15.29R | Manual import pending |

---

## Key Milestones

| Date | Milestone | Status |
|------|-----------|--------|
| 2026-04-08 | **Phase 1 COMPLETE** — 680 tests, all 6 IL done | ✅ DONE |
| TBD | Modulr sandbox integration | ⏳ Awaiting API key |
| TBD | Sardine.ai fraud scoring (live) | ⏳ Awaiting API key |
| TBD | FIN060 first submission | ⏳ Phase 3 |
| 2026-05-07 | **P0 deadline** | 🟢 On track |
