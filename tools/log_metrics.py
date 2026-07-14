#!/usr/bin/env python3
"""Log a metrics snapshot for a scheduled post.

Usage:
  python tools/log_metrics.py --id 2026-07-15-v2-1-reveal-li --impressions 342 --reactions 28 --comments 7 --reposts 3
  python tools/log_metrics.py --id 2026-07-15-v2-1-reveal-li --impressions 1200 --reactions 85 --comments 19 --reposts 8
  python tools/log_metrics.py --id 2026-07-15-v2-1-reveal-li --note "24h check"
  python tools/log_metrics.py --list
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

METRICS_FILE = Path(__file__).resolve().parent.parent / "state" / "post-metrics.json"


def load():
    if METRICS_FILE.exists():
        return json.loads(METRICS_FILE.read_text())
    return {"entries": []}


def save(data):
    METRICS_FILE.write_text(json.dumps(data, indent=2) + "\n")


def find_entry(data, queue_id):
    for e in data["entries"]:
        if e["queue_id"] == queue_id:
            return e
    return None


def init_entry(data, queue_id, platform="LinkedIn"):
    entry = {
        "queue_id": queue_id,
        "platform": platform,
        "snapshots": [],
    }
    data["entries"].append(entry)
    return entry


def log_snapshot(entry, args):
    snap = {"at": datetime.now(timezone.utc).isoformat()}
    if args.impressions is not None:
        snap["impressions"] = args.impressions
    if args.reactions is not None:
        snap["reactions"] = args.reactions
    if args.comments is not None:
        snap["comments"] = args.comments
    if args.reposts is not None:
        snap["reposts"] = args.reposts
    if args.note:
        snap["notes"] = args.note
    entry["snapshots"].append(snap)
    return snap


def print_summary(entry):
    print(f"\n  {entry['queue_id']} ({entry['platform']})")
    print(f"  {'Snapshots':>10}: {len(entry['snapshots'])}")
    if entry["snapshots"]:
        latest = entry["snapshots"][-1]
        print(f"  {'Latest at':>10}: {latest['at']}")
        for k in ("impressions", "reactions", "comments", "reposts"):
            if k in latest:
                print(f"  {k:>10}: {latest[k]}")
        if latest.get("notes"):
            print(f"  {'Note':>10}: {latest['notes']}")


def list_entries(data):
    if not data["entries"]:
        print("No tracked posts yet.")
        return
    print(f"\nTracked posts: {len(data['entries'])}")
    for e in data["entries"]:
        print_summary(e)
        print()


def main():
    parser = argparse.ArgumentParser(description="Log LinkedIn post metrics")
    parser.add_argument("--id", help="Queue ID of the post (e.g. 2026-07-15-v2-1-reveal-li)")
    parser.add_argument("--platform", default="LinkedIn", help="Platform (default: LinkedIn)")
    parser.add_argument("--impressions", type=int, help="Impression count")
    parser.add_argument("--reactions", type=int, help="Reaction count")
    parser.add_argument("--comments", type=int, help="Comment count")
    parser.add_argument("--reposts", type=int, help="Repost count")
    parser.add_argument("--note", help="Optional note (e.g. '24h check')")
    parser.add_argument("--list", action="store_true", help="List all tracked posts and snapshots")
    args = parser.parse_args()

    data = load()

    if args.list:
        list_entries(data)
        return

    if not args.id:
        parser.error("--id is required (or use --list)")

    entry = find_entry(data, args.id)
    if not entry:
        entry = init_entry(data, args.id, args.platform)
        print(f"Created entry for {args.id}")

    snap = log_snapshot(entry, args)
    save(data)

    print(f"Snapshot logged at {snap['at']}")
    print_summary(entry)


if __name__ == "__main__":
    main()
