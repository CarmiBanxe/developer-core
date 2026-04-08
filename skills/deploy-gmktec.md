---
name: deploy-gmktec
description: Деплой изменений banxe-emi-stack на GMKtec EVO-X2 — QRAA обязателен
---
# Skill: Deploy to GMKtec

## QRAA Требование

ПЕРЕД любым SSH-действием на GMKtec — ОБЯЗАТЕЛЕН QRAA:
1. **Diagnose** — read-only проверка текущего состояния
2. **Plan** — нумерованные шаги
3. **STOP** — ждать явного "да" от CEO
4. **Act** — выполнять только после акцепта
5. **Result** — показать результат + тест

## Стандартный деплой (code update)

```bash
# Запускать с Legion:
cd ~/banxe-emi-stack && git pull && bash scripts/deploy-safeguarding-gmktec.sh
```

Или ручной порядок:

```bash
# Step 1: Sync code (Legion → GMKtec)
rsync -az --delete \
  --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='.env' \
  ~/banxe-emi-stack/ gmktec:/data/banxe/banxe-emi-stack/

# Step 2: Install new deps (если requirements.txt изменился)
ssh gmktec "pip3 install --quiet --break-system-packages -r /data/banxe/banxe-emi-stack/requirements.txt"

# Step 3: Apply schema migrations (идемпотентно)
ssh gmktec "cd /data/banxe/banxe-emi-stack && python3 -c '
import sys; sys.path.insert(0, \".\")
from services.recon.clickhouse_client import ClickHouseReconClient
ClickHouseReconClient().ensure_schema()
print(\"Schema OK\")
'"

# Step 4: Run tests on GMKtec
ssh gmktec "cd /data/banxe/banxe-emi-stack && python3 -m pytest tests/ -q --tb=short 2>&1 | tail -10"

# Step 5: Verify services
ssh gmktec "systemctl status banxe-recon.timer --no-pager --lines=3"
ssh gmktec "curl -sf http://localhost:8095/health"  # Midaz
ssh gmktec "curl -sf http://localhost:8180/realms/banxe"  # Keycloak
```

## Деплой нового сервиса (FastAPI endpoint)

```bash
# Дополнительно к стандартному деплою:

# Рестарт FastAPI (если запущен как systemd):
ssh gmktec "systemctl restart banxe-api.service && systemctl status banxe-api.service --no-pager"

# Проверить endpoint:
ssh gmktec "curl -sf http://localhost:8000/health"
```

## Деплой systemd timer (новый cron)

```bash
# Создать unit файл → daemon-reload → enable → start
ssh gmktec "cat > /etc/systemd/system/banxe-NEW.service << 'UNIT'
[Unit]
Description=Banxe NEW Service
[Service]
Type=oneshot
User=banxe
ExecStart=/usr/bin/python3 -m services.NEW.cron_entry
UNIT"

ssh gmktec "systemctl daemon-reload && systemctl enable banxe-NEW.timer && systemctl start banxe-NEW.timer"
```

## Rollback

```bash
# Откатить код к предыдущему коммиту:
ssh gmktec "cd /data/banxe/banxe-emi-stack && git log --oneline -5"
# CEO выбирает commit hash:
ssh gmktec "cd /data/banxe/banxe-emi-stack && git reset --hard {COMMIT_HASH}"
```

## Чеклист после деплоя
- [ ] Tests pass on GMKtec
- [ ] Health endpoint returns healthy
- [ ] Systemd timer (если применимо) active
- [ ] Logs чистые (`ssh gmktec "journalctl -u banxe-* -n 20"`)
- [ ] IL запись обновлена с proof (SSH output)
