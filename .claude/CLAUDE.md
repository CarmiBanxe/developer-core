# CLAUDE.md — Developer Plane (developer-core)
**Repo:** CarmiBanxe/developer-core | **Plane:** Developer | **Updated:** 2026-04-08

---

## Spec-First Methodology (IL-045)

This plane contains the **Spec-First development infrastructure** for Banxe AI Bank.
All methodology files live in `~/developer/`. Nothing here goes into `banxe-emi-stack/` or `banxe-architecture/`.

### File Locations (MANDATORY — do not move)

| File | Location | Purpose |
|------|----------|---------|
| PROJECTIDEA.md | `spec-first/PROJECTIDEA.md` | Project vision, stack, metrics |
| SPEC-TEMPLATE.md | `spec-first/SPEC-TEMPLATE.md` | User stories, DB schema, API endpoints |
| spec_first_auditor.py | `spec-first/audit/spec_first_auditor.py` | Block verification script |
| audit_log.jsonl | `spec-first/audit/audit_log.jsonl` | Append-only audit log |
| quality.md | `rules/quality.md` | Code quality rules |
| compliance.md | `rules/compliance.md` | FCA compliance rules |
| testing.md | `rules/testing.md` | Test patterns + coverage rules |
| implement-feature.md | `skills/implement-feature.md` | Step-by-step feature implementation |
| create-migration.md | `skills/create-migration.md` | SQL migration skill |
| deploy-gmktec.md | `skills/deploy-gmktec.md` | GMKtec deployment skill |
| database-architect.md | `agents/database-architect.md` | DB schema specialist |
| backend-engineer.md | `agents/backend-engineer.md` | Port+Service+Adapter implementer |
| compliance-specialist.md | `agents/compliance-specialist.md` | FCA compliance reviewer |
| qa-reviewer.md | `agents/qa-reviewer.md` | Test quality + gate runner |
| devops-engineer.md | `agents/devops-engineer.md` | GMKtec infra specialist |

### Spec-First Passport (banxe-architecture)

Agent passport: `banxe-architecture/agents/passports/spec_first_auditor.yaml`
Passport lives in architecture repo (it IS an architectural artifact).

---

## EXECUTION ORDER (mandatory for all Banxe feature work)

Before ANY implementation in `banxe-emi-stack`:

```
1. Read SPEC-TEMPLATE.md → find user story
2. Write IL entry in banxe-architecture/INSTRUCTION-LEDGER.md (I-28)
3. Create Port → Service → MockAdapter (hexagonal pattern)
4. Write tests (≥15, coverage ≥80%)
5. bash scripts/quality-gate.sh PASS
6. Update IL with proof → commit → push
7. Run spec-first-auditor: python3 ~/developer/spec-first/audit/spec_first_auditor.py
```

No steps may be skipped. quality-gate.sh is always the final blocker.

---

## Territory Rules

ПРАВИЛО: Если файл описывает КАК РАЗРАБОТЧИК РАБОТАЕТ → `~/developer/`
         Если файл описывает ЧТО СИСТЕМА ДЕЛАЕТ → `banxe-emi-stack/`
         Если файл описывает ПОЧЕМУ ТАК РЕШИЛИ → `banxe-architecture/`

**Must NOT appear in banxe-emi-stack/.claude/:**
- rules/quality.md, rules/compliance.md, rules/testing.md
- skills/implement-feature.md, skills/create-migration.md, skills/deploy-gmktec.md
- agents/database-architect.md, etc.

---

## spec-first-auditor

Run after each development block:
```bash
python3 ~/developer/spec-first/audit/spec_first_auditor.py        # all blocks
python3 ~/developer/spec-first/audit/spec_first_auditor.py 3      # specific block
```

Exit 0 = PASS. Exit 1 = FAIL — do not proceed to next block.

---

## Key References

| Resource | Path |
|----------|------|
| Project spec | `~/developer/spec-first/SPEC-TEMPLATE.md` |
| Project idea | `~/developer/spec-first/PROJECTIDEA.md` |
| IL ledger | `~/banxe-architecture/INSTRUCTION-LEDGER.md` |
| Skills orchestration | `~/banxe-architecture/docs/SKILLS-ORCHESTRATION.md` |
| Invariants | `~/banxe-architecture/INVARIANTS.md` |
| Quality gate | `~/banxe-emi-stack/scripts/quality-gate.sh` |
