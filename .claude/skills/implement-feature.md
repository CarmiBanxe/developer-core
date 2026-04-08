---
name: implement-feature
description: Реализация новой фичи в banxe-emi-stack по Spec-First — от user story до IL DONE
---
# Skill: Implement Feature

## Когда применять
- Новая функциональность из SPEC-TEMPLATE.md
- Новый router / endpoint
- Новый domain service

## Шаги (строго по порядку)

### 1. Прочитать спецификацию
```
Открыть: ~/developer/spec-first/SPEC-TEMPLATE.md
Найти: User Story для фичи
Выписать: acceptance criteria, edge cases, Auth role, FCA rule
```

### 2. Определить department
```
Открыть: banxe-architecture/docs/DEPARTMENT-MAP.md
Найти: к какому bounded_context относится фича (CTX-NN)
```

### 3. Создать Port (Protocol ABC)
```python
# Файл: services/{domain}/{feature}_port.py
from typing import Protocol
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class FeatureRequest:
    # Всегда frozen=True (I-05, quality rule)
    ...

@dataclass(frozen=True)
class FeatureResult:
    ...

class FeaturePort(Protocol):
    def execute(self, request: FeatureRequest) -> FeatureResult:
        """One-line summary.
        
        Args:
            request: Validated feature request.
        Returns:
            FeatureResult with outcome and audit data.
        """
        ...
```

### 4. Создать Service (бизнес-логика)
```python
# Файл: services/{domain}/{feature}_service.py
class FeatureService:
    def __init__(self, port: FeaturePort) -> None:
        self._port = port
    
    def execute(self, request: FeatureRequest) -> FeatureResult:
        # Бизнес-логика здесь
        # Всегда: validate → execute → audit → return
        ...
```

### 5. Создать Mock Adapter
```python
# Файл: services/{domain}/mock_{feature}_adapter.py
class MockFeatureAdapter:
    """In-memory adapter for tests and sandbox mode."""
    def execute(self, request: FeatureRequest) -> FeatureResult:
        # Realistic mock behaviour
        ...
```

### 6. Создать Real Adapter stub
```python
# Файл: services/{domain}/{provider}_{feature}_adapter.py
class ProviderFeatureAdapter:
    """Live adapter — NotImplementedError until BT-NNN unblocked."""
    def execute(self, request: FeatureRequest) -> FeatureResult:
        raise NotImplementedError("BT-NNN: {provider} API key required")
```

### 7. Написать тесты
```bash
# Файл: tests/test_{feature}_service.py
# Минимум 15 тестов:
# - happy path (at least 3 scenarios)
# - edge cases (boundary values)
# - negative tests (invalid input, auth fail, timeout)
# - entity_type variants (INDIVIDUAL + COMPANY if applicable)
# - audit trail written (I-24)
```

### 8. Запустить quality gate
```bash
cd ~/banxe-emi-stack
bash scripts/quality-gate.sh --fast
# ЕСЛИ FAIL → исправить → повторить шаг 8
# Только PASS → перейти к шагу 9
```

### 9. Обновить IL
```
Открыть: banxe-architecture/INSTRUCTION-LEDGER.md
Добавить: IL-NNN запись со статусом DONE + proof
```

### 10. Commit + push
```bash
git add services/{domain}/ tests/test_{feature}*.py
git commit -m "feat(IL-NNN): implement {feature} service + mock adapter + tests"
git push
```

### 11. Verify
```bash
python3 ~/developer/spec-first/audit/spec_first_auditor.py
# Для сложных фич — вызвать spec-first-auditor
```

## Чеклист перед marking DONE
- [ ] Port создан (`*_port.py`)
- [ ] Service создан (`*_service.py`)
- [ ] Mock adapter создан
- [ ] ≥15 тестов, coverage ≥80% для новых файлов
- [ ] quality-gate.sh PASS
- [ ] IL запись обновлена
- [ ] Pushed to GitHub
