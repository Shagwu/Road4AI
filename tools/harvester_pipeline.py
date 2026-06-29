#!/usr/bin/env python3
"""
Full harvester pipeline: Twitter search → signal extraction → drift gate → routing.

Usage:
    python tools/harvester_pipeline.py --query "AI agents" --limit 5
    python tools/harvester_pipeline.py --query "local LLM" --limit 10 --dry-run
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harvester_drift_hook import gate_check, process_signal, load_gate


def run_twitter_search(query: str, limit: int = 5) -> list:
    """Run Twitter search via agent-reach twitter-cli."""
    env = os.environ.copy()

    # Load .env if exists
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("TWITTER_AUTH_TOKEN="):
                env["TWITTER_AUTH_TOKEN"] = line.split("=", 1)[1].strip()
            elif line.startswith("TWITTER_CT0="):
                env["TWITTER_CT0"] = line.split("=", 1)[1].strip()

    # Activate venv
    venv_path = Path.home() / ".agent-reach-venv"
    if venv_path.exists():
        activate = venv_path / "bin" / "activate"
        if activate.exists():
            env["PATH"] = str(venv_path / "bin") + ":" + env.get("PATH", "")

    try:
        result = subprocess.run(
            ["twitter", "search", query, "-n", str(limit)],
            capture_output=True, text=True, timeout=30, env=env
        )
        if result.returncode != 0:
            return []

        # Parse YAML-like output
        tweets = []
        current = {}
        in_metrics = False
        for line in result.stdout.splitlines():
            line = line.rstrip()
            if line.startswith("- id:"):
                if current:
                    tweets.append(current)
                current = {"id": line.split(":", 1)[1].strip().strip("'\"")}
                in_metrics = False
            elif line.strip() == "metrics:" and current:
                in_metrics = True
            elif in_metrics and line.startswith("    likes:") and current:
                current["likes"] = int(line.split(":", 1)[1].strip())
            elif in_metrics and line.startswith("    retweets:") and current:
                current["retweets"] = int(line.split(":", 1)[1].strip())
            elif in_metrics and line.startswith("    views:") and current:
                current["views"] = int(line.split(":", 1)[1].strip())
            elif not line.startswith("    ") and in_metrics:
                in_metrics = False
            elif line.startswith("  text:") and current:
                text = line.split(":", 1)[1].strip().strip("'\"")
                current["text"] = text
            elif line.startswith("    screenName:") and current:
                current["author"] = line.split(":", 1)[1].strip().strip("'\"")
        if current:
            tweets.append(current)

        return tweets
    except Exception as e:
        print(f"Twitter search failed: {e}")
        return []


def extract_signals(tweets: list, query: str) -> list:
    """Extract harvester signals from tweets."""
    signals = []
    for tweet in tweets:
        text = tweet.get("text", "")
        likes = tweet.get("likes", 0)
        retweets = tweet.get("retweets", 0)
        author = tweet.get("author", "unknown")

        # Engagement score: log scale to prevent mega-virality from dominating
        import math
        eng_raw = likes + retweets * 3
        engagement = min(1.0, math.log1p(eng_raw) / 10)  # log scale, capped at 1.0

        # Relevance: exact query match vs partial
        query_words = query.lower().split()
        text_lower = text.lower()
        matched = sum(1 for w in query_words if w in text_lower)
        relevance = matched / len(query_words) if query_words else 0.5

        # Road4AI keyword boost
        road4ai_keywords = ["skillopt", "hermes", "road4ai", "drift", "governance",
                            "local llm", "zero-cost", "multi-agent", "obsidian", "blotato"]
        keyword_boost = min(0.3, sum(0.1 for kw in road4ai_keywords if kw in text_lower))

        confidence = min(1.0, engagement * 0.3 + relevance * 0.4 + keyword_boost + 0.2)

        signal = {
            "source": "twitter",
            "query": query,
            "tweet_id": tweet.get("id", ""),
            "author": author,
            "text": text[:200],
            "confidence": round(confidence, 3),
            "engagement": {"likes": likes, "retweets": retweets},
            "domain": "social_voice",
            "extracted_at": datetime.now(timezone.utc).isoformat()
        }
        signals.append(signal)

    return signals


def run_pipeline(query: str, limit: int = 5, dry_run: bool = False) -> dict:
    """Run the full harvester pipeline."""
    print(f"=== Harvester Pipeline: '{query}' ===\n")

    # Step 1: Gate check
    print("[1/4] Gate check...")
    gate = gate_check()
    print(f"  Allowed: {gate['allowed']}")
    print(f"  Status: {gate['gate_status']}")
    if not gate["allowed"]:
        print(f"  BLOCKED: {gate.get('reason', 'Unknown')}")
        return {"status": "blocked", "reason": gate.get("reason")}

    # Step 2: Twitter search
    print(f"\n[2/4] Twitter search: '{query}' (limit={limit})...")
    tweets = run_twitter_search(query, limit)
    print(f"  Found: {len(tweets)} tweets")
    if not tweets:
        print("  No tweets found. Pipeline stopped.")
        return {"status": "no_data", "tweets": 0}

    for i, t in enumerate(tweets[:3]):
        text = t.get("text", "")[:80]
        print(f"  [{i+1}] @{t.get('author', '?')}: {text}...")

    # Step 3: Extract signals
    print(f"\n[3/4] Extracting signals...")
    signals = extract_signals(tweets, query)
    print(f"  Extracted: {len(signals)} signals")
    for s in signals[:3]:
        print(f"  [{s['source']}] conf={s['confidence']:.3f} — {s['text'][:60]}...")

    # Step 4: Route through drift gate
    print(f"\n[4/4] Routing through drift gate...")
    results = []
    for signal in signals:
        if dry_run:
            result = {"action": "dry-run", "signal": signal}
        else:
            result = process_signal(signal)
        results.append(result)
        print(f"  {result['action']:15s} conf={signal['confidence']:.3f} — {signal['text'][:50]}...")

    # Summary
    actions = {}
    for r in results:
        action = r.get("action", "unknown")
        actions[action] = actions.get(action, 0) + 1

    summary = {
        "status": "complete",
        "query": query,
        "tweets_found": len(tweets),
        "signals_extracted": len(signals),
        "actions": actions,
        "dry_run": dry_run,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    print(f"\n=== Summary ===")
    print(f"Tweets: {summary['tweets_found']}")
    print(f"Signals: {summary['signals_extracted']}")
    print(f"Actions: {json.dumps(actions)}")
    if dry_run:
        print("[DRY RUN — nothing logged]")

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Full harvester pipeline")
    parser.add_argument("--query", default="AI agents", help="Twitter search query")
    parser.add_argument("--limit", type=int, default=5, help="Number of tweets to fetch")
    parser.add_argument("--dry-run", action="store_true", help="Don't log to state files")
    args = parser.parse_args()

    result = run_pipeline(args.query, args.limit, args.dry_run)
    return 0 if result["status"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
