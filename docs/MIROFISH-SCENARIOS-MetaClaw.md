# docs/MIROFISH-SCENARIOS.md — MetaClaw Orchestration Platform

**Project:** MetaClaw  
**Type:** Orchestration & Scaling  
**MiroFish Role:** Load testing & scaling validation  
**Auto-trigger:** Scale keywords (100→10000 users, orchestration, load)

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
- **API rate limits:** External services (Moov, ClickHouse) throttle at 100 req/sec
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
- **Tenant A (Banxe):** High-security banking workload
- **Tenant B (Startup):** Low-priority dev environment
- **Tenant C (Enterprise):** Mission-critical production
- **Noisy Neighbor:** Tenant D generates 80% of load

**Isolation Tests:**
1. **CPU throttling:** Noisy neighbor can't starve others
2. **Memory limits:** Hard cgroups enforcement
3. **Database row-level security:** Tenant A can't query Tenant B data
4. **Cache key namespacing:** Redis keys prefixed with tenant_id

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
1. **Leader crash:** Primary orchestrator dies mid-workflow
2. **Split-brain:** Two leaders elected simultaneously
3. **Zombie leader:** Old leader doesn't step down
4. **Cascading failure:** Orchestrator + worker both crash

**Recovery Timeline:**
```
T0: Leader orchestrator crashes
T0+5s: Health check detects failure
T0+10s: Follower initiates leader election
T0+15s: New leader elected (Raft consensus)
T0+20s: In-flight workflows resumed from checkpoint
T0+30s: Full recovery, users unaware
```

**Validation Criteria:**
- RTO (Recovery Time Objective) < 30 seconds
- RPO (Recovery Point Objective) = 0 (no workflow loss)
- Automatic failover (no human intervention)
- Split-brain prevention (quorum-based election)

---

### 4. Worker Pool Exhaustion (`worker-exhaustion.yml`)

**Purpose:** System behavior when all workers are busy

**Triggers:** `worker exhaustion`, `queue full`, `backpressure`

**Load Pattern:**
```
Normal: 10 workers, 5 tasks/min, queue depth = 0
Spike: 10 workers, 100 tasks/min, queue depth = 90
Saturation: Queue full (max 500), new tasks rejected
```

**Backpressure Strategies:**
1. **Reject immediately:** HTTP 503 "Service Unavailable"
2. **Queue with timeout:** Accept, fail if not started in 60s
3. **Shed load:** Drop low-priority tasks first
4. **Auto-scale:** Spin up new workers (cold start: 45s)

**User Experience:**
- Graceful error message: "High demand, retry in 30s"
- Retry-after header for programmatic clients
- Priority queue for premium tenants

---

### 5. Cross-Region Replication (`cross-region-repl.yml`)

**Purpose:** Validate multi-region deployment consistency

**Triggers:** `cross-region`, `replication`, `geo-distribution`, `latency`

**Topology:**
```
Region 1: eu-west-2 (London) — Primary
Region 2: us-east-1 (NYC) — Read replica
Region 3: ap-southeast-1 (Singapore) — Read replica
```

**Replication Lag Scenarios:**
- **Normal:** 50-200ms lag (acceptable)
- **Network congestion:** 2-5 second lag (degraded)
- **Partition:** 30+ second lag (failover candidate)

**Consistency Models Tested:**
1. **Strong consistency:** Write to primary, wait for replication (slow)
2. **Eventual consistency:** Return immediately, replicate async (fast, stale reads possible)
3. **Read-your-writes:** Route user to primary after write (complex routing)

**Trade-off Analysis:**
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

**Manual trigger:**
```bash
cd ~/MetaClaw
bash ../mirofish-engine/run.sh scaling-stress
```

---

## Memory Updates

After each simulation:

```markdown
## 2026-04-03 — Scaling Stress Test

**Scenario:** scaling-stress.yml (100 → 10,000 users)  
**Result:** PASSED with bottlenecks identified  
**Key Finding:** Redis memory leak at 8,000+ users  
**Action:** Implement LRU eviction policy in cache layer  
**Owner:** @bereg2022
```

---

**Source:** `~/developer/docs/MIROFISH-SCENARIOS-MetaClaw.md` (MASTER)  
**Synced:** N/A (project-specific)  
**Last Updated:** 2026-04-03
