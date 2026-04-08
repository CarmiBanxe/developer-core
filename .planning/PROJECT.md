# PROJECT.md — Banxe AI Bank Sprint Plan

**Plane:** Developer | **Updated:** 2026-04-08 | **Managed by:** gsd-planner

---

## Active Sprint: Execution Plan P0 (IL-043 → IL-048)

### Задача 1: Safeguarding Deploy [AGENT: devops-engineer] — IN_PROGRESS
- IL: IL-043
- Files: `scripts/deploy-safeguarding-gmktec.sh`, `services/recon/cron_daily_recon.py`, `config/n8n/shortfall-alert-workflow.json`
- Acceptance: systemd timer active, n8n workflow imported, daily recon runs Mon-Fri 07:00 UTC
- Dependencies: QRAA (CEO must approve SSH to GMKtec)
- Status: PENDING CEO RUN

### Задача 2: FastAPI REST API Layer [AGENT: backend-engineer] — PENDING
- IL: IL-046 (to be created)
- Files: `api/main.py`, `api/routers/*.py`, `api/middleware/*.py`, `tests/test_api_*.py`
- Acceptance: GET /health + 6+ routers, Keycloak JWT auth, ≥15 tests per router
- Dependencies: Задача 1 (DONE state not required, independent)

### Задача 3: Notification Service S17-03 [AGENT: backend-engineer] — PENDING
- IL: IL-047 (to be created)
- Files: `services/notification/`, `tests/test_notification_*.py`
- Acceptance: Telegram + email channels, template system, audit trail
- Dependencies: none

### Задача 4: Redis VelocityTracker [AGENT: backend-engineer + database-architect] — PENDING
- IL: to be created
- Files: `services/velocity/`, `tests/test_velocity_*.py`
- Acceptance: 24h + 30d windows, sorted sets, TTL-native, ≥15 tests
- Dependencies: none

### Задача 5: Fraud + AML Pipeline Wiring S9-05 [AGENT: backend-engineer + compliance-specialist] — PENDING
- IL: to be created
- Files: `services/fraud/`, `services/aml/` (wiring update), `tests/test_fraud_*.py`
- Acceptance: real-time signals, AML integration, compliance review PASS
- Dependencies: Задача 4 (Redis VelocityTracker)

### Задача 6: Consumer Duty S9-06 FCA PS22/9 [AGENT: backend-engineer + compliance-specialist] — PENDING
- IL: to be created
- Files: `services/consumer_duty/`, `tests/test_consumer_duty_*.py`
- Acceptance: 4 outcomes modelled, PS22/9 compliance, compliance review PASS
- Dependencies: none

---

## Blocked Tasks
*(none currently)*

---

## Notes
- Все задачи P0 — deadline 7 May 2026
- Задача 1 ожидает QRAA подтверждения от CEO
- После каждой задачи: `git commit` + обновить STATE.md
