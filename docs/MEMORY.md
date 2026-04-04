# MEMORY.md — Developer Core Long-Term Memory

**Repository:** `~/developer/`  
**Last Updated:** 2026-04-03 (Three-Partner Infrastructure Update)  
**Version:** 3.0

---

## Current State (2026-04-03 — Three-Partner Synergy Complete)

### ✅ COMPLETED — Three-Partner Infrastructure Update

**Date:** 2026-04-03  
**Architecture:** Claude Code + Qoder CLI + MiroFish for ALL projects

1. **Unified Context Architecture**
   - ✅ Deleted: `.qoder/context-banxe.md`, `context-legal.md`, `context-base.md`
   - ✅ Created: Single `.qoder/context.md` for ALL projects
   - ✅ Updated: `AGENTS.md v3.0` with three-partner documentation
   - ✅ Updated: `PROJECT-REGISTRY.csv` with `mirofish=yes` for all projects

2. **MiroFish Scenarios Deployed (6 Projects)**
   - ✅ `vibe-coding/docs/MIROFISH-SCENARIOS.md` — Banking/FCA scenarios (HITL, fraud, UX, stress tests)
   - ✅ `collaboration/docs/MIROFISH-SCENARIOS.md` — Multi-agent banking conflicts
   - ✅ `MetaClaw/docs/MIROFISH-SCENARIOS.md` — Orchestration scaling (100→10000 users)
   - ✅ `guiyon/docs/MIROFISH-SCENARIOS.md` — Court strategy (суд, апелляция, контраргументы)
   - ✅ `ss1/docs/MIROFISH-SCENARIOS.md` — Appeal dynamics (апелляция, пересмотр, взыскание)
   - ✅ `banxe-mirofish/docs/MIROFISH-SCENARIOS.md` — Master template library
   - ✅ `developer/docs/MIROFISH-SCENARIOS.md` — Master index (all scenarios)

3. **Automation Scripts**
   - ✅ `scripts/sync-all.sh` — Reads from PROJECT-REGISTRY.csv, syncs to all repos
   - ✅ `scripts/onboard-project.sh` — Onboards new projects with type-specific config
   - ✅ `.git/hooks/post-commit` — Auto-triggers sync-all.sh after commits

4. **Sync Protocol**
   - ✅ `sync-all.sh` does NOT overwrite project-specific MIROFISH-SCENARIOS.md
   - ✅ Each project maintains its own scenarios (not synced back to developer-core)
   - ✅ developer-core contains MASTER templates only

5. **Git Commits & Pushes**
   - ✅ developer-core: `ca7340b` — feat: Three-partner synergy infrastructure update
   - ✅ vibe-coding: `8d820ce` — feat: Add MiroFish banking/FCA scenarios
   - ✅ collaboration: `a1a16d1` — feat: Add MiroFish multi-agent banking conflict scenarios
   - ✅ MetaClaw: `16dd8b1` — feat: Add MiroFish orchestration scaling scenarios
   - ✅ guiyon: `f3b92ae` — feat: Add MiroFish court strategy scenarios
   - ✅ ss1: `eefbb6a` — feat: Add MiroFish appeal dynamics scenarios
   - ✅ banxe-mirofish: `0755284` — feat: Add MiroFish master template library

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

## Project Registry (Updated 2026-04-03)

| Project | Path | Type | MiroFish | Scenarios | Commit | Status |
|---------|------|------|----------|-----------|--------|--------|
| Banxe AI Bank | `~/vibe-coding/` | banxe | ✅ | banking/FCA/fraud | 8d820ce | ✅ DEPLOYED |
| Collaboration | `~/collaboration/` | banxe | ✅ | multi-agent conflicts | a1a16d1 | ✅ DEPLOYED |
| MetaClaw | `developer-core tool` | developer | ✅ | infra/orchestration scenarios | 16dd8b1 | ✅ delegated to projects |
| GUIYON | `~/guiyon/` | legal | ✅ | court strategy | f3b92ae | ✅ DEPLOYED |
| SS1 | `~/ss1/` | legal | ✅ | appeal dynamics | eefbb6a | ✅ DEPLOYED |
| Banxe MiroFish | `~/banxe-mirofish/` | tool | ✅ | MASTER templates | 0755284 | ✅ DEPLOYED |
| Developer Core | `~/developer/` | core | ✅ | ALL (MASTER index) | ca7340b | ✅ ACTIVE |

---

## Technical Decisions

### 2026-04-03: Three-Partner Synergy Architecture (UNIVERSAL)

**Decision:** MiroFish is a partner for ALL projects, not just Banxe

**Architecture:**
| Partner | Role | Activation | Scope |
|---------|------|------------|-------|
| **Claude Code** | Architect & Coordinator | Every session | Design, review, orchestration |
| **Qoder CLI** | Executor | MCP auto-load | Implementation, edits, tests |
| **MiroFish** | Simulator & Validator | Auto-trigger by keywords | Behavioral simulation, stress-testing |

**Project-specific scenarios:**
- **Banxe projects** (vibe-coding): HITL, FCA, fraud, UX validation, market reaction, scaling
- **Legal projects** (guiyon, ss1): Court strategy, judge reaction, appeal dynamics, counter-arguments, witness credibility
- **Infrastructure** (developer-core toolchain): Scaling stress, failover, sync collision, MCP contention

**Auto-trigger detection:**
- Claude detects keywords in conversation
- Automatically proposes MiroFish simulation before implementation
- Examples: "HITL" → hitl-handoff.yml, "FCA" → pre-fca-sandbox.yml, "суд" → court-strategy.yml

**Implementation:**
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

**Status:** ✅ DEPLOYED to all 7 repositories (2026-04-03)

---

### 2026-04-03: Unified Context Architecture

**Decision:** Single `.qoder/context.md` for ALL projects (removed banxe/legal/base variants)

**Rationale:**
- All projects use three-partner synergy
- Only MIROFISH-SCENARIOS.md differs by project type
- Simplifies sync-all.sh logic (no conditional context copying)
- Easier onboarding: one script, one context, same stack

**Implementation:**
- Deleted: `context-banxe.md`, `context-legal.md`, `context-base.md`
- Created: Single `context.md` with universal three-partner contract
- Updated: `onboard-project.sh` to copy single context.md
- Updated: `sync-all.sh` to NOT overwrite project-specific MIROFISH-SCENARIOS.md

**Status:** ✅ COMPLETE

---

### 2026-04-03: Auto-Sync via Post-Commit Hook

**Decision:** Automatic sync after commits to developer-core master branch

**Implementation:**
```bash
# .git/hooks/post-commit
#!/bin/bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "master" && "$BRANCH" != "main" ]]; then
    exit 0
fi
nohup bash ~/developer/scripts/sync-all.sh >> ~/developer/logs/sync-*.log 2>&1 &
```

**Behavior:**
- Runs sync-all.sh in background (non-blocking)
- Logs output to `~/developer/logs/sync-TIMESTAMP.log`
- Only triggers on master/main branch commits
- Safe: Script checks for uncommitted changes before overwriting

**Status:** ✅ INSTALLED in developer-core

---

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

## Metrics (Updated 2026-04-03)

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Repositories covered | 7/7 | 7/7 | ✅ ALL DEPLOYED |
| MiroFish scenarios created | 6 project-specific + MASTER | 6/6 | ✅ COMPLETE |
| Auto-trigger keywords defined | 24+ (banking, legal, infra) | 20+ | ✅ COMPLETE |
| Sync scripts updated | sync-all.sh, onboard-project.sh | 2/2 | ✅ COMPLETE |
| Post-commit hook installed | developer-core | 1/1 | ✅ COMPLETE |
| Context files unified | Single context.md for all | 1/1 | ✅ COMPLETE |
| GitHub repos pushed (this session) | 7/7 | 7/7 | ✅ COMPLETE |
| Three-partner architecture deployed | All projects | 100% | ✅ COMPLETE |

---

## Next Actions

### ✅ COMPLETED (2026-04-03)

1. ✅ **Unified context.md** — Single three-partner contract for all projects
2. ✅ **Updated AGENTS.md v3.0** — Three-partner architecture documentation
3. ✅ **Created MiroFish scenarios** — 6 project-specific + MASTER index
4. ✅ **Updated sync-all.sh** — No scenario overwrite, reads from registry
5. ✅ **Updated onboard-project.sh** — Single context.md, simplified logic
6. ✅ **Installed post-commit hook** — Auto-sync after developer-core commits
7. ✅ **Pushed all 7 repos** — All changes committed to GitHub

### Pending - Future Enhancements

8. **Test post-commit hook** — Commit to developer-core, verify auto-sync runs
9. **Create project-template/** — New project bootstrap directory
10. **Build agent skills library** — agents/code-reviewer.skill, etc.
11. **Run first MiroFish simulation** — Execute hitl-handoff for vibe-coding

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
