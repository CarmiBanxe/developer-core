# MEMORY.md — Developer Core Long-Term Memory

**Repository:** `~/developer/`  
**Last Updated:** 2026-04-03  
**Version:** 1.0

---

## Current State (2026-04-03 — 13:30)

### ✅ Completed

1. **Developer Core Repository Created**
   - Location: `~/developer/`
   - Commit: `e323165` (latest)
   - Status: ✅ PUSHED TO GITHUB (CarmiBanxe/developer)

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
   - `docs/ALL-PHASES-COMPLETE.md` — Final deployment report
   - `docs/GITHUB-REGISTRY.md` — Repository registry
   - `docs/GITHUB-SETUP.md` — GitHub creation guide
   - `docs/GITHUB-FINAL-STEPS.md` — Manual UI checklist
   - `docs/MIROFISH-INTEGRATION.md` — MiroFish partner integration plan
   - `docs/MIROFISH-GITHUB-SETUP.md` — GitHub repos for MiroFish
   - `docs/MIROFISH-DEPLOY-GMKTEC.md` — GMKtec/NucBox deployment guide

4. **Phase 1 & 2 Deployment COMPLETE**
   - ✅ `vibe-coding/` — sync commit `dcdbf45`
   - ✅ `collaboration/` — sync commit `4018078`
   - ✅ `MetaClaw/` — sync commit `141d421`
   - ✅ `guiyon/` — sync commit `aa49077` (after SSH key removal)
   - ✅ `ss1/` — sync commit `7917d17`
   - ✅ `developer/` — sync commit `217f333`
   - All projects verified with `check-agent-instructions.sh`

5. **MiroFish Integration Prepared**
   - `mirofish/config-template.yml` — Base configuration
   - `mirofish/install-mirofish.sh` — Installation script
   - `mirofish/run-simulation.sh` — CLI runner
   - `mirofish/scenarios/*.yml` — 7 pre-built scenarios
   - `mirofish/README.md` — Quick start guide

6. **Banxe MiroFish Repository Created**
   - Location: `~/banxe-mirofish/`
   - Commit: `729144c`
   - Status: Ready for GitHub remote setup
   - Visibility: PRIVATE (scenarios + reports)
   - Components: `.qoder/`, AGENTS.md, CLAUDE.md, docs/COLLAB.md
   - `mirofish/run-simulation.sh` — Simulation runner CLI
   - `mirofish/scenarios/hitl-handoff.yml` — Scenario 1: HITL trust study
   - `mirofish/scenarios/pre-fca-sandbox.yml` — Scenario 2: Compliance testing
   - `mirofish/scenarios/fraud-social-eng.yml` — Scenario 3: Fraud patterns
   - `mirofish/scenarios/gtm-reaction.yml` — Scenario 4: Market reaction
   - `mirofish/scenarios/ux-validation.yml` — Scenario 5: UX validation
   - `mirofish/scenarios/fraud-stress-test.yml` — Scenario 6: Stress testing
   - `mirofish/scenarios/market-adoption.yml` — Scenario 7: Adoption curve

---

### 🔄 In Progress

1. **MiroFish Integration Phase 1**
   - Components: Installation scripts, configuration templates, 7 scenarios
   - Status: READY FOR USER REVIEW
   - Next: User approval → install-mirofish.sh execution → first simulation

---

### ⏳ Pending

1. **MiroFish Phase 2: First Production Simulation**
   - Target: Run hitl-handoff scenario for Banxe AI Bank
   - Expected output: HITL threshold recommendations for compliance stack
   - Updates: `src/compliance/hitl_gateway.py` decision thresholds

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

### 2026-04-03: Three-Partner Synergy (Claude + Qoder + MiroFish)

**Decision:** Integrate MiroFish as third partner following same algorithm

**Role definition:**
- **Claude Code**: Architect & Coordinator (design, review, orchestration)
- **Qoder CLI**: Executor (implementation, edits, tests)
- **MiroFish**: Simulator & Validator (behavioral simulation, stress-testing)

**When MiroFish activates:**
- Designing HITL handoff points (BCG requirement)
- Testing compliance policies before FCA Sandbox
- Validating UX flows before implementation
- Stress-testing fraud detection scenarios
- Simulating market reaction to product launches

**Architecture:**
```json
{
  "mcpServers": {
    "qoder": {
      "type": "stdio",
      "command": "qodercli",
      "args": ["mcp-server"]
    },
    "mirofish": {
      "type": "stdio",
      "command": "mirofish-cli",
      "args": ["mcp-server"],
      "env": {
        "MIROFISH_GRAPH_URI": "bolt://localhost:7687",
        "MIROFISH_LLM_URL": "http://localhost:11434/v1",
        "MIROFISH_MODEL": "qwen2.5:32b"
      }
    }
  }
}
```

**Seven high-value applications:**
1. HITL architecture simulation (дублёр trust thresholds)
2. Pre-FCA-Sandbox compliance testing
3. Fraud pattern detection via social simulation
4. Go-to-market market reaction modeling
5. UX validation pipeline (AutoResearchClaw → MiroFish → Claude Code)
6. Fraud scenario stress-testing (quarterly)
7. Market adoption curve modeling

**Integration status:** Components ready, awaiting Phase 1 installation

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
| Components created | 22 | 15+ | ✅ EXCEEDED |
| Sync scripts tested | 6/6 | 6/6 | ✅ All passed |
| GitHub repos pushed | 6/6 | 6/6 | ✅ COMPLETE |
| Documentation pages | 13 | 10+ | ✅ COMPLETE |
| Phase 1 deployment (Banxe) | 100% | 100% | ✅ COMPLETE |
| Phase 2 deployment (Legal) | 100% | 100% | ✅ COMPLETE |
| MiroFish scenarios created | 7/7 | 7/7 | ✅ READY |
| MiroFish integration status | Phase 1 ready | Phase 1 complete | 🔄 PENDING USER APPROVAL |

---

## Next Actions

### Immediate (DONE)

1. ~~**Sync to vibe-coding**~~ ✅ COMPLETE
2. ~~**Test synergy in vibe-coding**~~ ✅ VERIFIED
3. ~~**Deploy to collaboration/**~ ✅ COMPLETE
4. ~~**Deploy to MetaClaw/**~~ ✅ COMPLETE
5. ~~**Deploy to guiyon/**~~ ✅ COMPLETE
6. ~~**Deploy to ss1/**~~ ✅ COMPLETE
7. ~~**Push all repos to GitHub**~~ ✅ COMPLETE
8. ~~**Create MiroFish integration plan**~~ ✅ COMPLETE (docs/MIROFISH-INTEGRATION.md)
9. ~~**Create MiroFish scenarios (7)**~~ ✅ COMPLETE

### Pending - MiroFish Phase 1 Installation

10. **Review MiroFish integration proposal**
    - Read: `docs/MIROFISH-INTEGRATION.md`
    - Decision: Proceed with installation?
    
11. **Install MiroFish engine** (if approved)
    ```bash
    cd ~/developer
    bash mirofish/install-mirofish.sh
    ```
    
12. **Run first test simulation**
    ```bash
    bash mirofish/run-simulation.sh test
    ```
    
13. **Execute first production scenario**
    ```bash
    bash mirofish/run-simulation.sh hitl-handoff --agents 300 --rounds 40
    ```

### Pending - Future Work

14. **Create remaining templates**
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
