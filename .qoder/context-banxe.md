# .qoder/context.md — Qoder Execution Contract (Banxe Projects)

**Repository:** `~/vibe-coding/` | `~/collaboration/` | `~/MetaClaw/` | `~/banxe-mirofish/`  
**Purpose:** Banxe AI Bank — FCA authorised EMI development  
**Version:** 2.0 | 2026-04-03

---

## Core rule

**Repository scope = current project only.**

This is a **Banxe project** with three-partner synergy (Claude + Qoder + MiroFish).

### What this means

- All changes must comply with FCA requirements
- MiroFish auto-triggers for validation-critical tasks
- Read COMPLIANCE_ARCH.md before touching src/compliance/
- Never commit secrets or credentials
- Update docs/MEMORY.md after significant changes

---

## Project isolation

**Hard invariant:** One terminal = one project = one repository.

| Do | Don't |
|----|-------|
| Implement banking features | Mix files from other projects |
| Run compliance tests | Assume paths from other repos |
| Update MEMORY.md | Commit without testing |
| Follow FCA guidelines | Expose API keys in code |
| Trigger MiroFish simulations | Share proprietary scenarios |

### Violation is a critical error

Never:
- Read project files without explicit instruction
- Assume project structure matches templates
- Mix components from different projects

---

## Role definition

**Qoder CLI role in this repository:**

1. **Implementation executor** — write production code for Banxe AI Bank
2. **Test runner** — execute unit/integration tests
3. **Compliance checker** — validate against COMPLIANCE_ARCH.md invariants
4. **Simulation assistant** — help run MiroFish scenarios

### Typical tasks

- Implement compliance modules (src/compliance/)
- Write FastAPI endpoints
- Create unit tests
- Run MiroFish simulations (auto-triggered by keywords)
- Update documentation

---

## Working method

### For implementation tasks

1. Read relevant design docs
2. Check COMPLIANCE_ARCH.md if touching compliance
3. Implement with clear diff
4. Write tests
5. Update MEMORY.md
6. Commit with clear message

### For MiroFish simulations

When Claude detects validation-critical task:

1. Claude triggers MiroFish automatically
2. MiroFish runs simulation scenario
3. Results inform design decisions
4. Qoder implements based on validated design

**Auto-trigger keywords:** HITL, handoff, дублёр, FCA, fraud pattern, UX validation, stress test

---

## Instruction priority

When working in this repository:

1. **User instruction** — explicit implementation commands
2. **This context** (.qoder/context.md) — execution rules
3. **AGENTS.md** — three-partner agent instructions
4. **CLAUDE.md** — project context
5. **COMPLIANCE_ARCH.md** — FCA invariants (if applicable)
6. **docs/MIROFISH-SCENARIOS.md** — MiroFish scenario library
7. **Global defaults** (~/.claude/CLAUDE.md)

---

## Compliance-sensitive scope

**CRITICAL:** If task touches `src/compliance/`:

### Protected invariants

- Canonical key structure
- OFAC RSS status (dead since Jan 2025)
- Watchman minMatch = 0.80
- ClickHouse TTL = 5 YEAR
- AGPLv3 internal-only use
- GUIYON exclusion

**Any change to these requires explicit user approval.**

---

## Output expectations

After completing work:

```
✓ Component implemented: {name}
✓ Tests passed: {count}
✓ Compliance verified: yes/no
✓ MEMORY.md updated: yes
○ Pending: {follow-up actions}
```

---

## Quick reference

| Command | Purpose |
|---------|---------|
| `bash collab.sh worker "task" branch` | Parallel implementation |
| `bash collab.sh run "command"` | Single command execution |
| `bash collab.sh jobs` | Check active tasks |
| `bash ../developer/mirofish/run-simulation.sh <scenario>` | Run MiroFish simulation |
| `python -m pytest tests/` | Run test suite |

---

## Files in this repository

| Path | Purpose |
|------|---------|
| `.qoder/context.md` | This file — execution contract (Banxe version) |
| `.qoder/config.yml` | Qoder CLI configuration |
| `AGENTS.md` | Three-partner agent instructions |
| `CLAUDE.md` | Project context |
| `docs/COLLAB.md` | Collaboration pattern |
| `docs/MIROFISH-SCENARIOS.md` | MiroFish scenario library |
| `docs/MEMORY.md` | Long-term memory |
| `COMPLIANCE_ARCH.md` | FCA compliance invariants |

---

**Source:** `~/developer/.qoder/context-banxe.md` (MASTER)  
**Synced:** Auto-sync via sync-all.sh  
**Classification:** Banxe AI Bank Proprietary
