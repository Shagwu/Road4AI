#!/bin/bash

# Road4AI Content Commit Helper
# Modes: content, graph, dry-run

MODE=""
FORCE_AGENTS=false
DRY_RUN=false

usage() {
    echo "Usage: $0 [content|graph|dry-run] [--force-agents]"
    exit 1
}

# Parse positional argument (mode)
if [[ "$1" == "content" || "$1" == "graph" || "$1" == "dry-run" ]]; then
    MODE=$1
    shift
else
    # Fallback to checking flags if mode not provided as first arg
    MODE="dry-run"
fi

# Parse remaining flags
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --force-agents) FORCE_AGENTS=true ;;
        --dry-run) DRY_RUN=true ;;
        *) usage ;;
    esac
    shift
done

if [ "$MODE" == "dry-run" ]; then
    DRY_RUN=true
fi

echo "--- STEP 1: HEALTH CHECKS ---"

# 1. JSON and Content Validation
python3 tools/verify_content.py
if [ $? -ne 0 ]; then
    echo "🔴 Health checks failed. Aborting."
    exit 1
fi

# 2. AGENTS.md Protection
if git diff --cached --name-only | grep -q "AGENTS.md"; then
    if [ "$FORCE_AGENTS" = false ]; then
        echo "❌ BLOCKED: AGENTS.md is staged. This file requires manual approval gate."
        echo "Use --force-agents to override if you have human confirmation."
        exit 1
    else
        echo "⚠️  OVERRIDE: AGENTS.md staged with force flag."
    fi
fi

# 3. Cache/Log Exclusion
EXCLUDED=$(git diff --cached --name-only | grep -E "(__pycache__|\.log)$")
if [ ! -z "$EXCLUDED" ]; then
    echo "🧹 Unstaging cache/log files:"
    echo "$EXCLUDED"
    echo "$EXCLUDED" | xargs git reset HEAD > /dev/null
fi

if [ "$DRY_RUN" = true ]; then
    echo "✅ Dry run complete. No changes committed."
    exit 0
fi

echo "--- STEP 2: STAGING ---"

case $MODE in
    content)
        echo "Staging state/ and drafts/..."
        git add state/ drafts/
        ;;
    graph)
        echo "Updating graphify..."
        graphify update .
        echo "Staging graphify-out/ and hermes/..."
        git add graphify-out/ hermes/
        ;;
esac

echo "--- STEP 3: COMMIT ---"
git status --short

echo ""
read -p "Enter commit message (empty to abort): " MSG
if [ -z "$MSG" ]; then
    echo "Aborted."
    exit 0
fi

git commit -m "$MSG"
echo "✅ Commit successful."
