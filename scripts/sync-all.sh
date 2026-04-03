#!/bin/bash
# sync-all.sh — Умная синхронизация общего стека с чтением из PROJECT-REGISTRY.csv
# 
# Использование:
#   bash ~/developer/scripts/sync-all.sh [--dry-run]
#
# Реестр проектов: ~/developer/docs/PROJECT-REGISTRY.csv
# Формат: project|type|onboarded|repos|mirofish|scenarios

set -e

SOURCE=~/developer
DRY_RUN=false
REGISTRY="$SOURCE/docs/PROJECT-REGISTRY.csv"

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

# Функции логирования
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
# ЧТЕНИЕ РЕЕСТРА ПРОЕКТОВ
# ============================================

declare -A PROJECT_TYPES
declare -A PROJECT_REPOS
declare -A PROJECT_MIROFISH
declare -A PROJECT_SCENARIOS

read_registry() {
    log "📖 Чтение реестра проектов..."
    
    if [[ ! -f "$REGISTRY" ]]; then
        error "Реестр не найден: $REGISTRY"
        exit 1
    fi
    
    local first_line=true
    while IFS='|' read -r project type onboarded repos mirofish scenarios; do
        # Пропускаем заголовок
        if [[ "$first_line" == "true" ]]; then
            first_line=false
            continue
        fi
        
        # Пропускаем пустые строки и комментарии
        [[ -z "$project" || "$project" =~ ^# ]] && continue
        
        # Сохраняем данные
        PROJECT_TYPES["$project"]="$type"
        PROJECT_REPOS["$project"]="$repos"
        PROJECT_MIROFISH["$project"]="$mirofish"
        PROJECT_SCENARIOS["$project"]="$scenarios"
        
        log "  → $project (тип: $type, MiroFish: $mirofish, сценарии: $scenarios)"
    done < "$REGISTRY"
}

# ============================================
# СИНХРОНИЗАЦИЯ
# ============================================

sync_common_files() {
    local repo=$1
    local target=~/$(basename $repo)
    
    COMMON_FILES=(
        "AGENTS.md"
        "docs/COLLAB.md"
        "docs/MCP-BEST-PRACTICES.md"
        "scripts/check-agent-instructions.sh"
        ".qoder/config.yml"
    )
    
    for file in "${COMMON_FILES[@]}"; do
        SOURCE_FILE="$SOURCE/$file"
        
        if [[ ! -f "$SOURCE_FILE" ]]; then
            warning "  Файл $file не найден в источнике"
            continue
        fi
        
        mkdir -p "$target/$(dirname $file)"
        
        if [[ "$DRY_RUN" == "true" ]]; then
            echo "    [DRY] cp $file → $repo/"
        else
            cp "$SOURCE_FILE" "$target/$file"
            success "  Скопирован $file"
        fi
    done
}

sync_mirofish_scenarios() {
    local repo=$1
    local project_type=$2
    
    # НЕ копируем MIROFISH-SCENARIOS.md — у каждого проекта свои сценарии
    # Исключение: developer-core хранит MASTER копии всех сценариев
    # Если нужно обновить сценарий — редактируем в проекте и коммитим
    :
}

sync_context() {
    local repo=$1
    local target=~/$(basename $repo)
    
    # ЕДИНЫЙ context.md для ВСЕХ проектов
    CONTEXT_FILE="$SOURCE/.qoder/context.md"
    
    if [[ -f "$CONTEXT_FILE" ]]; then
        mkdir -p "$target/.qoder"
        if [[ "$DRY_RUN" == "true" ]]; then
            echo "    [DRY] cp context.md → $repo/.qoder/context.md"
        else
            cp "$CONTEXT_FILE" "$target/.qoder/context.md"
            success "  $repo: context.md (Three-Partner Synergy)"
        fi
    else
        error "  context.md не найден!"
    fi
}

commit_and_push() {
    local repo=$1
    local target=~/$(basename $repo)
    
    if [[ ! -d "$target" ]]; then
        return
    fi
    
    cd "$target"
    
    # Проверяем есть ли изменения
    if git diff --quiet && git diff --cached --quiet; then
        log "  $repo: изменений нет"
        cd - > /dev/null
        return
    fi
    
    log "  → $repo: коммит и пуш..."
    
    git add -A
    
    if git diff --cached --quiet; then
        log "    Нет изменений для коммита"
        cd - > /dev/null
        return
    fi
    
    git commit -m "$(cat <<'EOF'
sync: Update shared stack from developer-core

Components updated:
- AGENTS.md (three-partner synergy)
- .qoder/context.md (UNIVERSAL — Claude + Qoder + MiroFish)
- docs/COLLAB.md
- docs/MCP-BEST-PRACTICES.md
- .qoder/config.yml
- scripts/check-agent-instructions.sh
- docs/MIROFISH-SCENARIOS.md (project-specific)

Source: ~/developer/ (MASTER)
Synced via: sync-all.sh

🤖 Generated with [Qoder][https://qoder.com]
EOF
)"
    
    # Определяем основную ветку
    DEFAULT_BRANCH=$(git remote show origin 2>/dev/null | grep -oP 'HEAD branch: \K.*' || echo "main")
    
    if git push origin "$DEFAULT_BRANCH" 2>/dev/null; then
        success "  $repo: запушено в $DEFAULT_BRANCH"
    elif git push origin master 2>/dev/null; then
        success "  $repo: запушено в master"
    else
        error "  $repo: ошибка пуша!"
    fi
    
    cd - > /dev/null
}

# ============================================
# ОСНОВНОЙ ЦИКЛ
# ============================================

main() {
    read_registry
    
    log "📦 Синхронизация по реестру..."
    
    # Обрабатываем каждый проект из реестра
    for project in "${!PROJECT_REPOS[@]}"; do
        type="${PROJECT_TYPES[$project]}"
        repos="${PROJECT_REPOS[$project]}"
        mirofish="${PROJECT_MIROFISH[$project]}"
        scenarios="${PROJECT_SCENARIOS[$project]}"
        
        log "Проект: $project (тип: $type, MiroFish: $mirofish)"
        
        # Разделяем репозитории по запятой
        IFS=',' read -ra REPO_ARRAY <<< "$repos"
        
        for repo in "${REPO_ARRAY[@]}"; do
            target=~/$(basename $repo)
            
            if [[ ! -d "$target" ]]; then
                warning "  Репозиторий $target не найден, пропускаем..."
                continue
            fi
            
            log "  → $repo"
            
            # 1. Общий стек
            sync_common_files "$repo"
            
            # 2. Context (единый для всех)
            sync_context "$repo"
            
            # 3. MiroFish scenarios (кроме developer-core)
            if [[ "$mirofish" == "yes" ]]; then
                sync_mirofish_scenarios "$repo" "$type"
            fi
        done
    done
    
    # Коммит и пуш
    if [[ "$DRY_RUN" == "true" ]]; then
        log "🔍 DRY RUN завершён. Для реальной синхронизации запустите без --dry-run"
        exit 0
    fi
    
    log "🔄 Коммит и пуш изменений..."
    
    for project in "${!PROJECT_REPOS[@]}"; do
        repos="${PROJECT_REPOS[$project]}"
        
        IFS=',' read -ra REPO_ARRAY <<< "$repos"
        
        for repo in "${REPO_ARRAY[@]}"; do
            commit_and_push "$repo"
        done
    done
    
    log "✅ Синхронизация завершена!"
}

main
