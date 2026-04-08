# /gsd-health

Полный health check системы: spec-first audit + quality gate + IL status + infra.

## Что делает
1. Запускает **gsd-verifier** (read-only, no fixes)
2. `python3 ~/developer/spec-first/audit/spec_first_auditor.py --full`
3. `cd ~/banxe-emi-stack && bash scripts/quality-gate.sh`
4. Проверяет незакрытые IL в INSTRUCTION-LEDGER.md
5. Проверяет STATE.md на BLOCKED-задачи
6. Опционально: SSH health check GMKtec сервисов (с QRAA)

## Выход — Health Report
```
## Health Report — {дата}
### Spec-First Audit
  Blocks 0-7: PASS | FAIL (список failed)

### Quality Gate
  Tests: N passed, M failed
  Coverage: X% overall
  Semgrep: N violations
  Ruff: N violations

### IL Status
  Total: N | DONE: M | IN_PROGRESS: K | PENDING: J

### BLOCKED Tasks
  {список заблокированных задач}

### VERDICT: HEALTHY | ISSUES FOUND
```

## Когда использовать
- Утром перед началом работы
- Перед деплоем
- После длинной серии изменений
- По запросу CEO

## Аргументы
```
/gsd-health           # полный check (без GMKtec SSH)
/gsd-health --infra   # включая GMKtec services (QRAA required)
```
