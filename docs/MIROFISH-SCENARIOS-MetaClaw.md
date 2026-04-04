# docs/MIROFISH-SCENARIOS-MetaClaw.md — developer-core: Infrastructure & Orchestration Scenarios

**Layer:** developer-core toolchain
**Type:** Infrastructure & Orchestration
**MiroFish Role:** Load testing, scaling validation, failover simulation
**Auto-trigger:** Scale keywords (100→10000 users, orchestration, failover, load, multi-tenant)

> **Note:** These scenarios belong to the **developer-core** layer — they test infrastructure
> patterns applicable to all projects. They are not BANXE-specific. After delegation,
> each project inherits these patterns as part of its runtime operational layer.

---

## Scenario Library

### 1. Scaling 100 → 10,000 Users (`scaling-stress.yml`)

**Purpose:** Validate infrastructure handles exponential user growth

**Triggers:** `scaling`, `100 to 10000`, `load test`, `capacity planning`

**Growth Stages:**
```
Stage 1: 100 users    → Single server, SQLite adequate
Stage 2: 500 users    → Load balancer + 2 workers
Stage 3: 2,000 users  → Redis cache required
Stage 4: 5,000 users  → Database read replicas
Stage 5: 10,000 users → Sharding + CDN + auto-scaling
```

**Bottleneck Detection:**
- **Database connections:** Pool exhaustion at ~800 concurrent users
- **Redis memory:** Session storage grows 50MB per 1,000 users
- **API rate limits:** External services throttle at 100 req/sec
- **WebSocket connections:** File descriptor limits at ~4,000 simultaneous

**Validation Metrics:**
- P95 latency < 500ms at all stages
- Error rate < 0.1% during scaling transitions
- Auto-scaling trigger time < 30 seconds
- Zero data loss during scale-up/down

---

### 2. Multi-Tenant Orchestration (`tenant-isolation.yml`)

**Purpose:** Ensure tenant data isolation under load

**Triggers:** `multi-tenant`, `isolation`, `data leakage`, `tenant boundary`

**Scenario:** 50 tenants, each with 200 concurrent users

**Agents:**
- **Tenant A:** High-security workload (e.g. banking)
- **Tenant B:** Low-priority dev environment
- **Tenant C:** Mission-critical production
- **Noisy Neighbor:** Tenant D generates 80% of load

**Isolation Tests:**
1. CPU throttling: noisy neighbor can't starve others
2. Memory limits: hard cgroups enforcement
3. Database row-level security: tenants cannot cross-query
4. Cache key namespacing: keys prefixed with tenant_id

**Failure Mode:**
```
Bug: Cache key = "user_session_12345" (no tenant prefix)
Result: Tenant A user authenticated as Tenant B user
Severity: CRITICAL
Fix: Cache key = "tenant_a:user_session_12345"
```

---

### 3. Orchestrator Failover (`orchestrator-failover.yml`)

**Purpose:** Validate high availability when orchestrator crashes

**Triggers:** `failover`, `HA`, `orchestrator crash`, `leader election`

**Failure Scenarios:**
1. Leader crash: primary orchestrator dies mid-workflow
2. Split-brain: two leaders elected simultaneously
3. Zombie leader: old leader doesn't step down
4. Cascading failure: orchestrator + worker both crash

**Recovery Timeline:**
```
T0:     Leader orchestrator crashes
T0+5s:  Health check detects failure
T0+10s: Follower initiates leader election
T0+15s: New leader elected (Raft consensus)
T0+20s: In-flight workflows resumed from checkpoint
T0+30s: Full recovery, users unaware
```

**Validation Criteria:**
- RTO < 30 seconds, RPO = 0 (no workflow loss)
- Automatic failover (no human intervention)
- Split-brain prevention (quorum-based election)

---

### 4. Worker Pool Exhaustion (`worker-exhaustion.yml`)

**Purpose:** System behavior when all workers are busy

**Triggers:** `worker exhaustion`, `queue full`, `backpressure`

**Load Pattern:**
```
Normal:     10 workers, 5 tasks/min,   queue depth = 0
Spike:      10 workers, 100 tasks/min, queue depth = 90
Saturation: Queue full (max 500), new tasks rejected
```

**Backpressure Strategies:**
1. Reject immediately: HTTP 503 "Service Unavailable"
2. Queue with timeout: accept, fail if not started in 60s
3. Shed load: drop low-priority tasks first
4. Auto-scale: spin up new workers (cold start: 45s)

---

### 5. Cross-Region Replication (`cross-region-repl.yml`)

**Purpose:** Validate multi-region deployment consistency

**Triggers:** `cross-region`, `replication`, `geo-distribution`, `latency`

**Topology:**
```
Region 1: eu-west-2 (London)        — Primary
Region 2: us-east-1 (NYC)           — Read replica
Region 3: ap-southeast-1 (Singapore) — Read replica
```

**Consistency Models:**
- Banking transactions → Strong consistency (correctness > speed)
- Dashboard analytics → Eventual consistency (speed acceptable)
- User profile updates → Read-your-writes (UX critical)

---

## MiroFish Integration

### Auto-Trigger Keywords

| Keyword | Scenario | Priority |
|---------|----------|----------|
| `scaling`, `100 to 10000` | scaling-stress.yml | High |
| `multi-tenant`, `isolation` | tenant-isolation.yml | Critical |
| `failover`, `HA`, `leader` | orchestrator-failover.yml | Critical |
| `worker exhaustion`, `queue full` | worker-exhaustion.yml | High |
| `cross-region`, `replication` | cross-region-repl.yml | Medium |

### Running Simulations

**From developer-core:**
```bash
cd ~/developer-core
bash mirofish/run-simulation.sh scaling-stress
```

**After delegation — from any project:**
```bash
cd ~/vibe-coding   # or guiyon, ss1, etc.
bash ../developer-core/mirofish/run-simulation.sh scaling-stress
```

---

## Delegation Notes

These infrastructure scenarios are **developer-core master scenarios**. When a project needs
project-specific variants (e.g. BANXE needs FCA-compliant failover), it creates a
project-specific scenario file that extends the master pattern:

```
developer-core/mirofish/scenarios/orchestrator-failover.yml  ← master
vibe-coding/mirofish/scenarios/banxe-fca-failover.yml        ← BANXE extension
```

---

**Source:** `developer-core/docs/MIROFISH-SCENARIOS-MetaClaw.md` (MASTER — developer-core layer)
**Layer:** developer-core toolchain (not project-specific)
**Last Updated:** 2026-04-05
