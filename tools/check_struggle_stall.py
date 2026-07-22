#!/usr/bin/env python3
"""Struggle stall detector — flags long consecutive runs of non-Struggle posts.

Unlike check_struggle_ratio.py (which checks the trailing-window ratio),
this detects cliff breaks: sudden streaks where Struggle content vanishes.

Usage:
    python tools/check_struggle_stall.py                # check for streaks > 3
    python tools/check_struggle_stall.py --max-streak 5 # custom threshold
    python tools/check_struggle_stall.py --json         # machine-readable output

Exit codes:
    0 = pass (no streak exceeds threshold)
    1 = fail (streak detected)
    2 = error (missing queue file, parse failure)
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

QUEUE_PATH = Path(__file__).resolve().parent.parent / "state" / "current-queue.json"
DEFAULT_MAX_STREAK = 3


def load_queue():
    if not QUEUE_PATH.exists():
        return None
    with open(QUEUE_PATH) as f:
        data = json.load(f)
    return data.get("queue", [])


def sorted_by_date(queue):
    """Return active entries sorted by post date, newest first."""
    active_statuses = {"published", "scheduled", "ready_for_drafting",
                       "ready_for_edit", "ready_for_publishing"}
    active = [e for e in queue if e.get("status") in active_statuses]

    def post_date(e):
        if not isinstance(e, dict):
            return datetime.min.replace(tzinfo=None)
        for field in ("published_at", "published_time", "scheduled_time",
                      "status_updated_at"):
            val = e.get(field, "")
            if val:
                try:
                    return datetime.fromisoformat(str(val).replace("Z", "+00:00"))
                except (ValueError, TypeError):
                    continue
        return datetime.min.replace(tzinfo=None)

    active.sort(key=post_date, reverse=True)
    return active


def find_streaks(entries):
    """Find all consecutive non-Struggle streaks. Returns list of (length, start_id, end_id)."""
    streaks = []
    current_streak = 0
    streak_start = None

    for e in reversed(entries):  # oldest first
        if e.get("type") != "Struggle":
            if current_streak == 0:
                streak_start = e.get("id", "?")
            current_streak += 1
        else:
            if current_streak > 0:
                streaks.append((current_streak, streak_start, e.get("id", "?")))
            current_streak = 0
            streak_start = None

    if current_streak > 0:
        streaks.append((current_streak, streak_start, "latest"))

    return streaks


def main():
    parser = argparse.ArgumentParser(description="Struggle stall detector")
    parser.add_argument("--max-streak", type=int, default=DEFAULT_MAX_STREAK,
                        help=f"Max consecutive non-Struggle posts allowed (default: {DEFAULT_MAX_STREAK})")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON instead of human-readable text")
    args = parser.parse_args()

    queue = load_queue()
    if queue is None:
        print("ERROR: queue file not found", file=sys.stderr)
        sys.exit(2)

    entries = sorted_by_date(queue)
    streaks = find_streaks(entries)
    violating = [(l, s, e) for l, s, e in streaks if l > args.max_streak]

    if args.json:
        result = {
            "passed": len(violating) == 0,
            "max_streak": args.max_streak,
            "streaks": [{"length": l, "from": s, "to": e} for l, s, e in streaks],
            "violations": [{"length": l, "from": s, "to": e} for l, s, e in violating],
        }
        print(json.dumps(result))
    else:
        if not violating:
            print(f"No streaks exceed {args.max_streak} consecutive non-Struggle posts.")
            print("Status: PASS")
        else:
            worst = max(violating, key=lambda x: x[0])
            print(f"STALL DETECTED: {worst[0]} consecutive non-Struggle posts")
            print(f"  Streak: {worst[1]} → {worst[2]}")
            print(f"Threshold: {args.max_streak}")
            print("Status: FAIL")
            needed = worst[0] - args.max_streak
            print(f"Action: insert at least {needed} Struggle post(s) into this window")

    sys.exit(0 if not violating else 1)


if __name__ == "__main__":
    sys.exit(main())
