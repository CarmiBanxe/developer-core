#!/bin/bash
# collab.sh — Claude Code + Aider CLI collaboration launcher
# Version: 3.0 (Aider CLI, migrated from Qoder)
# Usage: bash collab.sh [command] [options]

set -e

WORKSPACE="/home/mmber/collaboration"
AIDER_BIN="aider"

case "$1" in
  session)
    # Интерактивная сессия Aider (загружает .aider.conf.yml автоматически)
    echo "[collab] Starting interactive session (Aider CLI)..."
    cd "$WORKSPACE"
    $AIDER_BIN --yes-always
    ;;

  worker)
    # Параллельный воркер через git worktree
    # Использование: bash collab.sh worker "задача" [branch-name]
    PROMPT="${2:?Usage: collab.sh worker <prompt> [branch]}"
    BRANCH="${3:-worker-$(date +%s)}"
    WORKTREE_PATH="/tmp/collab-worktree-$BRANCH"
    echo "[collab] Starting worktree worker on branch: $BRANCH"
    cd "$WORKSPACE"
    git worktree add "$WORKTREE_PATH" -b "$BRANCH" 2>/dev/null || \
      git worktree add "$WORKTREE_PATH" "$BRANCH"
    cd "$WORKTREE_PATH"
    cp "$WORKSPACE/.aider.conf.yml" . 2>/dev/null || true
    $AIDER_BIN --message "$PROMPT" --yes-always
    echo "[collab] Worker done. Worktree: $WORKTREE_PATH (branch: $BRANCH)"
    echo "[collab] To merge: cd $WORKSPACE && git merge $BRANCH"
    ;;

  run)
    # Одиночный non-interactive запрос
    # Использование: bash collab.sh run "задача" [model]
    PROMPT="${2:?Usage: collab.sh run <prompt> [model]}"
    MODEL="${3:-}"
    echo "[collab] Running single prompt..."
    cd "$WORKSPACE"
    if [ -n "$MODEL" ]; then
      $AIDER_BIN --message "$PROMPT" --yes-always --model "$MODEL"
    else
      $AIDER_BIN --message "$PROMPT" --yes-always
    fi
    ;;

  jobs)
    # Показать активные worktree задачи
    echo "[collab] Active git worktrees:"
    cd "$WORKSPACE"
    git worktree list
    ;;

  verify)
    # Запустить верификационную сеть для проверки агента
    # Использование: bash collab.sh verify "утверждение агента" [agent_id]
    STATEMENT="${2:?Usage: collab.sh verify <statement> [agent_id]}"
    AGENT_ID="${3:-unknown-agent}"
    echo "[collab] Running verification network for agent: $AGENT_ID"
    cd "$WORKSPACE"
    python3 -m compliance.verification.orchestrator \
      --statement "$STATEMENT" \
      --agent-id "$AGENT_ID"
    ;;

  train)
    # Запустить тест-корпус Promptfoo
    # Использование: bash collab.sh train [config]
    CONFIG="${2:-compliance/training/promptfoo.yaml}"
    echo "[collab] Running Promptfoo test corpus: $CONFIG"
    cd "$WORKSPACE"
    npx promptfoo eval --config "$CONFIG" --output compliance/training/results/latest.json
    ;;

  drift)
    # Проверить drift score через DeepEval
    echo "[collab] Running DeepEval drift check..."
    cd "$WORKSPACE"
    python3 -m compliance.training.deepeval_runner
    ;;

  sim)
    # Adversarial симуляция клиентов через TinyTroupe
    # Использование: bash collab.sh sim [agent-role] [scenarios]
    ROLE="${2:-KYC Specialist}"
    SCENARIOS="${3:-10}"
    echo "[collab] Starting adversarial simulation: $ROLE ($SCENARIOS scenarios)..."
    cd "$WORKSPACE"
    python3 -m compliance.training.adversarial_sim \
      --agent-role "$ROLE" --scenarios "$SCENARIOS"
    ;;

  status)
    echo "[collab] Aider status:"
    $AIDER_BIN --version
    echo ""
    echo "[collab] Model config (.aider.conf.yml):"
    grep "model:" "$WORKSPACE/.aider.conf.yml" 2>/dev/null || echo "  (not configured)"
    ;;

  *)
    echo ""
    echo "  collab.sh — Claude Code + Aider CLI синергия v3.0"
    echo "  Aider: $($AIDER_BIN --version 2>/dev/null | head -1)"
    echo ""
    echo "  Команды:"
    echo "    session              Интерактивная сессия Aider"
    echo "    worker <p> [branch]  Параллельный воркер через git worktree"
    echo "    run <prompt> [model] Одиночный запрос (non-interactive)"
    echo "    jobs                 Список активных git worktrees"
    echo "    verify <stmt> [id]   Верификационная сеть (3 агента, консенсус 2/3)"
    echo "    train [config]       Promptfoo тест-корпус"
    echo "    drift                DeepEval drift check"
    echo "    sim [role] [N]       Adversarial симуляция N клиентов (TinyTroupe)"
    echo "    status               Версия и конфигурация Aider"
    echo ""
    echo "  Конфиг модели: $WORKSPACE/.aider.conf.yml"
    echo ""
    ;;
esac
