# .qoder/context.md — Qoder Execution Contract (Legal Projects)

**Repository:** `~/guiyon/` | `~/ss1/`  
**Purpose:** Legal case management and appeal documentation  
**Version:** 2.0 | 2026-04-03

---

## Core rule

**Repository scope = current project only.**

This is a **Legal project** with two-partner synergy (Claude + Qoder).

### What this means

- Focus on legal documentation and case analysis
- No MiroFish simulations (not needed for legal work)
- Maintain strict confidentiality for sensitive cases
- Update docs/MEMORY.md after significant changes

---

## Project isolation

**Hard invariant:** One terminal = one project = one repository.

| Do | Don't |
|----|-------|
| Implement legal document features | Mix files from other projects |
| Run case analysis | Assume paths from other repos |
| Update MEMORY.md | Commit without review |
| Follow confidentiality rules | Expose sensitive case details |

### Violation is a critical error

Never:
- Read project files without explicit instruction
- Assume project structure matches templates
- Mix components from different projects
- Share confidential case information

---

## Role definition

**Qoder CLI role in this repository:**

1. **Document implementer** — write legal document generators
2. **Analysis assistant** — help parse case files
3. **Test runner** — execute validation tests
4. **Documentation helper** — update case documentation

### Typical tasks

- Implement document generation templates
- Write case analysis utilities
- Create validation tests
- Update documentation

---

## Working method

### For implementation tasks

1. Read relevant design docs
2. Implement with clear diff
3. Write tests
4. Update MEMORY.md
5. Commit with clear message

### No MiroFish integration

Legal projects do NOT use MiroFish simulations:
- Work is document-focused, not behavior-focused
- No user simulation needed
- Direct implementation without behavioral validation

---

## Instruction priority

When working in this repository:

1. **User instruction** — explicit implementation commands
2. **This context** (.qoder/context.md) — execution rules
3. **AGENTS.md** — agent instructions
4. **CLAUDE.md** — project context
5. **Global defaults** (~/.claude/CLAUDE.md)

---

## Output expectations

After completing work:

```
✓ Document implemented: {name}
✓ Analysis completed: {scope}
✓ Tests passed: {count}
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
| `python -m pytest tests/` | Run test suite |

---

## Files in this repository

| Path | Purpose |
|------|---------|
| `.qoder/context.md` | This file — execution contract (Legal version) |
| `.qoder/config.yml` | Qoder CLI configuration |
| `AGENTS.md` | Agent instructions |
| `CLAUDE.md` | Project context |
| `docs/COLLAB.md` | Collaboration pattern |
| `docs/MEMORY.md` | Long-term memory |

---

**Source:** `~/developer/.qoder/context-legal.md` (MASTER)  
**Synced:** Auto-sync via sync-all.sh  
**Classification:** Legal Confidential
