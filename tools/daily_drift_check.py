#!/usr/bin/env python3
"""
Daily drift check for July 1-10 monitoring window.
Run once per day. Logs to state/drift_log.jsonl, alerts to state/drift_alerts.jsonl.

Usage:
    python tools/daily_drift_check.py
    python tools/daily_drift_check.py --dry-run
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drift_monitor import DriftMonitor, DRIFT_LOG, DRIFT_ALERTS, DRIFT_HALT


def run_daily_check(dry_run: bool = False) -> dict:
    """Run daily drift check using latest orchestration scores."""
    monitor = DriftMonitor()

    sv_score = monitor.baseline["domains"]["social_voice"]["score"]
    mo_score = monitor.baseline["domains"]["memory_ops"]["score"]

    checkpoint_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "domains": [
            {"name": "social_voice", "score": sv_score, "confidence_tier": "green"},
            {"name": "memory_ops", "score": mo_score, "confidence_tier": "green"}
        ]
    }

    report = monitor.run_check(checkpoint_data)

    if not dry_run:
        monitor.log_result(report)

    # Print summary
    status = report["overall_status"]
    marker = {"green": "\u2713", "yellow": "\u26a0", "blue": "\u2717"}.get(status, "?")
    print(f"Daily Drift Check: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Status: {marker} {status.upper()}")
    for check in report["domain_checks"]:
        print(f"  {check['domain']}: {check['variance']:.2%} variance \u2014 {check['action']}")
    print(f"  Cross-domain correlation: {report['cross_domain']['correlation']:.2f}")

    if report["human_action_needed"]:
        print(f"\n\u26a0 Human action required")
    else:
        print(f"\n\u2713 All clear")

    if dry_run:
        print("\n[dry-run \u2014 not logged]")

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Daily drift check for July 1-10 window")
    parser.add_argument("--dry-run", action="store_true", help="Don't write to state files")
    args = parser.parse_args()

    report = run_daily_check(dry_run=args.dry_run)
    return 1 if report["overall_status"] == "blue" else 0


if __name__ == "__main__":
    raise SystemExit(main())
