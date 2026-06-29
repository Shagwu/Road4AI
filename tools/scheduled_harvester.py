#!/usr/bin/env python3
"""
Scheduled harvester — runs Twitter searches for predefined queries,
extracts signals, routes through drift gate, saves to signal log.

Usage:
    python tools/scheduled_harvester.py
    python tools/scheduled_harvester.py --dry-run
    python tools/scheduled_harvester.py --queries "query1,query2"
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harvester_pipeline import run_twitter_search, extract_signals
from harvester_drift_hook import gate_check, process_signal

SIGNAL_LOG = Path("state/signal_log.jsonl")
HARVESTER_CRON_LOG = Path("state/harvester-cron.log")

# Default queries — Road4AI-relevant topics
DEFAULT_QUERIES = [
    "AI agent memory local",
    "zero cost AI tools open source",
    "multi-agent orchestration",
    "Hermes AI memory",
    "build AI agent from scratch",
]


def run_scheduled_harvest(queries: list = None, dry_run: bool = False) -> dict:
    """Run scheduled harvest across predefined queries."""
    queries = queries or DEFAULT_QUERIES
    timestamp = datetime.now(timezone.utc).isoformat()

    print(f"=== Scheduled Harvest: {timestamp[:16]} ===\n")

    # Gate check
    gate = gate_check()
    if not gate["allowed"]:
        print(f"BLOCKED: {gate.get('reason', 'Gate closed')}")
        return {"status": "blocked", "timestamp": timestamp}

    all_signals = []
    for query in queries:
        print(f"Query: '{query}'")
        tweets = run_twitter_search(query, limit=5)
        if not tweets:
            print(f"  No results")
            continue

        signals = extract_signals(tweets, query)
        for signal in signals:
            result = process_signal(signal)
            action = result.get("action", "unknown")
            print(f"  [{action:15s}] conf={signal['confidence']:.3f} — {signal['text'][:60]}...")
            all_signals.append({
                "query": query,
                "tweet_id": signal.get("tweet_id", ""),
                "author": signal.get("author", ""),
                "text": signal.get("text", "")[:200],
                "confidence": signal.get("confidence", 0),
                "action": action,
                "engagement": signal.get("engagement", {}),
                "harvested_at": timestamp
            })

    # Summary
    actions = {}
    for s in all_signals:
        a = s["action"]
        actions[a] = actions.get(a, 0) + 1

    summary = {
        "status": "complete",
        "timestamp": timestamp,
        "queries_run": len(queries),
        "signals_total": len(all_signals),
        "actions": actions,
        "dry_run": dry_run
    }

    print(f"\n=== Summary ===")
    print(f"Queries: {summary['queries_run']}")
    print(f"Signals: {summary['signals_total']}")
    print(f"Actions: {json.dumps(actions)}")

    # Log results
    if not dry_run and all_signals:
        SIGNAL_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(SIGNAL_LOG, "a") as f:
            for signal in all_signals:
                f.write(json.dumps(signal) + "\n")
        print(f"\nLogged {len(all_signals)} signals to {SIGNAL_LOG}")

    # Log harvest run
    if not dry_run:
        HARVESTER_CRON_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(HARVESTER_CRON_LOG, "a") as f:
            f.write(json.dumps(summary) + "\n")

    if dry_run:
        print("\n[dry-run — nothing logged]")

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Scheduled harvester")
    parser.add_argument("--dry-run", action="store_true", help="Don't log results")
    parser.add_argument("--queries", help="Comma-separated custom queries")
    args = parser.parse_args()

    queries = args.queries.split(",") if args.queries else None
    result = run_scheduled_harvest(queries, args.dry_run)
    return 0 if result["status"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
