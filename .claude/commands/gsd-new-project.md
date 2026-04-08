# /gsd-new-project

Запускает полный Spec-First онбординг нового проекта или фичи.

## Что делает
1. Читает `~/developer/spec-first/PROJECTIDEA.md` — получает бизнес-контекст
2. Читает `~/developer/spec-first/SPEC-TEMPLATE.md` — получает user stories
3. Читает `~/banxe-architecture/INSTRUCTION-LEDGER.md` — проверяет незакрытые IL
4. Вызывает **gsd-planner** для декомпозиции в задачи
5. Создаёт `~/developer/.planning/PROJECT.md` с планом спринта
6. Создаёт IL-запись в INSTRUCTION-LEDGER.md (статус IN_PROGRESS)
7. Выводит план для подтверждения CEO

## Когда использовать
- Начало нового спринта
- Новая крупная фича (>3 tasks)
- После обновления SPEC-TEMPLATE.md

## Аргументы
```
/gsd-new-project                    # интерактивно (плanner читает всё сам)
/gsd-new-project "FastAPI Layer"    # конкретная фича
```

## Выход
`~/developer/.planning/PROJECT.md` с разбивкой на задачи, агентов, зависимости.
