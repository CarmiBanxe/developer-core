#!/bin/bash
# sync-to-project.sh — Distribute shared components from ~/developer to target projects
# Usage: bash scripts/sync-to-project.sh <project-name>
#
# Examples:
#   bash scripts/sync-to-project.sh vibe-coding
#   bash scripts/sync-to-project.sh collaboration
#   bash scripts/sync-to-project.sh guiyon

set -e

DEVELOPER_ROOT="$HOME/developer"
PROJECTS_DIR="$HOME"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}════════════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}○${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check arguments
if [ -z "$1" ]; then
    print_header "Developer Core Sync Tool"
    echo ""
    echo "Usage: bash scripts/sync-to-project.sh <project-name>"
    echo ""
    echo "Available projects:"
    ls -d "$PROJECTS_DIR"/*/ 2>/dev/null | grep -E "(vibe-coding|collaboration|guiyon|MetaClaw|ss1)" | xargs -n1 basename || echo "  (none found)"
    echo ""
    exit 1
fi

PROJECT_NAME="$1"
PROJECT_PATH="$PROJECTS_DIR/$PROJECT_NAME"

# Validate project exists
if [ ! -d "$PROJECT_PATH" ]; then
    print_error "Project not found: $PROJECT_PATH"
    exit 1
fi

# Validate it's a git repository
if [ ! -d "$PROJECT_PATH/.git" ]; then
    print_error "Not a git repository: $PROJECT_PATH"
    exit 1
fi

print_header "Sync: Developer → $PROJECT_NAME"
echo ""
echo "Source: $DEVELOPER_ROOT"
echo "Target: $PROJECT_PATH"
echo ""

# Detect project type for selective sync
COMPLIANCE_PROJECT=false
if [ "$PROJECT_NAME" = "vibe-coding" ]; then
    COMPLIANCE_PROJECT=true
    print_warning "Compliance project detected — will sync compliance components"
fi
echo ""

# Components to sync (always)
SYNC_COMPONENTS=(
    ".qoder/config.yml"
    ".qoder/context.md"
    "AGENTS.md"
    "docs/COLLAB.md"
    "docs/MCP-BEST-PRACTICES.md"
    "scripts/check-agent-instructions.sh"
)

# Compliance components (vibe-coding only)
if [ "$COMPLIANCE_PROJECT" = true ]; then
    SYNC_COMPONENTS+=("compliance/COMPLIANCE_ARCH.md")
fi

# Show what will be synced
print_header "Components to sync"
for component in "${SYNC_COMPONENTS[@]}"; do
    if [ -f "$DEVELOPER_ROOT/$component" ] || [ -d "$DEVELOPER_ROOT/$component" ]; then
        echo "  $component"
    else
        print_warning "Component not found: $component (skipping)"
    fi
done
echo ""

# Confirm before proceeding
read -p "Proceed with sync? (y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Sync cancelled."
    exit 0
fi
echo ""

# Create backup in target
print_header "Creating backup"
BACKUP_DIR="$PROJECT_PATH/.sync-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

for component in "${SYNC_COMPONENTS[@]}"; do
    target_file="$PROJECT_PATH/$component"
    if [ -e "$target_file" ]; then
        backup_parent="$BACKUP_DIR/$(dirname "$component")"
        mkdir -p "$backup_parent"
        cp -r "$target_file" "$backup_parent/"
        print_success "Backed up: $component"
    fi
done
echo ""

# Sync components
print_header "Syncing components"
for component in "${SYNC_COMPONENTS[@]}"; do
    source_path="$DEVELOPER_ROOT/$component"
    target_path="$PROJECT_PATH/$component"
    
    if [ ! -e "$source_path" ]; then
        print_warning "Source not found: $component (skipping)"
        continue
    fi
    
    # Create parent directory if needed
    target_parent="$(dirname "$target_path")"
    mkdir -p "$target_parent"
    
    # Copy file or directory
    if [ -d "$source_path" ]; then
        cp -r "$source_path"/* "$target_parent"/
    else
        cp "$source_path" "$target_path"
    fi
    
    print_success "Synced: $component"
done
echo ""

# Make scripts executable
print_header "Setting permissions"
chmod +x "$PROJECT_PATH/scripts/check-agent-instructions.sh" 2>/dev/null || true
print_success "Scripts made executable"
echo ""

# Verify sync
print_header "Verification"
cd "$PROJECT_PATH"

errors=0
for component in "${SYNC_COMPONENTS[@]}"; do
    target_file="$PROJECT_PATH/$component"
    if [ -e "$target_file" ]; then
        print_success "Verified: $component"
    else
        print_error "Missing: $component"
        ((errors++)) || true
    fi
done

if [ $errors -gt 0 ]; then
    echo ""
    print_error "Sync completed with $errors error(s)"
    echo "Rollback: Restore from $BACKUP_DIR"
    exit 1
fi

echo ""
print_success "All components verified"
echo ""

# Show git status
print_header "Git status in target"
git status --short || true
echo ""

# Summary
print_header "Sync Complete"
echo ""
echo "Synced $(echo ${#SYNC_COMPONENTS[@]}) components to $PROJECT_NAME"
echo "Backup location: $BACKUP_DIR"
echo ""
echo "Next steps:"
echo "  1. Review changes: cd $PROJECT_NAME && git diff"
echo "  2. Test functionality"
echo "  3. Commit if satisfied: git add . && git commit -m 'sync: from developer core'"
echo ""
echo "Rollback if needed:"
echo "  cd $PROJECT_NAME"
echo "  cp -r $BACKUP_DIR/* ."
echo ""
