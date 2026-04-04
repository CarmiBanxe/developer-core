# Architecture — Developer-Core Toolchain + Delegation Model

**Version:** 2.0 | 2026-04-05 (canonical rewrite)
**Project:** developer-core (all projects)

---

## Executive Summary

This document defines the **canonical delegation model**: developer-core tools are built and used by the developer, then forked/delegated to each project, where they continue to operate as part of that project's runtime.

MetaClaw is a **developer-core tool** — not a BANXE-specific product by default. In the BANXE project, the project-specific manifestation of MetaClaw-derived capabilities is called the **AML block**.

---

## Canonical Delegation Hierarchy

```
developer-core toolchain
    ↓ fork / delegate
project runtime (vibe-coding, guiyon, ss1, ...)
    ↓ operates as
project-specific operational layer
```

**Rule:** The developer uses each tool 100% during development. The same tooling is then delegated to each project, where it continues to operate in daily project work.

---

## Level 1: Development-Time Partners (Active Now)

These three partners collaborate in every development session:

| Partner | Role | Activation | Scope |
|---------|------|------------|-------|
| **Claude Code** | Architect & Coordinator | Every `claude` session | Design, review, orchestration |
| **Aider CLI** | Executor | MCP auto-load | Implementation, edits, tests |
| **MiroFish** | Simulator & Validator | Auto-trigger by keywords | Behavioral simulation, stress-testing |

**Workflow:**
```bash
cd ~/project && claude
# → Claude + Aider + MiroFish work together automatically
```

**Integration:** MCP (Model Context Protocol) via stdio
**Isolation:** One terminal = one project = one repository

---

## Level 2: Developer-Core Tools (Reusable Instruments)

These tools are built and maintained in developer-core, then delegated to projects:

| Tool | Role | Delegation model |
|------|------|-----------------|
| **MetaClaw** | Multi-agent orchestration layer (OpenClaw-based) | Forked to each project; customized per project runtime |
| **MiroFish engine** | Simulation & validation framework | Shared engine; project-specific scenarios |
| **Training block** | Agent training pipeline (corpus, eval, RLHF) | Developer builds agents → delegates trained agents to projects |

### MetaClaw — Canonical Definition

> MetaClaw is a developer-core tool used by the developer across projects during design, build, training, and delegation. It is **not a BANXE-specific product by default**.

- **Developer uses:** MetaClaw to design multi-agent orchestration patterns
- **Delegates to project:** Project receives a MetaClaw-derived configuration
- **Project runtime:** Continues using MetaClaw as its operational orchestration layer

### Training Block — Delegation Pattern

The training block follows the same pattern:
1. Developer uses training tools to create and train agents
2. Trained agents + evaluation framework are delegated to the project
3. Project continues using the framework as part of its operational system

---

## Level 3: Project-Specific Manifestations

After delegation, each project names its operational layer according to its domain:

| Project | MetaClaw manifestation | Notes |
|---------|----------------------|-------|
| **BANXE** | **AML block** | Includes banxe-lexisnexis-distro + more; will expand |
| **GUIYON** | Legal AI layer | Court, appeals, document analysis |
| **SS1** | Legal AI layer | Same family as GUIYON |

### BANXE: AML Block

In the BANXE project, the MetaClaw-derived operational layer is called the **AML block**:

- **AML block** is part of the BANXE project (vibe-coding)
- **banxe-lexisnexis-distro** is one component: *"installable AI compliance & knowledge platform for partners and employees"*
- The AML block is broader than banxe-lexisnexis-distro and will continue to evolve
- Do **not** call BANXE's AML capabilities "MetaClaw" in BANXE project documentation

---

## Why MetaClaw Is NOT a Fourth Partner

### Different Abstraction Levels

| Dimension | Three Partners | MetaClaw |
|-----------|----------------|----------|
| **When used** | Every dev session | Developer tool → delegates to projects |
| **What it is** | Active collaborators | Orchestration instrument |
| **Integration** | MCP in Claude session | Forked config + runtime |
| **User interaction** | Direct (via Claude) | Via project's operational layer |

### Clean Separation

```
Development Layer (active):
  Claude Code ←→ Aider CLI ←→ MiroFish
         ↓ build & delegate
Instrument Layer (developer-core):
  MetaClaw | Training Block | MiroFish engine
         ↓ fork to project
Project Runtime:
  BANXE AML block | GUIYON Legal AI | SS1 Legal AI
```

---

## Documentation Hierarchy

### Partner Documentation (Level 1)

| Document | Location | Describes |
|----------|----------|-----------|
| `COLLAB.md` | Each project + developer-core/docs/ | Three-partner workflow |
| `MIROFISH-INTEGRATION.md` | developer-core/docs/ | MiroFish setup & scenarios |
| `AGENTS.md` | Each project | Agent instructions (3 partners) |
| `~/.claude/CLAUDE.md` | Global | Three-partner contract |

### Developer-Core Tool Documentation (Level 2)

| Document | Location | Describes |
|----------|----------|-----------|
| `ARCHITECTURE.md` | developer-core/docs/ | Delegation model (this document) |
| `MIROFISH-SCENARIOS-MetaClaw.md` | developer-core/docs/ | Infrastructure scenarios (developer-core) |
| `SYNERGY-DEPLOYMENT.md` | developer-core/docs/ | Sync & deployment toolchain |

### Project-Specific Documentation (Level 3)

| Document | Location | Describes |
|----------|----------|-----------|
| `CLAUDE.md` | vibe-coding/ | BANXE project context |
| `docs/COMPLIANCE_ARCH.md` | vibe-coding/ | BANXE AML block architecture |
| `docs/SANCTIONS_POLICY.md` | vibe-coding/ | BANXE AML block policy |

---

## Decision Log

### 2026-04-05: Canonical Delegation Model (v2.0)

**Decision:** MetaClaw = developer-core tool. BANXE AML capabilities = AML block.

**Rationale:**
1. MetaClaw is reused across all projects via delegation — not BANXE-exclusive
2. BANXE needs its own domain terminology (AML block) per FCA/banking context
3. banxe-lexisnexis-distro is a component of AML block, not a synonym for MetaClaw
4. Training block follows same delegation pattern: developer builds → delegates → project runs

**Canonical hierarchy:** developer-core toolchain → fork/delegation → project runtime usage

### 2026-04-03: Three-Partner Model Confirmed (v1.0)

**Decision:** Maintain three partners (Claude + Aider + MiroFish), MetaClaw as developer instrument.

---

**Status:** Canonical model confirmed 2026-04-05
**Next Review:** When project delegation patterns change
