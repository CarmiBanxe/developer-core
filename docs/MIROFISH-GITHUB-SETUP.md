# MiroFish GitHub Repository Setup Guide

**Purpose:** Create required GitHub repositories for MiroFish integration  
**Date:** 2026-04-03  
**Account:** CarmiBanxe

---

## Repositories to Create

### 1. banxe-mirofish (PRIVATE)

**URL:** https://github.com/new

**Settings:**
- Repository name: `banxe-mirofish`
- Description: "Banxe AI Bank — Private MiroFish scenarios and simulation reports"
- Visibility: **Private** ⚠️
- Initialize with README: No
- Add .gitignore: None
- Add license: None

**After creation, set remote:**
```bash
cd ~/banxe-mirofish
git remote add origin git@github.com:CarmiBanxe/banxe-mirofish.git
git branch -M master
git push -u origin master
```

**Contents already prepared:**
- `.qoder/config.yml`
- `.qoder/context.md`
- `AGENTS.md`
- `CLAUDE.md` (CONFIDENTIAL)
- `README.md`
- `docs/COLLAB.md`

---

### 2. MiroFish-Offline (PUBLIC fork)

**Source:** https://github.com/nikmcfly/MiroFish-Offline

**Option A: Fork via GitHub UI (Recommended)**

1. Go to https://github.com/nikmcfly/MiroFish-Offline
2. Click "Fork" button
3. Owner: `CarmiBanxe`
4. Repository name: `MiroFish-Offline`
5. Click "Create fork"

**Option B: Manual mirror (if fork not allowed)**

```bash
cd ~/
git clone --mirror https://github.com/nikmcfly/MiroFish-Offline.git CarmiBanxe-MiroFish-Offline
cd CarmiBanxe-MiroFish-Offline
git remote rename upstream origin
# Create repo on GitHub first, then:
git remote add origin git@github.com:CarmiBanxe/MiroFish-Offline.git
git push -f origin master
```

**After fork, clone locally:**
```bash
cd ~
git clone git@github.com:CarmiBanxe/MiroFish-Offline.git mirofish-engine
cd mirofish-engine
# Configure environment
cp .env.example .env
# Edit .env with Banxe-specific settings
```

---

## Quick Setup Commands

### For banxe-mirofish (after GitHub creation)

```bash
# One-liner to create remote and push
cd ~/banxe-mirofish && \
git remote add origin git@github.com:CarmiBanxe/banxe-mirofish.git && \
git branch -M master && \
git push -u origin master
```

### For MiroFish-Offline (after fork)

```bash
# Clone fork to standard location
cd ~ && git clone git@github.com:CarmiBanxe/MiroFish-Offline.git mirofish-engine
cd ~/mirofish-engine

# Verify Docker setup
docker compose config

# Pull models
ollama pull qwen2.5:32b
ollama pull nomic-embed-text
```

---

## Verification Checklist

### banxe-mirofish repository

- [ ] Repository created on GitHub (Private)
- [ ] Remote added locally
- [ ] Initial commit pushed
- [ ] Visibility confirmed as Private

### MiroFish-Offline fork

- [ ] Fork created from nikmcfly/MiroFish-Offline
- [ ] Local clone at `~/mirofish-engine/`
- [ ] Docker Compose services start successfully
- [ ] Ollama models pulled

---

## Security Notes

### banxe-mirofish — PRIVATE

Contains:
- Proprietary banking scenarios
- Customer behavior models
- FCA compliance test results
- Fraud detection patterns

**NEVER:**
- Make this repository public
- Share scenarios outside CarmiBanxe org
- Commit production customer PII

### MiroFish-Offline — PUBLIC (fork)

Standard open-source engine fork.

**Custom modifications:**
- Keep Banxe-specific configs in `.env` (add to .gitignore)
- Store proprietary scenarios in `banxe-mirofish` repo only
- Don't commit API keys or credentials

---

## Troubleshooting

### Problem: SSH key not configured

```bash
# Generate SSH key if needed
ssh-keygen -t ed25519 -C "moriel@banxe.com"

# Add to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy output to: https://github.com/settings/keys

# Test connection
ssh -T git@github.com
```

### Problem: Permission denied creating fork

The original MiroFish repository may have restrictions.

**Solution:**
1. Use manual mirror method (see Option B above)
2. Or contact repository owner for fork permission

### Problem: Docker Compose not starting

```bash
cd ~/mirofish-engine
docker compose down -v
docker compose up -d
docker compose logs
```

---

## Next Steps After Setup

1. **Deploy MiroFish to GMKtec/NucBox**
   - See `docs/MIROFISH-DEPLOY-GMKTEC.md`

2. **Run first test simulation**
   ```bash
   cd ~/banxe-mirofish
   bash ../developer/mirofish/run-simulation.sh test
   ```

3. **Create first custom scenario**
   - Copy template from `developer/mirofish/scenarios/`
   - Customize for Banxe use case
   - Document in `docs/SCENARIOS.md`

---

## Contact

| Person | Role |
|--------|------|
| Moriel Carmi | CEO/CTIO |

---

## Related Documentation

- `MIROFISH-INTEGRATION.md` — Full integration plan
- `MIROFISH-DEPLOY-GMKTEC.md` — GMKtec deployment guide
- `~/developer/mirofish/README.md` — Quick start guide
