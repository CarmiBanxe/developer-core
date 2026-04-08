---
glob: "tests/**/*.py"
---
# Testing Rules — Banxe AI Bank (Quality Gate: ≥80% coverage)

## Минимальный объём
- Каждый новый service → минимум 15 unit tests
- Каждый новый Port (Protocol ABC) → минимум 3 contract tests
- Каждый новый adapter → минимум 5 adapter tests

## Изоляция
- Mock ВСЕ внешние зависимости в unit tests (no real HTTP/DB/Redis)
- Использовать `unittest.mock.patch` или `pytest-mock`
- InMemory adapters для ClickHouse, PostgreSQL, Redis в unit tests
- Integration tests (с реальным DB) → только в `tests/integration/` (не в CI по умолчанию)

## Coverage
- Coverage ≥80% для новых файлов (LucidShark target: 81%)
- `--cov=services --cov-report=term-missing` обязательно при запуске
- Missing coverage → добавить тесты, НЕ добавлять `# pragma: no cover` без причины

## Именование тестов
```
test_{service}_{method}_{scenario}
Примеры:
  test_tx_monitor_evaluate_individual_edd_triggered
  test_payment_router_fps_sla_under_15s
  test_aml_orchestrator_sanctions_hit_block
```

## Fixtures
- Shared fixtures → `conftest.py` (не дублировать в каждом файле)
- Именование fixture: `{entity}_{state}`: `customer_individual_active`, `payment_fps_pending`
- Никаких PII в fixtures (UK GDPR): использовать `FAKE_` prefix для имён/email

## Параметризация
- `@pytest.mark.parametrize` для граничных случаев (boundary values)
- Суммы: тестировать Decimal("9999.99"), Decimal("10000.00"), Decimal("10000.01") вокруг порогов
- Entity types: всегда тестировать оба — INDIVIDUAL и COMPANY

## Обязательные negative tests
- Invalid input → правильный HTTP status (422) и error format
- Auth failure → 401/403 (не 500)
- Timeout / service down → graceful degradation (не unhandled exception)
- Дублирующаяся операция → 409 или idempotent response

## Финансовые assertions
- НИКОГДА `float` в assertions (I-05):
  ```python
  # WRONG:
  assert result.amount == 10.50
  # CORRECT:
  assert result.amount == Decimal("10.50")
  ```
- НИКОГДА mock audit trail writes (I-24) — тест должен проверять что audit запись сделана

## Запуск
```bash
# Fast (unit only):
bash scripts/quality-gate.sh --fast

# Full (unit + lint + semgrep):
bash scripts/quality-gate.sh

# Specific file:
python3 -m pytest tests/test_payment_router.py -v --tb=short
```
