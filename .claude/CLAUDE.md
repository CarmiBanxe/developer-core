# CLAUDE.md — Developer Plane (developer-core)
**Repo:** CarmiBanxe/developer-core | **Plane:** Developer | **Updated:** 2026-04-08 (GSD v2)

---

## Spec-First Methodology (IL-045)

This plane contains the **Spec-First development infrastructure** for Banxe AI Bank.
All methodology files live in `~/developer/`. Nothing here goes into `banxe-emi-stack/` or `banxe-architecture/`.

### File Locations (MANDATORY — do not move)

| File | Location | Purpose |
|------|----------|---------|
| PROJECTIDEA.md | `spec-first/PROJECTIDEA.md` | Project vision, stack, metrics |
| SPEC-TEMPLATE.md | `spec-first/SPEC-TEMPLATE.md` | User stories, DB schema, API endpoints |
| spec_first_auditor.py | `spec-first/audit/spec_first_auditor.py` | Block verification script |
| audit_log.jsonl | `spec-first/audit/audit_log.jsonl` | Append-only audit log |
| quality.md | `.claude/rules/quality.md` | Code quality rules |
| compliance.md | `.claude/rules/compliance.md` | FCA compliance rules |
| testing.md | `.claude/rules/testing.md` | Test patterns + coverage rules |
| implement-feature.md | `.claude/skills/implement-feature.md` | Step-by-step feature implementation |
| create-migration.md | `.claude/skills/create-migration.md` | SQL migration skill |
| deploy-gmktec.md | `.claude/skills/deploy-gmktec.md` | GMKtec deployment skill |
| gsd-planner.md | `.claude/agents/gsd-planner.md` | GSD: decompose → sprint plan |
| gsd-executor.md | `.claude/agents/gsd-executor.md` | GSD: execute plan → call dev agents |
| gsd-verifier.md | `.claude/agents/gsd-verifier.md` | GSD: final verification (read-only) |
| database-architect.md | `.claude/agents/database-architect.md` | DB schema specialist |
| backend-engineer.md | `.claude/agents/backend-engineer.md` | Port+Service+Adapter implementer |
| compliance-specialist.md | `.claude/agents/compliance-specialist.md` | FCA compliance reviewer |
| qa-reviewer.md | `.claude/agents/qa-reviewer.md` | Test quality + gate runner |
| devops-engineer.md | `.claude/agents/devops-engineer.md` | GMKtec infra specialist |
| gsd-new-project.md | `.claude/commands/gsd-new-project.md` | Start new sprint from SPEC |
| gsd-plan-phase.md | `.claude/commands/gsd-plan-phase.md` | Plan next phase from ROADMAP |
| gsd-execute-plan.md | `.claude/commands/gsd-execute-plan.md` | Execute current PROJECT.md |
| gsd-quick.md | `.claude/commands/gsd-quick.md` | Single atomic task, no planning |
| gsd-health.md | `.claude/commands/gsd-health.md` | Full system health check |
| gsd-help.md | `.claude/commands/gsd-help.md` | GSD commands reference |
| PROJECT.md | `.planning/PROJECT.md` | Current sprint — tasks + agents |
| STATE.md | `.planning/STATE.md` | Task status (DONE/IN_PROGRESS/BLOCKED) |
| REQUIREMENTS.md | `.planning/REQUIREMENTS.md` | Technical constraints |
| ROADMAP.md | `.planning/roadmap/ROADMAP.md` | Long-term phases plan |

### Spec-First Passport (banxe-architecture)

Agent passport: `banxe-architecture/agents/passports/spec_first_auditor.yaml`
Passport lives in architecture repo (it IS an architectural artifact).

---

## EXECUTION ORDER (mandatory for all Banxe feature work)

Before ANY implementation in `banxe-emi-stack`:

```
1. Read SPEC-TEMPLATE.md → find user story
2. Write IL entry in banxe-architecture/INSTRUCTION-LEDGER.md (I-28)
3. Create Port → Service → MockAdapter (hexagonal pattern)
4. Write tests (≥15, coverage ≥80%)
5. bash scripts/quality-gate.sh PASS
6. Update IL with proof → commit → push
7. Run spec-first-auditor: python3 ~/developer/spec-first/audit/spec_first_auditor.py
```

No steps may be skipped. quality-gate.sh is always the final blocker.

---

## Territory Rules

ПРАВИЛО: Если файл описывает КАК РАЗРАБОТЧИК РАБОТАЕТ → `~/developer/`
         Если файл описывает ЧТО СИСТЕМА ДЕЛАЕТ → `banxe-emi-stack/`
         Если файл описывает ПОЧЕМУ ТАК РЕШИЛИ → `banxe-architecture/`

**Must NOT appear in banxe-emi-stack/.claude/:**
- `.claude/rules/quality.md`, `.claude/rules/compliance.md`, `.claude/rules/testing.md`
- `.claude/skills/implement-feature.md`, `.claude/skills/create-migration.md`, `.claude/skills/deploy-gmktec.md`
- `.claude/agents/database-architect.md`, `.claude/agents/backend-engineer.md`, `.claude/agents/qa-reviewer.md`

---

## spec-first-auditor

Run after each development block:
```bash
python3 ~/developer/spec-first/audit/spec_first_auditor.py        # all blocks
python3 ~/developer/spec-first/audit/spec_first_auditor.py 3      # specific block
```

Exit 0 = PASS. Exit 1 = FAIL — do not proceed to next block.

---

## GSD Framework (Get Shit Done)

GSD оркестрирует разработку через 3 мета-агента и 6 slash команд.

### Команды

| Команда | Назначение |
|---------|-----------|
| `/gsd-new-project` | Начать новый спринт (читает SPEC → создаёт PROJECT.md) |
| `/gsd-plan-phase` | Планировать следующую фазу по ROADMAP |
| `/gsd-execute-plan` | Выполнить текущий PROJECT.md полностью |
| `/gsd-quick "задача"` | Одна атомарная задача без планирования |
| `/gsd-health` | Health check: audit + quality gate + IL status |
| `/gsd-help` | Справка по всем командам |

### GSD Workflow
```
/gsd-new-project  →  PROJECT.md создан
/gsd-execute-plan →  все задачи выполнены
/gsd-health       →  VERDICT: SPRINT APPROVED
```

### State Management
| Файл | Назначение |
|------|-----------|
| `.planning/PROJECT.md` | Текущий спринт — задачи + агенты + зависимости |
| `.planning/STATE.md` | Статус задач (DONE/IN_PROGRESS/BLOCKED) |
| `.planning/REQUIREMENTS.md` | Технические требования и ограничения |
| `.planning/roadmap/ROADMAP.md` | Долгосрочный план фаз |

---

## Key References

| Resource | Path |
|----------|------|
| Project spec | `~/developer/spec-first/SPEC-TEMPLATE.md` |
| Project idea | `~/developer/spec-first/PROJECTIDEA.md` |
| Sprint plan | `~/developer/.planning/PROJECT.md` |
| State | `~/developer/.planning/STATE.md` |
| IL ledger | `~/banxe-architecture/INSTRUCTION-LEDGER.md` |
| Skills orchestration | `~/banxe-architecture/docs/SKILLS-ORCHESTRATION.md` |
| Invariants | `~/banxe-architecture/INVARIANTS.md` |
| Quality gate | `~/banxe-emi-stack/scripts/quality-gate.sh` |

---

## ДОПОЛНЕНИЕ: Авто-настройка + Контролёр + Obsidian Vault (GSD v3)

> Добавлено: 2026-04-08. Не удалять предыдущие блоки — они остаются в силе.

---

## Правила авто-одобрения (ОБЯЗАТЕЛЬНОЕ ИСПОЛНЕНИЕ)

### Автоматически одобрено (выполнять БЕЗ запроса CEO):
- `git add / commit / push` — ДА
- `pytest / ruff / semgrep` — ДА
- `rsync` к серверам (GMKtec, NucBox) — ДА
- Создание файлов и директорий — ДА
- Редактирование файлов — ДА
- Запуск Docker-контейнеров — ДА
- Создание/обновление заметок в Obsidian vault — ДА
- `python3 ~/developer/spec-first/audit/spec_first_auditor.py` — ДА
- `bash scripts/quality-gate.sh` — ДА

### Требует подтверждения CEO:
- Удаление файлов — СПРОСИТЬ
- Удаление репозиториев — СПРОСИТЬ
- Изменение прав доступа — СПРОСИТЬ
- Финансовые операции — СПРОСИТЬ
- Публикация в Product Plane (banxe-emi-stack) — СПРОСИТЬ

### Правило продолжения:
Разработчик ОБЯЗАН продолжать работу без остановки на вопросы,
КРОМЕ случаев из списка "Требует подтверждения".

---

## Агент-Контролёр исполнения (Supervisor Agent)

### Роль: Гарантировать выполнение ВСЕХ фаз GSD + Spec-First

### Алгоритм при старте КАЖДОЙ сессии:
1. Прочитать .planning/STATE.md
2. Прочитать banxe-architecture/INSTRUCTION-LEDGER.md
3. Прочитать obsidian-vault/sessions/ (последняя сессия)
4. Найти задачи != DONE
5. Отсортировать: P0 > P1 > P2
6. Определить текущую фазу
7. Предложить CEO: "Продолжаем [IL-XXX]? Фаза: [N]. План: [действия]"
8. При "да" / "продолжай" — выполнять без дополнительных вопросов
9. При завершении — перейти к следующей задаче по приоритету

### Самовозврат к работе:
При прерывании сессии или команде "продолжай":
- АВТОМАТИЧЕСКИ определяет точку остановки из STATE.md + sessions/
- Предлагает продолжение с конкретным планом действий
- НЕ ЖДЁТ повторного объяснения контекста от CEO
- Контекст берёт из данных (vault, STATE.md, IL), а не из чата

### Чек-лист закрытия задачи (ВСЕ 9 пунктов обязательны):
- [ ] IL-запись обновлена (статус = DONE)
- [ ] Тесты пройдены (pytest, coverage 80%+)
- [ ] Линтинг чист (ruff 0 errors)
- [ ] Security check (semgrep 0 critical)
- [ ] spec-first-auditor PASS (Exit 0)
- [ ] quality-gate.sh PASS
- [ ] Код закоммичен и запушен
- [ ] .planning/STATE.md обновлён
- [ ] Vault обновлён (knowledge/ + sessions/)

Если хоть ОДИН пункт не выполнен — задача НЕ закрыта.
Контролёр возвращает к незавершённому пункту. СТОП, выполнить, проверить 9/9, только потом дальше.

---

## Obsidian Knowledge Vault Protocol

### Расположение: ~/obsidian-vault/

Структура:
- 00-home/index.md — точка входа
- atlas/ — карты и индексы
- knowledge/integrations/ — API, внешние сервисы
- knowledge/decisions/ — архитектурные решения (ADR)
- knowledge/debugging/ — решённые баги и workarounds
- knowledge/patterns/ — повторяющиеся паттерны
- knowledge/business/ — бизнес-логика, регуляции
- sessions/ — логи сессий Claude Code
- inbox/ — необработанные заметки

### Когда записывать:
- Закрыл IL-задачу — sessions/YYYY-MM-DD.md (лог: что сделано, решения)
- Нашёл баг + решение — knowledge/debugging/ (проблема, причина, решение)
- Архитектурное решение — knowledge/decisions/ (ADR: контекст, варианты, решение)
- Обнаружил паттерн — knowledge/patterns/ (паттерн + примеры)
- Интеграция с API — knowledge/integrations/ (endpoint, auth, rate limits)
- Бизнес-правило — knowledge/business/ (правило + регуляция + ссылка)

### Формат заметки (frontmatter обязателен):
tags: [тема, технология], date: YYYY-MM-DD, related: [[связанная-заметка]], il: IL-XXX

### Правило 30-50 заметок:
При накоплении 30-50 заметок в директории — обновить index.md, создать atlas-карту.

---

## Memory Protocol

### Связь Memory / Vault / STATE:
- Memory (.claude/memory) = краткосрочный контекст сессии
- Vault (obsidian-vault) = долгосрочные знания
- STATE.md = оперативный статус задач
- При противоречии — vault имеет приоритет над memory

### Приоритет источников контекста:
1. .planning/STATE.md
2. INSTRUCTION-LEDGER.md
3. obsidian-vault/sessions/
4. obsidian-vault/knowledge/
5. .planning/PROJECT.md
6. .planning/REQUIREMENTS.md
7. COMPLIANCE-MATRIX.md
8. .claude/memory

---

## Инфраструктура серверов

### GMKtec Mini-PC:
- Keycloak: порт 8180, Docker services активны
- Деплой: rsync с Legion

### NucBox:
- Резервный сервер + бэкапы

### Legion (основная рабочая станция):
- WSL2/Ubuntu, все репозитории, Claude Code, SSH-ключи
- Obsidian vault: ~/obsidian-vault

### Сетевая схема:
Legion (WSL2) --rsync--> GMKtec (Docker)
Legion (WSL2) --rsync--> NucBox (backup)
Legion (WSL2) --git----> GitHub (CarmiBanxe/*)

---

## UI/UX Pipeline (banxe-ui)

Plane: Developer (НЕ production).
Промоушен в Product Plane: ТОЛЬКО после CEO review + IL entry.

Pipeline: bash scripts/banxe-build.sh (полный 8 стадий)
--from-stage 4 (с 4-й стадии), --stage quality-gate (только gate)

Документация в banxe-architecture/docs/:
- BANXE-UI-UX-RESEARCH.md, BANXE-UI-UX-SYSTEM.md
- BANXE-SCREEN-INVENTORY.md, BANXE-UI-ARCHITECTURE.md
- BANXE-CLAUDE-CODE-WORKFLOW.md, BANXE-HEADLESS-PIPELINE.md
- UI-PLANE-OPERATING-MODEL.md

---

## GSD Status Report (формат отчёта)

При запросе статуса или в конце сессии выводить:
- Завершено: IL-XXX..IL-XXX (N задач)
- В работе: IL-XXX — описание
- Очередь: IL-XXX, IL-XXX
- Тесты: N passed, 0 failed, Coverage: XX%
- Auditor: X/X PASS, Quality Gate: PASS/FAIL
- Деплой: статус GMKtec
- Vault: +N заметок
- Следующее действие: автоматически определено

---

## Execution Plan (дедлайн 7 мая 2026)

1. Safeguarding Deploy GMKtec | IL-043 | PENDING CEO RUN | P0
2. FastAPI REST API Layer | IL-046 | PENDING | P1
3. Notification Service S17-03 | IL-047 | PENDING | P1
4. Redis VelocityTracker | TBD | PENDING | P2
5. Fraud + AML Pipeline S9-05 | TBD | PENDING | P2
6. Consumer Duty S9-06 FCA PS22/9 | TBD | PENDING | P2

---

## Обязательность исполнения (ПРИКАЗ)

1. Контролёр запускается АВТОМАТИЧЕСКИ при каждом старте сессии
2. Все фазы GSD + Spec-First обязательны — пропуск = нарушение
3. Vault обновляется КАЖДУЮ сессию — без исключений
4. Территории соблюдаются ВСЕГДА:
   - ~/developer/.claude/ = настройки разработчика
   - ~/banxe-emi-stack/ = production код
   - ~/banxe-architecture/ = архитектура и решения
   - ~/banxe-ui/ = UI прототипы (Developer Plane)
   - ~/obsidian-vault/ = база знаний
5. spec-first-auditor Exit 0 + quality-gate.sh PASS = обязательны перед закрытием
6. Hexagonal pattern: Port -> Service -> MockAdapter — обязательный порядок
7. При "продолжай" — контролёр восстанавливает контекст из данных, не из чата
8. audit_log.jsonl — append-only, не редактировать вручную
