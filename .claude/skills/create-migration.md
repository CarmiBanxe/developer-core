---
name: create-migration
description: Создание SQL-схемы для ClickHouse или PostgreSQL — идемпотентно, с audit TTL
---
# Skill: Create Migration

## Когда применять
- Новая таблица нужна для фичи
- Существующая таблица требует нового поля
- Изменение индекса или TTL

## Правило выбора БД

| Тип данных | БД | Движок |
|-----------|-----|--------|
| Audit trail, события (append-only) | ClickHouse :9000 | ReplacingMergeTree + TTL |
| OLTP — клиенты, транзакции, agreements | PostgreSQL :5432 | Standard + pgAudit |
| Session / velocity state | Redis :6379 | Sorted sets, TTL-native |

## Шаги

### 1. Определить целевую БД
```
ClickHouse: safeguarding_events, payment_events, complaints → audit/OLAP
PostgreSQL: customers, agreements, notifications, config_overrides → OLTP
```

### 2. Написать SQL (идемпотентно!)
```sql
-- ClickHouse (ВСЕГДА IF NOT EXISTS):
CREATE TABLE IF NOT EXISTS banxe.my_table (
    id       UUID DEFAULT generateUUIDv4(),
    event_at DateTime64(3, 'UTC'),
    -- ... fields ...
    amount   Decimal64(8)  -- НИКОГДА Float64 (I-05)
) ENGINE = ReplacingMergeTree()
ORDER BY (id, event_at)
TTL event_at + INTERVAL 5 YEAR  -- I-08: минимум 5 лет
SETTINGS index_granularity = 8192;

-- PostgreSQL (ВСЕГДА IF NOT EXISTS):
CREATE TABLE IF NOT EXISTS my_table (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### 3. Разместить файл
```
scripts/schema/clickhouse_{table_name}.sql    — для ClickHouse
scripts/schema/postgres_{table_name}.sql      — для PostgreSQL
```

### 4. Для ClickHouse: проверить TTL
- Audit trail: TTL ≥ 5Y (I-08) — CASS 7.15, MLR 2017
- Complaints: TTL ≥ 7Y (FCA DISP)
- НЕ уменьшать существующий TTL — нарушение I-08

### 5. Для PostgreSQL: добавить constraints
```sql
-- Проверочные constraints:
CHECK (amount > 0)
CHECK (entity_type IN ('INDIVIDUAL', 'COMPANY'))
-- FK для integrity:
REFERENCES customers(id) ON DELETE RESTRICT
-- Индексы для часто запрашиваемых полей:
CREATE INDEX IF NOT EXISTS idx_my_table_customer_id ON my_table(customer_id);
```

### 6. Тестировать идемпотентность
```bash
# Запустить SQL дважды — должно работать без ошибок:
ssh gmktec "cd /data/banxe/banxe-emi-stack && \
  clickhouse-client < scripts/schema/clickhouse_my_table.sql && \
  clickhouse-client < scripts/schema/clickhouse_my_table.sql && \
  echo 'Idempotent OK'"
```

### 7. Обновить SERVICE-MAP.md
```
Открыть: banxe-architecture/docs/SERVICE-MAP.md
Добавить: новая таблица + её назначение + порт
```

## Запреты
- НИКОГДА `Float64` в ClickHouse для денег (I-05)
- НИКОГДА `REAL` или `FLOAT` в PostgreSQL для денег (I-05)
- НИКОГДА `ALTER TABLE ... DROP COLUMN` на audit таблицах (I-24)
- НИКОГДА уменьшать TTL (I-08)
