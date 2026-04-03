# Architecture — Three-Partner Synergy + Target Platform

**Version:** 1.0 | 2026-04-03  
**Project:** Banxe AI Bank Development

---

## Executive Summary

This document clarifies the architectural roles and prevents confusion between **development-time partners** and **production platform**.

---

## Two-Level Architecture

### Level 1: Development-Time Partners (Active Now)

These three partners collaborate in every development session:

| Partner | Role | Activation | Scope |
|---------|------|------------|-------|
| **Claude Code** | Architect & Coordinator | Every `claude` session | Design, review, orchestration |
| **Qoder CLI** | Executor | MCP auto-load | Implementation, edits, tests |
| **MiroFish** | Simulator & Validator | Auto-trigger by keywords | Behavioral simulation, stress-testing |

**Workflow:**
```bash
cd ~/project && claude
# → Claude + Qoder + Mirofish work together automatically
```

**Integration:** MCP (Model Context Protocol) via stdio  
**Isolation:** One terminal = one project = one repository

---

### Level 2: Production Platform (Target Product)

This is what we're building — not a development partner.

| Component | Role | Status |
|-----------|------|--------|
| **MetaClaw** | Banxe-customized OpenClaw fork | In development |
| **OpenClaw** | Multi-agent orchestration framework | External dependency |

**Purpose:** Production orchestrator for banking AI agents under human-in-the-loop control.

**Future Architecture (Production):**
```
MetaClaw/OpenClaw (Production Orchestrator)
├── Banking AI Agents (customer-facing)
├── Fraud Detection Agents
├── Compliance Agents (FCA reporting)
├── Human-in-the-Loop Gateway
└── MiroFish (continuous simulation & monitoring)
```

---

## Why MetaClaw Is NOT a Fourth Partner

### 1. Different Abstraction Levels

| Dimension | Three Partners | MetaClaw |
|-----------|----------------|----------|
| **When used** | Every dev session | Future production |
| **What it is** | Development tools | Product being built |
| **Integration** | MCP in Claude session | Standalone service |
| **User interaction** | Direct (via Claude) | Indirect (via API) |

**Analogy:**
> Three partners are the **construction crew** (Claude = architect, Qoder = builder, MiroFish = inspector).  
> MetaClaw is the **building** they're constructing.

### 2. Risk of Confusion

If MetaClaw were a "fourth partner":

❌ It would be both **developer** and **product**  
❌ Documentation would mix dev-tools with target-architecture  
❌ AGENTS.md would have circular references  
❌ Onboarding would be confusing ("which MetaClaw am I configuring?")

### 3. Clean Separation Enables Clarity

**Current model (recommended):**
```
Development Layer:
  Claude Code ←→ Qoder ←→ MiroFish
         ↓ (build)
Target Layer:
  MetaClaw (product)
```

**Alternative model (NOT recommended):**
```
Flat model with 4 partners:
  Claude Code ←→ Qoder ←→ MiroFish ←→ MetaClaw
         ↓ (build what?)
  ??? (circular dependency)
```

---

## Documentation Hierarchy

### Partner Documentation (Level 1)

| Document | Location | Describes |
|----------|----------|-----------|
| `COLLAB.md` | Each project + `developer/docs/` | Three-partner workflow |
| `MIROFISH-INTEGRATION.md` | `developer/docs/` | MiroFish setup & scenarios |
| `AGENTS.md` | Each project | Agent instructions (3 partners) |
| `~/.claude/CLAUDE.md` | Global | Three-partner contract |

### Platform Documentation (Level 2)

| Document | Location | Describes |
|----------|----------|-----------|
| `README.md` | `~/MetaClaw/` | MetaClaw product overview |
| `ARCHITECTURE.md` | `~/MetaClaw/` | Production orchestrator design |
| `OPENCLAW-INTEGRATION.md` | `~/MetaClaw/` | OpenClaw customization guide |

---

## When Does MetaClaw Become "Active"?

### Development Phase (Now)

MetaClaw is the **object of development**:
- Three partners build MetaClaw
- MetaClaw does NOT participate in its own creation
- Analogy: A house doesn't build itself

### Production Phase (Future)

MetaClaw becomes the **orchestration layer**:
```
User Request → MetaClaw (orchestrator)
                  ↓ routes to
              ┌─────────────────────┐
              │  Banking AI Agent   │
              │  (with HITL gate)   │
              └─────────────────────┘
                  ↓ uses for validation
              ┌─────────────────────┐
              │   MiroFish Engine   │
              │  (continuous sim)   │
              └─────────────────────┘
```

At this point, MetaClaw is **production infrastructure**, not a development partner.

---

## Decision Log

### 2026-04-03: Three-Partner Model Confirmed

**Decision:** Maintain three partners (Claude + Qoder + MiroFish), keep MetaClaw as target platform.

**Rationale:**
1. Clear separation of concerns (dev-tools vs. product)
2. Avoids circular dependency confusion
3. Matches actual usage patterns today
4. Scales better for documentation and onboarding

**Alternatives Considered:**
- ❌ Four-partner model (rejected: different abstraction levels)
- ❌ MetaClaw as MCP server (rejected: not ready, different purpose)

**Reviewed by:** Moriel Carmi (CEO/CTIO)

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `COLLAB.md` | Three-partner workflow guide |
| `MIROFISH-INTEGRATION.md` | MiroFish setup & scenarios |
| `~/MetaClaw/README.md` | MetaClaw product overview |
| `~/developer/docs/MEMORY.md` | Project state tracking |

---

## Quick Reference

**Question:** "Should I add MetaClaw to AGENTS.md?"  
**Answer:** No. AGENTS.md describes active development partners. MetaClaw is the product being built.

**Question:** "When will MetaClaw be a partner?"  
**Answer:** Never as a "partner". MetaClaw will be the production orchestrator that runs banking AI agents.

**Question:** "Can MetaClaw use MiroFish?"  
**Answer:** Yes! In production, MetaClaw can call MiroFish for continuous simulation. But that's runtime integration, not development partnership.

---

**Status:** Architecture confirmed 2026-04-03  
**Next Review:** When MetaClaw reaches production readiness
