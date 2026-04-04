# docs/MIROFISH-SCENARIOS.md — Developer Core MASTER Index

**Project:** developer-core  
**Type:** Infrastructure / Source of Truth  
**Role:** Master index linking to all project-specific scenarios  
**Auto-trigger:** Infrastructure validation, sync coordination

---

## Overview

This file serves as the **central index** for all MiroFish scenarios across the ecosystem. 

**Project-specific scenario files:**
- `MIROFISH-SCENARIOS-vibe-coding.md` → Banking/FCA scenarios
- `MIROFISH-SCENARIOS-collaboration.md` → Multi-agent conflicts
- `MIROFISH-SCENARIOS-MetaClaw.md` → Infrastructure & orchestration (developer-core layer)
- `MIROFISH-SCENARIOS-guiyon.md` → Court strategy (legal)
- `MIROFISH-SCENARIOS-ss1.md` → Appeal dynamics (legal)
- `MIROFISH-SCENARIOS-banxe-mirofish.md` → Master template library

---

## Scenario Matrix

### Banking & Compliance (BANXE Projects)

| Scenario | vibe-coding | collaboration | Auto-triggers |
|----------|:-----------:|:-------------:|:--------:|---------------|
| HITL Handoff | ✅ | ✅ | `HITL`, `дублёр` |
| FCA Sandbox | ✅ | ⚪ | `FCA`, `sandbox` |
| Fraud Detection | ✅ | ✅ | `fraud`, `phishing` |
| Market Reaction | ✅ | ⚪ | `launch`, `adoption` |
| UX Validation | ✅ | ✅ | `drop-off`, `conversion` |
| Stress Test | ✅ | ⚪ | `crash`, `crisis` |
| Multi-Agent Conflict | ⚪ | ✅ | `conflict`, `collision` |
| Distributed TXN | ⚪ | ✅ | `rollback`, `Saga` |

**Legend:** ✅ Used | ⚪ Not applicable

### Legal & Litigation (ГИЙОН/СС1 Projects)

| Scenario | guiyon | ss1 | Auto-triggers |
|----------|:------:|:---:|---------------|
| Court Strategy | ✅ | ✅ | `суд`, `иск` |
| Judge Reaction | ✅ | ⚪ | `судья`, `ruling` |
| Appeal Dynamics | ⚪ | ✅ | `апелляция`, `appeal` |
| Counter-Argument | ✅ | ✅ | `контраргумент` |
| Witness Credibility | ✅ | ⚪ | `witness`, `testimony` |
| Case Permutation | ✅ | ✅ | `strategy options` |
| Settlement Negotiation | ✅ | ✅ | `settlement`, `mediation` |
| Procedural Default | ✅ | ✅ | `waiver`, `deadline` |
| Enforcement | ⚪ | ✅ | `collection`, `recovery` |

### Infrastructure & Scaling (developer-core toolchain)

| Scenario | developer-core | All Projects* | Auto-triggers |
|----------|:--------:|:--------------:|:-------------:|---------------|
| Scaling Stress | ✅ | ⚪ | `100 to 10000` |
| Tenant Isolation | ✅ | ⚪ | `multi-tenant` |
| Orchestrator Failover | ✅ | ⚪ | `failover`, `HA` |
| Worker Exhaustion | ✅ | ⚪ | `queue full` |
| Cross-Region REPL | ✅ | ⚪ | `replication` |
| Sync Collision | ⚪ | ✅ | ✅ | `sync conflict` |
| MCP Contention | ⚪ | ✅ | ✅ | `MCP overload` |
| Human-AI Collision | ⚪ | ✅ | ✅ | `dual control` |

* Infra scenarios run via developer-core toolchain; inherited by all projects after delegation

---

## Infrastructure Validation Scenarios

These scenarios run in developer-core to validate sync infrastructure:

### 1. Sync Collision Test (`infra/sync-collision.yml`)

**Purpose:** Validate sync-all.sh behavior when projects have uncommitted changes

**Flow:**
```
T0: Developer edits vibe-coding/AGENTS.md
T1: developer-core/master updated
T2: sync-all.sh triggered
T3: Script detects uncommitted changes
T4: User warned, sync aborted (or stash applied)
```

**Expected:** No data loss, user notified

---

### 2. MCP Contention Test (`infra/mcp-contention.yml`)

**Purpose:** Validate MCP server handles concurrent Qoder workers

**Load:**
- 5 parallel workers
- 10 req/sec each
- Server capacity: 30 req/sec

**Expected:** Graceful queuing, no dropped requests

---

### 3. Human-AI Collision Test (`infra/human-ai-collision.yml`)

**Purpose:** Validate dual-control decision making

**Scenario:** Human and AI make opposite decisions simultaneously

**Expected:** Clear winner policy (human-always-wins or first-decision-wins), audit trail shows both

---

## Trigger Keyword Index

**Full list of auto-trigger keywords across all projects:**

### Banking Keywords
| Keyword | Scenario | Priority |
|---------|----------|----------|
| `HITL`, `handoff`, `дублёр` | hitl-handoff | High |
| `FCA`, `sandbox`, `compliance` | pre-fca-sandbox | Critical |
| `fraud`, `phishing`, `social engineering` | fraud-social-eng | High |
| `launch`, `market reaction`, `adoption` | gtm-reaction | Medium |
| `drop-off`, `conversion`, `UX validation` | ux-validation | Medium |
| `stress test`, `crash`, `crisis` | fraud-stress-test | High |
| `conflict`, `collision`, `concurrent` | multi-agent-conflict | High |
| `distributed transaction`, `rollback` | distributed-txn | Critical |

### Legal Keywords
| Keyword | Scenario | Priority |
|---------|----------|----------|
| `court`, `суд`, `иск`, `litigation` | court-strategy | High |
| `judge`, `судья`, `ruling` | judge-reaction | Medium |
| `appeal`, `апелляция`, `reversal` | appeal-dynamics | High |
| `counter-argument`, `контраргумент`, `weakness` | counter-argument | Critical |
| `witness`, `testimony`, `cross-examination` | witness-credibility | Medium |
| `settlement`, `mediation`, `negotiation` | settlement-negotiation | High |
| `procedural default`, `waiver`, `deadline` | procedural-default | Critical |
| `enforcement`, `collection`, `recovery` | enforcement-collection | Medium |

### Infrastructure Keywords
| Keyword | Scenario | Priority |
|---------|----------|----------|
| `scaling`, `100 to 10000`, `load test` | scaling-stress | High |
| `multi-tenant`, `isolation` | tenant-isolation | Critical |
| `failover`, `HA`, `leader election` | orchestrator-failover | Critical |
| `worker exhaustion`, `queue full` | worker-exhaustion | High |
| `cross-region`, `replication`, `latency` | cross-region-repl | Medium |
| `sync conflict`, `merge conflict` | sync-collision | Medium |
| `MCP overload`, `rate limit` | mcp-contention | High |
| `dual control`, `handoff collision` | human-ai-collision | Critical |

---

## Running Simulations from developer-core

### Direct Execution

```bash
cd ~/developer
python ~/mirofish-engine/app.py --scenario banking/hitl-handoff.yml
```

### Via Project Symlink

```bash
cd ~/developer
bash ../vibe-coding/docs/mirofish/run.sh hitl-handoff
```

### Batch Validation (All Scenarios)

```bash
cd ~/developer
python ~/mirofish-engine/batch_run.py \
  --categories banking,legal,infra \
  --output results/full-batch-$(date +%Y%m%d).json
```

---

## Memory Updates

After running infrastructure validation:

```markdown
## 2026-04-03 — Sync Collision Simulation

**Scenario:** infra/sync-collision.yml  
**Result:** PASSED  
**Key Finding:** Script correctly detects uncommitted changes, aborts safely  
**Action:** Add --force flag to override (use with caution)  
**Owner:** @bereg2022
```

---

## Scenario Development Workflow

1. **Identify need** (new feature requires validation)
2. **Create in banxe-mirofish** (master template library)
3. **Test locally** (run simulation, verify metrics)
4. **Copy to target projects** (per matrix above)
5. **Update this index** (add to matrix, add triggers)
6. **Update context.md** (add auto-trigger keywords)
7. **Run batch validation** (ensure no regressions)

---

**Source:** `~/developer/docs/MIROFISH-SCENARIOS.md` (MASTER INDEX)  
**Last Updated:** 2026-04-03  
**Maintainer:** @bereg2022
