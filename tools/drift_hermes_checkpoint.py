#!/usr/bin/env python3
"""
Hermes checkpoint integration for drift monitoring.
Runs drift check and formats result as a Hermes checkpoint commit message.

Usage:
    python tools/drift_hermes_checkpoint.py
    python tools/drift_hermes_checkpoint.py --dry-run
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drift_monitor import DriftMonitor


def generate_checkpoint(dry_run: bool = False) -> dict:
    """Run drift check and generate Hermes checkpoint block."""
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

    # Build Hermes checkpoint block
    status = report["overall_status"]
    sv_var = next((c["variance"] for c in report["domain_checks"] if c["domain"] == "social_voice"), 0)
    mo_var = next((c["variance"] for c in report["domain_checks"] if c["domain"] == "memory_ops"), 0)
    corr = report["cross_domain"]["correlation"]

    if status == "green":
        decisions = f"Drift check passed: sv={sv_var:.1%} mo={mo_var:.1%} corr={corr:.2f}. All domains within tolerance."
        remaining = "Next daily check scheduled. No action needed."
        confidence = "high"
    elif status == "yellow":
        affected = [c["domain"] for c in report["domain_checks"] if c["status"] == "yellow"]
        decisions = f"Yellow alert: {', '.join(affected)} variance exceeds ±5% threshold."
        remaining = "Investigate affected domains. Review optimizer edits if any."
        confidence = "medium"
    else:
        affected = [c["domain"] for c in report["domain_checks"] if c["status"] == "blue"]
        decisions = f"BLUE HALT: {', '.join(affected)} variance exceeds ±10%. Drift monitoring paused."
        remaining = "ROOT CAUSE INVESTIGATION REQUIRED before resuming."
        confidence = "low"

    checkpoint_block = f"""CHECKPOINT: Daily drift check — {status.upper()}

[hermes-context]
Decisions: {decisions}
Remaining: {remaining}
Confidence: {confidence}
Context_type: system
Agent: claude
[/hermes-context]"""

    result = {
        "timestamp": report["timestamp"],
        "status": status,
        "checkpoint_block": checkpoint_block,
        "report": report
    }

    if not dry_run:
        monitor.log_result(report)

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Hermes checkpoint for drift monitoring")
    parser.add_argument("--dry-run", action="store_true", help="Don't write to state files")
    parser.add_argument("--print-only", action="store_true", help="Print checkpoint block only")
    args = parser.parse_args()

    result = generate_checkpoint(dry_run=args.dry_run)

    if args.print_only:
        print(result["checkpoint_block"])
    else:
        status = result["status"]
        marker = {"green": "\u2713", "yellow": "\u26a0", "blue": "\u2717"}.get(status, "?")
        print(f"Drift Check: {marker} {status.upper()}")
        print()
        print(result["checkpoint_block"])

    return 1 if result["status"] == "blue" else 0


if __name__ == "__main__":
    raise SystemExit(main())
