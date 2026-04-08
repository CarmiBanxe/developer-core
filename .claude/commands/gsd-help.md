# /gsd-help

Справка по GSD (Get Shit Done) командам и агентам.

## GSD Команды

| Команда | Когда использовать |
|---------|-------------------|
| `/gsd-new-project` | Начало нового спринта / крупной фичи |
| `/gsd-plan-phase` | Планирование следующей фазы по roadmap |
| `/gsd-execute-plan` | Выполнение текущего PROJECT.md |
| `/gsd-quick "задача"` | Одна атомарная задача без планирования |
| `/gsd-health` | Health check всей системы |
| `/gsd-help` | Эта справка |

## GSD Агенты

| Агент | Роль |
|-------|------|
| gsd-planner | Декомпозиция фичи → атомарные задачи |
| gsd-executor | Выполнение плана → вызов dev-агентов |
| gsd-verifier | Финальная верификация (read-only) |

## Dev Агенты (вызываются executor'ом)

| Агент | Роль |
|-------|------|
| backend-engineer | Port + Service + Adapter + Tests |
| database-architect | SQL migrations (CH + PG + Redis) |
| compliance-specialist | FCA compliance review |
| qa-reviewer | Coverage + quality gate |
| devops-engineer | GMKtec deploy + systemd |

## Workflow

```
1. /gsd-new-project        → создаёт PROJECT.md
2. /gsd-execute-plan       → выполняет все задачи
3. /gsd-health             → верифицирует результат
```

## Ключевые файлы

| Файл | Назначение |
|------|-----------|
| `~/developer/spec-first/SPEC-TEMPLATE.md` | User stories, API, DB schema |
| `~/developer/spec-first/PROJECTIDEA.md` | Бизнес-контекст |
| `~/developer/.planning/PROJECT.md` | Текущий спринт |
| `~/developer/.planning/STATE.md` | Статус задач |
| `~/developer/.planning/roadmap/ROADMAP.md` | Долгосрочный план |
| `~/banxe-architecture/INSTRUCTION-LEDGER.md` | IL-записи |
