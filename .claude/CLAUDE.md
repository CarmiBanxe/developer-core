# CLAUDE.md — Developer Plane (developer-core)
**Repo:** CarmiBanxe/developer-core | **Plane:** Developer | **Updated:** 2026-04-08 (GSD v2)

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
| quality.md | `.claude/rules/quality.md` | Code quality rules |
| compliance.md | `.claude/rules/compliance.md` | FCA compliance rules |
| testing.md | `.claude/rules/testing.md` | Test patterns + coverage rules |
| implement-feature.md | `.claude/skills/implement-feature.md` | Step-by-step feature implementation |
| create-migration.md | `.claude/skills/create-migration.md` | SQL migration skill |
| deploy-gmktec.md | `.claude/skills/deploy-gmktec.md` | GMKtec deployment skill |
| gsd-planner.md | `.claude/agents/gsd-planner.md` | GSD: decompose → sprint plan |
| gsd-executor.md | `.claude/agents/gsd-executor.md` | GSD: execute plan → call dev agents |
| gsd-verifier.md | `.claude/agents/gsd-verifier.md` | GSD: final verification (read-only) |
| database-architect.md | `.claude/agents/database-architect.md` | DB schema specialist |
| backend-engineer.md | `.claude/agents/backend-engineer.md` | Port+Service+Adapter implementer |
| compliance-specialist.md | `.claude/agents/compliance-specialist.md` | FCA compliance reviewer |
| qa-reviewer.md | `.claude/agents/qa-reviewer.md` | Test quality + gate runner |
| devops-engineer.md | `.claude/agents/devops-engineer.md` | GMKtec infra specialist |
| gsd-new-project.md | `.claude/commands/gsd-new-project.md` | Start new sprint from SPEC |
| gsd-plan-phase.md | `.claude/commands/gsd-plan-phase.md` | Plan next phase from ROADMAP |
| gsd-execute-plan.md | `.claude/commands/gsd-execute-plan.md` | Execute current PROJECT.md |
| gsd-quick.md | `.claude/commands/gsd-quick.md` | Single atomic task, no planning |
| gsd-health.md | `.claude/commands/gsd-health.md` | Full system health check |
| gsd-help.md | `.claude/commands/gsd-help.md` | GSD commands reference |
| PROJECT.md | `.planning/PROJECT.md` | Current sprint — tasks + agents |
| STATE.md | `.planning/STATE.md` | Task status (DONE/IN_PROGRESS/BLOCKED) |
| REQUIREMENTS.md | `.planning/REQUIREMENTS.md` | Technical constraints |
| ROADMAP.md | `.planning/roadmap/ROADMAP.md` | Long-term phases plan |

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
- `.claude/rules/quality.md`, `.claude/rules/compliance.md`, `.claude/rules/testing.md`
- `.claude/skills/implement-feature.md`, `.claude/skills/create-migration.md`, `.claude/skills/deploy-gmktec.md`
- `.claude/agents/database-architect.md`, `.claude/agents/backend-engineer.md`, `.claude/agents/qa-reviewer.md`

---

## spec-first-auditor

Run after each development block:
```bash
python3 ~/developer/spec-first/audit/spec_first_auditor.py        # all blocks
python3 ~/developer/spec-first/audit/spec_first_auditor.py 3      # specific block
```

Exit 0 = PASS. Exit 1 = FAIL — do not proceed to next block.

---

## GSD Framework (Get Shit Done)

GSD оркестрирует разработку через 3 мета-агента и 6 slash команд.

### Команды

| Команда | Назначение |
|---------|-----------|
| `/gsd-new-project` | Начать новый спринт (читает SPEC → создаёт PROJECT.md) |
| `/gsd-plan-phase` | Планировать следующую фазу по ROADMAP |
| `/gsd-execute-plan` | Выполнить текущий PROJECT.md полностью |
| `/gsd-quick "задача"` | Одна атомарная задача без планирования |
| `/gsd-health` | Health check: audit + quality gate + IL status |
| `/gsd-help` | Справка по всем командам |

### GSD Workflow
```
/gsd-new-project  →  PROJECT.md создан
/gsd-execute-plan →  все задачи выполнены
/gsd-health       →  VERDICT: SPRINT APPROVED
```

### State Management
| Файл | Назначение |
|------|-----------|
| `.planning/PROJECT.md` | Текущий спринт — задачи + агенты + зависимости |
| `.planning/STATE.md` | Статус задач (DONE/IN_PROGRESS/BLOCKED) |
| `.planning/REQUIREMENTS.md` | Технические требования и ограничения |
| `.planning/roadmap/ROADMAP.md` | Долгосрочный план фаз |

---

## Key References

| Resource | Path |
|----------|------|
| Project spec | `~/developer/spec-first/SPEC-TEMPLATE.md` |
| Project idea | `~/developer/spec-first/PROJECTIDEA.md` |
| Sprint plan | `~/developer/.planning/PROJECT.md` |
| State | `~/developer/.planning/STATE.md` |
| IL ledger | `~/banxe-architecture/INSTRUCTION-LEDGER.md` |
| Skills orchestration | `~/banxe-architecture/docs/SKILLS-ORCHESTRATION.md` |
| Invariants | `~/banxe-architecture/INVARIANTS.md` |
| Quality gate | `~/banxe-emi-stack/scripts/quality-gate.sh` |
