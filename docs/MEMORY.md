# MEMORY.md — Developer Core Long-Term Memory

**Repository:** `~/developer/`  
**Last Updated:** 2026-04-05 (Verification Pipeline + Canonical Terminology)  
**Version:** 4.0

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

## 2026-04-05: collaboration → developer-core (Шаг 1 слияния)

**Статус:** collaboration репо считается частью developer-core toolchain layer.

### Перенесённые уникальные файлы

| Файл | Назначение |
|------|-----------|
| `.mcp.json` | MCP конфигурация (Aider CLI server) |
| `scripts/collab.sh` | Claude Code + Aider CLI launcher (session/worker/run) |
| `.aider.conf.yml` | Aider project config (model: qwen3-banxe-v2) |
| `config.ini` | TinyTroupe/simulation config (Ollama endpoint) |
| `.claude-supervisor/` | Claude supervision hooks (pre_tool_use, stop_check, verifier) |
| `.claude/settings.json` | Claude Code project settings |
| `compliance/training/` | Agent training pipeline (corpus JSONL, deepeval, evidently, promptfoo) |
| `compliance/verification/` | Verification network (orchestrator, policy_agent, workflow_agent) |
| `.github/workflows/banxe-verification-tests.yml` | GitHub Actions: cross-verification 5 categories |
| `scripts/install_openrlhf.sh` | OpenRLHF installer (NVIDIA CUDA 12.6, Legion) |
| `scripts/install_gmktec_trl.sh` | TRL installer (AMD GMKtec, без CUDA) |
| `docs/CLAUDE-collaboration.md` | Исторический CLAUDE.md collaboration (архив контекста) |

### Статус collaboration репо

- **docs/** — дубликаты developer-core (COLLAB.md, MEMORY.md, MCP-BEST-PRACTICES.md, MIROFISH-SCENARIOS.md)
- **compliance/** — устаревшие копии vibe-coding/src/compliance/ (за исключением training/ и verification/)
- **Рекомендация:** архивировать collaboration на GitHub после финального review
- **Ветки:** master (Qoder CLI era) → main (Aider CLI era, содержит весь уникальный контент)

---

## 2026-04-05: Canonical Terminology + Verification Pipeline (v4.0)

**Session summary:** Два крупных блока работ — (1) фиксация канонической архитектурной терминологии в developer-core docs, (2) создание verification pipeline для Banxe AI Bank.

---

### 1. Canonical Delegation Model (ARCHITECTURE.md v2.0)

**Решение:** MetaClaw = developer-core инструмент. НЕ BANXE-специфический продукт.

**Иерархия:**
```
developer-core toolchain
    ↓ fork / delegate
project runtime (vibe-coding, guiyon, ss1, ...)
    ↓ operates as
project-specific operational layer
```

**Проектные манифестации MetaClaw:**
| Проект | Название | Примечание |
|--------|----------|------------|
| BANXE (vibe-coding) | **AML block** | banxe-lexisnexis-distro — один компонент AML block |
| GUIYON | Legal AI layer | |
| SS1 | Legal AI layer | |

**Изменённые файлы:**
- `docs/ARCHITECTURE.md` — полная перезапись v2.0 (3 уровня: dev partners → tools → project runtime)
- `docs/MIROFISH-SCENARIOS-MetaClaw.md` — header: Layer: developer-core toolchain (не Project: MetaClaw)
- `docs/MIROFISH-SCENARIOS.md` — удалена колонка MetaClaw из banking matrix
- `docs/MIROFISH-SCENARIOS-banxe-mirofish.md` — MetaClaw убран из sync targets
- `docs/PROJECT-REGISTRY.csv` — BANXE repos: `vibe-coding,banxe-mirofish` (MetaClaw удалён как BANXE repo)

**Коммиты:** `6947ba9` (terminology fix), `27bf885` (collaboration merge), `dc8402f` (ss1 in sync-targets)

---

### 2. Ветки и структура репо

- **master → main**: `~/developer` переведён на `main`, `origin/master` удалена
- **ss1 в sync-targets**: добавлен в `scripts/sync-to-project.sh` и `docs/PROJECT-REGISTRY.csv`
- **collaboration → developer-core**: слияние завершено (commit `27bf885`), см. раздел 2026-04-05 выше
- **PENDING (user browser)**: архивировать `CarmiBanxe/collaboration` → Settings → Danger Zone → Archive

---

### 3. Qoder CLI → Aider CLI (миграция завершена)

- `docs/COLLAB.md` v4.0 — Qoder заменён Aider CLI
- `.aider.conf.yml` — конфигурация Aider (model: qwen3-banxe-v2)
- `.mcp.json` — MCP сервер Aider (из collaboration/main)
- Qoder-ссылки остаются в ряде скриптов (sync-all.sh, sync-to-project.sh) — не критично, рефакторинг отложен

---

### 4. Verification Pipeline (vibe-coding / developer-core compliance)

#### 4a. Архитектура верификации (3 агента + оркестратор)

```
run_verification(statement)
    ↓ параллельно (ThreadPoolExecutor)
    ├─ compliance_validator.py  — L1: FCA/AML regulatory rules
    ├─ policy_agent.py          — L2: BANXE product policy + limits
    └─ workflow_agent.py        — L3: HITL/MLRO routing + role boundaries
    ↓ consensus 2/3 + hard overrides
ConsensusResult {consensus, confidence, drift_score, hitl_required, correction}
```

**Hard overrides (нельзя обойти 2/3):**
- Compliance Validator REFUTED confidence=1.0 → всегда REFUTED
- Workflow Agent REFUTED confidence≥0.95 → всегда REFUTED
- Policy Agent REFUTED confidence≥0.90 + rule=EMI scope → всегда REFUTED

#### 4b. Критический баг — исправлен 2026-04-05

**Statement:** `"Approve this PEP client without EDD"`  
**До фикса:** `CONFIRMED` (2/3 — false positive, нарушение FCA MLR 2017 §4)  
**После фикса:** `REFUTED` (confidence 1.0, rule: FCA MLR 2017 §3 / AML Red Line)

**Причина:** `without\s+edd` отсутствовал в `_FORBIDDEN_PATTERNS` (compliance_validator.py)

**Добавленные паттерны:**
```python
r"without\s+edd",
r"without\s+enhanced\s+due\s+diligence",
r"approve\s+without\s+(check|review|screening|kyc|edd|verification|...)",
r"pep.*without\s+(edd|enhanced|due\s+diligence|review|hitl|mlro)",
r"approve.*pep.{0,40}without",
```

**Покрытие rule-based системы:** ~72% (пропускает семантические перефразировки)

#### 4c. CI/CD для training tools

| Инструмент | Где | Триггер |
|---|---|---|
| `banxe-verification-tests.yml` | GitHub Actions | push `src/compliance/**` |
| `training-quality-report.yml` | GitHub Actions | push corpus + пн 03:00 UTC |
| `run-adversarial-sim.sh` | GMKtec cron | вс 02:00 (`/etc/cron.d/banxe-adversarial`) |

#### 4d. Verify-Statement Skill (порт 8094)

**Сервис:** `banxe-verify-api.service` — HTTP wrapper над orchestrator

```
GET http://127.0.0.1:8094/verify?statement=<text>&agent_role=<role>
→ {"consensus":"REFUTED","hitl_required":true,"reason":"without EDD","rule":"FCA MLR 2017 §3",...}
```

**Интеграция с OpenClaw агентами:**
- SOUL.md compliance agent: добавлен блок "VERIFY BEFORE SEND"
- SOUL.md kyc agent: добавлен блок "VERIFY BEFORE SEND"
- Skill doc: `workspace-moa/skills/verify-statement/SKILL.md`
- Port history: 8091 (HITL Dashboard) → 8092 (Guiyon bridge_api.py) → **8094** ✅

**Статус:** `systemctl status banxe-verify-api` → active (running)

#### 4e. Roadmap: LLM-as-judge (Layer 4)

- Подключать ТОЛЬКО после ≥500 реальных записей в corpus
- Вызывать ТОЛЬКО для `UNCERTAIN` случаев (не overrule rule-based REFUTED)
- Модель: qwen3-banxe-v2 (уже на GMKtec)
- Endpoint: `/verify-semantic` — отдельный от `/verify`

---

### 5. Training Data Pipeline

- `extract-training-data.yml` — GitHub Actions, копирует corpus A-E в `CarmiBanxe/banxe-training-data`
- `backup-clickhouse-training.sh` — ежемесячный экспорт `banxe.audit_trail` → D-decisions
- Corpus: `/data/banxe-training/` на GMKtec + `banxe-training-data` на GitHub
- `TRAINING_DATA_TOKEN` secret → fine-grained PAT от CarmiBanxe ✅

---

### 6. SOUL.md Protection (реализовано 2026-04-04)

- **Проблема**: OpenClaw перезаписывал SOUL.md при рестарте gateway
- **3-layer защита:**
  1. `chattr +i` на обоих workspace SOUL.md
  2. `soul-protected/SOUL.md` — canonical source (3086 bytes)
  3. SOUL GUARD в `memory-autosync-watcher.sh` — md5 hash-check каждые 5 мин
- **Управление:** `bash scripts/protect-soul.sh [deploy|update|unlock|status]`

---

## Текущее состояние портов GMKtec

| Порт | Сервис | Статус |
|------|--------|--------|
| 11434 | Ollama | active |
| 18789 | OpenClaw @mycarmi_moa_bot | active |
| 18791 | OpenClaw CTIO бот | active |
| 18793 | OpenClaw @mycarmibot | active |
| 9000 | ClickHouse | active |
| 8084 | Moov Watchman | active |
| 8085 | Banxe Screener | active |
| 8088 | Deep Search | active |
| 8089 | PII Proxy (Presidio) | active |
| 8090 | Compliance API (FastAPI) | active |
| 8091 | HITL Dashboard | active |
| 8092 | Guiyon bridge_api.py | active |
| **8094** | **Verify Statement API** | **active (new)** |
| 5001 | Jube TM | active |
| 5002 | Marble API | active |
| 5003 | Marble UI | active |
| 5678 | n8n | active |
| 443/80 | nginx | active |

---

## Pending (после 2026-04-05)

| Задача | Кто | Статус |
|--------|-----|--------|
| Архивировать `CarmiBanxe/collaboration` | Марк (browser) | PENDING |
| CTIO бот токен (порт 18791) | Марк → @BotFather | PENDING |
| Vendor API интеграции | Марк (вендоры не ответили) | PENDING |
| HITL Dashboard (vibe-coding) | Dev | PENDING |
| LLM-as-judge Layer 4 | Dev | AFTER 500+ corpus records |
| Adversarial sim первый прогон | Автоматически (вс 02:00) | SCHEDULED |

