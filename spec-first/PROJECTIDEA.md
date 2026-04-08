# PROJECTIDEA.md — Banxe AI Bank
**Plane:** Developer | **Date:** 2026-04-08 | **IL-ref:** IL-045

---

## 1. Название

**Banxe AI Bank** — FCA-regulated Electronic Money Institution (EMI) с AI-native compliance engine и agent-driven operations.

---

## 2. Проблема

Традиционные банки и ЕМИ работают на legacy-стеках (COBOL, монолиты, ручной compliance). Это приводит к:
- Медленным KYC/AML проверкам (дни → должно быть минуты)
- Высоким операционным расходам на compliance (MLRO, CCO, ручные SAR)
- Плохой масштабируемости при изменениях FCA-правил
- Невозможности соответствовать FCA CASS 15 deadline (7 May 2026) без автоматизации

**Решение:** EMI без legacy. AI-native compliance — агенты проверяют каждую транзакцию, поддерживают dual-entity модель, автоматически генерируют FIN060 и MLRO-отчёты. HITL только для HIGH-risk решений.

---

## 3. Целевая аудитория

| Роль | Потребность |
|------|-------------|
| FCA-регулируемый fintech | EMI infrastructure без legacy |
| MLRO (SMF17) | Автоматический SAR + отчёты |
| Compliance Officer | Real-time AML monitoring, EDD workflow |
| Treasury Manager | FPS <15s routing, NOSTRO reconciliation |
| Customer | Мгновенные GBP/EUR платежи, прозрачный KYC |

---

## 4. Ключевые фичи (из DEPARTMENT-MAP.md)

1. **KYC/Identity** — dual-entity (Individual/Company), UBO registry, Sumsub IDV integration
2. **AML/Compliance** — Watchman sanctions, Jube fraud scoring, dual-entity thresholds (£10k / £50k EDD)
3. **Payment Routing** — FPS (TomPayment1 <15s), SEPA SCT (EUR), CHAPS (>£250k), BACS batch
4. **Safeguarding (CASS 15)** — daily reconciliation, FIN060 PDF, ClickHouse audit trail (5Y TTL)
5. **Consumer Duty (PS22/9)** — 4 outcomes assessor, fair value, vulnerable customer detection
6. **Core Banking (Midaz CBS)** — LedgerPort, double-entry, GL, NOSTRO reconciliation
7. **Notification Service** — email (SendGrid) + SMS (Twilio) + Telegram + push (4 channels)
8. **Agreement Management** — T&C versioning, digital signature, product binding post-KYC
9. **Security/IAM** — Keycloak 26.2.5, 7 roles, 2FA TOTP, SCA gate >£30 (PSR 2017 Reg.71)
10. **Regulatory Reporting** — FIN060 (CASS 15.12.4R), MLRO annual, client statements, RegData

---

## 5. Стек технологий

### Deployed на GMKtec EVO-X2 (192.168.0.72)

| Компонент | Версия | Порт | Назначение |
|-----------|--------|------|-----------|
| Python | 3.12 | — | Основной язык |
| FastAPI | latest | :8000 | REST API (Task 2) |
| Midaz CBS | latest | :8095 | Core Banking System |
| ClickHouse | latest | :9000 | Audit trail, OLAP (TTL 5Y) |
| PostgreSQL + pgAudit 17.1 | 17.1 | :5432 | OLTP, KYC, agreements |
| Keycloak | 26.2.5 | :8180 | IAM, JWT, 7 roles |
| Frankfurter FX | latest | :8181 | ECB FX rates (self-hosted) |
| mock-ASPSP | FastAPI | :8888 | PSD2 sandbox (adorsys) |
| n8n | latest | :5678 | MLRO alerts, webhooks |
| Redis | 7.x | :6379 | VelocityTracker (Task 4) |
| Ollama | 0.18.3 | :11434 | qwen3-banxe-v2 AI model |
| dbt Core | latest | — | staging→safeguarding→fin060 |
| WeasyPrint | latest | — | FIN060 PDF generation |

### Planned

| Компонент | Назначение | Blocker |
|-----------|-----------|---------|
| Modulr/ClearBank API | Live payment rails | BT-001 (CEO: register) |
| Sumsub IDV | Real KYC verification | BT-004 (CEO: API key) |
| SendGrid + Twilio | Notification delivery | BT-010 (CEO: API keys) |
| Kafka | Event streaming | BT-007 |
| Sardine.ai | Live fraud adapter | BT-009 |

---

## 6. Бизнес-модель

- **FCA EMI License** — Electronic Money Institution authorised by FCA (FRN pending)
- **Revenue streams:**
  - Payment processing fees (FPS: flat fee per transaction)
  - FX spread (EUR/GBP conversions via Frankfurter)
  - Monthly account fees (business accounts)
  - CASS 7 safeguarding float (interest on pooled client funds)
- **Cost model:** AI replaces manual compliance ops (MLRO headcount = 1 vs industry 5+)

---

## 7. MVP scope

### В MVP (7 May 2026 deadline)

- ✅ CASS 15 Safeguarding reconciliation (daily, automated)
- ✅ AML monitoring (dual-entity thresholds, structuring detection)
- ✅ KYC dual-entity model (Individual + Company stubs)
- ✅ Payment mock routing (FPS/SEPA mock via MockAdapter)
- ✅ REST API 9 routers (Task 2 — FastAPI)
- ✅ 2FA TOTP + Keycloak JWT (SCA gate)
- ✅ FIN060 PDF generation (WeasyPrint)
- ✅ Config-as-Data (fees/limits from YAML)
- ✅ Notification port (mock adapter, channels defined)

### НЕ в MVP

- ❌ Live Modulr/ClearBank payment rails (BT-001)
- ❌ Live Sumsub IDV (BT-004)
- ❌ Live SendGrid/Twilio (BT-010)
- ❌ Kafka event streaming (BT-007)
- ❌ Sardine.ai live fraud (BT-009)
- ❌ Saga Coordinator (BT-012)
- ❌ Three-Balance model (BT-013)

---

## 8. Метрики успеха

| Метрика | Текущее | Цель |
|---------|---------|------|
| Тесты | 480/480 PASS | ≥500 после Task 2+3 |
| Coverage | ~80% | ≥81% (LucidShark target) |
| quality-gate.sh | ✅ PASS | PASS всегда |
| IL velocity | 44 IL closed | Все P0 до 7 May |
| CASS 15 deadline | 7 May 2026 | Safeguarding deployed ✅ |
| FPS SLA | MockAdapter | <15s при Modulr live |
| AML SLA | InMemory | <100ms (S5-22) |

---

## 9. Известные ограничения (BT-001..BT-013)

| ID | Ограничение | Разблокирует |
|----|-------------|-------------|
| BT-001 | Modulr API key | Live payment rails |
| BT-002 | MLRO (SMF17) не назначен | Dual-sign FIN060, SAR |
| BT-003 | CFO/CRO/CCO не назначены | Governance |
| BT-004 | Sumsub API key | Live KYC |
| BT-005 | Companies House API | UBO registry |
| BT-006 | GL logic (CBS) | Balance sheet |
| BT-007 | Kafka | Event streaming |
| BT-008 | Compliance officer training | HITL automation |
| BT-009 | Sardine.ai keys | Live fraud |
| BT-010 | SendGrid/Twilio | Live notifications |
| BT-011 | ~~Keycloak deploy~~ | ✅ UNBLOCKED 2026-04-08 |
| BT-012 | Saga Coordinator | Payment flow orchestration |
| BT-013 | Three-Balance model | Full CBS |

---

## 10. AI-специфика

| Компонент | Технология | Детали |
|-----------|-----------|--------|
| LLM | Ollama qwen3-banxe-v2 | Локально на GMKtec (no cloud) |
| Orchestration | LangGraph (planned) | Agent graph, stateful workflow |
| Agent Passports | 13 YAML passports | banxe-architecture/agents/passports/ |
| Autonomy levels | L1 (auto) → L4 (MLRO) | 4 уровня автоматизации |
| Trust zones | GREEN / AMBER / RED | Цветовая классификация рисков |
| HITL | Telegram bot | CEO/MLRO подтверждение RED-зоны |
| Skills | 10 skills × 3 planes | SKILLS-MATRIX.md |
| Orchestration model | 10 сценариев A–J | SKILLS-ORCHESTRATION.md |
| Memory | Claude Code auto-memory | ~/.claude/projects/*/memory/ |
