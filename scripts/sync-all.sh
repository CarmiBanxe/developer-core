#!/bin/bash
# sync-all.sh — Умная синхронизация общего стека по 4 проектам
# 
# Матрица синхронизации:
#   - developer-core → мастер-копия общего стека
#   - Общий стек → все 6 репо
#   - MiroFish → только Banxe-репо (vibe-coding, collaboration, MetaClaw, banxe-mirofish)
#   - Legal-контекст → только guiyon и ss1
#   - Banxe-контекст → только Banxe-репо
#
# Использование:
#   bash ~/developer/scripts/sync-all.sh [--dry-run]
#

set -e

SOURCE=~/developer
DRY_RUN=false

# Парсинг аргументов
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "🔍 DRY RUN MODE — изменения не применяются"
fi

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для логирования
log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✓${NC} $1"
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
}

# ============================================
# КОНФИГУРАЦИЯ СИНХРОНИЗАЦИИ
# ============================================

# Общий стек → ВСЕ 6 репо
COMMON_FILES=(
    "AGENTS.md"
    "docs/COLLAB.md"
    "docs/MCP-BEST-PRACTICES.md"
    "scripts/check-agent-instructions.sh"
    ".qoder/config.yml"
)

ALL_REPOS=(
    "vibe-coding"
    "collaboration"
    "MetaClaw"
    "guiyon"
    "ss1"
    "banxe-mirofish"
)

# MiroFish компоненты → только Banxe-репо
MIROFISH_FILES=(
    "docs/MIROFISH-SCENARIOS.md"
)

BANXE_REPOS=(
    "vibe-coding"
    "collaboration"
    "MetaClaw"
    "banxe-mirofish"
)

# Legal проекты → только guiyon и ss1
LEGAL_REPOS=(
    "guiyon"
    "ss1"
)

# ============================================
# СИНХРОНИЗАЦИЯ ОБЩЕГО СТЕКА
# ============================================

log "📦 Синхронизация общего стека..."

for repo in "${ALL_REPOS[@]}"; do
    TARGET=~/$(basename $repo)
    
    if [[ ! -d "$TARGET" ]]; then
        warning "Репозиторий $TARGET не найден, пропускаем..."
        continue
    fi
    
    log "  → $repo"
    
    for file in "${COMMON_FILES[@]}"; do
        SOURCE_FILE="$SOURCE/$file"
        TARGET_DIR="$TARGET/$(dirname $file)"
        
        if [[ ! -f "$SOURCE_FILE" ]]; then
            warning "  Файл $file не найден в источнике"
            continue
        fi
        
        mkdir -p "$TARGET_DIR"
        
        if [[ "$DRY_RUN" == "true" ]]; then
            echo "    [DRY] cp $file → $repo/"
        else
            cp "$SOURCE_FILE" "$TARGET/$file"
            success "  Скопирован $file"
        fi
    done
done

# ============================================
# СИНХРОНИЗАЦИЯ MIROFISH (только Banxe)
# ============================================

log "🐟 Синхронизация MiroFish компонентов (Banxe projects)..."

for repo in "${BANXE_REPOS[@]}"; do
    TARGET=~/$(basename $repo)
    
    if [[ ! -d "$TARGET" ]]; then
        warning "Репозиторий $TARGET не найден, пропускаем..."
        continue
    fi
    
    log "  → $repo"
    
    for file in "${MIROFISH_FILES[@]}"; do
        SOURCE_FILE="$SOURCE/$file"
        TARGET_DIR="$TARGET/$(dirname $file)"
        
        if [[ ! -f "$SOURCE_FILE" ]]; then
            warning "  Файл $file не найден в источнике"
            continue
        fi
        
        mkdir -p "$TARGET_DIR"
        
        if [[ "$DRY_RUN" == "true" ]]; then
            echo "    [DRY] cp $file → $repo/"
        else
            cp "$SOURCE_FILE" "$TARGET/$file"
            success "  Скопирован $file"
        fi
    done
done

# ============================================
# СИНХРОНИЗАЦИЯ CONTEXT.MD (разные версии)
# ============================================

log "📄 Синхронизация .qoder/context.md..."

# Banxe-версия (с MiroFish)
log "  Banxe-версия (с MiroFish pipeline)..."
BANXE_CONTEXT="$SOURCE/.qoder/context-banxe.md"

if [[ -f "$BANXE_CONTEXT" ]]; then
    for repo in "${BANXE_REPOS[@]}"; do
        TARGET=~/$(basename $repo)
        
        if [[ ! -d "$TARGET" ]]; then
            continue
        fi
        
        if [[ "$DRY_RUN" == "true" ]]; then
            echo "    [DRY] cp context-banxe.md → $repo/.qoder/context.md"
        else
            mkdir -p "$TARGET/.qoder"
            cp "$BANXE_CONTEXT" "$TARGET/.qoder/context.md"
            success "  $repo: context-banxe.md"
        fi
    done
else
    error "  context-banxe.md не найден!"
fi

# Legal-версия (без MiroFish)
log "  Legal-версия (без MiroFish)..."
LEGAL_CONTEXT="$SOURCE/.qoder/context-legal.md"

if [[ -f "$LEGAL_CONTEXT" ]]; then
    for repo in "${LEGAL_REPOS[@]}"; do
        TARGET=~/$(basename $repo)
        
        if [[ ! -d "$TARGET" ]]; then
            continue
        fi
        
        if [[ "$DRY_RUN" == "true" ]]; then
            echo "    [DRY] cp context-legal.md → $repo/.qoder/context.md"
        else
            mkdir -p "$TARGET/.qoder"
            cp "$LEGAL_CONTEXT" "$TARGET/.qoder/context.md"
            success "  $repo: context-legal.md"
        fi
    done
else
    error "  context-legal.md не найден!"
fi

# ============================================
# КОММИТ И ПУШ
# ============================================

if [[ "$DRY_RUN" == "true" ]]; then
    log "🔍 DRY RUN завершён. Для реальной синхронизации запустите без --dry-run"
    exit 0
fi

log "🔄 Коммит и пуш изменений..."

for repo in "${ALL_REPOS[@]}"; do
    TARGET=~/$(basename $repo)
    
    if [[ ! -d "$TARGET" ]]; then
        continue
    fi
    
    cd "$TARGET"
    
    # Проверяем есть ли изменения
    if git diff --quiet && git diff --cached --quiet; then
        log "  $repo: изменений нет"
        continue
    fi
    
    log "  → $repo: коммит и пуш..."
    
    git add -A
    
    if git diff --cached --quiet; then
        log "    Нет изменений для коммита"
        continue
    fi
    
    git commit -m "$(cat <<'EOF'
sync: Update shared stack from developer-core

Components updated:
- AGENTS.md (three-partner synergy)
- .qoder/context.md (Banxe/Legal version)
- docs/COLLAB.md
- docs/MCP-BEST-PRACTICES.md
- .qoder/config.yml
- scripts/check-agent-instructions.sh

Source: ~/developer/ (MASTER)
Synced via: sync-all.sh

🤖 Generated with [Qoder][https://qoder.com]
EOF
)"
    
    # Определяем основную ветку
    DEFAULT_BRANCH=$(git remote show origin 2>/dev/null | grep -oP 'HEAD branch: \K.*' || echo "main")
    
    if git push origin "$DEFAULT_BRANCH" 2>/dev/null; then
        success "  $repo: запушено в $DEFAULT_BRANCH"
    else
        # Пробуем master если main не сработал
        if git push origin master 2>/dev/null; then
            success "  $repo: запушено в master"
        else
            error "  $repo: ошибка пуша!"
        fi
    fi
    
    cd - > /dev/null
done

log "✅ Синхронизация завершена!"
