# REQUIREMENTS.md — Banxe AI Bank Technical Requirements

**Plane:** Developer | **Updated:** 2026-04-08

---

## Architecture Constraints

### Hexagonal Architecture (mandatory)
- Every feature: Port (Protocol ABC) → Service (business logic) → Adapter (infrastructure)
- No direct infrastructure calls from Service layer
- MockAdapter required for every real adapter (enables testing without infrastructure)

### Technology Stack
| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.11+ |
| API Framework | FastAPI | 0.100+ |
| ORM/DB | PostgreSQL direct (psycopg2) | 15+ |
| OLAP | ClickHouse | 23+ |
| Cache/Velocity | Redis | 7+ |
| Auth | Keycloak JWT | 26.2.5 |
| Testing | pytest + pytest-cov | latest |
| Linting | ruff + mypy | latest |
| SAST | semgrep | latest |

### Financial Invariants
- **I-05**: All monetary amounts → `Decimal`, never `float`
- **I-08**: Audit trail TTL ≥ 5 years (ClickHouse)
- **I-24**: Audit write BEFORE any business action
- **I-02**: Jurisdiction check BEFORE any transaction

### Quality Gates (mandatory, non-negotiable)
- Unit test coverage ≥ 80% for new files
- Overall coverage ≥ 75%
- 0 semgrep violations (banxe-rules.yml)
- 0 ruff errors
- Minimum 15 tests per new service

### Compliance Stack
- FCA MLR 2017 (AML thresholds)
- POCA 2002 (SAR workflow)
- CASS 7.15 (Safeguarding reconciliation)
- PSR 2017 (FPS SLA <15s, SCA >£30)
- PS22/9 Consumer Duty (4 outcomes)
- UK GDPR Art.5 (PII minimisation)

---

## Infrastructure (GMKtec EVO-X2 — 192.168.0.72)

| Service | Port | Status |
|---------|------|--------|
| Midaz CBS | 8095 | LIVE |
| ClickHouse | 9000 | LIVE |
| PostgreSQL | 5432 | LIVE |
| Keycloak | 8180 | LIVE (realm: banxe) |
| Frankfurter FX | 8181 | LIVE |
| mock-ASPSP | 8888 | LIVE |
| n8n | 5678 | LIVE |
| Redis | 6379 | LIVE |
| FastAPI (banxe-api) | 8000 | TO DEPLOY |

## Blocked Providers (BT = Blocked Task)
| Provider | BT | What's needed |
|----------|----|---------------|
| Modulr | BT-001 | API key from modulrfinance.com/developer |
| Companies House | BT-002 | COMPANIES_HOUSE_API_KEY |
| OpenCorporates | BT-003 | OPENCORPORATES_API_KEY |

---

## Development Rules
- All methodology files → `~/developer/.claude/` (NOT into banxe-emi-stack)
- All business logic → `~/banxe-emi-stack/services/`
- All architecture decisions → `~/banxe-architecture/`
- Run `spec_first_auditor.py` after each block
- Run `quality-gate.sh` before every commit
