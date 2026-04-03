# GitHub Repository Registry — Все репозитории CarmiBanxe

**Date:** 2026-04-03  
**Account:** github.com/CarmiBanxe  
**Status:** Consolidated

---

## Complete Repository List (6 проектов)

| # | Project | Local Path | GitHub Repo | Status | Sync Commit |
|---|---------|------------|-------------|--------|-------------|
| 1 | **vibe-coding** | `~/vibe-coding/` | CarmiBanxe/vibe-coding | ✅ EXISTS | dcdbf45 |
| 2 | **collaboration** | `~/collaboration/` | CarmiBanxe/collaboration | ⏳ CREATE | 4018078 |
| 3 | **MetaClaw** | `~/MetaClaw/` | CarmiBanxe/MetaClaw | ⏳ CREATE | 141d421 |
| 4 | **guiyon** | `~/guiyon/` | CarmiBanxe/guiyon | ⏳ CREATE | 6a2bc2e |
| 5 | **ss1** | `~/ss1/` | CarmiBanxe/ss1 | ⏳ CREATE | 7917d17 |
| 6 | **developer-core** | `~/developer/` | CarmiBanxe/developer-core | ⏳ CREATE | 221d2a1 |

---

## Existing vs Required

### ✅ Already on GitHub (1)

| Repo | URL | Notes |
|------|-----|-------|
| vibe-coding | https://github.com/CarmiBanxe/vibe-coding | Ready to push new commits |

### ⏳ Need Creation on GitHub (5)

Эти репозитории нужно создать через https://github.com/new:

1. **collaboration** — Infrastructure sync
2. **MetaClaw** — Crypto AML module
3. **guiyon** — Legal project (France civil law)
4. **ss1** — Legal project (France criminal law)
5. **developer-core** — Central shared components

---

## Quick Push Commands

После создания репозиториев на GitHub:

```bash
# One-liner для всех 6 репозиториев
for repo in vibe-coding collaboration MetaClaw guiyon ss1 developer-core; do
    echo "=== Pushing $repo ==="
    cd ~/$(basename $repo)
    [ "$repo" = "developer-core" ] && cd ~/developer
    git push -u origin master || echo "FAILED: $repo (create on GitHub first)"
    cd ~
done
```

Или по одному:

```bash
# 1. vibe-coding (уже существует)
cd ~/vibe-coding && git push

# 2. collaboration (нужно создать)
# Создать: https://github.com/new?name=collaboration
cd ~/collaboration && git push -u origin master

# 3. MetaClaw (нужно создать)
# Создать: https://github.com/new?name=MetaClaw
cd ~/MetaClaw && git push -u origin master

# 4. guiyon (нужно создать)
# Создать: https://github.com/new?name=guiyon
cd ~/guiyon && git push -u origin master

# 5. ss1 (нужно создать)
# Создать: https://github.com/new?name=ss1
cd ~/ss1 && git push -u origin master

# 6. developer-core (нужно создать)
# Создать: https://github.com/new?name=developer-core
cd ~/developer && git push -u origin master
```

---

## Remote Configuration Summary

Все remote настроены на **git@github.com:CarmiBanxe/**:

```bash
# Проверка всех remote
for repo in vibe-coding collaboration MetaClaw guiyon ss1; do
    echo "=== $repo ==="
    cd ~/$repo && git remote -v
done
echo "=== developer-core ==="
cd ~/developer && git remote -v
```

**Ожидаемый результат:**
```
origin	git@github.com:CarmiBanxe/{repo}.git (fetch)
origin	git@github.com:CarmiBanxe/{repo}.git (push)
```

---

## SSH Key Requirement

Для пуша через SSH требуется добавить публичный ключ в GitHub:

1. Проверить наличие ключа:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. Если нет — создать:
   ```bash
   ssh-keygen -t ed25519 -C "mmber@banxe.ai"
   ```

3. Добавить публичный ключ в GitHub:
   - Settings → SSH and GPG keys → New SSH key
   - Вставить содержимое `~/.ssh/id_ed25519.pub`

4. Проверить подключение:
   ```bash
   ssh -T git@github.com
   ```

---

## Alternative: GitHub CLI

Если установлен `gh`, можно создать репозитории автоматически:

```bash
# Authenticate
gh auth login

# Create all repos
gh repo create CarmiBanxe/collaboration --public --source=~/collaboration --push
gh repo create CarmiBanxe/MetaClaw --public --source=~/MetaClaw --push
gh repo create CarmiBanxe/guiyon --public --source=~/guiyon --push
gh repo create CarmiBanxe/ss1 --public --source=~/ss1 --push
gh repo create CarmiBanxe/developer-core --public --source=~/developer --push
```

---

## Related Documents

- `GITHUB-SETUP.md` — Detailed setup instructions
- `ALL-PHASES-COMPLETE.md` — Deployment completion report
- `MEMORY.md` — Project memory

---

**Last Updated:** 2026-04-03  
**Next Action:** Create 5 repositories on GitHub, then push all 6
