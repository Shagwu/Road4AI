#!/usr/bin/env python3
"""Harvester reader — reads signals from platforms via agent-reach CLIs.

Feeds signals into harvester_drift_hook.py for confidence-tiered routing.

Usage:
    python tools/harvester_reader.py --platform twitter --query "Road4AI" --limit 5
    python tools/harvester_reader.py --platform github --query "Road4AI" --limit 5
    python tools/harvester_reader.py --platform rss --url "https://example.com/feed.xml"
    python tools/harvester_reader.py --all --query "Road4AI"
"""
import argparse
import json
import subprocess
import sys
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from harvester_drift_hook import load_gate, route_signal, save_gate

# Relevance keywords for confidence scoring
HIGH_RELEVANCE = ["road4ai", "shagwu", "multi-agent", "hermes", "voice-match", "skillopt", "blotato"]
MEDIUM_RELEVANCE = ["ai agent", "local inference", "ollama", "zero-cost", "content pipeline", "build in public"]
LOW_RELEVANCE = ["ai", "agent", "llm", "automation"]


def score_confidence(text: str, source: str) -> float:
    """Score signal confidence based on keyword relevance."""
    text_lower = text.lower()
    score = 0.3  # base score

    for kw in HIGH_RELEVANCE:
        if kw in text_lower:
            score += 0.25
            break

    for kw in MEDIUM_RELEVANCE:
        if kw in text_lower:
            score += 0.15
            break

    for kw in LOW_RELEVANCE:
        if kw in text_lower:
            score += 0.05
            break

    return min(score, 1.0)


def read_twitter(query: str, limit: int = 5) -> list:
    """Read tweets matching query."""
    try:
        result = subprocess.run(
            ["twitter", "search", query, "-n", str(limit), "--json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            # Try without --json
            result = subprocess.run(
                ["twitter", "search", query, "-n", str(limit)],
                capture_output=True, text=True, timeout=30
            )
        if result.returncode != 0:
            print(f"[harvester] twitter error: {result.stderr[:200]}", file=sys.stderr)
            return []

        lines = [l for l in result.stdout.strip().split("\n") if l.strip()]
        signals = []
        for line in lines[:limit]:
            try:
                tweet = json.loads(line)
                text = tweet.get("text", tweet.get("full_text", ""))
                signals.append({
                    "id": f"tw-{tweet.get('id', 'unknown')}",
                    "source": "twitter",
                    "content": text,
                    "author": tweet.get("user", {}).get("screen_name", "unknown"),
                    "url": f"https://twitter.com/i/status/{tweet.get('id', '')}",
                    "timestamp": tweet.get("created_at", datetime.now(timezone.utc).isoformat()),
                })
            except json.JSONDecodeError:
                # Plain text output
                signals.append({
                    "id": f"tw-{datetime.now(timezone.utc).timestamp()}",
                    "source": "twitter",
                    "content": line,
                    "author": "unknown",
                    "url": None,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
        return signals
    except FileNotFoundError:
        print("[harvester] twitter CLI not found", file=sys.stderr)
        return []
    except subprocess.TimeoutExpired:
        print("[harvester] twitter search timed out", file=sys.stderr)
        return []


def read_github(query: str, limit: int = 5) -> list:
    """Read GitHub repos/issues matching query."""
    try:
        result = subprocess.run(
            ["gh", "search", "repos", query, "--sort", "updated", "--limit", str(limit), "--json", "name,owner,description,updatedAt,url"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            print(f"[harvester] github error: {result.stderr[:200]}", file=sys.stderr)
            return []

        repos = json.loads(result.stdout)
        signals = []
        for repo in repos:
            desc = repo.get("description", "") or ""
            signals.append({
                "id": f"gh-{repo['owner']['login']}-{repo['name']}",
                "source": "github",
                "content": f"{repo['name']}: {desc}",
                "author": repo["owner"]["login"],
                "url": repo["url"],
                "timestamp": repo.get("updatedAt", datetime.now(timezone.utc).isoformat()),
            })
        return signals
    except FileNotFoundError:
        print("[harvester] gh CLI not found", file=sys.stderr)
        return []
    except subprocess.TimeoutExpired:
        print("[harvester] github search timed out", file=sys.stderr)
        return []
    except json.JSONDecodeError:
        print("[harvester] github output not JSON", file=sys.stderr)
        return []


def read_rss(url: str, limit: int = 5) -> list:
    """Read RSS feed items."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "--max-time", "15", url],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode != 0:
            print(f"[harvester] curl error: {result.stderr[:200]}", file=sys.stderr)
            return []

        # Simple XML parsing for RSS/Atom
        text = result.stdout
        signals = []

        # Match <item> or <entry> blocks
        items = re.findall(r"<item>(.*?)</item>", text, re.DOTALL) or \
                re.findall(r"<entry>(.*?)</entry>", text, re.DOTALL)

        for item in items[:limit]:
            title = re.search(r"<title[^>]*>(.*?)</title>", item, re.DOTALL)
            link = re.search(r"<link[^>]*>(.*?)</link>", item, re.DOTALL)
            desc = re.search(r"<description[^>]*>(.*?)</description>", item, re.DOTALL) or \
                   re.search(r"<summary[^>]*>(.*?)</summary>", item, re.DOTALL)

            title_text = title.group(1).strip() if title else ""
            desc_text = desc.group(1).strip() if desc else ""
            link_text = link.group(1).strip() if link else url

            # Strip HTML tags
            title_text = re.sub(r"<[^>]+>", "", title_text)
            desc_text = re.sub(r"<[^>]+>", "", desc_text)

            signals.append({
                "id": f"rss-{hash(title_text + link_text)}",
                "source": "rss",
                "content": f"{title_text}: {desc_text[:200]}",
                "author": "rss",
                "url": link_text,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        return signals
    except FileNotFoundError:
        print("[harvester] curl not found", file=sys.stderr)
        return []
    except subprocess.TimeoutExpired:
        print("[harvester] RSS fetch timed out", file=sys.stderr)
        return []


PLATFORM_READERS = {
    "twitter": read_twitter,
    "github": read_github,
    "rss": read_rss,
}


def main():
    parser = argparse.ArgumentParser(description="Harvester reader — reads signals from platforms")
    parser.add_argument("--platform", choices=list(PLATFORM_READERS.keys()), help="Platform to read from")
    parser.add_argument("--query", default="Road4AI", help="Search query")
    parser.add_argument("--url", help="RSS feed URL (for --platform rss)")
    parser.add_argument("--limit", type=int, default=5, help="Max signals per platform")
    parser.add_argument("--all", action="store_true", help="Read from all available platforms")
    parser.add_argument("--dry-run", action="store_true", help="Score but don't route to drift hook")
    args = parser.parse_args()

    gate = load_gate()
    all_signals = []

    platforms = list(PLATFORM_READERS.keys()) if args.all else [args.platform]
    if not platforms:
        print("Error: specify --platform or --all", file=sys.stderr)
        sys.exit(1)

    for platform in platforms:
        reader = PLATFORM_READERS[platform]
        if platform == "rss" and args.url:
            signals = reader(args.url, args.limit)
        elif platform == "rss":
            print(f"[harvester] RSS requires --url", file=sys.stderr)
            continue
        else:
            signals = reader(args.query, args.limit)

        # Score and route each signal
        for sig in signals:
            sig["confidence"] = score_confidence(sig["content"], sig["source"])
            if args.dry_run:
                print(json.dumps(sig, indent=2))
            else:
                result = route_signal(gate, sig)
                print(json.dumps(result))
            all_signals.append(sig)

    if not args.dry_run:
        save_gate(gate)

    print(f"\n[harvester] Processed {len(all_signals)} signals from {len(platforms)} platform(s)", file=sys.stderr)


if __name__ == "__main__":
    main()
