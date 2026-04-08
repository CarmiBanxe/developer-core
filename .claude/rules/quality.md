---
glob: "services/**/*.py"
---
# Quality Rules — Banxe AI Bank (I-29 Documentation Standard)

## Type Annotations
- Все функции: type hints обязательны (mypy-compatible)
- Return type явный: `def foo() -> dict[str, str]:`, не `-> dict`
- `Optional[X]` → предпочтительно `X | None` (Python 3.10+)
- `from __future__ import annotations` в каждом файле с forward refs

## Docstrings
- Все публичные методы и классы: docstring (Google style)
- Формат: одна строка summary, затем Args/Returns/Raises если нужно
- Ports (Protocol ABC): обязательно документировать каждый метод

## Secrets и конфигурация
- Никаких hardcoded passwords, tokens, API keys в коде
- Только `os.environ.get("KEY")` или `os.getenv("KEY", "default")`
- Все .env переменные задокументированы в `.env.example`

## Imports
- Порядок: stdlib → third-party → local (isort-compatible)
- Абсолютные импорты внутри пакета: `from services.payment.payment_port import PaymentPort`
- Никаких `from module import *`

## Размер файлов
- Максимум 300 строк на файл. Больше → разделить на port + service + adapter
- Каждый новый Protocol/ABC — в отдельном файле `*_port.py`
- Каждый service — в отдельном файле `*_service.py`
- Каждый adapter — в отдельном файле `{provider}_*_adapter.py`

## Dataclasses
- `frozen=True` для всех dataclass (immutability)
- `@dataclass(frozen=True)` не `@dataclass` (mutable)
- Финансовые поля: `Decimal`, не `float` (I-05)

## Именование
- snake_case для функций и переменных
- PascalCase для классов
- UPPER_CASE для константы
- `*_port.py` для Protocol/ABC, `*_service.py` для business logic, `*_adapter.py` для adapters

## Запреты
- Никаких `float()` в финансовом контексте (I-05)
- Никаких `eval()`, `exec()` (semgrep rule)
- Никаких bare `except:` (ruff E722 + semgrep)
- Никаких `subprocess.shell=True` с user input (injection)
