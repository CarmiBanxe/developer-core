# GitHub Repository Setup Instructions

**Date:** 2026-04-03  
**Status:** MANUAL ACTION REQUIRED

---

## Summary

Все локальные репозитории готовы к пушу. Требуется **создать пустые репозитории на GitHub** и запушить код.

---

## Repositories to Create

### 1. Developer Core (NEW)

**Name:** `developer-core`  
**Description:** Central shared components for Claude Code + Qoder CLI synergy  
**Visibility:** Public (рекомендуется) или Private

```bash
# После создания репозитория на GitHub:
cd ~/developer
git remote set-url origin git@github.com:CarmiBanxe/developer-core.git
git push -u origin master
```

**URL:** https://github.com/new?name=developer-core

---

### 2. Collaboration (UPDATE REMOTE)

**Name:** `collaboration`  
**Description:** Claude Code + Qoder CLI collaboration infrastructure  
**Visibility:** Public

```bash
# Remote уже настроен, нужно создать репозиторий:
cd ~/collaboration
git push -u origin master
```

**URL:** https://github.com/new?name=collaboration

---

## Existing Repositories (Already on GitHub)

Эти репозитории уже существуют и запушены:

| Project | Remote | Status |
|---------|--------|--------|
| vibe-coding | CarmiBanxe/vibe-coding | ✅ EXISTS |
| MetaClaw | aiming-lab/MetaClaw | ✅ EXISTS |
| guiyon-project | CarmiBanxe/guiyon-project | ✅ EXISTS |
| ss1 | CarmiBanxe/ss1 | ✅ EXISTS |

Для них достаточно сделать пуш последних изменений:

```bash
# Banxe AI Bank
cd ~/vibe-coding && git push

# MetaClaw
cd ~/MetaClaw && git push

# GUIYON
cd ~/guiyon && git push

# SS1
cd ~/ss1 && git push
```

---

## Quick Setup Commands

### Option A: Create via GitHub CLI (if available later)

```bash
# Install gh CLI
sudo apt install gh

# Authenticate
gh auth login

# Create repositories
gh repo create CarmiBanxe/developer-core --public --source=~/developer --push
gh repo create CarmiBanxe/collaboration --public --source=~/collaboration --push
```

---

### Option B: Create via Web Interface

1. Открой https://github.com/new
2. Введи имя репозитория
3. Выбери владельца (CarmiBanxe)
4. Выбери Public/Private
5. **НЕ** ставь галочки "Initialize with README"
6. Click "Create repository"
7. Запушь локальный код:

```bash
cd ~/path-to-repo
git remote set-url origin git@github.com:CarmiBanxe/REPO-NAME.git
git push -u origin master
```

---

### Option C: Use GitHub API (automated)

```bash
# С токеном (требуется PAT с scope 'repo')
TOKEN="ghp_YOUR_PERSONAL_ACCESS_TOKEN"

# Create developer-core
curl -X POST "https://api.github.com/user/repos" \
  -H "Authorization: token $TOKEN" \
  -d '{"name":"developer-core","private":false,"auto_init":false}'

# Create collaboration
curl -X POST "https://api.github.com/user/repos" \
  -H "Authorization: token $TOKEN" \
  -d '{"name":"collaboration","private":false,"auto_init":false}'

# Then push
cd ~/developer && git push -u origin master
cd ~/collaboration && git push -u origin master
```

---

## Checklist

- [ ] Создать `CarmiBanxe/developer-core` на GitHub
- [ ] Создать `CarmiBanxe/collaboration` на GitHub
- [ ] Запушить `~/developer` → `developer-core`
- [ ] Запушить `~/collaboration` → `collaboration`
- [ ] Обновить изменения в существующих репозиториях:
  - [ ] `vibe-coding` (sync commit dcdbf45)
  - [ ] `MetaClaw` (sync commit 141d421)
  - [ ] `guiyon-project` (sync commit 6a2bc2e)
  - [ ] `ss1` (sync commit 7917d17)

---

## Verification After Push

После пуша проверь:

```bash
# Проверка что remote доступен
cd ~/developer && git fetch origin
cd ~/collaboration && git fetch origin

# Проверка что коммиты на месте
cd ~/developer && git log --oneline -3
cd ~/collaboration && git log --oneline -3
```

Открой в браузере:
- https://github.com/CarmiBanxe/developer-core
- https://github.com/CarmiBanxe/collaboration

---

## SSH Key Setup (if not already configured)

Если SSH ключ не настроен:

```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "mmber@banxe.ai" -f ~/.ssh/id_ed25519_github

# Add to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_github

# Copy public key
cat ~/.ssh/id_ed25519_github.pub

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
```

SSH config для нескольких ключей (`~/.ssh/config`):

```
# Personal GitHub
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github

# GUIYON project (separate account/org)
Host github-guiyon
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_guiyon

# SS1 project (separate account/org)
Host github-ss1
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_ss1
```

---

## Troubleshooting

### Problem: "Repository not found"

**Solution:** Репозиторий не создан на GitHub. Создай через веб-интерфейс.

### Problem: "Permission denied (publickey)"

**Solution:** SSH ключ не добавлен в GitHub. Добавь в Settings → SSH and GPG keys.

### Problem: "Authentication failed"

**Solution:** 
- Для HTTPS: нужен Personal Access Token (PAT)
- Для SSH: проверь ключ командой `ssh -T git@github.com`

---

## Related Documents

- `ALL-PHASES-COMPLETE.md` — Deployment completion report
- `SYNERGY-DEPLOYMENT.md` — Full deployment plan
- `MEMORY.md` — Project memory

---

**Last Updated:** 2026-04-03  
**Status:** Awaiting manual repository creation on GitHub
