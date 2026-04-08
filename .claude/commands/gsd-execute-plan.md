# /gsd-execute-plan

Выполняет текущий план из PROJECT.md — задача за задачей до завершения.

## Что делает
1. Читает `~/developer/.planning/PROJECT.md` — список задач
2. Определяет порядок выполнения (зависимости)
3. Вызывает **gsd-executor** который назначает задачи dev-агентам
4. После каждой задачи: обновляет STATE.md + git commit
5. После всех задач: вызывает **gsd-verifier** для финального check
6. Обновляет IL-запись в INSTRUCTION-LEDGER.md

## Выполнение задачи
```
Для каждой задачи:
  → Назначить агента (backend-engineer / database-architect / etc)
  → Выполнить (port + service + tests)
  → quality-gate.sh --fast (PASS обязателен)
  → git commit
  → STATE.md update
```

## Правила остановки
- quality-gate.sh FAIL → стоп, ждать исправления
- Критическая зависимость заблокирована → переход к независимой задаче
- CEO написал "стоп" → немедленная остановка

## Когда использовать
- После `/gsd-new-project` или `/gsd-plan-phase`
- Когда PROJECT.md готов и одобрен

## Выход
Все задачи плана выполнены + Verification Report от gsd-verifier.
