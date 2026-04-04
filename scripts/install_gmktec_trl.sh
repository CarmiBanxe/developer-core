#!/usr/bin/env bash
# install_gmktec_trl.sh — TRL + HuggingFace стек для GMKtec (AMD Ryzen AI MAX+)
#
# Замена OpenRLHF (требует NVIDIA CUDA) на TRL (работает на CPU/AMD).
# TRL покрывает SFT, DPO, GRPO — то же самое preference alignment без Ray/vLLM.
#
# Запуск ЛОКАЛЬНО (деплоит на GMKtec):
#   bash ~/collaboration/scripts/install_gmktec_trl.sh
#
# Запуск ПРЯМО НА GMKtec:
#   bash install_gmktec_trl.sh --local
#
set -euo pipefail

REMOTE_HOST="${GMKTEC_HOST:-gmktec}"
LOG_FILE="/tmp/install_trl_$(date +%Y%m%d_%H%M%S).log"
SEP="=================================================="

log()  { echo "$@" | tee -a "$LOG_FILE"; }
step() { echo ""; log "$SEP"; log "  $1"; log "$SEP"; }
ok()   { log "  ✅ $*"; }
warn() { log "  ⚠️  $*"; }
fail() { log "  ❌ $*"; exit 1; }

# ─── Режим: локальный или SSH ─────────────────────────────────
LOCAL_MODE=0
for arg in "$@"; do [[ "$arg" == "--local" ]] && LOCAL_MODE=1; done

run() {
    if [ "$LOCAL_MODE" = "1" ]; then
        bash -c "$1" 2>&1 | tee -a "$LOG_FILE"
    else
        ssh "$REMOTE_HOST" "$1" 2>&1 | tee -a "$LOG_FILE"
    fi
}

log ""
log "  TRL Installer — GMKtec / AMD Ryzen AI MAX+"
log "  $(date)"
log "  Режим: $([ $LOCAL_MODE = 1 ] && echo 'local' || echo "SSH → $REMOTE_HOST")"
log "  Log: $LOG_FILE"

# ──────────────────────────────────────────────────────────────
# ШАГ 1: Проверяем машину
# ──────────────────────────────────────────────────────────────
step "1/4  Проверяем окружение"

run "python3 --version"
run "uname -m"

# Проверяем что CUDA нет (ожидаемо на AMD)
if run "nvidia-smi &>/dev/null 2>&1 && echo HAS_NVIDIA || echo NO_NVIDIA" | grep -q "NO_NVIDIA"; then
    ok "AMD машина — CUDA нет, TRL через CPU/torch (ожидаемо)"
else
    warn "NVIDIA обнаружен — OpenRLHF предпочтительнее для GPU-обучения"
fi

# ──────────────────────────────────────────────────────────────
# ШАГ 2: Устанавливаем TRL стек
# ──────────────────────────────────────────────────────────────
step "2/4  Устанавливаем TRL + HuggingFace стек"

PACKAGES=(
    "trl"           # DPOTrainer, GRPOTrainer, SFTTrainer
    "transformers"  # модели HuggingFace
    "peft"          # LoRA / QLoRA адаптеры
    "accelerate"    # device map, CPU offload
    "datasets"      # HuggingFace datasets
    "bitsandbytes"  # квантизация (опционально, может пропустить без GPU)
)

for pkg in "${PACKAGES[@]}"; do
    log "  pip install $pkg..."
    run "pip install $pkg --break-system-packages -q 2>&1 | tail -3" || \
    warn "$pkg — пропущен (не критично)"
done

# ──────────────────────────────────────────────────────────────
# ШАГ 3: Синхронизируем collaboration репозиторий
# ──────────────────────────────────────────────────────────────
step "3/4  Обновляем collaboration repo на GMKtec"

run "cd ~/collaboration && git pull 2>&1 | tail -5" || warn "git pull не выполнен"

# ──────────────────────────────────────────────────────────────
# ШАГ 4: Финальная проверка полного стека на GMKtec
# ──────────────────────────────────────────────────────────────
step "4/4  Финальная проверка стека на GMKtec"

run "python3 - <<'PYCHECK'
import sys

checks = [
    ('langgraph',    'LangGraph'),
    ('evidently',    'Evidently AI'),
    ('deepeval',     'DeepEval'),
    ('trl',          'TRL (замена OpenRLHF)'),
    ('transformers', 'Transformers'),
    ('peft',         'PEFT / LoRA'),
    ('accelerate',   'Accelerate'),
    ('datasets',     'HuggingFace Datasets'),
    ('networkx',     'AMLSim (networkx)'),
]

all_ok = True
for mod, label in checks:
    try:
        m = __import__(mod)
        ver = getattr(m, '__version__', '?')
        print(f'  ✅  {label:<25} {ver}')
    except ImportError as e:
        print(f'  ❌  {label:<25} {e}')
        all_ok = False

print()
if all_ok:
    print('  🟢  GMKtec стек 100% — TRL готов к SFT/DPO/GRPO')
else:
    print('  🔴  Некоторые компоненты не установлены')
    sys.exit(1)
PYCHECK"

log ""
log "$SEP"
log "  GMKtec: установка завершена."
log "  TRL заменяет OpenRLHF для AMD:"
log "    SFTTrainer  — supervised fine-tuning"
log "    DPOTrainer  — direct preference optimization"
log "    GRPOTrainer — group relative policy optimization"
log "$SEP"
log ""
