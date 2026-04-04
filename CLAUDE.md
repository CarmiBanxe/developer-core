# CLAUDE.md — Developer-Core: Claude Code + Qoder CLI

> Версия: 2.1 | Qoder CLI v0.1.38 | 2026-04-05
> Imported from collaboration repo, adapted for developer-core layer

## Проект

developer-core — центральный хаб инструментов разработки.
Claude Code (архитектор) + Qoder CLI (исполнитель) работают совместно.

## Роль Claude Code (я)

- Архитектор — проектирую модули, API, схемы данных
- Ревьюер — анализирую код, нахожу баги, уязвимости
- Оркестратор — разбиваю задачи для параллельных воркеров Qoder
- Память — обновляю docs/MEMORY.md после каждого значимого действия

## Роль Qoder CLI

- Быстрый исполнитель задач (model: efficient / auto)
- Параллельные воркеры через `--worktree` (разные ветки одновременно)
- Альтернативные модели: qmodel, kmodel, performance, ultimate
- Интерактивные сессии с загрузкой моего конфига (`--with-claude-config`)

## Workspace

- Репозиторий: /home/mmber/developer-core/ (git: master -> main)
- Основной проект BANXE: /home/mmber/vibe-coding/
- MCP конфиг: /home/mmber/developer-core/.mcp.json
- Память: /home/mmber/developer-core/docs/MEMORY.md

## Запуск синергии

```bash
cd /home/mmber/developer-core

# Интерактивная сессия (Claude MCP + Qoder в одном терминале)
bash scripts/collab.sh session

# Параллельный воркер
bash scripts/collab.sh worker "реализуй модуль X" feature-x

# Одиночный запрос
bash scripts/collab.sh run "проверь compliance модуль на уязвимости"

# Статус активных задач
bash scripts/collab.sh jobs
```

## Канон (обязательные правила)

### Безопасность

- Никаких секретов в коде — только переменные окружения
- Все платёжные операции через HITL (Human In The Loop)
- FCA compliance: sanctions check обязателен для каждой транзакции

### Память

- После каждого значимого изменения — обновить docs/MEMORY.md
- Коммитить с понятным сообщением

### Стиль

- Язык общения: русский
- Код: английский
- Без лишних файлов, без over-engineering

## Стек

- Python 3.12 / FastAPI / ClickHouse
- Moov Watchman (санкции), Wikidata (PEP), FINOS OpenAML (crypto)
- Redis (velocity checks), PassportEye (MRZ)
- API порт: 8090 (compliance), 8085 (screener), 8084 (watchman)

## Архитектура (канон)

- MetaClaw = developer-core tool (НЕ продукт BANXE)
- MiroFish engine в developer-core/mirofish/
- Делегирование: developer-core создаёт -> форкает -> проект использует
- 1 терминал = 1 проект = 1 репозиторий
