# docs/MIROFISH-SCENARIOS.md — Banxe Collaboration Hub

**Project:** collaboration  
**Type:** Multi-Agent Banking Conflicts  
**MiroFish Role:** Conflict resolution & orchestration validation  
**Auto-trigger:** Multi-agent keywords (conflict, orchestration, consensus)

---

## Scenario Library

### 1. Multi-Agent Banking Conflicts (`multi-agent-conflict.yml`)

**Purpose:** Validate conflict resolution when multiple AI agents access same banking resources

**Triggers:** `conflict`, `concurrent access`, `race condition`, `agent collision`

**Scenario:** Three agents simultaneously modify the same customer's risk profile

**Agents:**
- **Compliance Agent:** Updates risk score after sanctions check
- **Fraud Agent:** Adjusts limits based on transaction patterns
- **UX Agent:** Requests temporary limit increase for VIP customer

**Conflict Matrix:**
```
Time T0: Compliance sets risk=0.8 (high), daily_limit=£5k
Time T0+1s: Fraud detects unusual pattern, sets limit=£1k
Time T0+2s: UX requests VIP override, limit=£50k
Time T0+3s: ??? (Which value wins?)
```

**Resolution Strategies Tested:**
1. **Last-write-wins:** ❌ Data loss (compliance flag overwritten)
2. **Priority-based:** ✅ Compliance > Fraud > UX (regulatory safe)
3. **Consensus:** ⚠️ Too slow (requires 2/3 agreement)
4. **Merge-conflict:** ⚠️ Human intervention needed

**Validation Criteria:**
- Compliance flags NEVER lost
- Audit trail shows all conflicting writes
- Resolution time < 100ms
- No deadlocks

---

### 2. Cross-Project Sync Conflicts (`sync-collision.yml`)

**Purpose:** Detect issues when sync-all.sh runs while projects are being edited

**Triggers:** `sync conflict`, `git merge`, `concurrent edit`

**Scenario:** Developer edits AGENTS.md in vibe-coding while sync-all.sh distributes from developer-core

**Agents:**
- **Developer:** Edits local AGENTS.md
- **Sync Script:** Overwrites with master copy
- **Git:** Detects merge conflict

**Flow:**
```
T0: Developer commits to vibe-coding/AGENTS.md
T1: developer-core/master updated
T2: sync-all.sh runs
T3: CONFLICT: Local changes vs upstream changes
```

**Expected Behavior:**
- Sync script checks for uncommitted changes first
- If detected: warn user, abort auto-commit
- Offer: stash → sync → reapply stash

---

### 3. MCP Server Resource Contention (`mcp-contention.yml`)

**Purpose:** Test behavior when multiple Qoder workers share MCP server

**Triggers:** `MCP overload`, `rate limit`, `server busy`

**Load Scenario:**
- 5 parallel Qoder workers
- Each makes 10 req/sec to MCP server
- Server capacity: 30 req/sec

**Failure Modes:**
- Queue overflow (requests dropped)
- Timeout cascade (all workers block)
- Partial completion (some succeed, some fail)

**Mitigation Validation:**
- Request queuing with backpressure
- Graceful degradation (reduce worker count)
- Fallback to local execution

---

### 4. Human-AI Handoff Collisions (`human-ai-collision.yml`)

**Purpose:** Validate smooth transitions between human and AI decision-making

**Triggers:** `handoff collision`, `dual control`, `human override`

**Scenario:** AI approves payment, human simultaneously rejects it

**Timeline:**
```
T0: AI receives £10k payment request
T0+500ms: AI scores risk=0.4 (APPROVED)
T0+600ms: Human reviewer opens dashboard
T0+700ms: Human sees "Pending Review" (stale UI)
T0+800ms: Human clicks REJECT
T0+900ms: AI sends APPROVE to core banking
T1: ??? (Which decision executes?)
```

**Resolution Requirements:**
- Immutable audit log (both decisions recorded)
- First-decision-wins OR human-always-wins policy
- User notified of final outcome within 2 seconds
- No double-processing

---

### 5. Distributed Transaction Orchestration (`distributed-txn.yml`)

**Purpose:** Validate multi-step banking transactions across services

**Triggers:** `distributed transaction`, `Saga pattern`, `rollback`

**Transaction Flow:**
```
Step 1: Debit source account (✓)
Step 2: FX conversion (✓)
Step 3: Credit destination account (✗ FAILS)
Step 4: ROLLBACK required
```

**Failure Points Simulated:**
- Network timeout at Step 3
- Insufficient liquidity at Step 3
- Sanctions match discovered mid-transaction

**Compensation Actions:**
- Reverse Step 2 (FX reversal at current rate — loss?)
- Reverse Step 1 (credit back to source)
- Notify compliance of failed transaction
- Flag account for manual review

**Success Criteria:**
- No orphaned transactions
- Customer balance correct within 5 seconds
- Audit trail complete (including rollback)

---

## MiroFish Integration

### Auto-Trigger Keywords

| Keyword | Scenario | Priority |
|---------|----------|----------|
| `conflict`, `collision` | multi-agent-conflict.yml | High |
| `sync conflict`, `merge` | sync-collision.yml | Medium |
| `MCP overload`, `rate limit` | mcp-contention.yml | High |
| `handoff collision`, `dual control` | human-ai-collision.yml | Critical |
| `distributed transaction`, `rollback` | distributed-txn.yml | Critical |

### Running Simulations

**Manual trigger:**
```bash
cd ~/collaboration
bash ../mirofish-engine/run.sh multi-agent-conflict
```

---

## Memory Updates

After each simulation:

```markdown
## 2026-04-03 — Multi-Agent Conflict Simulation

**Scenario:** multi-agent-conflict.yml  
**Result:** PASSED with priority-based resolution  
**Key Finding:** Compliance flags preserved, UX overrides blocked  
**Action:** Implement priority queue in src/orchestrator.py  
**Owner:** @bereg2022
```

---

**Source:** `~/developer/docs/MIROFISH-SCENARIOS-collaboration.md` (MASTER)  
**Synced:** N/A (project-specific)  
**Last Updated:** 2026-04-03
