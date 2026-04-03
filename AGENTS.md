# AGENTS.md — Developer Core: Central Repository for Shared Components

**Repository:** `~/developer/`  
**Version:** 3.0 | 2026-04-03  
**Purpose:** Shared components, templates, and configurations distributed across all projects  
**Architecture:** Three-Partner Synergy (Claude Code + Qoder CLI + MiroFish)

---

## Core mission

This repository is the **central source of truth** for:

- Agent instructions (AGENTS.md, CLAUDE.md templates)
- Qoder CLI configurations (.qoder/config.yml)
- **Three-partner synergy architecture** (Claude + Qoder + MiroFish)
- Compliance architecture (COMPLIANCE_ARCH.md)
- Shared scripts and automation (sync-all.sh, onboard-project.sh)
- Project templates
- MCP best practices
- **MiroFish scenario templates** (MASTER copies for all projects)

### Three-Partner Architecture

All projects use the same three-partner stack:

| Partner | Role | Activation | Scope |
|---------|------|------------|-------|
| **Claude Code** | Architect & Coordinator | Every session | Design, review, orchestration |
| **Qoder CLI** | Executor | MCP auto-load | Implementation, edits, tests |
| **MiroFish** | Simulator & Validator | Auto-trigger by keywords | Behavioral simulation, stress-testing |

**Key principle:** MiroFish is a partner for ALL projects, not just Banxe.
- Banxe projects: banking/FCA/fraud scenarios
- Legal projects: court/judge/appeal scenarios
- Developer-core: infrastructure & sync validation

### Distribution model

Components from this repository are synced to:

| Project | Type | Sync target | MiroFish | Scenarios |
|---------|------|-------------|----------|-----------|
| vibe-coding | banxe | `/home/mmber/vibe-coding/` | ✅ | banking/FCA/fraud |
| collaboration | banxe | `/home/mmber/collaboration/` | ✅ | multi-agent conflicts |
| MetaClaw | banxe | `/home/mmber/MetaClaw/` | ✅ | orchestration scaling |
| guiyon | legal | `/home/mmber/guiyon/` | ✅ | court strategy |
| ss1 | legal | `/home/mmber/ss1/` | ✅ | appeal dynamics |
| banxe-mirofish | tool | `/home/mmber/banxe-mirofish/` | ✅ | MASTER templates |
| developer-core | core | `/home/mmber/developer/` | ✅ | ALL (MASTER) |

---

## Instruction hierarchy (for THIS repository)

1. **Explicit user instruction** (highest authority)
2. **Repository-level contracts**:
   - `.qoder/context.md` (execution contract)
   - `CLAUDE.md` (project context)
3. **Global defaults**: `~/.claude/CLAUDE.md`

### Rule for downstream projects

When syncing components TO a project, that project's local files take precedence over these templates.

**These are templates and starting points, not immutable laws.**

---

## Repository structure

```
~/developer/
├── .claude/CLAUDE.md          ← Global collaboration contract (symlink target)
├── .qoder/config.yml          ← Qoder configuration template
├── .qoder/context.md          ← Qoder execution contract template
├── AGENTS.md                  ← This file — agent instructions template
├── docs/
│   ├── COLLAB.md              ← Collaboration pattern documentation
│   └── MCP-BEST-PRACTICES.md  ← MCP server configuration guide
├── scripts/
│   ├── check-agent-instructions.sh  ← Diagnostic tool
│   └── sync-to-project.sh           ← Sync script (TO BE CREATED)
├── templates/
│   ├── project-template/            ← New project bootstrap
│   └── compliance-module/           ← AML/KYC module template
├── agents/
│   ├── code-reviewer.skill          ← Code review skill
│   ├── test-runner.subagent         ← Test execution agent
│   └── compliance-checker.subagent  ← FCA compliance agent
└── compliance/
    ├── COMPLIANCE_ARCH.md           ← Invariants contract
    └── api.py                       ← Reference implementation
```

---

## Component catalog

### Templates (copy to new projects)

| Component | Source | Target | Purpose |
|-----------|--------|--------|---------|
| `AGENTS.md` | `./AGENTS.md` | `{project}/AGENTS.md` | Agent instructions |
| `.qoder/config.yml` | `./.qoder/config.yml` | `{project}/.qoder/config.yml` | Qoder config |
| `.qoder/context.md` | `./.qoder/context.md` | `{project}/.qoder/context.md` | Execution contract |
| `docs/COLLAB.md` | `./docs/COLLAB.md` | `{project}/docs/COLLAB.md` | Collaboration docs |
| `docs/MCP-BEST-PRACTICES.md` | `./docs/MCP-BEST-PRACTICES.md` | `{project}/docs/MCP-BEST-PRACTICES.md` | MCP guide |

### Compliance stack (read-only reference)

| Component | Purpose | Projects using |
|-----------|---------|----------------|
| `compliance/COMPLIANCE_ARCH.md` | Invariants contract | vibe-coding |
| `compliance/api.py` | Reference API | vibe-coding |
| `compliance/sanctions_check.py` | OFAC Watchman integration | vibe-coding |
| `compliance/audit_trail.py` | ClickHouse audit logging | vibe-coding |

### Scripts (shared utilities)

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/sync-all.sh` | Sync all projects from registry | `bash sync-all.sh [--dry-run]` |
| `scripts/onboard-project.sh` | Onboard new project | `./onboard-project.sh <name> <type>` |
| `scripts/check-agent-instructions.sh` | Verify instruction hierarchy | Debug agent setup |

---

## Sync protocol

### Sync protocol

#### Manual sync (current method)

```bash
cd ~/developer
bash scripts/sync-all.sh
```

#### Automatic sync (future state)

**Post-commit hook** (`~/developer/.git/hooks/post-commit`):
- On commit to `~/developer/`: auto-run sync-all.sh
- Detect changed components
- Identify affected projects
- Commit and push to all repos automatically

### Change management

### Safe changes (auto-sync allowed)

- Documentation updates
- Comment additions
- Formatting fixes
- Test additions

### Review-required changes (manual sync)

- Configuration changes (.qoder/config.yml)
- Instruction hierarchy changes (AGENTS.md)
- Compliance invariant changes (COMPLIANCE_ARCH.md)
- Script logic changes

### Sync approval workflow

1. Change committed to `~/developer/`
2. User runs `bash scripts/sync-to-project.sh <project>`
3. Script shows diff for each target
4. User approves/rejects per project
5. Changes applied to targets

---

## Project isolation enforcement

**CRITICAL:** This repository contains SHARED templates and MASTER scenario copies.

When working IN this repository:
- Edit templates for distribution
- Test changes before syncing
- Document breaking changes
- Maintain MiroFish scenario templates (MASTER)

When working IN a target project:
- Use synced templates as starting point
- Local overrides allowed and expected (especially MIROFISH-SCENARIOS.md)
- Report useful improvements back to developer/
- Project-specific scenarios stay in the project (not synced back)

---

## Testing requirements

Before syncing any component:

| Component type | Required validation |
|----------------|---------------------|
| Config files | Syntax check + dry-run |
| Scripts | Shellcheck + manual test |
| Templates | Bootstrap test project |
| Compliance | Compare with production |
| Documentation | Link check + build |

---

## Version tracking

Each synced component should include:

```markdown
**Source:** `~/developer/{path}`  
**Synced:** YYYY-MM-DD  
**Version:** X.Y
```

---

## Rollback procedure

If a synced change breaks a project:

1. Identify the broken component
2. Restore previous version in target project
3. Report issue to `~/developer/`
4. Fix in developer repo
5. Re-sync when ready

---

## Quick start for new components

To add a new shared component:

1. Create in appropriate directory (`scripts/`, `templates/`, etc.)
2. Add documentation header with purpose and usage
3. Test in isolation
4. Commit to `~/developer/`
5. Manually sync to interested projects
6. Update this AGENTS.md if needed

---

## People and responsibilities

| Role | Person | Scope |
|------|--------|-------|
| Component author | Any developer | Create/maintain specific components |
| Sync coordinator | Moriel Carmi | Approve cross-project distribution |
| Integration tester | Qoder CLI | Validate synced components work |

---

## Files reference

| File | Purpose | Sync targets |
|------|---------|--------------|
| `AGENTS.md` | This file — three-partner agent instructions | All projects |
| `.qoder/config.yml` | Qoder CLI configuration | All projects |
| `.qoder/context.md` | Qoder execution contract (UNIVERSAL) | All projects |
| `docs/COLLAB.md` | Collaboration documentation | All projects |
| `docs/MCP-BEST-PRACTICES.md` | MCP server guide | All projects |
| `docs/PROJECT-REGISTRY.csv` | Project registry for sync-all.sh | Internal use |
| `scripts/sync-all.sh` | Multi-repo sync automation | Internal use |
| `scripts/onboard-project.sh` | New project onboarding | Internal use |
| `scripts/check-agent-instructions.sh` | Diagnostic tool | All projects |
| `compliance/COMPLIANCE_ARCH.md` | Compliance invariants | vibe-coding |

---

## Definition of done (for component development)

A component is ready for sync when:

- [ ] Implementation complete and tested
- [ ] Documentation header added
- [ ] No project-specific assumptions
- [ ] Works in isolation
- [ ] Backward-compatible or migration documented
- [ ] Committed to `~/developer/`
- [ ] Synced to at least one target project

---

## Next steps (pending work)

- [x] Create sync-all.sh for automated distribution
- [x] Update AGENTS.md with three-partner architecture
- [x] Create onboard-project.sh for new project onboarding
- [ ] Create git post-commit hook for auto-sync
- [ ] Deploy full Qoder stack to banxe-mirofish
- [ ] Create project-specific MIROFISH-SCENARIOS.md for all 6 projects
- [ ] Update MEMORY.md with three-partner documentation
