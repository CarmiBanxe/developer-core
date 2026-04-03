# Synergy Deployment — Внедрение технологии синергии

**Repository:** `~/developer/docs/`  
**Version:** 1.0 | 2026-04-03  
**Author:** Developer Core Team  
**Status:** ACTIVE DEPLOYMENT

---

## Executive Summary

Технология **Claude Code + Qoder CLI Single-Terminal Synergy** автоматически внедряется во все проекты через центральный репозиторий `~/developer/`.

### Принцип

```
~/developer/ (CORE)
    ↓ sync
┌───┴────────────┬──────────────┬─────────────┐
│                │              │             │
vibe-coding/   guiyon/       ss1/        MetaClaw/
(Banxe)        (Legal)        (Legal)     (Crypto)
```

---

## Architecture

### Global Layer (~/.claude/)

| File | Purpose | Status |
|------|---------|--------|
| `~/.claude/CLAUDE.md` | Global collaboration contract | ✅ Deployed |
| `~/.claude/settings.json` | MCP server auto-load | ✅ Deployed |

### Project Layer ({project}/)

| Component | Source | Target | Status |
|-----------|--------|--------|--------|
| `AGENTS.md` | `~/developer/AGENTS.md` | `{project}/AGENTS.md` | Per project |
| `.qoder/context.md` | `~/developer/.qoder/context.md` | `{project}/.qoder/context.md` | Per project |
| `docs/COLLAB.md` | `~/developer/docs/COLLAB.md` | `{project}/docs/COLLAB.md` | Per project |
| `docs/MCP-BEST-PRACTICES.md` | `~/developer/docs/MCP-BEST-PRACTICES.md` | `{project}/docs/MCP-BEST-PRACTICES.md` | Per project |
| `scripts/check-agent-instructions.sh` | `~/developer/scripts/` | `{project}/scripts/` | Per project |

### Compliance Layer (Banxe only)

| Component | Source | Target | Status |
|-----------|--------|--------|--------|
| `compliance/COMPLIANCE_ARCH.md` | `~/developer/compliance/` | `vibe-coding/src/compliance/` | ✅ Deployed |

---

## Deployment Phases

### Phase 1: Banxe AI Bank (CURRENT)

**Target:** `vibe-coding/` + `collaboration/` + `MetaClaw/`

**Components:**
- Full synergy stack
- MCP auto-load
- Compliance invariants
- WSL optimizations

**Status:** IN PROGRESS

**Commands:**
```bash
cd ~/developer
bash scripts/sync-to-project.sh vibe-coding
bash scripts/sync-to-project.sh collaboration
bash scripts/sync-to-project.sh MetaClaw
```

---

### Phase 2: Legal Projects

**Target:** `guiyon/` + `ss1/`

**Components:**
- Core synergy (no compliance)
- Legal-specific instructions
- Shared GUIYON→SS1 technology transfer

**Status:** PENDING

**Commands:**
```bash
cd ~/developer
bash scripts/sync-to-project.sh guiyon
bash scripts/sync-to-project.sh ss1
```

---

## Pre-Deployment Checklist

Before syncing to any project:

- [ ] Developer repo committed and tested
- [ ] Syntax validation passed (YAML, JSON, shell)
- [ ] Diagnostic script runs successfully
- [ ] Backup strategy documented
- [ ] Rollback plan reviewed

---

## Deployment Command

```bash
# From developer repository
cd ~/developer

# Sync to specific project
bash scripts/sync-to-project.sh <project-name>

# Example
bash scripts/sync-to-project.sh vibe-coding
```

### What the script does:

1. Validates target project exists
2. Creates timestamped backup
3. Copies components from developer/
4. Sets executable permissions on scripts
5. Verifies all files present
6. Shows git status in target

---

## Post-Deployment Verification

After sync, run in target project:

```bash
cd ~/target-project
bash scripts/check-agent-instructions.sh
```

**Expected output:**
```
════════════════════════════════════════════
  Active Agent Instructions Checker
════════════════════════════════════════════

Repository root: /home/mmber/vibe-coding

=== GLOBAL INSTRUCTIONS ===
✓ ~/.claude/CLAUDE.md exists
  Key rules:
  ### Core rule
  ### Project isolation
  ### Collaboration behavior

=== PROJECT INSTRUCTIONS ===
✓ CLAUDE.md exists
✓ AGENTS.md exists
✓ docs/COLLAB.md exists

=== QODER CONTEXT ===
✓ .qoder/context.md exists

=== MCP CONFIG ===
✓ ~/.claude/settings.json exists
  Qoder MCP server: configured

════════════════════════════════════════════
  Instruction hierarchy is COMPLETE
════════════════════════════════════════════
```

---

## Testing Synergy

### Test 1: Basic invocation
```bash
cd ~/vibe-coding
claude
# Should load automatically with MCP
```

### Test 2: Context loading
```bash
cd ~/vibe-coding
claude
# Ask: "What instruction files are active?"
# Should list: AGENTS.md, .qoder/context.md, CLAUDE.md, COLLAB.md
```

### Test 3: Repository isolation
```bash
cd ~/vibe-coding
claude
# Ask: "Read ../guiyon/CLAUDE.md"
# Should refuse: cross-repository access denied
```

### Test 4: Compliance invariant protection
```bash
cd ~/vibe-coding
claude
# Ask: "Change minMatch to 0.90 in sanctions_check.py"
# Should warn: COMPLIANCE_ARCH.md invariant violation
```

---

## Rollback Procedure

If deployment causes issues:

### Immediate rollback
```bash
cd ~/target-project
cp -r .sync-backup-*/{component} .
git restore {component}
```

### Full disable
```bash
# Edit ~/.claude/settings.json
# Remove or comment out mcpServers section

# Restart Claude session
exit
cd ~/project
claude  # Now without MCP
```

---

## Deployment Log

| Date | Project | Version | Status | Commit | Notes |
|------|---------|---------|--------|--------|-------|
| 2026-04-03 | vibe-coding | 1.0 | ✅ COMPLETE | dcdbf45 | Banxe AI Bank main repo |
| 2026-04-03 | collaboration | 1.0 | ✅ COMPLETE | 4018078 | Infrastructure sync |
| 2026-04-03 | MetaClaw | 1.0 | ✅ COMPLETE | 141d421 | Crypto AML module |
| TBD | guiyon | 1.0 | ⏳ PENDING | — | Legal projects phase |
| TBD | ss1 | 1.0 | ⏳ PENDING | — | Sub-project of GUIYON |

---

## Support & Troubleshooting

### Issue: MCP server not starting

**Check:**
```bash
ps aux | grep qodercli
qodercli --version
```

**Fix:**
```bash
pkill -f "qodercli mcp-server"
cd ~/project
claude
```

### Issue: Context files missing

**Check:**
```bash
ls -la AGENTS.md .qoder/context.md docs/COLLAB.md
```

**Fix:**
```bash
cd ~/developer
bash scripts/sync-to-project.sh <project>
```

### Issue: WSL hangs

**Fix:**
```yaml
# In ~/.qoder/config.yml
wsl:
  watchPolling: true
  watchInterval: 1000
  maxConcurrentOperations: 2
```

---

## Next Steps

1. **Complete Banxe deployment** (vibe-coding, collaboration, MetaClaw)
2. **Test all components** in production workflow
3. **Deploy to legal projects** (guiyon, ss1)
4. **Monitor and iterate** based on feedback

---

## Related Documents

- `COLLAB.md` — Single-terminal synergy pattern
- `MCP-BEST-PRACTICES.md` — MCP server configuration guide
- `SYNERGY-ROLLBACK.md` — Rollback plan
- `../AGENTS.md` — Agent instructions template
- `../compliance/COMPLIANCE_ARCH.md` — Compliance invariants
