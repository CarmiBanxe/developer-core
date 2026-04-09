#!/usr/bin/env bash
# screenshot-to-code-setup.sh — Install abi/screenshot-to-code locally
# IL-063 | Developer Plane
#
# Клонирует и настраивает abi/screenshot-to-code (71 900+ GitHub stars)
# для локальной работы через Ollama (код не покидает сервер).
#
# Usage: bash ~/developer/scripts/screenshot-to-code-setup.sh
# After: open http://localhost:7001

set -euo pipefail

TARGET_DIR="$HOME/tools/screenshot-to-code"
OLLAMA_URL="${OLLAMA_BASE_URL:-http://gmktec:11434}"

RED="\033[0;31m" GREEN="\033[0;32m" YELLOW="\033[1;33m" BOLD="\033[1m" RESET="\033[0m"

echo ""
echo -e "${BOLD}═══ screenshot-to-code Setup ══════════════════════════${RESET}"
echo -e "  Target: $TARGET_DIR"
echo -e "  Ollama: $OLLAMA_URL"
echo ""

# ── 1. Clone ──────────────────────────────────────────────────────────────────
if [[ -d "$TARGET_DIR" ]]; then
  echo -e "  ${YELLOW}Already cloned — pulling latest${RESET}"
  cd "$TARGET_DIR" && git pull --quiet
else
  echo -e "  Cloning abi/screenshot-to-code..."
  git clone --depth=1 https://github.com/abi/screenshot-to-code "$TARGET_DIR"
  echo -e "  ${GREEN}✅ Cloned${RESET}"
fi

# ── 2. Backend setup ──────────────────────────────────────────────────────────
echo ""
echo -e "  Setting up Python backend..."
cd "$TARGET_DIR/backend"

if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt -q
echo -e "  ${GREEN}✅ Backend deps installed${RESET}"

# ── 3. Frontend setup ─────────────────────────────────────────────────────────
echo ""
echo -e "  Setting up frontend..."
cd "$TARGET_DIR/frontend"
if command -v yarn &>/dev/null; then
  yarn install --silent
elif command -v npm &>/dev/null; then
  npm install --silent
fi
echo -e "  ${GREEN}✅ Frontend deps installed${RESET}"

# ── 4. Env file ───────────────────────────────────────────────────────────────
echo ""
cat > "$TARGET_DIR/backend/.env" << EOF
# screenshot-to-code — BANXE AI BANK config
# Using Ollama locally (code stays on GMKtec)
OPENAI_API_KEY=ollama
OPENAI_BASE_URL=$OLLAMA_URL/v1

# Anthropic (for Claude vision — optional)
# ANTHROPIC_API_KEY=<your-key>

# Preferred model (Ollama)
# SCREENSHOT_TO_CODE_MODEL=llava:latest
EOF
echo -e "  ${GREEN}✅ .env configured (Ollama: $OLLAMA_URL)${RESET}"

# ── 5. Start script ───────────────────────────────────────────────────────────
cat > "$TARGET_DIR/start-banxe.sh" << 'STARTSCRIPT'
#!/usr/bin/env bash
# Start screenshot-to-code for BANXE AI BANK
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🖼  Starting screenshot-to-code..."
echo "   Backend: http://localhost:7001"
echo "   Frontend: http://localhost:5173"
echo ""
echo "   Usage: drag a screenshot of Revolut/Wise/banxe.com → get React code"
echo "   Output: copy into ~/banxe-ui/apps/web/src/screens/"
echo ""

# Backend
cd "$DIR/backend"
source .venv/bin/activate
uvicorn main:app --reload --port 7001 &
BACKEND_PID=$!

# Frontend
cd "$DIR/frontend"
PORT=5173 yarn dev &
FRONTEND_PID=$!

echo "PIDs: backend=$BACKEND_PID frontend=$FRONTEND_PID"
echo "Stop: kill $BACKEND_PID $FRONTEND_PID"

wait
STARTSCRIPT
chmod +x "$TARGET_DIR/start-banxe.sh"

echo ""
echo -e "${BOLD}───────────────────────────────────────────────────────${RESET}"
echo -e "  ${GREEN}✅ screenshot-to-code готов к использованию${RESET}"
echo ""
echo -e "  Запуск:"
echo -e "    ${YELLOW}bash $TARGET_DIR/start-banxe.sh${RESET}"
echo ""
echo -e "  Workflow для BANXE AI BANK:"
echo -e "    1. Открой http://localhost:5173"
echo -e "    2. Загрузи скриншот Revolut / Wise / N26 / banxe.com"
echo -e "    3. Выбери: React + Tailwind"
echo -e "    4. Получи React код"
echo -e "    5. Скопируй в ~/banxe-ui/apps/web/src/screens/<ScreenName>/"
echo -e "    6. Адаптируй под BANXE дизайн-систему (tailwind.config.ts)"
echo ""
echo -e "${BOLD}═══════════════════════════════════════════════════════${RESET}"
echo ""
