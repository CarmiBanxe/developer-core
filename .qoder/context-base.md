# .qoder/context.md — Qoder Execution Contract (Base Version)

**Repository:** Generic project template  
**Purpose:** Minimal execution contract for non-Banxe/non-Legal projects  
**Version:** 1.0 | 2026-04-03

---

## Core rule

**Repository scope = current project only.**

This is a **generic project** with two-partner synergy (Claude + Qoder).

### What this means

- Focus on project-specific implementation
- No MiroFish simulations (not configured)
- Update docs/MEMORY.md after significant changes

---

## Project isolation

**Hard invariant:** One terminal = one project = one repository.

| Do | Don't |
|----|-------|
| Implement project features | Mix files from other projects |
| Run tests | Assume paths from other repos |
| Update MEMORY.md | Commit without review |

### Violation is a critical error

Never:
- Read project files without explicit instruction
- Assume project structure matches templates
- Mix components from different projects

---

## Role definition

**Qoder CLI role in this repository:**

1. **Implementation executor** — write code
2. **Test runner** — execute tests
3. **Documentation helper** — update docs

### Typical tasks

- Implement features
- Write tests
- Update documentation

---

## Working method

### For implementation tasks

1. Read relevant design docs
2. Implement with clear diff
3. Write tests
4. Update MEMORY.md
5. Commit with clear message

---

## Instruction priority

When working in this repository:

1. **User instruction** — explicit commands
2. **This context** (.qoder/context.md) — execution rules
3. **AGENTS.md** — agent instructions
4. **CLAUDE.md** — project context
5. **Global defaults** (~/.claude/CLAUDE.md)

---

## Output expectations

After completing work:

```
✓ Task completed: {description}
✓ Files changed: {count}
✓ Tests passed: {count}
✓ MEMORY.md updated: yes/no
○ Pending: {follow-up actions}
```

---

## Quick reference

| Command | Purpose |
|---------|---------|
| `bash collab.sh worker "task" branch` | Parallel implementation |
| `bash collab.sh run "command"` | Single command |
| `bash collab.sh jobs` | Check active tasks |

---

## Files in this repository

| Path | Purpose |
|------|---------|
| `.qoder/context.md` | This file — execution contract (Base version) |
| `.qoder/config.yml` | Qoder CLI configuration |
| `AGENTS.md` | Agent instructions |
| `CLAUDE.md` | Project context |
| `docs/COLLAB.md` | Collaboration pattern |
| `docs/MEMORY.md` | Long-term memory |

---

**Source:** `~/developer/.qoder/context-base.md` (MASTER)  
**Synced:** Auto-sync via sync-all.sh
