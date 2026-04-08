---
glob: "services/aml/**/*.py,services/recon/**/*.py,services/compliance/**/*.py,services/payment/**/*.py"
---
# Compliance Rules — Banxe AI Bank (FCA MLR 2017, POCA 2002, CASS 7, PSR 2017)

## Audit Trail (I-24)
- Каждое решение BLOCK/HOLD/SAR → запись в ClickHouse audit trail ПЕРЕД любым другим действием
- Формат: `safeguarding_events` / `payment_events` (append-only, no UPDATE/DELETE)
- TTL: ≥5 лет (I-08). Нельзя уменьшать TTL.
- Если audit write упал → логировать критический error, НЕ молча продолжать

## SAR и RED-zone операции
- SAR filing → ТОЛЬКО через MLRO approval (L3 autonomy, RED trust zone)
- Никаких auto-approve для RED trust zone решений
- HIGH risk → обязательный HITL (Telegram alert CEO/MLRO)

## Суммы и валюты
- Все финансовые суммы → `Decimal` (не `float`) (I-05)
- Валюта → ISO 4217 3-letter code: `GBP`, `EUR`, `USD`
- Никогда не округлять промежуточные результаты — только финальный `quantize(Decimal("0.01"))`

## PII в логах
- PII (имена, адреса, DOB, IBAN, email) → НИКОГДА в логах
- Используй hash (`sha256`) или маску (`****1234`) для идентификации в логах
- UK GDPR Art.5 — data minimisation в log entries

## Entity-aware thresholds (IL-041)
- INDIVIDUAL: EDD trigger >£10,000 (MLR 2017 Reg.28(3))
- COMPANY: EDD trigger >£50,000
- Всегда получать entity_type из customer profile перед AML evaluation

## Структурирование (POCA 2002 s.330)
- 3+ транзакции <EDD_threshold в 24h от одного клиента → structuring_signal=True
- structuring_signal=True → SAR consideration (не автоматический SAR, но флаг)

## Заблокированные юрисдикции
- Проверять jurisdiction против BLOCKED_JURISDICTIONS перед любой транзакцией (I-02)
- Россия, Беларусь, Иран, КНДР, Куба — BLOCK (полный список в COMPLIANCE-MATRIX.md)
- Сирия → HOLD (EDD required, обновлено июль 2025)

## FPS SLA (I-05)
- FPS транзакции: ответ <15 секунд (PSR APP 2024)
- Timeout >15s → log + fallback rail (CHAPS если >£250k) или retry
