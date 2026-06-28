#!/bin/bash
# Install/uninstall drift monitor daily schedule (macOS launchd)
#
# Usage:
#     ./config/install_drift_schedule.sh install
#     ./config/install_drift_schedule.sh uninstall
#     ./config/install_drift_schedule.sh status

PLIST_NAME="com.road4ai.drift-monitor"
PLIST_SRC="$(dirname "$0")/${PLIST_NAME}.plist"
PLIST_DST="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"

case "${1:-status}" in
    install)
        cp "$PLIST_SRC" "$PLIST_DST"
        launchctl load "$PLIST_DST" 2>/dev/null
        echo "Installed: drift monitor runs daily at 09:00 UTC"
        echo "Plist: $PLIST_DST"
        echo "Logs: state/drift-cron.log, state/drift-cron-error.log"
        ;;
    uninstall)
        launchctl unload "$PLIST_DST" 2>/dev/null
        rm -f "$PLIST_DST"
        echo "Uninstalled: drift monitor schedule removed"
        ;;
    status)
        if launchctl list | grep -q "$PLIST_NAME"; then
            echo "Active: drift monitor is scheduled"
            launchctl list | grep "$PLIST_NAME"
        else
            echo "Inactive: drift monitor is not scheduled"
        fi
        echo "Plist exists: $([ -f "$PLIST_DST" ] && echo "yes" || echo "no")"
        ;;
    *)
        echo "Usage: $0 {install|uninstall|status}"
        exit 1
        ;;
esac
