# Developer Core — Central Repository for Shared Components

**Location:** `~/developer/`  
**Purpose:** Single source of truth for agent configurations, compliance stack, and automation  
**Version:** 1.0 | 2026-04-03

---

## What This Repository Contains

This is the **central hub** for all shared components used across your projects:

| Directory | Contents | Synced to |
|-----------|----------|-----------|
| `.aider.conf.yml/` | Aider CLI configs | All projects |
| `docs/` | Collaboration docs (COLLAB.md, MCP best practices) | All projects |
| `scripts/` | Automation & diagnostic tools | All projects |
| `templates/` | Project bootstrap templates | Copy on demand |
| `agents/` | Agent skills & subagents | All projects |
| `compliance/` | AML/KYC reference implementation | vibe-coding only |

---

## Quick Start

### For new projects

```bash
# Clone this repository (if not already present)
cd ~/new-project
bash ~/developer/scripts/sync-to-project.sh new-project
```

### For existing projects

```bash
# Sync latest components to a project
cd ~/developer
bash scripts/sync-to-project.sh vibe-coding
```

### Verify setup

```bash
# Check instruction hierarchy in any project
cd ~/project
bash scripts/check-agent-instructions.sh
```

---

## Architecture

```
┌────────────────────────────────────────────────────┐
│               ~/developer/ (CORE)                  │
│                                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │ .aider.conf.yml/  │  │  docs/   │  │    scripts/      │ │
│  │ config   │  │ COLLAB   │  │   sync-to-*.sh   │ │
│  └──────────┘  └──────────┘  └──────────────────┘ │
│                                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │ agents/  │  │templates/│  │   compliance/    │ │
│  │ skills   │  │ bootstrap│  │  COMPLIANCE_ARCH │ │
│  └──────────┘  └──────────┘  └──────────────────┘ │
└────────────────────────────────────────────────────┘
              ↓         ↓         ↓
    ┌─────────┴─────────┴─────────┴─────────┐
    │                                       │
┌───▼───────┐  ┌───────────┐  ┌────────────▼───┐
│vibe-coding│  │ guiyon    │  │  MetaClaw      │
│           │  │           │  │                │
│ AGENTS.md │  │ AGENTS.md │  │  AGENTS.md     │
│ .aider.conf.yml/   │  │ .aider.conf.yml/   │  │  .aider.conf.yml/       │
│ docs/     │  │ docs/     │  │  docs/         │
└───────────┘  └───────────┘  └────────────────┘
```

---

## Instruction Hierarchy

Agents working in any project follow this priority:

1. **Explicit user instruction** (highest authority)
2. **Repository-level contracts**:
   - `CLAUDE.md` — project context
   - `.aider.conf.yml` — Aider execution contract
   - `AGENTS.md` — agent instructions
   - `COLLAB.md` — collaboration pattern
   - `COMPLIANCE_ARCH.md` — compliance invariants (if applicable)
3. **Global defaults**: `~/.claude/CLAUDE.md`

**Rule:** Closer to working directory = higher priority.

---

## Sync Workflow

### Manual sync (current)

```bash
cd ~/developer
bash scripts/sync-to-project.sh <project-name>
```

The script will:
1. Show what components will be synced
2. Create backup in target project
3. Copy files
4. Verify success
5. Show git status

### Rollback

If something breaks:

```bash
cd ~/target-project
cp -r .sync-backup-*/{component} .
git restore {component}
```

---

## Component Catalog

### Always synced (all projects)

| Component | Purpose | When to update |
|-----------|---------|----------------|
| `.aider.conf.yml` | Aider CLI configuration | WSL optimizations, MCP settings |
| `.aider.conf.yml` | Aider execution contract | Role definitions, scope rules |
| `AGENTS.md` | Agent instructions template | Collaboration model changes |
| `docs/COLLAB.md` | Single-terminal synergy docs | Workflow updates |
| `docs/MCP-BEST-PRACTICES.md` | MCP server guide | New best practices |
| `scripts/check-agent-instructions.sh` | Diagnostic tool | Enhanced diagnostics |

### Selective sync

| Component | Target | Purpose |
|-----------|--------|---------|
| `compliance/COMPLIANCE_ARCH.md` | vibe-coding | FCA compliance invariants |
| `templates/project-template/` | New projects | Bootstrap structure |

---

## Version Tracking

Components are versioned implicitly via git commits.

After syncing, check target project:

```bash
cd ~/vibe-coding
git log --oneline -5
```

Sync commits should have message format:
```
sync: Update from developer core (YYYY-MM-DD)
```

---

## Testing Before Sync

Before syncing to production projects:

1. **Test in developer repo:**
   ```bash
   cd ~/developer
   bash scripts/check-agent-instructions.sh
   ```

2. **Test in non-production project first** (if available)

3. **Verify syntax:**
   ```bash
   # Shell scripts
   shellcheck scripts/*.sh
   
   # YAML configs
   python3 -c "import yaml; yaml.safe_load(open('.aider.conf.yml'))"
   
   # JSON
   python3 -c "import json; json.load(open('some-file.json'))"
   ```

---

## Adding New Components

To add a new shared component:

1. **Create in appropriate directory:**
   ```bash
   mkdir -p ~/developer/new-component
   ```

2. **Add documentation header:**
   ```markdown
   # Component Name
   
   **Purpose:** What this does
   **Sync targets:** Which projects receive this
   **Version:** 1.0 | YYYY-MM-DD
   ```

3. **Test in isolation**

4. **Commit to developer:**
   ```bash
   cd ~/developer
   git add new-component/
   git commit -m "feat: Add new-component for distribution"
   ```

5. **Sync manually first:**
   ```bash
   bash scripts/sync-to-project.sh vibe-coding
   ```

6. **Update AGENTS.md** if component changes catalog

---

## Project Isolation

**CRITICAL:** This repository contains **templates**, not project-specific code.

### Do:
- Edit for downstream distribution
- Test before syncing
- Document breaking changes

### Don't:
- Implement project-specific features here
- Hardcode paths to specific projects
- Run production services from here

---

## Related Repositories

| Repository | Path | Purpose |
|------------|------|---------|
| vibe-coding | `~/vibe-coding/` | Banxe AI Bank — primary project |
| collaboration | `~/collaboration/` | Claude Code + Aider CLI setup docs |
| guiyon | `~/guiyon/` | Separate entity (excluded from Banxe) |
| MetaClaw | `~/MetaClaw/` | Crypto AML project |

---

## People

| Role | Person | Responsibility |
|------|--------|----------------|
| CEO/CTIO | Moriel Carmi | Final approval on syncs |
| Developer | You | Component creation/maintenance |

---

## Troubleshooting

### Sync fails with permission error

```bash
chmod +x ~/developer/scripts/sync-to-project.sh
```

### Target project has local overrides

The sync script will backup but still copy. Review after sync:

```bash
cd ~/target-project
git diff
```

Restore specific files if needed:
```bash
git restore CLAUDE.md  # Keep project-specific version
```

### Component not found after sync

Check if component exists in developer:
```bash
ls -la ~/developer/{component}
```

Check sync script includes it:
```bash
grep "{component}" ~/developer/scripts/sync-to-project.sh
```

---

## Definition of Done

A component is ready for distribution when:

- [ ] Implemented and tested in `~/developer/`
- [ ] Documentation header added
- [ ] No project-specific assumptions
- [ ] Syntax validated
- [ ] Synced to at least one target successfully
- [ ] No breaking changes (or migration documented)

---

## License

All components in this repository are internal-use only unless otherwise specified.

Compliance components (under `compliance/`) are subject to FCA regulations and cannot be redistributed externally without review.
