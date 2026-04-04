#!/usr/bin/env bash
# install_openrlhf.sh — CUDA Toolkit 12.6 + OpenRLHF
#
# Режимы:
#   INSTALL_MODE=root  — через официальный NVIDIA APT repo (по умолчанию, если есть sudo)
#   INSTALL_MODE=user  — без root, через NVIDIA .run toolkit-only installer
#
# Запуск:
#   bash ~/collaboration/scripts/install_openrlhf.sh
#   INSTALL_MODE=root bash ~/collaboration/scripts/install_openrlhf.sh
#   INSTALL_MODE=user bash ~/collaboration/scripts/install_openrlhf.sh
#
set -euo pipefail

CUDA_VERSION="12.6"
CUDA_PKG="cuda-toolkit-12-6"
VENV_DIR="${HOME}/.venvs/openrlhf"
LOG_FILE="/tmp/install_openrlhf_$(date +%Y%m%d_%H%M%S).log"

SEP="=================================================="

log() { echo "$@" | tee -a "$LOG_FILE"; }
step() { echo ""; log "$SEP"; log "  $1"; log "$SEP"; }
ok()   { log "  ✅ $*"; }
fail() { log "  ❌ $*"; exit 1; }
warn() { log "  ⚠️  $*"; }

log ""
log "  OpenRLHF Installer — BANXE AI Bank"
log "  $(date)"
log "  Log: $LOG_FILE"

# ──────────────────────────────────────────────────────────────
# ШАГ 0: Определяем режим установки
# ──────────────────────────────────────────────────────────────
step "0/6  Определяем режим установки"

if [ -z "${INSTALL_MODE:-}" ]; then
    if sudo -n true 2>/dev/null; then
        INSTALL_MODE=root
    else
        INSTALL_MODE=user
    fi
fi

log "  INSTALL_MODE=$INSTALL_MODE"

# ──────────────────────────────────────────────────────────────
# ШАГ 1: Проверяем NVIDIA GPU
# ──────────────────────────────────────────────────────────────
step "1/6  Проверяем NVIDIA GPU"

if ! command -v nvidia-smi &>/dev/null; then
    fail "nvidia-smi не найден. Нужна NVIDIA GPU с установленным драйвером."
fi
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader 2>/dev/null | while IFS= read -r line; do
    log "       GPU: $line"
done
DRIVER_CUDA=$(nvidia-smi | grep -oP 'CUDA Version: \K[0-9]+\.[0-9]+' | head -1)
ok "NVIDIA driver OK  (поддерживаемая CUDA: $DRIVER_CUDA)"

# ──────────────────────────────────────────────────────────────
# ШАГ 2: Установка CUDA Toolkit
# ──────────────────────────────────────────────────────────────
step "2/6  Устанавливаем CUDA Toolkit $CUDA_VERSION"

install_cuda_apt() {
    log "  → Режим: APT (официальный NVIDIA repo)"

    # Определяем дистрибутив
    . /etc/os-release
    OS_ID="${ID}"          # ubuntu
    OS_VER="${VERSION_ID}" # 22.04 / 24.04
    ARCH=$(uname -m)       # x86_64 / aarch64

    case "$OS_VER" in
        22.04) DISTRO="ubuntu2204" ;;
        24.04) DISTRO="ubuntu2404" ;;
        *)     fail "Неподдерживаемая версия Ubuntu: $OS_VER (нужна 22.04 или 24.04)" ;;
    esac

    case "$ARCH" in
        x86_64)  ARCH_SHORT="x86_64" ;;
        aarch64) ARCH_SHORT="sbsa" ;;
        *)        fail "Неподдерживаемая архитектура: $ARCH" ;;
    esac

    KEYRING_DEB="cuda-keyring_1.1-1_all.deb"
    KEYRING_URL="https://developer.download.nvidia.com/compute/cuda/repos/${DISTRO}/${ARCH_SHORT}/${KEYRING_DEB}"

    log "  Дистрибутив: $DISTRO / $ARCH_SHORT"
    log "  Скачиваем cuda-keyring..."

    TMP_DEB=$(mktemp /tmp/cuda-keyring-XXXXXX.deb)
    curl -fsSL "$KEYRING_URL" -o "$TMP_DEB" || fail "Не удалось скачать $KEYRING_URL"

    sudo dpkg -i "$TMP_DEB" && rm -f "$TMP_DEB"
    sudo apt-get update -qq
    sudo apt-get install -y "$CUDA_PKG"

    ok "cuda-toolkit-${CUDA_VERSION} установлен через APT"
}

install_cuda_runfile() {
    log "  → Режим: user-space .run toolkit-only (без root)"

    ARCH=$(uname -m)
    case "$ARCH" in
        x86_64)  RUN_URL="https://developer.download.nvidia.com/compute/cuda/12.6.0/local_installers/cuda_12.6.0_560.28.03_linux.run" ;;
        aarch64) RUN_URL="https://developer.download.nvidia.com/compute/cuda/12.6.0/local_installers/cuda_12.6.0_560.28.03_linux_sbsa.run" ;;
        *)        fail "Неподдерживаемая архитектура: $ARCH" ;;
    esac

    RUN_FILE="/tmp/cuda_12.6_installer.run"
    CUDA_USER_DIR="${HOME}/cuda-${CUDA_VERSION}"

    if [ ! -f "$RUN_FILE" ]; then
        log "  Скачиваем CUDA .run (~3 ГБ) — может занять время..."
        curl -fL "$RUN_URL" -o "$RUN_FILE" --progress-bar || fail "Не удалось скачать .run файл"
    else
        log "  .run файл уже скачан: $RUN_FILE"
    fi

    chmod +x "$RUN_FILE"
    log "  Запускаем installer (toolkit only, без драйвера, в $CUDA_USER_DIR)..."
    "$RUN_FILE" \
        --silent \
        --toolkit \
        --toolkitpath="$CUDA_USER_DIR" \
        --no-drm \
        --no-man-page \
        --override \
        2>&1 | tee -a "$LOG_FILE" || fail "Установка .run завершилась с ошибкой"

    ok "CUDA Toolkit установлен в $CUDA_USER_DIR"
    CUDA_INSTALL_PATH="$CUDA_USER_DIR"
}

# Выбираем путь
if nvcc --version &>/dev/null 2>&1; then
    ok "nvcc уже установлен: $(nvcc --version | head -1)"
    CUDA_INSTALL_PATH=$(dirname "$(dirname "$(which nvcc)")")
else
    if [ "$INSTALL_MODE" = "root" ]; then
        install_cuda_apt
        CUDA_INSTALL_PATH=$(ls -d /usr/local/cuda-${CUDA_VERSION} 2>/dev/null || ls -d /usr/local/cuda* | sort -V | tail -1)
    else
        install_cuda_runfile
    fi
fi

# ──────────────────────────────────────────────────────────────
# ШАГ 3: Настраиваем CUDA_HOME, PATH, LD_LIBRARY_PATH
# ──────────────────────────────────────────────────────────────
step "3/6  Настраиваем CUDA окружение"

export CUDA_HOME="${CUDA_INSTALL_PATH}"
export PATH="${CUDA_HOME}/bin:${PATH}"
export LD_LIBRARY_PATH="${CUDA_HOME}/lib64:${LD_LIBRARY_PATH:-}"

# Проверяем nvcc
if ! nvcc --version &>/dev/null; then
    fail "nvcc не найден после установки. CUDA_HOME=$CUDA_HOME"
fi
NVCC_VER=$(nvcc --version | grep -oP 'release \K[0-9]+\.[0-9]+')
ok "nvcc $NVCC_VER  (CUDA_HOME=$CUDA_HOME)"

# Прописываем в ~/.bashrc если ещё нет
BASHRC_MARKER="# >>> CUDA Toolkit (install_openrlhf.sh) <<<"
if ! grep -qF "$BASHRC_MARKER" ~/.bashrc 2>/dev/null; then
    cat >> ~/.bashrc <<BASHRC_BLOCK

${BASHRC_MARKER}
export CUDA_HOME=${CUDA_HOME}
export PATH=\${CUDA_HOME}/bin:\${PATH}
export LD_LIBRARY_PATH=\${CUDA_HOME}/lib64:\${LD_LIBRARY_PATH:-}
# <<< CUDA Toolkit <<<
BASHRC_BLOCK
    ok "CUDA_HOME добавлен в ~/.bashrc"
fi

# ──────────────────────────────────────────────────────────────
# ШАГ 3.5: Java для запуска AMLSim JAR
# ──────────────────────────────────────────────────────────────
step "3.5/6  Проверяем Java (нужна для AMLSim JAR)"

if java -version &>/dev/null 2>&1; then
    ok "Java уже установлена: $(java -version 2>&1 | head -1)"
else
    log "  Java не найдена — устанавливаем default-jdk-headless..."
    sudo apt-get install -y default-jdk-headless 2>&1 | tee -a "$LOG_FILE"
    ok "Java установлена: $(java -version 2>&1 | head -1)"
fi

# Проверяем AMLSim JAR
AMLSIM_JAR=$(find ~ -name "amlsim-*.jar" 2>/dev/null | head -1)
if [ -n "$AMLSIM_JAR" ]; then
    ok "AMLSim JAR: $AMLSIM_JAR"
else
    warn "AMLSim JAR не найден — сборка не выполнялась или JAR в другом месте"
fi

# ──────────────────────────────────────────────────────────────
# ШАГ 4: Создаём venv
# ──────────────────────────────────────────────────────────────
step "4/6  Создаём venv: $VENV_DIR"

if [ -d "$VENV_DIR" ]; then
    warn "venv уже существует — переиспользуем"
else
    python3 -m venv "$VENV_DIR"
    ok "venv создан: $VENV_DIR"
fi

# Активируем
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"
ok "venv активирован: $(python3 --version)"

# Обновляем pip внутри venv
pip install --upgrade pip -q

# ──────────────────────────────────────────────────────────────
# ШАГ 5: Устанавливаем PyTorch + OpenRLHF
# ──────────────────────────────────────────────────────────────
step "5/6  Устанавливаем PyTorch (cu126) + OpenRLHF"

# PyTorch с CUDA 12.6
log "  Устанавливаем torch (cu126)..."
pip install torch --index-url https://download.pytorch.org/whl/cu126 -q

TORCH_VER=$(python3 -c "import torch; print(torch.__version__)")
TORCH_CUDA=$(python3 -c "import torch; print(torch.version.cuda)")
ok "torch $TORCH_VER  (CUDA $TORCH_CUDA)"

# Проверяем что torch видит GPU
GPU_AVAIL=$(python3 -c "import torch; print(torch.cuda.is_available())")
if [ "$GPU_AVAIL" = "True" ]; then
    GPU_NAME=$(python3 -c "import torch; print(torch.cuda.get_device_name(0))")
    ok "torch.cuda.is_available() = True  ($GPU_NAME)"
else
    warn "torch.cuda.is_available() = False — OpenRLHF установится, но обучение недоступно"
fi

# OpenRLHF
log "  Устанавливаем openrlhf..."
pip install openrlhf -q

RLHF_VER=$(python3 -c "import openrlhf; print(openrlhf.__version__)")
ok "openrlhf $RLHF_VER"

# ──────────────────────────────────────────────────────────────
# ШАГ 6: Финальная проверка полного стека
# ──────────────────────────────────────────────────────────────
step "6/6  Финальная проверка стека"

python3 - <<'PYCHECK'
import sys

checks = [
    ("torch",       "PyTorch"),
    ("openrlhf",    "OpenRLHF"),
    ("langgraph",   "LangGraph"),
    ("evidently",   "Evidently AI"),
    ("deepeval",    "DeepEval"),
    ("networkx",    "AMLSim (networkx)"),
]

all_ok = True
for mod, label in checks:
    try:
        m = __import__(mod)
        ver = getattr(m, "__version__", "?")
        print(f"  ✅  {label:<20} {ver}")
    except ImportError as e:
        print(f"  ❌  {label:<20} {e}")
        all_ok = False

# CUDA check
try:
    import torch
    if torch.cuda.is_available():
        gpu = torch.cuda.get_device_name(0)
        mem = torch.cuda.get_device_properties(0).total_memory // (1024**3)
        print(f"\n  🟢  CUDA GPU: {gpu} ({mem} GB)")
    else:
        print("\n  ⚠️   CUDA не доступна в torch (но стек установлен)")
except Exception as e:
    print(f"\n  ⚠️   CUDA check: {e}")

print()
if all_ok:
    print("  🟢  ВЕСЬ СТЕК УСТАНОВЛЕН — OpenRLHF готов к обучению")
else:
    print("  🔴  Некоторые компоненты не установлены — см. выше")
    sys.exit(1)
PYCHECK

log ""
log "$SEP"
log "  Установка завершена."
log "  Активируй окружение в новом терминале:"
log "    source ${VENV_DIR}/bin/activate"
log "  Или добавь alias в ~/.bashrc:"
log "    alias openrlhf-env='source ${VENV_DIR}/bin/activate'"
log "$SEP"
log ""
