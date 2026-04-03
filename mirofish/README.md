# MiroFish Integration — Quick Start Guide

**Status:** Phase 1 READY | Awaiting User Approval  
**Version:** 1.0 | 2026-04-03  
**Documentation:** `~/developer/docs/MIROFISH-INTEGRATION.md`

---

## What is MiroFish?

MiroFish is a **multi-agent social simulation engine** that becomes your third development partner alongside Claude Code (architect) and Qoder CLI (executor).

### Role Comparison

| Partner | Role | When It Activates |
|---------|------|-------------------|
| **Claude Code** | Architect & Coordinator | All tasks |
| **Qoder CLI** | Executor | Implementation tasks |
| **MiroFish** | Simulator & Validator | Validation-critical tasks |

---

## Seven High-Value Applications

1. **HITL Architecture (Дублёр)** — Simulate when users lose trust in AI agents and when human approval gates are mandatory (BCG requirement)

2. **Pre-FCA-Sandbox Testing** — Test draft compliance policies before FCA Regulatory Sandbox submission

3. **Fraud Pattern Detection** — Model coordinated social attacks that historical data doesn't capture

4. **Go-to-Market Reaction** — Media, regulator, skeptic reactions to "AI-agent bank" concept

5. **UX Validation Pipeline** — Three-stage validation: AutoResearchClaw → MiroFish → Claude Code

6. **Fraud Stress-Testing** — Quarterly comprehensive crisis simulation

7. **Market Adoption Modeling** — Consumer reaction simulation, adoption curve projections

---

## Installation (Phase 1)

### Prerequisites

- Docker Desktop with Compose
- 32GB+ RAM recommended (for 200+ agent simulations)
- Ollama (optional, for local LLM)

### Step 1: Run Installation Script

```bash
cd ~/developer
bash mirofish/install-mirofish.sh
```

This will:
- Clone MiroFish-Offline repository to `~/mirofish-engine/`
- Configure Docker services (Neo4j + Ollama + Flask app)
- Pull required LLM models (qwen2.5:32b, nomic-embed-text)
- Copy configuration template to `~/.mirofish/config.yml`

**Duration:** ~10 minutes (mostly model downloads)

### Step 2: Verify Installation

```bash
# Check services running
docker compose ps -C

# Test API health
curl http://localhost:3000/api/health

# Expected: {"status":"ok","agents":0,"simulations":0}
```

### Step 3: Run Test Simulation

```bash
bash mirofish/run-simulation.sh test
```

---

## Usage Examples

### First Production Simulation (HITL Handoff)

```bash
cd ~/vibe-coding
bash ../developer/mirofish/run-simulation.sh hitl-handoff \
  --agents 300 \
  --rounds 40
```

**Expected output:**
- Trust threshold map by user segment
- Optimal handoff trigger points
- Communication templates minimizing trust decay

**Updates artifact:** `src/compliance/hitl_gateway.py`

### Pre-FCA Policy Testing

```bash
bash ../developer/mirofish/run-simulation.sh pre-fca-sandbox \
  --agents 250 \
  --rounds 30
```

**Expected output:**
- Ambiguous clauses requiring rewrite
- Segment-specific interpretation gaps
- Regulatory risk heat map

### Fraud Pattern Detection

```bash
bash ../developer/mirofish/run-simulation.sh fraud-social-eng \
  --agents 400 \
  --rounds 50
```

**Expected output:**
- Novel fraud patterns not in historical data
- Early warning indicators
- Prevention rule recommendations

---

## Scenario Library

All scenarios located in `~/developer/mirofish/scenarios/`:

| File | Application | Agents | Rounds |
|------|-------------|--------|--------|
| `hitl-handoff.yml` | HITL trust study | 300 | 40 |
| `pre-fca-sandbox.yml` | Compliance testing | 250 | 30 |
| `fraud-social-eng.yml` | Fraud patterns | 400 | 50 |
| `gtm-reaction.yml` | Market reaction | 350 | 35 |
| `ux-validation.yml` | UX validation | 200 | 25 |
| `fraud-stress-test.yml` | Stress testing | 500 | 50 |
| `market-adoption.yml` | Adoption curve | 600 | 60 |

---

## Automatic Trigger Detection

Claude Code automatically proposes MiroFish simulation when detecting these keywords:

| Keyword Pattern | Auto-Triggered Scenario |
|-----------------|------------------------|
| "human approval", "handoff", "дублёр" | hitl-handoff |
| "FCA", "sandbox", "compliance policy" | pre-fca-sandbox |
| "fraud pattern", "social engineering" | fraud-social-eng |
| "market reaction", "launch strategy" | gtm-reaction |
| "UX validation", "drop-off", "onboarding" | ux-validation |
| "stress test", "crisis scenario" | fraud-stress-test |
| "adoption curve", "market sizing" | market-adoption |

### Override Mechanism

To skip simulation:
```
"Design the HITL gateway WITHOUT MiroFish simulation"
→ Claude proceeds directly to implementation
```

---

## Performance Expectations

### Simulation Times (Local LLM)

| Size | Agents | Rounds | Est. Time |
|------|--------|--------|-----------|
| Small | 100 | 20 | ~5 min |
| Medium | 300 | 40 | ~25 min |
| Large | 600 | 60 | ~75 min |

### Cost Estimates (API-based LLM)

| Size | Tokens | Est. Cost |
|------|--------|-----------|
| Small | 2M | ~$2.50 |
| Medium | 8M | ~$10 |
| Large | 20M | ~$25 |

**Recommendation:** Use local Ollama for development/testing.

---

## Output Format

All simulations produce JSON reports in `docs/simulations/`:

```json
{
  "simulation_id": "hitl-handoff-20260403-143022",
  "scenario": "hitl_trust_handoff",
  "summary": {
    "key_finding": "Trust collapses at composite_score < 0.65 for SME segment",
    "recommendation": "Set HITL trigger at 0.70 (15% safety margin)"
  },
  "segment_results": [...],
  "patterns_detected": [...],
  "raw_data_path": "simulations/hitl-handoff-20260403-143022/raw/"
}
```

---

## Security Considerations

### Data Isolation Rules

- **NEVER** use production customer data in simulations
- **ALWAYS** sanitize seed documents (remove PII)
- **EPHEMERAL** simulation graphs (destroyed after analysis)

### Configuration

```yaml
# ~/.mirofish/config.yml
security:
  allowProductionData: false
  requireSanitizationCheck: true
  maxDataRetentionDays: 7
  auditAllSimulations: true  # ClickHouse audit trail
```

---

## Troubleshooting

### Problem: API Not Responding

```bash
# Restart services
cd ~/mirofish-engine
docker compose restart

# Check logs
docker compose logs mirofish-app
```

### Problem: Simulation Results Generic

**Cause:** Seed material too vague

**Fix:** Provide specific seed documents:
```yaml
seed_documents:
  - "Banxe_Agent_Banking_Whitepaper_v2.3.pdf"
  - "UK_SME_Banking_Needs_Analysis_Q1_2026.xlsx"
```

### Problem: WSL Performance Issues

**Fix:** Increase Docker memory allocation:
```json
// ~/.docker/daemon.json
{
  "memory": "32g",
  "swap": "8g"
}
```

---

## Next Steps

### Immediate (User Decision Required)

1. **Review integration proposal:** `docs/MIROFISH-INTEGRATION.md`
2. **Approve installation:** Confirm readiness to proceed
3. **Run installation:** `bash mirofish/install-mirofish.sh`

### After Installation

4. **First test simulation:** `bash run-simulation.sh test`
5. **First production scenario:** HITL handoff for Banxe
6. **Integrate findings:** Update `src/compliance/hitl_gateway.py`

### Quarterly Schedule

- **Q2 2026 (July):** First fraud stress test
- **Q3 2026 (October):** Pre-FCA sandbox simulation
- **Q4 2026 (January):** Market adoption study

---

## Related Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| Full Integration Plan | `developer/docs/MIROFISH-INTEGRATION.md` | Complete architecture |
| Scenario Library | `developer/mirofish/scenarios/` | 7 pre-built scenarios |
| Configuration Template | `developer/mirofish/config-template.yml` | Base config |
| Memory Update | `developer/docs/MEMORY.md` | Partnership state |
| Global Contract | `~/.claude/CLAUDE.md` | Updated for 3 partners |

---

## Contact

| Role | Person | Scope |
|------|--------|-------|
| CEO/CTIO | Moriel Carmi (Mark) | Final approval |
| Developer | You | Implementation |
| CTIO Deputy | Олег | Infrastructure (GMKtec sudo) |

---

**Ready to proceed?** Run `bash mirofish/install-mirofish.sh` or ask for clarification.
