#!/bin/bash
# Install/uninstall Road4AI scheduled tasks (macOS launchd)
#
# Usage:
#     ./config/install_schedule.sh install [drift|harvester|all]
#     ./config/install_schedule.sh uninstall [drift|harvester|all]
#     ./config/install_schedule.sh status

SCRIPT_DIR="$(dirname "$0")"
TARGET="${2:-all}"

install_task() {
    local name="$1"
    local plist="com.road4ai.${name}"
    local src="${SCRIPT_DIR}/${plist}.plist"
    local dst="$HOME/Library/LaunchAgents/${plist}.plist"

    if [ ! -f "$src" ]; then
        echo "Plist not found: $src"
        return 1
    fi

    cp "$src" "$dst"
    launchctl unload "$dst" 2>/dev/null
    launchctl load "$dst" 2>/dev/null
    echo "Installed: $name"
}

uninstall_task() {
    local name="$1"
    local plist="com.road4ai.${name}"
    local dst="$HOME/Library/LaunchAgents/${plist}.plist"

    launchctl unload "$dst" 2>/dev/null
    rm -f "$dst"
    echo "Uninstalled: $name"
}

status_task() {
    local name="$1"
    local plist="com.road4ai.${name}"
    local dst="$HOME/Library/LaunchAgents/${plist}.plist"

    if launchctl list 2>/dev/null | grep -q "$plist"; then
        echo "  ✓ $name: active"
    else
        echo "  ✗ $name: inactive"
    fi
    echo "    Plist: $([ -f "$dst" ] && echo "installed" || echo "missing")"
}

case "${1:-status}" in
    install)
        case "$TARGET" in
            drift)     install_task "drift-monitor" ;;
            harvester) install_task "scheduled-harvester" ;;
            all)       install_task "drift-monitor"
                       install_task "scheduled-harvester" ;;
            *)         echo "Unknown task: $TARGET (use drift, harvester, or all)"; exit 1 ;;
        esac
        echo ""
        echo "Logs: state/drift-cron.log, state/harvester-cron.log"
        ;;
    uninstall)
        case "$TARGET" in
            drift)     uninstall_task "drift-monitor" ;;
            harvester) uninstall_task "scheduled-harvester" ;;
            all)       uninstall_task "drift-monitor"
                       uninstall_task "scheduled-harvester" ;;
            *)         echo "Unknown task: $TARGET (use drift, harvester, or all)"; exit 1 ;;
        esac
        ;;
    status)
        echo "=== Road4AI Scheduled Tasks ==="
        status_task "drift-monitor"
        status_task "scheduled-harvester"
        ;;
    *)
        echo "Usage: $0 {install|uninstall|status} [drift|harvester|all]"
        exit 1
        ;;
esac
