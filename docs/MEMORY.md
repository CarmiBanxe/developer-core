# MEMORY.md — Developer Core Long-Term Memory

**Repository:** `~/developer/`  
**Last Updated:** 2026-04-03  
**Version:** 1.0

---

## Current State (2026-04-03 — 11:36)

### ✅ Completed

1. **Developer Core Repository Created**
   - Location: `~/developer/`
   - Commit: `e323165` (latest)
   - Status: Local only (GitHub push pending auth)

2. **Core Components Deployed**
   - `.qoder/config.yml` — WSL-optimized Qoder config
   - `.qoder/context.md` — Execution contract template
   - `AGENTS.md` — Agent instructions template
   - `docs/COLLAB.md` — Single-terminal synergy v3.0
   - `docs/MCP-BEST-PRACTICES.md` — MCP configuration guide
   - `scripts/check-agent-instructions.sh` — Diagnostic tool
   - `scripts/sync-to-project.sh` — Automated distribution
   - `compliance/COMPLIANCE_ARCH.md` — FCA invariants contract

3. **Documentation Created**
   - `README.md` — Project overview
   - `docs/SYNERGY-DEPLOYMENT.md` — Deployment plan (ACTIVE)
   - `docs/SYNERGY-ROLLBACK.md` — Rollback procedures
   - `docs/MEMORY.md` — This file

4. **Phase 1 Deployment COMPLETE**
   - ✅ `vibe-coding/` — sync commit `dcdbf45`
   - ✅ `collaboration/` — sync commit `4018078`
   - ✅ `MetaClaw/` — sync commit `141d421`
   - All projects verified with `check-agent-instructions.sh`

---

### 🔄 In Progress

1. **GitHub Remote Setup**
   - Repo: CarmiBanxe/developer
   - Status: Auth required (SSH key or token)

---

### ⏳ Pending

1. **Legal Projects Deployment (Phase 2)**
   - Target: `guiyon/`, `ss1/`
   - Status: Ready to deploy
   - Note: SS1 uses GUIYON tech stack, legally independent

---

### ⏳ Pending

1. **Legal Projects Deployment (Phase 2)**
   - Target: `guiyon/`, `ss1/`
   - Status: Waiting Phase 1 completion
   - Note: SS1 uses GUIYON tech stack, legally independent

2. **Project Template Creation**
   - Location: `templates/project-template/`
   - Status: Not started

3. **Agent Skills Library**
   - Location: `agents/`
   - Status: Not started

---

## Project Registry

| Project | Path | Type | Synergy Status | Commit |
|---------|------|------|----------------|--------|
| Banxe AI Bank | `~/vibe-coding/` | Primary | ✅ DEPLOYED | dcdbf45 |
| Collaboration | `~/collaboration/` | Infra | ✅ DEPLOYED | 4018078 |
| MetaClaw | `~/MetaClaw/` | Module | ✅ DEPLOYED | 141d421 |
| GUIYON | `~/guiyon/` | Legal | ✅ DEPLOYED | 6a2bc2e |
| SS1 | `~/ss1/` | Legal | ✅ DEPLOYED | 7917d17 |
| Developer | `~/developer/` | Core | ACTIVE | 5ffcfcc |

---

## Technical Decisions

### 2026-04-03: Single-Terminal Architecture

**Decision:** Claude Code + Qoder CLI collaborate via MCP in single terminal

**Rationale:**
- User requested "100% Qoder usage" but "no manual coordination"
- Two-terminal workflow rejected as "not synergy"
- MCP auto-load from `~/.claude/settings.json` solves both requirements

**Implementation:**
```json
{
  "mcpServers": {
    "qoder": {
      "type": "stdio",
      "command": "qodercli",
      "args": ["mcp-server"]
    }
  }
}
```

**Result:** User runs `cd ~/project && claude`, Qoder loads automatically.

---

### 2026-04-03: Central Developer Repository

**Decision:** Create `~/developer/` for shared components

**Rationale:**
- Multiple projects need same configs (AGENTS.md, .qoder/config.yml, etc.)
- Manual copying is error-prone
- Sync script automates distribution with backup/rollback

**Structure:**
```
~/developer/
├── .qoder/           → Synced to all projects
├── docs/             → Synced to all projects
├── scripts/          → Synced to all projects
├── compliance/       → Banxe only (FCA invariants)
├── templates/        → Copy on demand
└── agents/           → Future skills library
```

---

### 2026-04-03: Instruction Hierarchy

**Decision:** Closer to working directory = higher priority

**Order:**
1. Explicit user instruction (highest)
2. Repository contracts (CLAUDE.md, .qoder/context.md, AGENTS.md)
3. Global defaults (~/.claude/CLAUDE.md)

**Enforcement:** Project isolation is hard invariant. Cross-repo access forbidden without explicit naming.

---

### 2026-04-03: Compliance Invariants (Banxe)

**Protected constants** (cannot change without MLRO approval):

1. Canonical key: `(jurisdiction_code, registration_number)`
2. OFAC RSS: DEAD since 31 Jan 2025 (HTML scrape only)
3. Watchman minMatch: 0.80 (Jaro-Winkler)
4. ClickHouse TTL: 5 YEAR (FCA MLR 2017)
5. Jube license: AGPLv3 internal only
6. GUIYON: Categorically excluded from Banxe

---

## Open Issues

### GitHub Authentication

**Problem:** Cannot push to GitHub (no SSH key configured)

**Workaround:**
```bash
# Option 1: SSH key
ssh-add ~/.ssh/id_ed25519
git remote add origin git@github.com:CarmiBanxe/developer.git
git push -u origin master

# Option 2: HTTPS token
git remote add origin https://github.com/CarmiBanxe/developer.git
# Will prompt for PAT
```

**Status:** Pending user action

---

### WSL Filesystem Hangs

**Problem:** File watchers can hang on large directories

**Mitigation:**
```yaml
wsl:
  watchPolling: true
  watchInterval: 1000
  maxConcurrentOperations: 2
  disableInterop: true
```

**Status:** Configured in `.qoder/config.yml`, monitoring ongoing

---

## Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Repositories covered | 6/6 | 6/6 | ✅ ALL DEPLOYED |
| Components created | 12 | 15+ | On track |
| Sync scripts tested | 6/6 | 6/6 | ✅ All passed |
| GitHub repos pushed | 0/6 | 6/6 | Auth pending |
| Documentation pages | 7 | 10+ | In progress |
| Phase 1 deployment (Banxe) | 100% | 100% | ✅ COMPLETE |
| Phase 2 deployment (Legal) | 100% | 100% | ✅ COMPLETE |

---

## Next Actions

### Immediate (DONE)

1. ~~**Sync to vibe-coding**~~ ✅ COMPLETE
2. ~~**Test synergy in vibe-coding**~~ ✅ VERIFIED
3. ~~**Deploy to collaboration/**~~ ✅ COMPLETE
4. ~~**Deploy to MetaClaw/**~~ ✅ COMPLETE
5. ~~**Deploy to guiyon/**~~ ✅ COMPLETE
6. ~~**Deploy to ss1/**~~ ✅ COMPLETE

### Pending

7. **Push all repos to GitHub**
   ```bash
   # Developer Core
   cd ~/developer && git push
   
   # Banxe Group
   cd ~/vibe-coding && git push
   cd ~/collaboration && git push
   cd ~/MetaClaw && git push
   
   # Legal Group
   cd ~/guiyon && git push
   cd ~/ss1 && git push
   ```

8. **Create remaining templates**
   - `templates/project-template/` — new project bootstrap
   - `agents/` — skills library

---

## Historical Context

### Previous Session (Summary)

- Established Claude Code + Qoder CLI dual-agent collaboration
- Created COLLAB.md v3.0 (single-terminal automatic synergy)
- Built MCP best practices documentation
- Initialized developer core repository
- Defined project hierarchy (Banxe group, GUIYON group)

### Key User Requirements

1. **"One terminal = one project"** — Strict isolation
2. **"100% Qoder usage"** — But automatic, no manual commands
3. **"Under the hood collaboration"** — User sees unified result
4. **"Central developer repo"** — Shared components across projects
5. **"SS1 ⊂ GUIYON"** — Technology sharing, legal independence

---

## Related Files

| File | Purpose | Location |
|------|---------|----------|
| `MEMORY.md` | Long-term memory | `~/developer/docs/` |
| `SYNERGY-DEPLOYMENT.md` | Deployment plan | `~/developer/docs/` |
| `SYNERGY-ROLLBACK.md` | Rollback procedures | `~/developer/docs/` |
| `COLLAB.md` | Synergy pattern | `~/developer/docs/` + synced |
| `AGENTS.md` | Agent instructions | `~/developer/` + synced |
| `COMPLIANCE_ARCH.md` | FCA invariants | `~/developer/compliance/` |

---

## Contact

| Role | Person | Scope |
|------|--------|-------|
| CEO/CTIO | Moriel Carmi (Mark) | Final authority |
| Developer | You | Component creation |
| CTIO Deputy | Олег | Infrastructure (GMKtec sudo) |

---

**Last commit:** `9eaff5c` — init: Developer Core — shared components for all projects  
**Next review:** After Phase 1 deployment completion
