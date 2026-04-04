# docs/MIROFISH-SCENARIOS.md — MiroFish Master Template Library

**Project:** banxe-mirofish  
**Type:** Tool / Scenario Template Repository  
**Role:** MASTER copy of all scenario templates for distribution  
**Auto-trigger:** Template creation, scenario authoring

---

## Purpose

This repository contains **MASTER COPIES** of all MiroFish scenarios used across the ecosystem:

- **Banking scenarios** → Synced to vibe-coding (primary BANXE runtime)
- **Legal scenarios** → Synced to guiyon, ss1
- **Infrastructure scenarios** → Used in developer-core

**DO NOT EDIT** project-specific scenarios here. Edit in the target project, then copy improvements back to this template library.

---

## Scenario Taxonomy

### Category 1: Banking & Compliance (Banxe)

| Scenario | File | Projects | Auto-trigger |
|----------|------|----------|--------------|
| HITL Handoff | `banking/hitl-handoff.yml` | vibe-coding, collaboration | `HITL`, `дублёр` |
| FCA Sandbox | `banking/pre-fca-sandbox.yml` | vibe-coding | `FCA`, `sandbox` |
| Fraud Detection | `banking/fraud-social-eng.yml` | vibe-coding, collaboration | `fraud`, `phishing` |
| Market Reaction | `banking/gtm-reaction.yml` | vibe-coding | `launch`, `adoption` |
| UX Validation | `banking/ux-validation.yml` | vibe-coding, collaboration | `drop-off`, `conversion` |
| Stress Test | `banking/fraud-stress-test.yml` | vibe-coding | `crash`, `crisis` |
| Multi-Agent Conflict | `banking/multi-agent-conflict.yml` | collaboration | `conflict`, `collision` |
| Distributed TXN | `banking/distributed-txn.yml` | vibe-coding | `rollback`, `Saga` |

### Category 2: Legal & Litigation (ГИЙОН/СС1)

| Scenario | File | Projects | Auto-trigger |
|----------|------|----------|--------------|
| Court Strategy | `legal/court-strategy.yml` | guiyon, ss1 | `суд`, `иск` |
| Judge Reaction | `legal/judge-reaction.yml` | guiyon | `судья`, `ruling` |
| Appeal Dynamics | `legal/appeal-dynamics.yml` | ss1 | `апелляция`, `appeal` |
| Counter-Argument | `legal/counter-argument.yml` | guiyon, ss1 | `контраргумент` |
| Witness Credibility | `legal/witness-credibility.yml` | guiyon | `witness`, `testimony` |
| Case Permutation | `legal/case-permutation.yml` | guiyon, ss1 | `strategy options` |
| Settlement Negotiation | `legal/settlement-negotiation.yml` | guiyon, ss1 | `settlement`, `mediation` |
| Procedural Default | `legal/procedural-default.yml` | guiyon, ss1 | `waiver`, `deadline` |
| Enforcement | `legal/enforcement-collection.yml` | ss1 | `collection`, `recovery` |

### Category 3: Infrastructure & Scaling (developer-core toolchain)

| Scenario | File | Projects | Auto-trigger |
|----------|------|----------|--------------|
| Scaling Stress | `infra/scaling-stress.yml` | developer-core | `100 to 10000` |
| Tenant Isolation | `infra/tenant-isolation.yml` | developer-core | `multi-tenant` |
| Orchestrator Failover | `infra/orchestrator-failover.yml` | developer-core | `failover`, `HA` |
| Worker Exhaustion | `infra/worker-exhaustion.yml` | developer-core | `queue full` |
| Cross-Region REPL | `infra/cross-region-repl.yml` | developer-core | `replication` |
| Sync Collision | `infra/sync-collision.yml` | developer-core, all | `sync conflict` |
| MCP Contention | `infra/mcp-contention.yml` | developer-core, all | `MCP overload` |
| Human-AI Collision | `infra/human-ai-collision.yml` | developer-core, all | `dual control` |

---

## Template Structure

Every scenario YAML file follows this schema:

```yaml
scenario:
  name: "hitl-handoff-simulation"
  version: "1.0"
  category: "banking"
  description: "Validate human-in-the-loop trust thresholds"
  
  triggers:
    keywords: ["HITL", "handoff", "дублёр", "trust threshold"]
    priority: "high"  # low | medium | high | critical
    
  agents:
    - role: "User"
      persona: "Initiates high-value payment"
      behavior: "impatient, expects instant approval"
      
    - role: "Compliance Bot"
      persona: "Automated AML/KYC check"
      behavior: "strict rule enforcement"
      
    - role: "Human Approver"
      persona: "Дублёр (backup decision maker)"
      behavior: "risk-averse, requests additional info"
      
    - role: "Fraud Detector"
      persona: "Pattern analysis engine"
      behavior: "flags anomalies, blocks suspicious"
  
  flow:
    - step: 1
      action: "User submits £75k payment"
      expected_result: "Payment queued for review"
      
    - step: 2
      action: "Compliance Bot runs sanctions check"
      expected_result: "Moov Watchman: CLEAR"
      
    - step: 3
      action: "Risk scoring engine calculates score"
      expected_result: "Score: 0.73 (threshold: 0.70)"
      
    - step: 4
      action: "HITL triggered (score > threshold)"
      expected_result: "Human Approver notified"
      
    - step: 5
      action: "Human Approver reviews + decides"
      branches:
        - APPROVE: "Continue to step 6"
        - REJECT: "Return to User with reason"
        - REQUEST_INFO: "Pause, await documentation"
      
    - step: 6
      action: "Payment executed via Moov API"
      expected_result: "Transaction ID returned"
      
    - step: 7
      action: "Audit trail written to ClickHouse"
      expected_result: "Immutable record created"
  
  validation:
    metrics:
      - name: "false_positive_rate"
        target: "< 5%"
        measurement: "rejected_payments / total_flagged"
        
      - name: "handoff_time"
        target: "< 2 minutes"
        measurement: "T(step_5) - T(step_4)"
        
      - name: "user_dropoff"
        target: "< 15%"
        measurement: "abandoned_at_HITL / total_HITL"
    
    pass_criteria:
      - "All metrics within target range"
      - "No compliance violations"
      - "Audit trail complete"
      
  outputs:
    - type: "metrics_dashboard"
      format: "JSON"
      destination: "./results/metrics.json"
      
    - type: "audit_log"
      format: "CSV"
      destination: "./results/audit_trail.csv"
      
    - type: "recommendation_report"
      format: "Markdown"
      destination: "./results/recommendations.md"
```

---

## Creating New Scenarios

### Step 1: Identify Validation Need

Ask: "What decision requires simulation before implementation?"

Examples:
- New banking feature needs FCA compliance validation
- UX change might increase drop-off rates
- Architecture change introduces single point of failure
- Legal strategy has unknown success probability

### Step 2: Define Agents & Roles

List all actors in the scenario:
- Human users (personas with specific behaviors)
- AI agents (automated systems with rules)
- External systems (APIs, databases, regulators)
- Adversaries (fraudsters, opposing counsel)

### Step 3: Map Decision Flow

Create step-by-step flowchart:
```
Start → Decision Point → Branch A/Branch B → Convergence → End
```

Include:
- Expected path (happy path)
- Alternative branches (what-if scenarios)
- Failure modes (system errors, timeouts)
- Rollback procedures (compensation actions)

### Step 4: Define Validation Metrics

For each metric:
- Name: Clear identifier
- Target: Quantitative goal (< 5%, > 99%, etc.)
- Measurement: How calculated
- Data source: Where measured (logs, DB, API response)

### Step 5: Write YAML Template

Use the structure above. Save to appropriate category folder:
- `banking/` for Banxe scenarios
- `legal/` for court/litigation scenarios
- `infra/` for scaling/orchestration scenarios

### Step 6: Test Simulation

Run locally:
```bash
cd ~/banxe-mirofish
python run_simulation.py banking/hitl-handoff.yml
```

Verify:
- All agents behave as specified
- Metrics calculated correctly
- Outputs generated in expected format

### Step 7: Distribute to Projects

Copy to target projects:
```bash
cp banking/hitl-handoff.yml ~/vibe-coding/docs/mirofish/scenarios/
cp banking/hitl-handoff.yml ~/collaboration/docs/mirofish/scenarios/
```

Update PROJECT-REGISTRY.csv if new scenario type added.

---

## Running Simulations

### Manual Execution

```bash
# From any project directory
cd ~/vibe-coding
bash ../mirofish-engine/run.sh hitl-handoff

# Or direct Python invocation
python ~/mirofish-engine/app.py --scenario banking/hitl-handoff.yml
```

### Auto-Trigger (Claude-Detected)

When Claude sees trigger keywords in conversation:

```
User: "Need to implement HITL handoff for large payments"
Claude: [Detects keyword "HITL"]
        "Запускаю MiroFish симуляцию hitl-handoff.yml..."
        [Simulation executes in background]
        "Результаты показывают 12% false positive rate.
         Рекомендую снизить порог с 0.70 до 0.65."
```

### Batch Testing

Run all scenarios to validate infrastructure changes:

```bash
cd ~/banxe-mirofish
python run_all_scenarios.py --category banking --output results/banking-batch.json
```

---

## Version Control

Scenario templates are versioned:

```yaml
scenario:
  version: "1.0"  # MAJOR.MINOR
  changelog:
    - version: "1.0"
      date: "2026-04-03"
      changes: ["Initial release"]
    - version: "1.1"
      date: "2026-04-15"
      changes: ["Added fraud detector agent", "Tuned risk threshold"]
```

**Versioning rules:**
- MINOR bump: Add agents, refine metrics, fix bugs
- MAJOR bump: Change flow structure, add/remove steps, change validation criteria

---

## Integration with MEMORY.md

After each simulation run, update project's MEMORY.md:

```markdown
## 2026-04-03 — HITL Handoff Simulation

**Scenario:** hitl-handoff.yml v1.0  
**Project:** vibe-coding  
**Result:** PASSED with recommendations  
**Metrics:**
- False positive rate: 12% (target: <5%) ❌
- Handoff time: 1.8 min (target: <2 min) ✅
- Drop-off rate: 18% (target: <15%) ❌

**Key Findings:**
1. Risk threshold 0.70 too aggressive
2. False positives concentrated in crypto-to-fiat flows
3. Users abandon when asked for additional documentation

**Recommendations:**
1. Lower threshold to 0.65
2. Add progressive disclosure (request docs only for score >0.80)
3. Improve UX messaging at HITL stage

**Next Steps:**
- [ ] Implement threshold change in src/compliance/api.py
- [ ] A/B test new UX copy
- [ ] Re-run simulation Q2 2026

**Owner:** @bereg2022
```

---

## Scenario Authoring Best Practices

### DO:
- Start with clear validation question ("Does X work under Y conditions?")
- Define measurable success criteria (quantitative targets)
- Include failure modes and rollback paths
- Use realistic personas (based on user research)
- Keep scenarios focused (one decision per scenario)
- Document assumptions explicitly

### DON'T:
- Create mega-scenarios (20+ steps, 10+ agents)
- Mix validation types (banking + legal in same scenario)
- Hard-code values that should be parameters
- Forget to update MEMORY.md after running
- Assume scenario is "done" (iterate based on learnings)

---

## Troubleshooting

### Problem: Simulation hangs indefinitely

**Diagnosis:**
- Check agent deadlock (circular wait condition)
- Verify external API mocks are responding
- Increase timeout in config.yml

**Fix:**
```yaml
simulation:
  timeout_seconds: 300  # Default: 180
  max_steps: 50         # Prevent infinite loops
```

### Problem: Metrics not calculated

**Diagnosis:**
- Verify metric names match flow step outputs
- Check data source paths (logs, DB tables)
- Ensure agents emit required telemetry

**Fix:**
```yaml
validation:
  metrics:
    - name: "handoff_time"
      data_source: "step_outputs.step_4.timestamp"  # Verify path exists
```

### Problem: Auto-trigger not working

**Diagnosis:**
- Keywords not registered in context.md
- MiroFish MCP server not loaded
- Trigger priority too low

**Fix:**
```markdown
# In .qoder/context.md
Auto-trigger keywords:
- `HITL`, `handoff` → hitl-handoff.yml (priority: high)
```

---

**Source:** `~/developer/docs/MIROFISH-SCENARIOS-banxe-mirofish.md` (MASTER TEMPLATE LIBRARY)  
**Last Updated:** 2026-04-03  
**Maintainer:** @bereg2022
