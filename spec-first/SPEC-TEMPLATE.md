# SPEC-TEMPLATE.md — Banxe AI Bank Product Specification
**Plane:** Developer (reference for Product Plane implementation)
**Date:** 2026-04-08 | **IL-ref:** IL-045 | **FCA deadline:** 7 May 2026

---

## Section A: User Stories

### Router: /customers — Customer Lifecycle

**Story C-01**
```
As OPERATOR I want to create a customer profile (Individual or Company)
so that KYC can begin for the new customer.
Acceptance: Profile created with entity_type, lifecycle_state=ONBOARDING, risk_level=UNKNOWN.
            Returns customer_id (UUID).
Edge cases: Missing required field → 422. Duplicate email → 409. Blocked jurisdiction → 403.
Auth: JWT Bearer (role: OPERATOR, ADMIN)
FCA: MLR 2017 §18 (CDD), UK GDPR Art.5
```

**Story C-02**
```
As COMPLIANCE_OFFICER I want to get customer profile by ID
so that I can review KYC status and risk level.
Acceptance: Returns full profile including kyc_status, risk_level, entity_type.
Edge cases: Not found → 404. Insufficient role → 403.
Auth: JWT Bearer (role: COMPLIANCE_OFFICER, OPERATOR, ADMIN)
```

**Story C-03**
```
As OPERATOR I want to update customer lifecycle state
so that customer moves through ONBOARDING → ACTIVE → DORMANT → OFFBOARDED.
Acceptance: Valid state transition only. Invalid transition → 400.
            Audit trail written to ClickHouse (I-24).
Edge cases: DECEASED state requires MLRO approval (L3 autonomy).
Auth: JWT Bearer (role: OPERATOR, ADMIN)
FCA: FCA COBS 9A — customer record keeping
```

---

### Router: /auth — Authentication

**Story A-01**
```
As USER I want to login with email + password
so that I receive a JWT access token and refresh token.
Acceptance: Valid credentials → 200 + {access_token, refresh_token, expires_in}.
            Invalid credentials → 401. Account locked → 423.
Edge cases: Rate limit >5 failures → temporary lock. Missing 2FA if enabled → 403.
Auth: None (public endpoint)
```

**Story A-02**
```
As USER I want to verify my TOTP 2FA code
so that SCA requirement is met for transactions >£30 (PSR 2017 Reg.71).
Acceptance: Valid TOTP → 200 + sca_token. Invalid → 401. Expired → 401.
Edge cases: Clock drift ±30s tolerance. Replay attack (used code) → 403.
Auth: JWT Bearer (pre-SCA token)
FCA: PSR 2017 Reg.71 — Strong Customer Authentication
```

**Story A-03**
```
As USER I want to refresh my JWT token
so that my session stays active without re-authentication.
Acceptance: Valid refresh_token → 200 + new access_token. Expired → 401.
Auth: Refresh token (Bearer)
```

---

### Router: /payments — Payment Routing

**Story P-01**
```
As USER I want to initiate a GBP payment
so that funds reach the beneficiary via FPS (<15s) or CHAPS (>£250k).
Acceptance: AML pre-screen PASS → SCA gate (>£30) → rail selection → ledger post → confirmation.
            FPS response <15s (I-05). Returns payment_id, status, rail_used.
Edge cases: Insufficient balance → 402. Blocked jurisdiction → 403. SCA fail → 403.
            AML HOLD → 202 (pending). AML BLOCK → 403.
Auth: JWT Bearer + SCA token (role: USER, OPERATOR)
FCA: PSR 2017 Reg.71 (SCA), PSR APP 2024 (APP scam detection)
```

**Story P-02**
```
As USER I want to initiate a EUR payment via SEPA SCT
so that funds reach EU beneficiary.
Acceptance: Currency=EUR → SEPA_SCT rail. FX rate from Frankfurter :8181.
            Returns payment_id, fx_rate_used, gbp_equivalent.
Edge cases: Non-EUR/GBP currency → 422. FX service down → 503.
Auth: JWT Bearer + SCA token
```

**Story P-03**
```
As TREASURY_MANAGER I want to create a BACS batch payment
so that multiple payroll/bulk payments are sent efficiently.
Acceptance: Batch up to 1000 payments. BACS processing 2 business days.
            mass_payment_batch caller only.
Auth: JWT Bearer (role: TREASURY_MANAGER)
FCA: FCA PS7/24 — payment service requirements
```

---

### Router: /kyc — KYC Verification

**Story K-01**
```
As COMPLIANCE_OFFICER I want to start KYC verification for a customer
so that identity is confirmed before account activation.
Acceptance: Creates KYC job. Returns kyc_job_id, status=PENDING.
            Triggers Sumsub IDV (mock in sandbox, BT-004 blocks live).
Edge cases: Customer not in ONBOARDING state → 409. Missing DOB for Individual → 422.
Auth: JWT Bearer (role: COMPLIANCE_OFFICER, OPERATOR)
FCA: MLR 2017 §18 (CDD requirements)
```

**Story K-02**
```
As COMPLIANCE_OFFICER I want to poll KYC status
so that I know when verification is complete or requires EDD.
Acceptance: Returns kyc_status: PENDING | APPROVED | REJECTED | EDD_REQUIRED.
            EDD_REQUIRED if risk_level HIGH or PEP detected.
Auth: JWT Bearer (role: COMPLIANCE_OFFICER)
```

---

### Router: /aml — AML Transaction Monitoring

**Story M-01**
```
As SYSTEM I want to evaluate a transaction against AML rules
so that suspicious activity is detected before payment executes.
Acceptance: Returns MonitorResult: sanctions_block, edd_required, sar_required, reasons.
            Entity-aware: Individual (EDD >£10k) vs Company (EDD >£50k) (IL-041).
Edge cases: Sanctions hit → immediate BLOCK (no override). PEP → EDD always.
            Structuring (3 txs <£9k in 24h) → SAR signal.
Auth: Service-to-service (internal only, no JWT)
FCA: MLR 2017 Reg.28 (ongoing monitoring), POCA 2002 s.330
```

**Story M-02**
```
As AML_ANALYST I want to retrieve AML monitoring results for a customer
so that I can review transaction history and risk signals.
Acceptance: Returns last 30 days of MonitorResult records for customer_id.
Auth: JWT Bearer (role: AML_ANALYST, COMPLIANCE_OFFICER)
```

---

### Router: /statements — Account Statements

**Story S-01**
```
As USER I want to download my monthly statement in CSV or JSON
so that I have a record of all transactions for the period.
Acceptance: Accepts period (YYYY-MM) and format (csv|json).
            Returns statement with all transactions, opening/closing balance.
Edge cases: Future period → 422. No transactions → empty statement (not 404).
Auth: JWT Bearer (role: USER, OPERATOR)
FCA: CASS 15, FCA PS7/24 — client statement obligations
```

---

### Router: /complaints — Complaint Management

**Story CP-01**
```
As USER I want to file a complaint about a payment or service
so that my issue is tracked and resolved within FCA SLA (8 weeks).
Acceptance: Creates complaint with complaint_id, status=OPEN, sla_deadline=+8weeks.
            Written to ClickHouse complaints table.
Edge cases: Empty description → 422.
Auth: JWT Bearer (role: USER)
FCA: FCA DISP 1.3 — 8-week resolution SLA
```

**Story CP-02**
```
As COMPLIANCE_OFFICER I want to escalate unresolved complaint to FOS
so that regulatory obligation is met if unresolved >8 weeks.
Acceptance: status transitions OPEN → ESCALATED_FOS. Notification sent to customer.
Auth: JWT Bearer (role: COMPLIANCE_OFFICER, ADMIN)
FCA: FCA DISP 1.3.1R — escalation to FOS
```

---

### Router: /health — System Health

**Story H-01**
```
As DEVOPS I want to check health of all service adapters
so that outages are detected before they impact customers.
Acceptance: Returns health map: {clickhouse, midaz, keycloak, frankfurter, aspsp, redis}.
            Each: status (ok|degraded|down), latency_ms.
            Overall: healthy (all ok) | degraded (any degraded) | critical (any down).
Edge cases: Health check timeout 2s per adapter. Partial failure → degraded, not 500.
Auth: None (public) or JWT Bearer (role: ADMIN for detail)
```

---

### Router: /fraud — Fraud Scoring

**Story F-01**
```
As SYSTEM I want to score a transaction for fraud risk
so that high-risk transactions are flagged before payment executes.
Acceptance: Returns FraudScoringResult: score (0-100), risk_level (LOW/MEDIUM/HIGH/CRITICAL),
            factors [], entity_type-aware thresholds (IL-041).
            Score >70 → HOLD. Score >85 → BLOCK (or SAR if >£10k).
Edge cases: Entity type affects EDD threshold (Individual £10k, Company £50k).
Auth: Service-to-service (internal only)
FCA: FCA PS7/24, POCA 2002 s.330
```

---

## Section B: Database Schema

### PostgreSQL :5432 — New Tables (OLTP)

```sql
-- Customer profiles (dual-entity: Individual + Company)
CREATE TABLE IF NOT EXISTS customers (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type     TEXT NOT NULL CHECK (entity_type IN ('INDIVIDUAL', 'COMPANY')),
    email           TEXT UNIQUE NOT NULL,
    profile         JSONB NOT NULL DEFAULT '{}',
    lifecycle_state TEXT NOT NULL DEFAULT 'ONBOARDING'
                    CHECK (lifecycle_state IN ('ONBOARDING','ACTIVE','DORMANT','OFFBOARDED','DECEASED')),
    risk_level      TEXT NOT NULL DEFAULT 'UNKNOWN'
                    CHECK (risk_level IN ('UNKNOWN','LOW','MEDIUM','HIGH','CRITICAL')),
    kyc_status      TEXT NOT NULL DEFAULT 'PENDING'
                    CHECK (kyc_status IN ('PENDING','APPROVED','REJECTED','EDD_REQUIRED')),
    is_pep          BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Agreement / T&C versioning
CREATE TABLE IF NOT EXISTS agreements (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id     UUID NOT NULL REFERENCES customers(id),
    product_type    TEXT NOT NULL,
    version         INTEGER NOT NULL DEFAULT 1,
    signed_at       TIMESTAMPTZ,
    t_and_c_hash    TEXT,
    status          TEXT NOT NULL DEFAULT 'PENDING'
                    CHECK (status IN ('PENDING','SIGNED','REVOKED')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Notification delivery log
CREATE TABLE IF NOT EXISTS notifications (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(id),
    channel     TEXT NOT NULL CHECK (channel IN ('EMAIL','SMS','TELEGRAM','PUSH')),
    template    TEXT NOT NULL,
    recipient   TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'PENDING'
                CHECK (status IN ('PENDING','SENT','FAILED','BOUNCED')),
    sent_at     TIMESTAMPTZ,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Config overrides (runtime, non-code config)
CREATE TABLE IF NOT EXISTS config_overrides (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key         TEXT UNIQUE NOT NULL,
    value       JSONB NOT NULL,
    updated_by  TEXT NOT NULL,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### ClickHouse :9000 — Existing Tables (OLAP / Audit)

| Table | Engine | TTL | Purpose |
|-------|--------|-----|---------|
| `banxe.safeguarding_events` | ReplacingMergeTree | 5Y | CASS 15 daily recon (I-08, I-24) |
| `banxe.safeguarding_breaches` | MergeTree | 5Y | CASS 15 breach escalation |
| `banxe.payment_events` | MergeTree | 5Y | Payment audit trail (I-24) |
| `banxe.complaints` | MergeTree | 7Y | FCA DISP complaint log |
| `banxe.complaint_events` | MergeTree | 7Y | Complaint state transitions |

---

## Section C: API Endpoints

| Method | Path | Request | Response | Auth | FCA Rule |
|--------|------|---------|----------|------|---------|
| POST | /customers | CustomerCreateRequest | CustomerResponse (201) | OPERATOR | MLR 2017 §18 |
| GET | /customers/{id} | — | CustomerResponse | COMPLIANCE_OFFICER | COBS 9A |
| PATCH | /customers/{id}/lifecycle | {state} | CustomerResponse | OPERATOR | COBS 9A |
| POST | /customers/{id}/kyc/start | — | KYCJobResponse | COMPLIANCE_OFFICER | MLR 2017 §18 |
| GET | /customers/{id}/kyc/status | — | KYCStatusResponse | COMPLIANCE_OFFICER | MLR 2017 §18 |
| POST | /auth/login | {email, password} | TokenResponse | None | PSR 2017 Reg.71 |
| POST | /auth/2fa/verify | {totp_code} | SCATokenResponse | pre-SCA JWT | PSR 2017 Reg.71 |
| POST | /auth/refresh | {refresh_token} | TokenResponse | Refresh token | — |
| POST | /payments | PaymentRequest | PaymentResponse (202) | USER + SCA | PSR 2017 Reg.71 |
| GET | /payments/{id} | — | PaymentDetailResponse | USER, OPERATOR | — |
| POST | /payments/batch | BatchPaymentRequest | BatchResponse | TREASURY_MANAGER | PS7/24 |
| POST | /aml/monitor | TxMonitorRequest | MonitorResult | Internal | MLR 2017 Reg.28 |
| GET | /aml/history/{customer_id} | ?days=30 | MonitorResultList | AML_ANALYST | MLR 2017 |
| POST | /fraud/score | FraudScoringRequest | FraudScoringResult | Internal | PS7/24 |
| GET | /statements/{customer_id} | ?period=2026-04&format=csv | StatementResponse | USER | CASS 15, PS7/24 |
| POST | /complaints | ComplaintCreateRequest | ComplaintResponse (201) | USER | FCA DISP 1.3 |
| GET | /complaints/{id} | — | ComplaintDetailResponse | USER, COMPLIANCE_OFFICER | FCA DISP 1.3 |
| PATCH | /complaints/{id}/escalate | — | ComplaintResponse | COMPLIANCE_OFFICER | FCA DISP 1.3.1R |
| GET | /health | — | HealthMapResponse | None/ADMIN | — |
| GET | /health/detailed | — | DetailedHealthResponse | ADMIN | — |

**Total: 20 endpoints across 9 routers.**

---

## Spec-First Methodology Reminder

```
1. User Story → 2. Spec (this doc) → 3. Port (Protocol ABC) → 
4. Service (business logic) → 5. Adapter (mock first, real later) → 
6. Tests (≥15 per service) → 7. quality-gate.sh PASS → 8. IL DONE
```

Before any implementation: run `context_memory_sync` + check this spec.
Before any API change: run `api_contract_guardian`.
Before any commit: `bash scripts/quality-gate.sh PASS`.

## User Stories
<!-- See Section A above -->

## DB Schema
<!-- See Section B: DB Schema above -->
