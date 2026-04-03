#!/bin/bash
# onboard-project.sh — Онбординг нового проекта в инфраструктуру
# 
# Использование:
#   ./onboard-project.sh <имя-проекта> <тип: banxe|legal|other>
#
# Примеры:
#   ./onboard-project.sh my-new-project banxe
#   ./onboard-project.sh legal-case-2026 legal
#   ./onboard-project.sh experimental other

set -e

# ============================================
# КОНФИГУРАЦИЯ
# ============================================

PROJECT=$1
TYPE=$2
SOURCE=~/developer
REGISTRY="$SOURCE/docs/PROJECT-REGISTRY.csv"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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
# ПРОВЕРКА ПАРАМЕТРОВ
# ============================================

if [[ -z "$PROJECT" || -z "$TYPE" ]]; then
    error "Использование: $0 <имя-проекта> <тип: banxe|legal|other>"
    echo ""
    echo "Типы проектов:"
    echo "  banxe — Banxe AI Bank проекты (с MiroFish)"
    echo "  legal — Юридические проекты (без MiroFish)"
    echo "  other — Другие проекты (базовая конфигурация)"
    exit 1
fi

if [[ ! "$TYPE" =~ ^(banxe|legal|other)$ ]]; then
    error "Неверный тип: $TYPE. Допустимы: banxe, legal, other"
    exit 1
fi

TARGET=~/$(basename $PROJECT)

# ============================================
# ОНБОРДИНГ
# ============================================

log "🚀 Онбординг проекта: $PROJECT (тип: $TYPE)"

# Проверка что директория существует
if [[ ! -d "$TARGET" ]]; then
    error "Директория не найдена: $TARGET"
    echo ""
    echo "Сначала создайте директорию и инициализируйте git:"
    echo "  mkdir -p $TARGET"
    echo "  cd $TARGET"
    echo "  git init"
    echo "  git remote add origin git@github.com:CarmiBanxe/$PROJECT.git"
    exit 1
fi

cd "$TARGET"

# Проверка что это git репозиторий
if [[ ! -d ".git" ]]; then
    error "Это не git репозиторий: $TARGET"
    echo ""
    echo "Инициализируйте git:"
    echo "  cd $TARGET"
    echo "  git init"
    exit 1
fi

log "📁 Директория: $TARGET"
log "🏷️  Тип проекта: $TYPE"

# ============================================
# 1. ВНЕДРЕНИЕ ОБЩЕГО СТЕКА
# ============================================

log "📦 Внедрение общего стека..."

mkdir -p .qoder docs scripts

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
        warning "Файл не найден: $file (пропускаем)"
        continue
    fi
    
    mkdir -p "$(dirname $file)"
    cp "$SOURCE_FILE" "$file"
    success "  Скопирован $file"
done

# ============================================
# 2. CONTEXT.MD ПО ТИПУ
# ============================================

log "📄 Настройка context.md для типа '$TYPE'..."

case $TYPE in
    banxe)
        cp "$SOURCE/.qoder/context-banxe.md" .qoder/context.md
        success "  context-banxe.md (с MiroFish pipeline)"
        
        # Копируем MIROFISH-SCENARIOS.md если есть
        if [[ -f "$SOURCE/docs/MIROFISH-SCENARIOS.md" ]]; then
            cp "$SOURCE/docs/MIROFISH-SCENARIOS.md" docs/
            success "  MIROFISH-SCENARIOS.md"
        else
            warning "  MIROFISH-SCENARIOS.md не найден в источнике"
        fi
        ;;
    legal)
        cp "$SOURCE/.qoder/context-legal.md" .qoder/context.md
        success "  context-legal.md (без MiroFish)"
        ;;
    *)
        cp "$SOURCE/.qoder/context-base.md" .qoder/context.md
        success "  context-base.md (базовая версия)"
        ;;
esac

# ============================================
# 3. РЕГИСТРАЦИЯ В РЕЕСТРЕ
# ============================================

log "📝 Регистрация в PROJECT-REGISTRY.csv..."

TODAY=$(date +%Y-%m-%d)

# Проверяем есть ли уже проект в реестре
if grep -q "^$PROJECT|" "$REGISTRY" 2>/dev/null; then
    warning "Проект уже зарегистрирован: $PROJECT"
else
    # Добавляем новую запись
    echo "$PROJECT|$TYPE|$TODAY|$PROJECT|no|active" >> "$REGISTRY"
    success "  Проект добавлен в реестр"
fi

# ============================================
# 4. ДОБАВЛЕНИЕ В sync-all.sh
# ============================================

log "🔄 Обновление sync-all.sh..."

# sync-all.sh теперь читает из реестра автоматически
# Ничего дополнительно делать не нужно
success "  sync-all.sh автоматически подхватит проект из реестра"

# ============================================
# 5. ПЕРВЫЙ КОММИТ
# ============================================

log "📝 Первый коммит..."

git add -A

if git diff --cached --quiet; then
    log "  Нет изменений для коммита (уже всё закоммичено)"
else
    git commit -m "$(cat <<'EOF'
feat: Onboard into synergy infrastructure

Project type: TYPE_PLACEHOLDER
Qoder stack integrated:
- AGENTS.md (agent instructions)
- .qoder/context.md (execution contract)
- .qoder/config.yml (Qoder configuration)
- docs/COLLAB.md (collaboration pattern)
- docs/MCP-BEST-PRACTICES.md (MCP guide)
- scripts/check-agent-instructions.sh (diagnostic tool)

Ready for: cd ~/PROJECT_PLACEHOLDER && claude

🤖 Generated with [Qoder][https://qoder.com]
EOF
)"
    # Заменяем плейсхолдеры на реальные значения
    git commit --amend -m "$(cat <<EOF
feat: Onboard into synergy infrastructure

Project type: $TYPE
Qoder stack integrated:
- AGENTS.md (agent instructions)
- .qoder/context.md (execution contract)
- .qoder/config.yml (Qoder configuration)
- docs/COLLAB.md (collaboration pattern)
- docs/MCP-BEST-PRACTICES.md (MCP guide)
- scripts/check-agent-instructions.sh (diagnostic tool)

Ready for: cd ~/$PROJECT && claude

🤖 Generated with [Qoder][https://qoder.com]
EOF
)" 2>/dev/null || true
fi

# ============================================
# 6. ПУШ
# ============================================

log "🚀 Пуш в GitHub..."

# Определяем основную ветку
DEFAULT_BRANCH=$(git remote show origin 2>/dev/null | grep -oP 'HEAD branch: \K.*' || echo "main")

if git push -u origin "$DEFAULT_BRANCH" 2>/dev/null; then
    success "  Запушено в $DEFAULT_BRANCH"
elif git push -u origin master 2>/dev/null; then
    success "  Запушено в master"
else
    warning "  Не удалось запушить. Выполните вручную:"
    echo "    cd $TARGET"
    echo "    git push -u origin main"
fi

# ============================================
# ИТОГ
# ============================================

echo ""
echo "═══════════════════════════════════════════════════"
echo -e "${GREEN}✅ $PROJECT онбордирован успешно!${NC}"
echo "═══════════════════════════════════════════════════"
echo ""
echo "Тип проекта: $TYPE"
echo "Расположение: $TARGET"
echo ""

if [[ "$TYPE" == "banxe" ]]; then
    echo "MiroFish: ✅ Подключён (автоматические симуляции)"
    echo ""
    echo "Для запуска сессии:"
    echo "  cd $TARGET && claude"
elif [[ "$TYPE" == "legal" ]]; then
    echo "MiroFish: ❌ Не используется (документо-ориентированный проект)"
    echo ""
    echo "Для запуска сессии:"
    echo "  cd $TARGET && claude"
else
    echo "MiroFish: ❌ Не настроен (базовая конфигурация)"
    echo ""
    echo "Для запуска сессии:"
    echo "  cd $TARGET && claude"
fi

echo ""
echo "Синхронизация:"
echo "  bash $SOURCE/scripts/sync-all.sh"
echo ""
echo "═══════════════════════════════════════════════════"
