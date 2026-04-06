# CLAUDE.md — Developer-Core: BANXE AI Stack v2.0

> Версия: 4.0 | 2026-04-06
> Sprint 9: Four-Partner Swarm Architecture

## Проект

developer-core — центральный хаб инструментов разработки.  
Архитектура: Claude Code (архитектор) + Ruflo (оркестратор) + Aider CLI (исполнитель) + MiroFish (симулятор).

## Роль Claude Code (я)

- Архитектор — проектирую модули, API, схемы данных
- Ревьюер — анализирую код, нахожу баги, уязвимости
- Оркестратор — запускаю subagent паттерны (RIV / MFR / CA / PDG / MED)
- Память — обновляю docs/MEMORY.md после каждого значимого действия

## Роль Aider CLI (единственный code executor)

- Реализует код через LiteLLM :4000
- 4 режима: `--fast` (glm-4-flash), `--full` (qwen3-30b), `--banxe` (qwen3-banxe), `--unrestricted` (gpt-oss-20b)
- Запуск: `bash scripts/aider-banxe.sh [--fast|--full|--banxe] [аргументы]`

## Роль Ruflo (multi-step orchestration)

- Координирует многошаговые потоки
- Конфиг: `ruflo/config.yaml`
- Запуск: `bash ruflo/start-ruflo.sh`

## Роль MiroFish (behavioural simulator)

- Симуляция человеческого поведения, fraud, regulatory edge cases
- API: `http://localhost:3000/api`
- Активируется ключевыми словами: "human approval", "FCA", "fraud pattern", "market reaction"

## Workspace

- Репозиторий: /home/mmber/developer/ (git: main)
- Основной проект BANXE: /home/mmber/vibe-coding/ (отдельный репозиторий)
- Память: /home/mmber/developer/docs/MEMORY.md

## Запуск стека

```bash
cd /home/mmber/developer

# Проверить все компоненты
bash scripts/start_banxe_stack.sh

# Запустить Ruflo + проверить инфраструктуру
bash ruflo/start-ruflo.sh

# Выполнить код через Aider
bash scripts/aider-banxe.sh --full

# Верификация файла
bash scripts/parallel-verify.sh --file path/to/file.py
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
- 1 терминал = 1 проект = 1 репозиторий

## Стек

- Python 3.12 / FastAPI / ClickHouse
- Moov Watchman (санкции), Wikidata (PEP), FINOS OpenAML (crypto)
- Redis (velocity checks), PassportEye (MRZ)
- API порт: 8090 (compliance), 8085 (screener), 8084 (watchman)

## Архитектура (канон)

- MetaClaw = developer-core tool (НЕ продукт BANXE)
- MiroFish engine в developer-core/mirofish/
- LiteLLM :4000 = model routing layer (инфраструктура, не партнёр)
- Делегирование: developer-core создаёт -> форкает -> проект использует
