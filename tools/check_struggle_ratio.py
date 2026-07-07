#!/usr/bin/env python3
"""Struggle ratio guardrail — blocks queue writes when Struggle content drops below threshold.

Usage:
    python tools/check_struggle_ratio.py                # check last 10 entries
    python tools/check_struggle_ratio.py --window 15    # custom window
    python tools/check_struggle_ratio.py --threshold 25 # custom threshold (%)
    python tools/check_struggle_ratio.py --json          # machine-readable output

Exit codes:
    0 = pass (ratio >= threshold)
    1 = fail (ratio < threshold)
    2 = error (missing queue file, parse failure)
"""

import argparse
import json
import sys
from pathlib import Path

QUEUE_PATH = Path(__file__).resolve().parent.parent / "state" / "current-queue.json"
DEFAULT_WINDOW = 10
DEFAULT_THRESHOLD = 25  # percent


def load_queue():
    if not QUEUE_PATH.exists():
        return None
    with open(QUEUE_PATH) as f:
        data = json.load(f)
    return data.get("queue", [])


def recent_entries(queue, window):
    """Return the last N entries by recency (published + scheduled + ready)."""
    active_statuses = {"published", "scheduled", "ready_for_drafting", "ready_for_edit"}
    active = [e for e in queue if e.get("status") in active_statuses]
    return active[-window:]


def struggle_ratio(entries):
    if not entries:
        return 0.0, 0
    struggle_count = sum(1 for e in entries if e.get("type") == "Struggle")
    return (struggle_count / len(entries)) * 100, struggle_count


def main():
    parser = argparse.ArgumentParser(description="Check Struggle ratio guardrail")
    parser.add_argument("--window", type=int, default=DEFAULT_WINDOW,
                        help=f"Number of recent entries to check (default: {DEFAULT_WINDOW})")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help=f"Minimum Struggle ratio in percent (default: {DEFAULT_THRESHOLD})")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON instead of human-readable text")
    args = parser.parse_args()

    queue = load_queue()
    if queue is None:
        print("ERROR: queue file not found", file=sys.stderr)
        sys.exit(2)

    entries = recent_entries(queue, args.window)
    ratio, count = struggle_ratio(entries)
    passed = ratio >= args.threshold

    if args.json:
        result = {
            "passed": passed,
            "ratio": round(ratio, 1),
            "struggle_count": count,
            "window": len(entries),
            "threshold": args.threshold,
        }
        print(json.dumps(result))
    else:
        status = "PASS" if passed else "FAIL"
        print(f"Struggle ratio: {count}/{len(entries)} = {ratio:.1f}% (threshold: {args.threshold}%)")
        print(f"Status: {status}")
        if not passed:
            deficit = args.threshold - ratio
            needed = max(1, int((args.threshold / 100) * len(entries)) - count + 1)
            print(f"Deficit: {deficit:.1f} percentage points")
            print(f"Action: generate at least {needed} Struggle post(s) before next queue write")

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
