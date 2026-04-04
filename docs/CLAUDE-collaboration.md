# CLAUDE.md — Collaboration: Claude Code + Aider CLI

> Версия: 3.0 | Aider CLI standalone | 2026-04-03

## Проект
Banxe AI Bank — EMI, FCA authorised.
Совместная разработка AML/KYC compliance стека силами Claude Code (архитектор) и Aider CLI (исполнитель).

## Роль Claude Code (я)
- Архитектор — проектирую модули, API, схемы данных
- Ревьюер — анализирую код, нахожу баги, уязвимости
- Оркестратор — разбиваю задачи для параллельных воркеров Aider
- Память — обновляю docs/MEMORY.md после каждого значимого действия

## Роль Aider CLI
- Быстрый исполнитель задач (model: efficient / auto)
- Параллельные воркеры через `--worktree` (разные ветки одновременно)
- Альтернативные модели: qmodel, kmodel, performance, ultimate
- Интерактивные сессии с загрузкой моего конфига (`--with-claude-config`)

## Workspace
- Репозиторий: /home/mmber/collaboration/ (git: master)
- Compliance stack: /home/mmber/collaboration/compliance/
- Основной проект: /home/mmber/vibe-coding/
- MCP конфиг: /home/mmber/collaboration/.mcp.json
- Память: /home/mmber/collaboration/docs/MEMORY.md

## Запуск синергии

```bash
cd /home/mmber/collaboration

# Интерактивная сессия (Claude MCP + Aider в одном терминале)
bash collab.sh session

# Параллельный воркер
bash collab.sh worker "реализуй модуль X" feature-x

# Одиночный запрос
bash collab.sh run "проверь compliance/api.py на уязвимости"

# Статус активных задач
bash collab.sh jobs
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
