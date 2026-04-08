# CLAUDE.md — Developer Plane (developer-core)
**Repo:** CarmiBanxe/developer-core | **Plane:** Developer | **Updated:** 2026-04-08 (GSD v4 — Obsidian integrated)

---

## БЛОК 0: ТЕРРИТОРИИ (ОБЯЗАТЕЛЬНО)

### Территория разработчика (конфигурация):
```
~/developer/.claude/          ← ТОЛЬКО ЗДЕСЬ настройки разработчика
├── CLAUDE.md                 ← Этот файл (главный конфиг)
├── settings.json             ← Параметры Claude Code
├── rules/                    ← Правила поведения
├── skills/                   ← Навыки разработчика
├── agents/                   ← Агенты (controller, architect, reviewer)
├── commands/                 ← Slash-команды GSD
└── memory/                   ← Память Claude Code (авто)

~/developer/.planning/        ← Текущий спринт
├── PROJECT.md                ← Задачи + назначенные агенты
├── STATE.md                  ← Статус (DONE/IN_PROGRESS/BLOCKED)
├── REQUIREMENTS.md           ← Технические ограничения
└── roadmap/ROADMAP.md        ← Долгосрочные фазы
```

### Территория проектов (код):
```
~/banxe-emi-stack/            ← Product Plane (production код)
~/banxe-ui/                   ← Developer Plane (UI прототипы)
```

### Территория архитектуры (решения):
```
~/banxe-architecture/         ← Architecture Plane (IL, compliance, docs)
```

### Obsidian Knowledge Vault:
```
~/obsidian-vault/             ← База знаний (Obsidian)
├── 00-home/index.md          ← Точка входа
├── atlas/                    ← Карты и индексы (.md)
├── knowledge/
│   ├── integrations/         ← API, внешние сервисы
│   ├── decisions/            ← Архитектурные решения (ADR)
│   ├── debugging/            ← Решённые баги и workarounds
│   ├── patterns/             ← Повторяющиеся паттерны
│   └── business/             ← Бизнес-логика, регуляции
├── sessions/                 ← Логи сессий Claude Code
└── inbox/                    ← Необработанные заметки
```

**ЗАПРЕТ:** Конфигурация из `~/developer/.claude/` НИКОГДА не копируется в директории проектов. Проекты содержат ТОЛЬКО свой код. Vault содержит ТОЛЬКО знания.

---

## БЛОК 1: МЕТОДОЛОГИЯ GSD + SPEC-FIRST

**Принцип:** Идея → Спецификация → Код → Тесты → Деплой → Знания

Каждая задача проходит 9 фаз:

| # | Фаза | Действие | Файл |
|---|------|----------|------|
| 1 | IDEA | Описать идею | `.planning/PROJECT.md` |
| 2 | SPEC | IL-запись + спецификация | `INSTRUCTION-LEDGER.md` |
| 3 | DESIGN | ArchiMate/C4 (если архитектура) | `banxe-architecture/docs/` |
| 4 | IMPLEMENT | Код по спецификации | `banxe-emi-stack/` или `banxe-ui/` |
| 5 | TEST | pytest + ruff + semgrep (≥80%) | тесты в проекте |
| 6 | REVIEW | Авто code review агентом | PR review |
| 7 | DEPLOY | rsync/git push | GMKtec/NucBox |
| 8 | CLOSE | IL → DONE, COMPLIANCE-MATRIX | `banxe-architecture/` |
| 9 | VAULT | Записать знания в Obsidian | `obsidian-vault/knowledge/` |

### Фаза 9 — VAULT (обязательна после каждой задачи):

- Создать/обновить заметку в `knowledge/` (решения, баги, паттерны)
- Обновить `sessions/` с логом что было сделано
- Связать с существующими заметками (wiki-линки `[[]]`)
- Если найден баг/workaround → `knowledge/debugging/`
- Если принято архитектурное решение → `knowledge/decisions/`
- Если обнаружен паттерн → `knowledge/patterns/`

### Spec-First Passport:
Agent passport: `banxe-architecture/agents/passports/spec_first_auditor.yaml`

Run after each development block:
```bash
python3 ~/developer/spec-first/audit/spec_first_auditor.py        # all blocks
python3 ~/developer/spec-first/audit/spec_first_auditor.py 3      # specific block
```
Exit 0 = PASS. Exit 1 = FAIL — do not proceed to next block.

---

## БЛОК 2: ПРАВИЛА АВТО-ОДОБРЕНИЯ (ОБЯЗАТЕЛЬНОЕ ИСПОЛНЕНИЕ)

### Автоматически одобрено (выполнять БЕЗ запроса CEO):
- `git add / commit / push` — ДА
- `pytest / ruff / semgrep` — ДА
- `rsync` к серверам (GMKtec, NucBox) — ДА
- Создание файлов и директорий — ДА
- Редактирование файлов — ДА
- Запуск Docker-контейнеров — ДА
- Создание/обновление заметок в Obsidian vault — ДА
- Чтение vault для контекста — ДА
- `python3 ~/developer/spec-first/audit/spec_first_auditor.py` — ДА
- `bash scripts/quality-gate.sh` — ДА

### Требует подтверждения CEO:
- Удаление файлов — СПРОСИТЬ
- Удаление репозиториев — СПРОСИТЬ
- Изменение прав доступа — СПРОСИТЬ
- Финансовые операции — СПРОСИТЬ
- Публикация в Product Plane (banxe-emi-stack) — СПРОСИТЬ

### Правило продолжения:
Разработчик ОБЯЗАН продолжать работу без остановки на вопросы, КРОМЕ случаев из списка "Требует подтверждения".

---

## БЛОК 3: АГЕНТ-КОНТРОЛЁР ИСПОЛНЕНИЯ (Supervisor Agent)

**Роль:** Гарантировать выполнение ВСЕХ 9 фаз GSD

### Алгоритм при старте сессии:
```
1. Прочитать INSTRUCTION-LEDGER.md (banxe-architecture)
2. Прочитать .planning/STATE.md (developer)
3. Прочитать obsidian-vault/sessions/ (последняя сессия)
4. Найти задачи со статусом != DONE
5. Отсортировать по приоритету (P0 > P1 > P2)
6. Определить текущую фазу GSD (1-9)
7. Предложить CEO: "Продолжаем [IL-XXX]? Фаза: [N]. План: [действия]"
8. При "да" / "продолжай" → выполнять без вопросов
9. При завершении задачи → перейти к следующей по приоритету
```

### Самовозврат к работе:
При прерывании сессии или команде "продолжай":
- АВТОМАТИЧЕСКИ определяет точку остановки из STATE.md + sessions/
- Предлагает продолжение с конкретным планом действий
- НЕ ЖДЁТ повторного объяснения контекста от CEO
- Контекст берёт из vault (не из чата)

### Чек-лист закрытия задачи (ВСЕ 8 пунктов обязательны):
- [ ] IL-запись обновлена (статус = DONE)
- [ ] Тесты пройдены (pytest ≥80%, ruff 0 errors)
- [ ] Security check (semgrep 0 critical)
- [ ] Код закоммичен и запушен
- [ ] COMPLIANCE-MATRIX обновлена
- [ ] `.planning/STATE.md` обновлён
- [ ] Vault обновлён (`knowledge/` + `sessions/`)
- [ ] Следующая задача определена

Если хоть ОДИН пункт не выполнен → задача НЕ закрыта. Контролёр возвращает к незавершённому пункту.

### Порядок действий контролёра при нарушении:
```
1. Обнаружил незакрытый пункт чек-листа
2. СТОП — не продолжать к следующей задаче
3. Вернуться к незавершённому пункту
4. Выполнить пункт
5. Повторить проверку чек-листа
6. Только после 8/8 PASS → перейти к следующей задаче
7. Записать нарушение в sessions/ для анализа
```

---

## БЛОК 4: НАВЫКИ (SKILLS)

| Навык | Файл |
|-------|------|
| GitHub Navigation | `.claude/skills/github-navigation.md` |
| Spec Writing | IL-формат: `IL-XXX | Статус | Приоритет | Описание | Блокировки | Дата` |
| Testing | pytest coverage ≥80%, ruff (0 errors), semgrep (0 critical) |
| Implement Feature | `.claude/skills/implement-feature.md` |
| Create Migration | `.claude/skills/create-migration.md` |
| Deploy GMKtec | `.claude/skills/deploy-gmktec.md` |
| Obsidian Vault Management | Создание заметок + wiki-линки + рефакторинг vault |

**Obsidian Vault Management (из PDF alexmagnier):**
- Создание заметок в формате markdown с frontmatter (tags, date, related, il)
- Wiki-линки между заметками `[[имя-заметки]]`
- Структура: `00-home → atlas → knowledge → sessions → inbox`
- При накоплении 30-50 заметок → рефакторинг vault (index.md обновление)
- При обнаружении повторяющегося паттерна → `knowledge/patterns/`
- При решении бага → `knowledge/debugging/` (с решением и workaround)
- Сессионные логи → `sessions/YYYY-MM-DD.md`

---

## БЛОК 5: ИНФРАСТРУКТУРА

### Репозитории (Planes):
| Репо | Plane | Назначение |
|------|-------|-----------|
| developer-core | Developer | Конфигурация разработчика (`.claude/`) |
| banxe-architecture | Architecture | IL, compliance, docs, ArchiMate |
| banxe-emi-stack | Product | EMI стек, микросервисы (production) |
| banxe-ui | Developer | UI прототипы, design tokens |

**Config-as-Data:** Все конфигурации — данные в репозитории. Никаких хардкод-значений.

---

## БЛОК 6: OBSIDIAN KNOWLEDGE VAULT PROTOCOL

### Когда записывать в vault:

| Событие | Куда | Формат |
|---------|------|--------|
| Закрыл IL-задачу | `sessions/YYYY-MM-DD.md` | Лог: что сделано, решения |
| Нашёл баг + решение | `knowledge/debugging/` | Проблема → Причина → Решение |
| Принял архитектурное решение | `knowledge/decisions/` | ADR: контекст, варианты, решение |
| Обнаружил паттерн | `knowledge/patterns/` | Паттерн + примеры использования |
| Интеграция с API | `knowledge/integrations/` | Endpoint, auth, rate limits, gotchas |
| Бизнес-правило | `knowledge/business/` | Правило + регуляция + ссылка |

### Формат заметки (frontmatter обязателен):
```markdown
---
tags: [debugging, keycloak, gmktec]
date: 2026-04-08
related: [[keycloak-setup]], [[gmktec-deploy]]
il: IL-043
---
# Заголовок

## Контекст
...

## Решение
...

## Связанные заметки
- [[другая-заметка]]
```

### Правило 30-50 заметок:
При накоплении 30-50 заметок в любой директории → обновить `index.md`, создать atlas-карту, вычистить дубликаты.

---

## БЛОК 7: ФОРМАТ ОТЧЁТА

При запросе статуса или в конце сессии:
```
GSD Status Report
═══════════════════════════════
Завершено: IL-XXX..IL-XXX (N задач)
В работе:  IL-XXX — [описание]
Очередь:   IL-XXX, IL-XXX
Тесты:     N passed, 0 failed
Coverage:  XX%
Auditor:   X/X PASS | Quality Gate: PASS
Деплой:    [статус GMKtec]
Vault:     +N заметки (N debugging, N decision, N session)
═══════════════════════════════
Следующее действие: [автоматически определено]
```

---

## БЛОК 8: SLASH-КОМАНДЫ GSD

| Команда | Действие | Файл |
|---------|----------|------|
| `/gsd-new-project` | Начать новый спринт от SPEC | `.claude/commands/gsd-new-project.md` |
| `/gsd-plan-phase` | Планировать следующую фазу из ROADMAP | `.claude/commands/gsd-plan-phase.md` |
| `/gsd-execute-plan` | Выполнить текущий PROJECT.md | `.claude/commands/gsd-execute-plan.md` |
| `/gsd-quick "задача"` | Одна атомарная задача без планирования | `.claude/commands/gsd-quick.md` |
| `/gsd-health` | Полная проверка системы | `.claude/commands/gsd-health.md` |
| `/gsd-help` | Справка по командам | `.claude/commands/gsd-help.md` |

### GSD Workflow:
```
/gsd-new-project  →  PROJECT.md создан
/gsd-execute-plan →  все задачи выполнены
/gsd-health       →  VERDICT: SPRINT APPROVED
```

---

## БЛОК 9: ОБЯЗАТЕЛЬНОСТЬ ИСПОЛНЕНИЯ

Этот промт является **ПРИКАЗОМ**, а не рекомендацией.

1. Контролёр запускается АВТОМАТИЧЕСКИ при каждом старте сессии
2. Все 9 фаз обязательны — пропуск любой фазы = нарушение
3. Vault обновляется КАЖДУЮ сессию — без исключений
4. Территории соблюдаются ВСЕГДА — конфигурация ≠ проект ≠ архитектура
5. При нарушении → контролёр останавливает работу + отчёт CEO
6. При "продолжай" → контролёр восстанавливает контекст из vault + STATE.md
7. Самовозврат → не ждать объяснений, брать контекст из данных

### Приоритет источников контекста:
```
1. .planning/STATE.md          (что в работе сейчас)
2. INSTRUCTION-LEDGER.md       (полный реестр задач)
3. obsidian-vault/sessions/    (логи предыдущих сессий)
4. obsidian-vault/knowledge/   (накопленные знания)
5. .planning/PROJECT.md        (текущий спринт)
6. .planning/REQUIREMENTS.md   (технические ограничения)
7. COMPLIANCE-MATRIX.md        (матрица соответствия)
8. DEPARTMENT-MAP.md           (карта департаментов)
```

---

## БЛОК 10: MEMORY PROTOCOL

### Связь Memory ↔ Vault:
```
Memory (краткосрочно)  →  "IL-046 в работе, фаза TEST"
Vault (долгосрочно)    →  "FastAPI: используем Pydantic v2, async handlers"
STATE.md (оперативно)  →  "IL-046 | IN_PROGRESS | P1"
```

- При закрытии сессии → сохранить ключевые решения в memory
- При старте сессии → прочитать memory + `vault/sessions/`
- Memory НЕ заменяет vault — memory = краткосрочный контекст, vault = долгосрочные знания
- **Если memory и vault противоречат → vault имеет приоритет**

### State Management:
| Файл | Назначение |
|------|-----------|
| `.planning/PROJECT.md` | Текущий спринт — задачи + агенты + зависимости |
| `.planning/STATE.md` | Статус задач (DONE/IN_PROGRESS/BLOCKED) |
| `.planning/REQUIREMENTS.md` | Технические требования и ограничения |
| `.planning/roadmap/ROADMAP.md` | Долгосрочный план фаз |

---

## БЛОК 11: ИНФРАСТРУКТУРА СЕРВЕРОВ

### GMKtec Mini-PC:
- IP: 192.168.x.x (локальная сеть)
- Keycloak: порт 8180, Docker services активны
- Деплой: rsync с Legion

### NucBox:
- Резервный сервер + бэкапы

### Legion (основная рабочая станция):
- WSL2/Ubuntu, все репозитории, Claude Code, SSH-ключи
- Obsidian vault: `~/obsidian-vault`

### Сетевая схема:
```
Legion (WSL2) --rsync--> GMKtec (Docker)
Legion (WSL2) --rsync--> NucBox (backup)
Legion (WSL2) --git----> GitHub (CarmiBanxe/*)
```

---

## БЛОК 12: UI/UX PIPELINE (banxe-ui)

Plane: Developer (НЕ production).
Промоушен в Product Plane: ТОЛЬКО после CEO review + IL entry.

```bash
bash scripts/banxe-build.sh                    # Полный pipeline (8 стадий)
bash scripts/banxe-build.sh --from-stage 4    # С 4-й стадии
bash scripts/banxe-build.sh --stage quality-gate  # Только quality gate
```

### Документация UI/UX (banxe-architecture/docs/):
| Документ | Содержание |
|----------|-----------|
| BANXE-UI-UX-RESEARCH.md | Классификация инструментов |
| BANXE-UI-UX-SYSTEM.md | Дизайн-система: цвета, шрифты, компоненты |
| BANXE-SCREEN-INVENTORY.md | 6 web + 6 mobile экранов |
| BANXE-UI-ARCHITECTURE.md | Структура, стратегия компонентов |
| BANXE-CLAUDE-CODE-WORKFLOW.md | Claude Code для UI работы |
| BANXE-HEADLESS-PIPELINE.md | 8-стадийный pipeline |
| UI-PLANE-OPERATING-MODEL.md | Governance: Dev/Product/Standby planes |

---

## БЛОК 13: EXECUTION PLAN (дедлайн 7 мая 2026)

| # | Задача | IL | Статус | Приоритет |
|---|--------|-----|--------|-----------|
| 1 | Safeguarding Deploy GMKtec | IL-043 | DONE ✅ | P0 |
| 2 | FastAPI REST API Layer | IL-046 | PENDING | P1 |
| 3 | Notification Service S17-03 | IL-047 | PENDING | P1 |
| 4 | Redis VelocityTracker | TBD | PENDING | P2 |
| 5 | Fraud + AML Pipeline S9-05 | TBD | PENDING | P2 |
| 6 | Consumer Duty S9-06 FCA PS22/9 | TBD | PENDING | P2 |

При команде "продолжай": Контролёр берёт первую незавершённую задачу по приоритету и выполняет без вопросов.

---

## БЛОК 14: ПОЛНАЯ СТРУКТУРА ФАЙЛОВ

```
~/developer/                          ← БЛОК РАЗРАБОТЧИКА
├── .claude/
│   ├── CLAUDE.md                     ← ЭТОТ ФАЙЛ
│   ├── settings.json                 ← Параметры Claude Code
│   ├── memory/                       ← Авто-память Claude Code
│   ├── rules/
│   │   ├── quality.md                ← Правила качества кода
│   │   ├── compliance.md             ← FCA compliance правила
│   │   └── testing.md                ← Тесты + coverage правила
│   ├── skills/
│   │   ├── implement-feature.md      ← Имплементация фичей
│   │   ├── create-migration.md       ← Миграции БД
│   │   └── deploy-gmktec.md          ← Деплой на GMKtec
│   ├── agents/
│   │   ├── gsd-planner.md            ← GSD: декомпозиция → план
│   │   ├── gsd-executor.md           ← GSD: выполнение плана
│   │   ├── gsd-verifier.md           ← GSD: финальная верификация
│   │   ├── database-architect.md     ← БД архитектор
│   │   ├── backend-engineer.md       ← Backend инженер
│   │   ├── compliance-specialist.md  ← FCA compliance
│   │   ├── qa-reviewer.md            ← QA ревьюер
│   │   └── devops-engineer.md        ← DevOps GMKtec
│   └── commands/
│       ├── gsd-new-project.md        ← /gsd-new-project
│       ├── gsd-plan-phase.md         ← /gsd-plan-phase
│       ├── gsd-execute-plan.md       ← /gsd-execute-plan
│       ├── gsd-quick.md              ← /gsd-quick
│       ├── gsd-health.md             ← /gsd-health
│       └── gsd-help.md               ← /gsd-help
├── .planning/
│   ├── PROJECT.md                    ← Текущий спринт
│   ├── STATE.md                      ← Статусы задач
│   ├── REQUIREMENTS.md               ← Технические ограничения
│   └── roadmap/ROADMAP.md            ← Долгосрочный план
├── spec-first/
│   ├── PROJECTIDEA.md                ← Шаблон идеи
│   ├── SPEC-TEMPLATE.md              ← Шаблон спецификации
│   └── audit/
│       ├── spec_first_auditor.py     ← Block verification script
│       └── audit_log.jsonl           ← Append-only audit log
└── logs/                             ← Логи sync

~/banxe-architecture/                 ← АРХИТЕКТУРА (не трогать настройки)
├── INSTRUCTION-LEDGER.md
├── COMPLIANCE-MATRIX.md
├── DEPARTMENT-MAP.md
├── BLOCKED-TASKS.md
├── PLANES.md
├── agents/passports/                 ← Паспорта агентов
└── docs/                             ← UI/UX документация

~/banxe-emi-stack/                    ← PRODUCT PLANE (production)
~/banxe-ui/                           ← DEVELOPER PLANE (прототипы)
~/obsidian-vault/                     ← KNOWLEDGE VAULT (знания)
```

---

## КОНТРОЛЬНЫЙ СПИСОК ПРОМТА

| # | Блок | Содержание | Статус |
|---|------|-----------|--------|
| 0 | Территории | 4 зоны: developer, проекты, архитектура, vault | ✅ |
| 1 | GSD + Spec-First | 9 фаз включая Vault | ✅ |
| 2 | Авто-одобрения | ДА/СПРОСИТЬ списки | ✅ |
| 3 | Контролёр | Supervisor Agent + самовозврат + чек-лист 8/8 | ✅ |
| 4 | Навыки | GitHub, Spec, Testing, ArchiMate, Vault Management | ✅ |
| 5 | Инфраструктура | Репозитории, Planes | ✅ |
| 6 | Vault Protocol | Когда/куда/как записывать знания | ✅ |
| 7 | Формат отчёта | GSD Status Report с vault-статистикой | ✅ |
| 8 | Slash-команды | 6 GSD команд | ✅ |
| 9 | Обязательность | Приказ + приоритет контекста + действия при нарушении | ✅ |
| 10 | Memory Protocol | memory ↔ vault связь | ✅ |
| 11 | Серверы | GMKtec, NucBox, Legion — полная схема | ✅ |
| 12 | UI/UX Pipeline | banxe-ui + 8-стадийный pipeline + docs | ✅ |
| 13 | Execution Plan | 6 задач до 7 мая 2026 | ✅ |
| 14 | Структура файлов | Полное дерево всех файлов | ✅ |
