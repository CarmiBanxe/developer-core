# GitHub Final Steps — Manual Actions Required

**Date:** 2026-04-03  
**Status:** AWAITING MANUAL COMPLETION

---

## ✅ Completed (Automated)

1. **All 6 repositories pushed to GitHub**
   - vibe-coding, collaboration, MetaClaw, guiyon, ss1, developer-core
2. **SSH key removed from guiyon history**
   - `git filter-branch` executed
   - Force push successful
3. **SSH keys added to .gitignore (guiyon)**
   - Prevents future accidental commits

---

## ⏳ Pending (Manual GitHub UI Actions)

### 1. Change Repository Visibility to Private

**Required:** GitHub authentication (2FA/password)

#### Option A: Via Web UI

For each repository, visit and change visibility:

| Repository | Settings URL | Action |
|------------|--------------|--------|
| collaboration | https://github.com/CarmiBanxe/collaboration/settings | Danger Zone → Make private |
| MetaClaw | https://github.com/CarmiBanxe/MetaClaw/settings | Danger Zone → Make private |
| developer-core | https://github.com/CarmiBanxe/developer-core/settings | Danger Zone → Make private |

**Steps:**
1. Open URL
2. Scroll to **"Danger Zone"** (bottom of page)
3. Click **"Change visibility" → "Make private"**
4. Confirm repository name
5. Enter password / 2FA code if prompted

---

#### Option B: Via GitHub CLI (if authenticated)

If `gh auth login` is configured:

```bash
# Install gh CLI first if needed
sudo apt install gh

# Authenticate (one-time)
gh auth login

# Change visibility
gh repo edit CarmiBanxe/collaboration --visibility private
gh repo edit CarmiBanxe/MetaClaw --visibility private
gh repo edit CarmiBanxe/developer-core --visibility private
```

---

### 2. Delete Duplicate Repository

**guiyon-project** is now obsolete (replaced by guiyon):

1. Visit: https://github.com/CarmiBanxe/guiyon-project/settings
2. Scroll to **"Danger Zone"**
3. Click **"Delete this repository"**
4. Type repository name to confirm
5. Click **"I want to delete this repository"**

---

### 3. Delete Carmi61/All (Optional)

This repository contains only test artifacts:

1. Visit: https://github.com/Carmi61/All/settings
2. Scroll to **"Danger Zone"**
3. Click **"Delete this repository"**
4. Confirm deletion

**Alternative:** Keep as sandbox for experiments.

---

### 4. Revoke Compromised SSH Key

**Important:** The `.ssh_deploy_key` was exposed in guiyon history.

**If this key was ever used:**

1. **Revoke immediately:**
   - Remove from any servers/services where it's deployed
   - Remove from GitHub: Settings → SSH and GPG keys → Delete old keys

2. **Generate new key:**
   ```bash
   ssh-keygen -t ed25519 -C "new-deploy-key-2026-04-03" -f ~/.ssh/new_deploy_key
   
   # Add to GitHub
   cat ~/.ssh/new_deploy_key.pub
   # Copy output and add to: https://github.com/settings/keys
   ```

3. **Update deployment scripts** with new key path

**If this was a test key (never deployed):**
- No action needed
- Just don't use it going forward

---

## 🔒 Security Checklist

- [ ] SSH key revoked/replaced (if was in production use)
- [ ] `.gitignore` updated (✅ DONE for guiyon)
- [ ] Sensitive repos made private (collaboration, MetaClaw, developer-core)
- [ ] Duplicate guiyon-project deleted
- [ ] Old SSH keys removed from GitHub settings

---

## 📊 Current Repository Status

| Repository | Visibility | Status | Notes |
|------------|------------|--------|-------|
| vibe-coding | Public | ✅ Complete | Main Banxe project |
| collaboration | Public | ⏳ Make private | Contains infra configs |
| MetaClaw | Public | ⏳ Make private | Crypto AML module |
| guiyon | Public | ✅ Complete | SSH key cleaned |
| ss1 | Private | ✅ Complete | Already private |
| developer-core | Public | ⏳ Make private | Central templates |
| guiyon-project | Private | ⏳ Delete | Obsolete duplicate |

---

## 🛠️ Quick Commands (Post-Visibility-Change)

After making repos private, verify access:

```bash
# Test pull from private repos
cd ~/collaboration && git fetch origin
cd ~/MetaClaw && git fetch origin
cd ~/developer && git fetch origin
```

If authentication fails, you may need to:
1. Use SSH instead of HTTPS: `git remote set-url origin git@github.com:CarmiBanxe/REPO.git`
2. Or configure Git credential helper for HTTPS

---

## Related Documents

- `GITHUB-REGISTRY.md` — Full repository list
- `GITHUB-SETUP.md` — Setup instructions
- `ALL-PHASES-COMPLETE.md` — Deployment report
- `SYNERGY-DEPLOYMENT.md` — Technical details

---

**Last Updated:** 2026-04-03  
**Next Action:** Complete manual steps above via GitHub UI or gh CLI
