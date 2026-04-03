# MIROFISH-INTEGRATION.md — Third Partner Integration Plan

**Pattern:** Claude Code + Qoder CLI + MiroFish automatic collaboration via MCP  
**Repository:** `~/developer/` (and all downstream projects)  
**Version:** 1.0 | 2026-04-03  
**Status:** PROPOSED

---

## Executive Summary

MiroFish is integrated as a **specialized simulation partner** following the same algorithm as Claude Code + Qoder CLI synergy. Unlike Qoder (executor), MiroFish serves as a **validation and stress-testing engine** for pre-design decisions.

### Role Definition

| Partner | Role | Scope | Trigger |
|---------|------|-------|---------|
| **Claude Code** | Architect & Coordinator | Design, review, orchestration | All tasks |
| **Qoder CLI** | Executor | Implementation, edits, tests | Implementation tasks |
| **MiroFish** | Simulator & Validator | Behavioral simulation, stress-testing | Validation-critical tasks |

### When MiroFish Activates Automatically

MiroFish joins the workflow when:
- Designing human-in-the-loop (HITL) handoff points
- Testing compliance policies before FCA Sandbox submission
- Validating UX flows before implementation
- Stress-testing fraud detection scenarios
- Simulating market reaction to product launches

---

## Architecture: Three-Partner Synergy

```
┌─────────────────────────────────────────────────────────────┐
│                      USER TERMINAL                           │
│                                                               │
│  cd ~/project                                                 │
│  claude                                                       │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │           Claude Code (coordinator)                     │  │
│  │   • Reads project context                               │  │
│  │   • Designs architecture                                │  │
│  │   • Decides when simulation needed                      │  │
│  │   • Reviews simulation results                          │  │
│  │   • Presents unified outcome                            │  │
│  └────────────────────────────────────────────────────────┘  │
│              ↓ MCP call                    ↓ MCP call         │
│  ┌──────────────────────────┐   ┌──────────────────────────┐ │
│  │   Qoder CLI mcp-server   │   │   MiroFish MCP server    │ │
│  │   (stdio executor)       │   │   (stdio simulator)      │ │
│  │   • Implements            │   │   • Simulates users     │ │
│  │   • Edits files          │   │   • Models behavior      │ │
│  │   • Runs tests           │   │   • Reports patterns     │ │
│  │   • Fixes bugs           │   │   • Stress-tests         │ │
│  └──────────────────────────┘   └──────────────────────────┘ │
│              ↓                             ↓                  │
│  Repository (isolated scope)    Simulation Graph (Neo4j)      │
└───────────────────────────────────────────────────────────────┘
```

---

## Configuration: MCP Setup for MiroFish

### Global MCP configuration (~/.claude/settings.json)

```json
{
  "skipDangerousModePermissionPrompt": true,
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
        "MIROFISH_MODEL": "qwen2.5:32b",
        "MIROFISH_EMBEDDING": "nomic-embed-text"
      }
    }
  }
}
```

### Why stdio for both partners

- **Lowest latency**: Direct process communication, no network overhead
- **Automatic lifecycle**: Partners start/stop with Claude session
- **No coordination overhead**: User doesn't manage separate processes

---

## MiroFish Installation & Setup

### Prerequisites

MiroFish requires:
- Docker Compose (for Neo4j + Ollama containers)
- 32GB+ RAM recommended for large simulations (200+ agents)
- Local LLM (Ollama with qwen2.5:32b or equivalent)

### Installation script (TO BE CREATED)

```bash
# ~/developer/scripts/install-mirofish.sh
#!/bin/bash

set -e

echo "Installing MiroFish simulation engine..."

# Clone MiroFish Offline
git clone https://github.com/nikmcfly/MiroFish-Offline.git ~/mirofish-engine
cd ~/mirofish-engine

# Configure environment
cp .env.example .env
cat >> .env << EOF
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL_NAME=qwen2.5:32b
NEO4J_URI=bolt://localhost:7687
EMBEDDING_MODEL=nomic-embed-text
EOF

# Start services
docker compose up -d

# Pull models
ollama pull qwen2.5:32b
ollama pull nomic-embed-text

echo "MiroFish installed successfully!"
echo "Access UI: http://localhost:3000"
```

### Verification

```bash
# Check services running
docker compose ps
# Should show: neo4j, ollama, mirofish-app

# Test API
curl http://localhost:3000/api/health
# Expected: {"status": "ok", "agents": 0, "simulations": 0}
```

---

## Instruction Hierarchy: MiroFish Scope

### Priority order (unchanged from COLLAB.md v3.0)

1. **Explicit user instruction** (highest authority)
2. **Repository-level contracts**:
   - `CLAUDE.md` — project context
   - `.qoder/context.md` — Qoder execution contract
   - `AGENTS.md` — agent instructions
   - `COLLAB.md` — collaboration pattern
   - `MIROFISH.md` — **NEW: MiroFish simulation contract**
   - `COMPLIANCE_ARCH.md` — compliance invariants
3. **Global defaults**: `~/.claude/CLAUDE.md`

### MiroFish-specific instruction layer

New file: `.mirofish/config.yml` (per-project)

```yaml
# MiroFish simulation configuration template
# Source: ~/developer/mirofish/config-template.yml
# Synced: YYYY-MM-DD

simulation:
  defaultAgents: 200
  defaultRounds: 30
  maxConcurrentAgents: 500
  
llm:
  baseUrl: http://localhost:11434/v1
  model: qwen2.5:32b
  embeddingModel: nomic-embed-text
  temperature: 0.7
  maxTokens: 2048

graph:
  uri: bolt://localhost:7687
  user: neo4j
  password: ${NEO4J_PASSWORD:-changeme}

output:
  format: json
  saveTo: docs/simulations/
  includeRawData: true
  
triggers:
  # Auto-trigger simulation for these scenarios
  autoTrigger:
    - "human-in-the-loop"
    - "handoff"
    - "fraud"
    - "compliance"
    - "UX validation"
    - "stress-test"
```

---

## The Agentic Pipeline: AutoResearchClaw → MiroFish → Claude Code

This three-stage pipeline validates designs before implementation:

```
┌─────────────────┐
│ STAGE 1:        │
│ AutoResearchClaw│
│                 │
│ Input: Hypothesis               │
│ Output: Research document       │
│ Sources: Academic papers,       │
│          FCA guidelines,        │
│          industry reports       │
└────────┬────────┘
         │
         ↓ Research document (structured)
┌─────────────────┐
│ STAGE 2:        │
│ MiroFish        │
│                 │
│ Input: Research brief           │
│ Output: Simulation report       │
│ Agents: 200-500 personas        │
│ Rounds: 20-50 iterations        │
└────────┬────────┘
         │
         ↓ Behavioral patterns + validated design
┌─────────────────┐
│ STAGE 3:        │
│ Claude Code +   │
│ Qoder CLI       │
│                 │
│ Input: Validated brief          │
│ Output: Production artifact     │
│ (component, API, test, etc.)    │
└─────────────────┘
```

### Example: HITL Handoff Design

**Stage 1 — AutoResearchClaw:**
```
Query: "Research human-in-the-loop requirements for AI banking agents.
        Focus on BCG 2026 agentic banking report, FCA approval gate
        requirements, and user trust thresholds."

Output: research/hitl-banking-requirements.md
```

**Stage 2 — MiroFish:**
```
Simulation: "Generate 300 UK SME banking users. Simulate their
             reaction to AI agent autonomously blocking suspicious
             transactions. Measure trust decay by user segment.
             Identify optimal handoff triggers to human doppelgänger."

Output: simulations/hitl-handoff-trust-study.json
```

**Stage 3 — Claude Code + Qoder CLI:**
```
Task: "Implement HITL gateway component with handoff triggers
       identified by MiroFish simulation. Write unit tests.
       Update COMPLIANCE_ARCH.md if thresholds changed."

Output: src/compliance/hitl_gateway.py + tests
```

---

## Seven High-Value Applications: Detailed Scenarios

### 1. Human-in-the-Loop (Дублёр) Architecture Simulation

**Purpose:** Identify when users lose trust in AI agents and when human approval gates are mandatory (BCG requirement).

**MiroFish Query Template:**
```yaml
scenario: hitl_trust_handoff
agents: 300
demographics:
  - UK_SME_banking: 40%
  - retail_crypto_users: 35%
  - traditional_bankers: 25%
  
injection: |
  AI agent blocks £50,000 transaction due to fraud suspicion.
  No prior warning given. Decision made in <100ms.
  
measure:
  - trust_decay_by_segment
  - churn_probability
  - handoff_acceptance_rate
  - social_amplification_factor
  
rounds: 40
```

**Expected Output:**
- Trust threshold map by user segment
- Optimal handoff trigger points (composite score ≥ X → human review)
- Communication templates that minimize trust decay

**Integration Point:** Before implementing `src/compliance/hitl_gateway.py`

---

### 2. Pre-FCA-Sandbox Compliance Simulation

**Purpose:** Test draft policies before FCA Regulatory Sandbox submission.

**MiroFish Query Template:**
```yaml
scenario: pre_fca_sandbox
agents: 250
demographics:
  - compliance_officers: 20%
  - fintech_lawyers: 15%
  - sme_customers: 40%
  - retail_users: 25%

seed_documents:
  - draft_AML_policy_v0.3.pdf
  - customer_disclosure_template.md
  - terms_of_service_draft.docx

injection: |
  FCA examiner reviews your sandbox application.
  Different agent types interpret disclosure language.
  
measure:
  - misunderstanding_rate
  - regulatory_risk_flags
  - ambiguous_clause_detection
  - segment_specific_confusion
  
rounds: 30
```

**Expected Output:**
- Ambiguous clauses requiring rewrite
- Segment-specific interpretation gaps
- Regulatory risk heat map before submission

**Integration Point:** Before FCA Regulatory Sandbox application

---

### 3. Fraud Pattern Detection via Social Simulation

**Purpose:** Model coordinated social attacks and social engineering that historical data doesn't capture.

**MiroFish Query Template:**
```yaml
scenario: fraud_social_engineering
agents: 400
malicious_actors: 8%  # 32 fraud actors

fraud_patterns:
  - coordinated_complaint_flood: 15 agents
  - social_engineering_support: 10 agents
  - synthetic_identity_cluster: 7 agents

measure:
  - attack_success_rate
  - detection_latency
  - false_positive_spillover
  - community_trust_collapse
  
rounds: 50
```

**Expected Output:**
- New fraud patterns not in historical data
- Early warning indicators for coordinated attacks
- False positive spillover analysis

**Integration Point:** Complement to statistical fraud detection in `src/fraud/detection.py`

---

### 4. Go-to-Market Reaction Simulation

**Purpose:** Media, regulator, skeptic reactions to "AI-agent bank" concept before real launch.

**MiroFish Query Template:**
```yaml
scenario: gtm_market_reaction
agents: 350
demographics:
  - fintech_journalists: 15%
  - early_adopters: 25%
  - skeptical_traditional: 20%
  - fca_regulators: 10%
  - potential_users: 30%

seed_documents:
  - product_launch_press_release.md
  - competitor_analysis_revolut_monzo.md
  - unique_value_proposition.md

injection: |
  "First AI-agent bank with human doppelgänger oversight"
  messaging goes viral on Twitter/LinkedIn.
  
measure:
  - narrative_dominance
  - objection_patterns
  - messaging_resonance_by_segment
  - regulator_concern_flags
  
rounds: 35
```

**Expected Output:**
- Dominant narratives (positive/negative)
- Systematic objections to address pre-launch
- Regulator concern flags requiring proactive engagement

**Integration Point:** 3 months before public launch

---

### 5. UX Validation Pipeline

**Purpose:** Three-stage validation before implementation.

**Full Pipeline Example:**

```yaml
# Stage 1: AutoResearchClaw
query: |
  Research crypto exchange drop-off points during KYC onboarding.
  Focus on: biometric friction, document rejection rates,
  completion time by demographic.
output: research/crypto-kyc-ux-patterns.md

# Stage 2: MiroFish
scenario: kyc_onboarding_dropoff
agents: 200
onboarding_steps:
  - email_signup
  - phone_verification
  - id_document_upload
  - biometric_selfie
  - source_of_funds
  - video_call_optional

measure:
  - step_abandonment_rate
  - frustration_signals
  - completion_time_distribution
  - segment_specific_barriers
  
output: simulations/kyc-ux-validation.json

# Stage 3: Claude Code + Qoder CLI
task: |
  Implement optimized KYC flow with MiroFish-validated changes:
  - Move biometric after document upload (↓ abandonment)
  - Add progress indicator showing remaining steps
  - Offer video call fallback for biometric failures
output: src/onboarding/kyc_flow.py + tests
```

---

### 6. Fraud Scenario Stress-Testing

**Purpose:** Simulate fraud actors in community to identify new prevention patterns.

**MiroFish Query Template:**
```yaml
scenario: fraud_stress_test
agents: 500
baseline_fraud_rate: 2%
stress_injections:
  - btc_crash_40_percent: round 15
  - service_outage_3hr: round 25
  - competitor_launch: round 35

fraud_actor_adaptation: |
  Fraud agents observe prevention measures and adapt tactics
  every 5 rounds. Measure evolution of attack vectors.
  
measure:
  - novel_attack_vectors
  - prevention_evasion_rate
  - collateral_damage_legit_users
  - system_resilience_under_stress
  
rounds: 50
```

**Expected Output:**
- Novel attack vectors not yet seen in production
- Prevention rule gaps requiring updates
- Legitimate user impact from fraud measures

**Integration Point:** Quarterly stress-testing of `src/fraud/prevention_rules.py`

---

### 7. Market/Media Response Modeling

**Purpose:** Consumer reaction simulation, adoption curve projections.

**MiroFish Query Template:**
```yaml
scenario: market_adoption_curve
agents: 600
diffusion_segments:
  - innovators: 2.5%
  - early_adopters: 13.5%
  - early_majority: 34%
  - late_majority: 34%
  - laggards: 16%

messaging_variants:
  - A: "AI-agent banking with human oversight"
  - B: "Traditional banking, 10x faster with AI"
  - C: "Your personal banking doppelgänger"

measure:
  - adoption_velocity_by_variant
  - word_of_mouth_coefficient
  - skepticism_half_life
  - critical_mass_threshold
  
rounds: 60
```

**Expected Output:**
- Optimal messaging variant by segment
- Adoption velocity projection
- Critical mass timeline estimate

**Integration Point:** Marketing campaign planning, investor pitch refinement

---

## Scenario Table: Quick Reference

| # | Scenario | Agents | Rounds | Trigger | Output Artifact |
|---|----------|--------|--------|---------|-----------------|
| 1 | HITL handoff trust study | 300 | 40 | Before HITL implementation | `hitl_thresholds.json` |
| 2 | Pre-FCA policy test | 250 | 30 | Before sandbox submission | `regulatory_risk_map.json` |
| 3 | Fraud social engineering | 400 | 50 | Quarterly | `novel_fraud_patterns.json` |
| 4 | GTM market reaction | 350 | 35 | 3mo before launch | `messaging_optimization.json` |
| 5 | UX validation (KYC) | 200 | 25 | Before UX implementation | `ux_dropoff_heatmap.json` |
| 6 | Fraud stress test | 500 | 50 | Quarterly | `fraud_evolution_report.json` |
| 7 | Market adoption curve | 600 | 60 | Before marketing campaign | `adoption_projection.json` |

---

## File Structure: MiroFish Components

```
~/developer/
├── mirofish/
│   ├── config-template.yml          ← Base configuration template
│   ├── install-mirofish.sh          ← Installation script
│   ├── verify-install.sh            ← Health check script
│   └── run-simulation.sh            ← CLI wrapper for simulations
│
├── mirofish/scenarios/
│   ├── hitl-handoff.yml             ← Scenario 1: HITL trust study
│   ├── pre-fca-sandbox.yml          ← Scenario 2: Compliance test
│   ├── fraud-social-eng.yml         ← Scenario 3: Fraud patterns
│   ├── gtm-reaction.yml             ← Scenario 4: Market reaction
│   ├── ux-validation.yml            ← Scenario 5: UX pipeline
│   ├── fraud-stress-test.yml        ← Scenario 6: Stress testing
│   └── market-adoption.yml          ← Scenario 7: Adoption curve
│
├── mirofish/templates/
│   ├── simulation-request.template  ← JSON template for API calls
│   ├── persona-generator.template   ← Agent persona template
│   └── report-extractor.template    ← Results extraction template
│
└── docs/
    ├── MIROFISH-INTEGRATION.md      ← This document
    ├── MIROFISH-SCENARIOS.md        ← Detailed scenario library
    └── SIMULATION-RESULTS/          ← Historical simulation outputs
```

---

## Sync Protocol: MiroFish to Projects

### Components synced to all projects

| Source | Target | Purpose |
|--------|--------|---------|
| `mirofish/config-template.yml` | `{project}/.mirofish/config.yml` | Project simulation config |
| `mirofish/scenarios/*.yml` | `{project}/scenarios/` | Pre-built scenarios |
| `mirofish/run-simulation.sh` | `{project}/scripts/` | Simulation runner |

### Project-specific customization

Each project can override:
- Default agent count (based on complexity)
- LLM model (if using different models)
- Scenario parameters (domain-specific)
- Output paths (project structure)

---

## Automatic Trigger Detection

Claude Code automatically triggers MiroFish when detecting these patterns in user requests:

| Keyword Pattern | Auto-Trigger | Default Scenario |
|-----------------|--------------|------------------|
| "human approval", "handoff", "дублёр" | ✅ YES | hitl-handoff.yml |
| "FCA", "sandbox", "compliance policy" | ✅ YES | pre-fca-sandbox.yml |
| "fraud pattern", "social engineering" | ✅ YES | fraud-social-eng.yml |
| "market reaction", "launch strategy" | ✅ YES | gtm-reaction.yml |
| "UX validation", "drop-off", "onboarding" | ✅ YES | ux-validation.yml |
| "stress test", "crisis scenario" | ✅ YES | fraud-stress-test.yml |
| "adoption curve", "market sizing" | ✅ YES | market-adoption.yml |

### Override mechanism

User can explicitly disable:
```
"Design the HITL gateway WITHOUT MiroFish simulation"
→ Claude skips simulation, proceeds directly to implementation
```

---

## Output Format: Simulation Reports

Standard output structure for all MiroFish simulations:

```json
{
  "simulation_id": "hitl-handoff-20260403-143022",
  "scenario": "hitl_trust_handoff",
  "timestamp": "2026-04-03T14:30:22Z",
  "parameters": {
    "agents": 300,
    "rounds": 40,
    "seed": 42
  },
  "summary": {
    "key_finding": "Trust collapses at composite_score < 0.65 for SME segment",
    "recommendation": "Set HITL trigger at 0.70 (15% safety margin)"
  },
  "segment_results": [
    {
      "segment": "UK_SME_banking",
      "trust_threshold": 0.65,
      "churn_probability": 0.42,
      "handoff_acceptance": 0.78
    }
  ],
  "patterns_detected": [
    "Panic cascade when blocked >£10k without immediate human contact option",
    "Trust recovery possible within 3 rounds if human responds in <5min"
  ],
  "raw_data_path": "simulations/hitl-handoff-20260403-143022/raw/",
  "visualization_path": "simulations/hitl-handoff-20260403-143022/charts/"
}
```

---

## Performance Expectations

### Simulation time estimates

| Agents | Rounds | Est. Time (local LLM) | Est. Time (API) |
|--------|--------|----------------------|-----------------|
| 100 | 20 | ~5 min | ~2 min |
| 200 | 30 | ~12 min | ~5 min |
| 300 | 40 | ~25 min | ~10 min |
| 500 | 50 | ~50 min | ~20 min |
| 600 | 60 | ~75 min | ~30 min |

**Recommendation:** Use local Ollama for development/testing, API for production-scale simulations.

### Cost estimates (if using API)

Assuming $0.50/1M tokens input, $1.50/1M tokens output:

| Simulation | Est. Tokens | Est. Cost |
|------------|-------------|-----------|
| Small (100 agents) | 2M tokens | ~$2.50 |
| Medium (300 agents) | 8M tokens | ~$10 |
| Large (600 agents) | 20M tokens | ~$25 |

---

## Security Considerations

### Data isolation

- **Production data NEVER enters MiroFish** — only synthetic personas
- **Seed documents must be sanitized** — remove PII, real customer data
- **Simulation graphs are ephemeral** — Neo4j container destroyed after analysis

### Access control

```yaml
# .mirofish/config.yml
security:
  allowProductionData: false
  requireSanitizationCheck: true
  maxDataRetentionDays: 7
  auditAllSimulations: true
```

---

## Troubleshooting

### Problem: MiroFish service not responding

**Symptoms:** Claude waits for simulation result indefinitely

**Diagnosis:**
```bash
docker compose ps
# Should show: mirofish-app as running
```

**Fix:**
```bash
docker compose restart mirofish-app
# Or reinstall:
bash ~/developer/scripts/install-mirofish.sh
```

### Problem: Simulation results irrelevant/generic

**Cause:** Seed material too vague or generic

**Fix:** Provide more specific seed documents:
```yaml
# Instead of:
seed: "AI banking product description"

# Use:
seed_documents:
  - "Banxe_Agent_Banking_Whitepaper_v2.3.pdf"
  - "UK_SME_Banking_Needs_Analysis_Q1_2026.xlsx"
  - "FCA_Crypto_Registration_Guidance_Jan2025.pdf"
```

### Problem: WSL performance issues

**Symptoms:** Neo4j container hangs, high CPU

**Fix:** Increase Docker memory allocation:
```yaml
# ~/.docker/daemon.json (WSL)
{
  "memory": "32g",
  "swap": "8g"
}
```

---

## Success Metrics

### Phase 1: Installation Complete

- [ ] MiroFish services running (`docker compose ps`)
- [ ] Health check passes (`curl localhost:3000/api/health`)
- [ ] Test simulation completes (100 agents, 10 rounds)
- [ ] Configuration synced to vibe-coding

### Phase 2: First Production Simulation

- [ ] Run HITL handoff scenario for Banxe
- [ ] Results integrated into `src/compliance/hitl_gateway.py`
- [ ] MEMORY.md updated with findings
- [ ] Simulation report archived

### Phase 3: Full Integration

- [ ] All 7 scenarios tested
- [ ] Auto-trigger detection working
- [ ] Pipeline documented in COLLAB.md
- [ ] Team trained on simulation authoring

---

## Next Steps (Immediate Actions)

### 1. Install MiroFish Engine

```bash
cd ~/developer
bash scripts/install-mirofish.sh
```

### 2. Create Configuration Templates

- [ ] `mirofish/config-template.yml`
- [ ] `mirofish/install-mirofish.sh`
- [ ] `mirofish/run-simulation.sh`

### 3. Build First Scenario

- [ ] Create `mirofish/scenarios/hitl-handoff.yml`
- [ ] Test with 100 agents, 20 rounds
- [ ] Validate output format

### 4. Integrate with Banxe Workflow

- [ ] Sync to `~/vibe-coding/.mirofish/`
- [ ] Run first simulation: HITL handoff
- [ ] Apply findings to compliance stack

### 5. Document & Iterate

- [ ] Update MEMORY.md with lessons learned
- [ ] Refine auto-trigger detection
- [ ] Add remaining 6 scenarios

---

## Related Documents

- `COLLAB.md` — Collaboration pattern (extended for 3 partners)
- `AGENTS.md` — Agent instructions (includes MiroFish role)
- `docs/SYNERGY-DEPLOYMENT.md` — Deployment plan (MiroFish phase)
- `docs/MEMORY.md` — Long-term memory (updated with MiroFish state)

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-04-03 | Initial proposal — 7 applications mapped |

---

**Status:** READY FOR REVIEW  
**Decision Required:** Proceed with Phase 1 installation?
