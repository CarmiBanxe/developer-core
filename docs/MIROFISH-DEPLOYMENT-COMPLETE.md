# MiroFish Integration — Complete Deployment Report

**Date:** 2026-04-03  
**Status:** Phase 1 COMPLETE — Ready for GitHub setup & GMKtec deployment  
**Version:** 1.0

---

## Executive Summary

MiroFish integration prepared following the same algorithm as Claude Code + Qoder CLI synergy. All components ready for deployment.

### Three-Partner Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  USER WORKFLOW                           │
│                                                           │
│  cd ~/project                                            │
│  claude                                                  │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │        Claude Code (Architect/Coordinator)         │ │
│  │   • Design architecture                            │ │
│  │   • Review code                                    │ │
│  │   • Trigger simulations when needed                │ │
│  └────────────────────────────────────────────────────┘ │
│              ↓ MCP                        ↓ MCP          │
│  ┌──────────────────────┐   ┌──────────────────────────┐│
│  │   Qoder CLI          │   │   MiroFish               ││
│  │   (Executor)         │   │   (Simulator)            ││
│  │   • Implement        │   │   • Model users          ││
│  │   • Edit files       │   │   • Stress-test          ││
│  │   • Run tests        │   │   • Validate UX          ││
│  └──────────────────────┘   └──────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

---

## Repositories Prepared

### 1. banxe-mirofish (PRIVATE)

**Local path:** `~/banxe-mirofish/`  
**GitHub:** `CarmiBanxe/banxe-mirofish` (to be created)  
**Commit:** `729144c`

**Purpose:** Private repository for proprietary simulation assets

**Contents:**
| File | Purpose |
|------|---------|
| `.qoder/config.yml` | Qoder CLI configuration |
| `.qoder/context.md` | Execution contract |
| `AGENTS.md` | Agent instructions |
| `CLAUDE.md` | Project context (CONFIDENTIAL) |
| `README.md` | Repository overview |
| `docs/COLLAB.md` | Collaboration pattern |

**Next action:** Create GitHub repo (Private) and push

---

### 2. MiroFish-Offline (FORK)

**Source:** `nikmcfly/MiroFish-Offline`  
**GitHub:** `CarmiBanxe/MiroFish-Offline` (to be forked)  
**Local path:** `~/mirofish-engine/` (after cloning)

**Purpose:** MiroFish engine fork for customization and deployment

**Deployment target:** GMKtec EVO-X2 (128 GB RAM, ROCm)

---

### 3. developer-core (UPDATED)

**GitHub:** `CarmiBanxe/developer-core` ✅ ALREADY PUSHED  
**Latest commit:** `530d640`

**New documentation:**
- `docs/MIROFISH-INTEGRATION.md` — Full integration plan (450+ lines)
- `docs/MIROFISH-GITHUB-SETUP.md` — GitHub repository creation guide
- `docs/MIROFISH-DEPLOY-GMKTEC.md` — GMKtec deployment instructions
- `docs/MEMORY.md` — Updated with MiroFish state

**MiroFish components:**
- `mirofish/config-template.yml`
- `mirofish/install-mirofish.sh`
- `mirofish/run-simulation.sh`
- `mirofish/scenarios/*.yml` (7 scenarios)
- `mirofish/README.md`

---

## Seven High-Value Applications

All scenarios created and ready to use:

| # | Scenario | Agents | Rounds | Use Case |
|---|----------|--------|--------|----------|
| 1 | HITL handoff trust study | 300 | 40 | BCG human approval gates |
| 2 | Pre-FCA-Sandbox testing | 250 | 30 | Compliance policy validation |
| 3 | Fraud social engineering | 400 | 50 | Novel attack pattern detection |
| 4 | GTM market reaction | 350 | 35 | Launch strategy optimization |
| 5 | UX validation pipeline | 200 | 25 | KYC onboarding optimization |
| 6 | Fraud stress test | 500 | 50 | Quarterly crisis simulation |
| 7 | Market adoption curve | 600 | 60 | Go-to-market planning |

---

## Immediate Actions Required

### Step 1: Create GitHub Repositories

**A. banxe-mirofish (PRIVATE)**

```bash
# Via GitHub UI: https://github.com/new
# Name: banxe-mirofish
# Visibility: Private ⚠️
# Initialize: NO

# Then push:
cd ~/banxe-mirofish
git remote add origin git@github.com:CarmiBanxe/banxe-mirofish.git
git branch -M master
git push -u origin master
```

**B. MiroFish-Offline (FORK)**

```bash
# Via GitHub UI: https://github.com/nikmcfly/MiroFish-Offline
# Click "Fork" → Owner: CarmiBanxe → Create fork

# Then clone:
cd ~
git clone git@github.com:CarmiBanxe/MiroFish-Offline.git mirofish-engine
```

---

### Step 2: Deploy to GMKtec/NucBox

**SSH to GMKtec:**
```bash
ssh gmktec
# Or: ssh mmber@192.168.0.72
```

**Follow deployment guide:**
```bash
# On GMKtec
cd ~
git clone https://github.com/CarmiBanxe/MiroFish-Offline.git mirofish-engine
cd mirofish-engine
cp .env.example .env
# Edit .env with Banxe settings
docker compose up -d
ollama pull qwen2.5:32b
ollama pull nomic-embed-text
```

**Full instructions:** See `docs/MIROFISH-DEPLOY-GMKTEC.md`

---

### Step 3: Verify Installation

**Test API health:**
```bash
curl http://localhost:3000/api/health
# Expected: {"status":"ok","agents":0,"simulations":0}
```

**Run test simulation:**
```bash
cd ~/banxe-mirofish
bash ../developer/mirofish/run-simulation.sh test
```

---

## Documentation Index

| Document | Location | Purpose |
|----------|----------|---------|
| Full Integration Plan | `developer/docs/MIROFISH-INTEGRATION.md` | Complete architecture |
| GitHub Setup Guide | `developer/docs/MIROFISH-GITHUB-SETUP.md` | Repository creation |
| GMKtec Deployment | `developer/docs/MIROFISH-DEPLOY-GMKTEC.md` | Server deployment |
| Quick Start | `developer/mirofish/README.md` | Usage guide |
| Scenario Library | `developer/mirofish/scenarios/` | 7 pre-built scenarios |
| Memory State | `developer/docs/MEMORY.md` | Partnership tracking |

---

## Security Classification

| Repository | Visibility | Contents |
|------------|------------|----------|
| `banxe-mirofish` | **PRIVATE** | Proprietary scenarios, FCA test results |
| `MiroFish-Offline` | Public | Engine fork (open source) |
| `developer-core` | Public | Integration components |
| `vibe-coding` | Public | Production banking stack |

---

## Success Metrics

### Phase 1: Preparation ✅ COMPLETE

- [x] Integration proposal documented
- [x] 7 scenarios created
- [x] Installation scripts written
- [x] banxe-mirofish repository prepared
- [x] GitHub setup guide created
- [x] GMKtec deployment guide created
- [x] Documentation pushed to GitHub

### Phase 2: Deployment 🔄 PENDING

- [ ] GitHub repositories created
- [ ] MiroFish forked from nikmcfly
- [ ] Engine deployed to GMKtec
- [ ] First test simulation run
- [ ] HITL scenario executed for Banxe

### Phase 3: Production 📅 FUTURE

- [ ] Custom Banxe scenarios created
- [ ] Quarterly stress-test schedule established
- [ ] FCA Sandbox pre-testing workflow active
- [ ] Fraud pattern library populated

---

## Contact

| Role | Person | Access |
|------|--------|--------|
| CEO/CTIO | Moriel Carmi (Mark) | Full access |
| CTIO Deputy | Олег | GMKtec sudo NOPASSWD |

---

## Related Files

| Path | Purpose |
|------|---------|
| `~/developer/docs/MIROFISH-INTEGRATION.md` | Master integration plan |
| `~/developer/docs/MIROFISH-GITHUB-SETUP.md` | GitHub repository guide |
| `~/developer/docs/MIROFISH-DEPLOY-GMKTEC.md` | GMKtec deployment |
| `~/banxe-mirofish/` | Private scenarios repository |
| `~/.claude/CLAUDE.md` | Updated for three-partner model |

---

**Status:** READY FOR USER ACTION  
**Next:** Create GitHub repositories → Deploy to GMKtec → Run first simulation
