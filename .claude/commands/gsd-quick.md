# /gsd-quick

Быстрое выполнение одной атомарной задачи без полного цикла планирования.

## Что делает
1. Принимает описание задачи из аргумента
2. Читает контекст из SPEC-TEMPLATE.md и STATE.md
3. Сразу вызывает нужного агента (минуя плanner)
4. Выполняет задачу
5. git commit + STATE.md update
6. quality-gate.sh --fast

## Когда использовать
- Небольшой фикс (≤1 file)
- Одиночный endpoint без сложных зависимостей
- Hotfix в production-ready коде
- Дополнение тестов для уже реализованной фичи

## НЕ использовать для
- Фич с зависимостями на другие задачи
- Изменений затрагивающих ≥3 файлов
- Compliance-критичных изменений (использовать `/gsd-execute-plan`)

## Аргументы
```
/gsd-quick "добавить endpoint GET /health"
/gsd-quick "fix coverage for tx_monitor_service.py"
/gsd-quick "add index to customers.email"
```

## Выход
Задача выполнена, тесты прошли, commit запушен.
