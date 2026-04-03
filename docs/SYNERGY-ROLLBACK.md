# Synergy Rollback Plan — Откат технологии синергии

**Repository:** `~/developer/docs/`  
**Version:** 1.0 | 2026-04-03  
**Purpose:** План отката на случай проблем с Claude Code + Qoder CLI синергией

---

## Что такое откат

Откат = вернуться к работе без MCP-синергии, только с прямыми командами.

---

## Сценарии отката

### Сценарий 1: MCP сервер зависает

**Симптомы:**
- Claude не получает ответ от Qoder
- Терминал висит без вывода
- `ps aux | grep qodercli` показывает процесс

**Решение:**
```bash
# Убить MCP сервер
pkill -f "qodercli mcp-server"

# Перезапустить сессию Claude
exit
cd ~/project
claude
```

### Сценарий 2: Контекст не загружается

**Симптомы:**
- Qoder игнорирует правила проекта
- Инструкции из AGENTS.md не применяются

**Решение:**
```bash
# Проверить конфиг
cat ~/.qoder/config.yml

# Проверить наличие файлов
ls -la AGENTS.md .qoder/context.md CLAUDE.md

# Перезагрузить Qoder
pkill -f qodercli
cd ~/project
claude
```

### Сценарий 3: WSL filesystem hangs

**Симптомы:**
- Высокий CPU при работе с файлами
- Git команды зависают
- Node_modules сканирование вызывает freeze

**Решение:**
```bash
# Временно отключить watchPolling
# Edit ~/.qoder/config.yml:
wsl:
  watchPolling: false

# Или увеличить интервал
wsl:
  watchInterval: 5000
```

### Сценарий 4: Полная деактивация синергии

**Если нужно полностью отключить MCP:**

1. **Edit `~/.claude/settings.json`:**
```json
{
  // Закомментировать или удалить MCP секцию
  // "mcpServers": { ... }
}
```

2. **Работать напрямую:**
```bash
cd ~/project
# Прямые команды вместо синергии
qodercli -p "сделай X"
```

---

## Backup инструкции

Перед любым обновлением синергии:

```bash
cd ~/project
mkdir -p .synergy-backup-$(date +%Y%m%d-%H%M%S)
cp AGENTS.md .qoder/context.md docs/COLLAB.md .synergy-backup-/
```

Восстановление:
```bash
cd ~/project
cp .synergy-backup-*/{file} .
git restore {file}
```

---

## Диагностика

### Check script
```bash
bash scripts/check-agent-instructions.sh
```

### Ручная проверка
```bash
# 1. MCP настроен?
grep -A5 "mcpServers" ~/.claude/settings.json

# 2. Qoder установлен?
qodercli --version

# 3. Контекст загружен?
ls -la ~/.qoder/config.yml

# 4. Проектные файлы на месте?
ls -la AGENTS.md .qoder/context.md docs/COLLAB.md
```

---

## Эскалация

Если откат не помог:

1. Сохранить логи:
```bash
cp ~/.qoder/logs/*.log ./synergy-issue-$(date +%Y%m%d).log
```

2. Описать проблему в issue tracker

3. Временно работать без синергии
