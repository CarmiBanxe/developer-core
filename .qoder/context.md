# .qoder/context.md — Qoder Execution Contract (Developer Core Template)

**Repository:** `~/developer/`  
**Purpose:** Central repository for shared components across all projects  
**Version:** 1.0 | 2026-04-03

---

## Core rule

**Repository scope = ~/developer/ only.**

This is a **template repository** containing shared components for distribution.

### What this means

- Edit files here for downstream distribution
- Test changes before syncing to projects
- Never assume project-specific paths or configs
- Report breaking changes clearly

---

## Project isolation

**Hard invariant:** This repository is NOT a working project.

| Do | Don't |
|----|-------|
| Create templates for new projects | Implement project-specific features here |
| Update shared scripts | Hardcode paths to specific projects |
| Maintain compliance reference | Run production services from here |
| Sync tested components | Auto-sync without review |

### Violation is a critical error

Never:
- Read project files without explicit instruction
- Assume project structure matches templates
- Mix components from different downstream projects

---

## Role definition

**Qoder CLI role in this repository:**

1. **Template maintainer** — edit files that will be copied to projects
2. **Sync executor** — run distribution scripts when requested
3. **Integration tester** — validate components work in target projects

### Typical tasks

- Update AGENTS.md template
- Modify .qoder/config.yml defaults
- Add new scripts to scripts/
- Create project templates in templates/
- Test sync workflow

---

## Working method

### For template edits

1. Identify the component to update
2. Make changes with clear diff
3. Test syntax/validity
4. Commit with version bump
5. Note which projects should receive update

### For sync operations

1. User specifies target project(s)
2. Show diff for each target
3. Wait for explicit approval
4. Execute sync
5. Verify success

### For testing

1. Pick non-production project first
2. Apply component
3. Verify functionality
4. Report results
5. Ready for broader sync

---

## Instruction priority

When working in this repository:

1. **User instruction** — explicit sync/deploy commands
2. **This context** (.qoder/context.md) — execution rules
3. **AGENTS.md** — component catalog and procedures
4. **Global defaults** (~/.claude/CLAUDE.md)

### Downstream precedence

Components synced TO projects become templates there. Local project files override these defaults.

---

## Compliance-sensitive repositories

If syncing TO `vibe-coding`:

### Special handling required

Before syncing compliance components:

1. Read target's `COMPLIANCE_ARCH.md`
2. Compare with source in `developer/compliance/`
3. Identify any invariant changes
4. Require explicit user approval for:
   - Threshold changes
   - Source weight modifications
   - Retention assumption updates
   - Licensing boundary shifts

### Protected invariants (vibe-coding)

- Canonical key structure
- OFAC RSS status (dead since Jan 2025)
- Watchman minMatch = 0.80
- ClickHouse TTL = 5 YEAR
- AGPLv3 internal-only use
- GUIYON exclusion

**Never sync changes to these without explicit review.**

---

## Output expectations

After completing work in this repository:

```
✓ Component updated: {name}
✓ Tests passed: {test_type}
✓ Ready for sync to: {projects}
○ Pending: {follow-up actions}
```

### For sync operations

```
═══════════════════════════════════════
  Sync Report: Developer → {project}
═══════════════════════════════════════

Updated components:
  ✓ AGENTS.md (v1.0 → v1.1)
  ✓ .qoder/config.yml (WSS polling added)
  ○ scripts/sync-to-project.sh (new)

Skipped (local overrides detected):
  ○ CLAUDE.md (project-specific)

Verification:
  ✓ Syntax check passed
  ✓ Target tests run successfully
  ✓ No breaking changes detected

Rollback available: git stash apply
═══════════════════════════════════════
```

---

## Quick reference

| Command | Purpose |
|---------|---------|
| `bash scripts/sync-to-project.sh <name>` | Sync to project |
| `bash scripts/check-agent-instructions.sh` | Verify setup |
| `git diff --stat origin/master` | See pending changes |
| `ls templates/` | List available templates |

---

## Files in this repository

| Path | Purpose | Sync status |
|------|---------|-------------|
| `.qoder/context.md` | This file — execution contract | Template |
| `.qoder/config.yml` | Qoder configuration | Sync to all |
| `AGENTS.md` | Agent instructions template | Sync to all |
| `docs/COLLAB.md` | Collaboration docs | Sync to all |
| `docs/MCP-BEST-PRACTICES.md` | MCP guide | Sync to all |
| `scripts/` | Shared utilities | Sync to all |
| `templates/` | Project bootstraps | Copy on demand |
| `compliance/` | Reference implementation | vibe-coding only |
