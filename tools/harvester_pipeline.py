#!/usr/bin/env python3
"""
Full harvester pipeline: RSS feed search → signal extraction → drift gate → routing.

Usage:
    python tools/harvester_pipeline.py --query "AI agents" --limit 5
    python tools/harvester_pipeline.py --query "local LLM" --limit 10 --dry-run
"""

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from html import unescape

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harvester_drift_hook import gate_check, process_signal

try:
    import feedparser
except ImportError:
    feedparser = None

try:
    import requests
except ImportError:
    requests = None

# RSS feeds relevant to Road4AI topics
RSS_FEEDS = {
    # Mainstream AI news
    "ars_technica": "https://feeds.arstechnica.com/arstechnica/technology-lab",
    "techcrunch_ai": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "mit_tech_review": "https://www.technologyreview.com/feed/",
    # Local LLM & open source AI
    "ollama_blog": "https://ollama.com/blog/rss.xml",
    "huggingface_blog": "https://huggingface.co/blog/feed.xml",
    # AI research & governance
    "ai_alignment_forum": "https://www.alignmentforum.org/feed.xml",
    "lesswrong_ai": "https://www.lesswrong.com/feed.xml?view=ai",
    "synced_ai": "https://syncedreview.com/feed/",
}

# Keyword mappings for query routing
QUERY_TO_FEEDS = {
    "AI agent memory local": ["techcrunch_ai", "huggingface_blog", "ollama_blog"],
    "zero cost AI tools open source": ["ollama_blog", "huggingface_blog", "ars_technica"],
    "multi-agent orchestration": ["techcrunch_ai", "ai_alignment_forum", "lesswrong_ai"],
    "Hermes AI memory": ["huggingface_blog", "ollama_blog", "synced_ai"],
    "build AI agent from scratch": ["techcrunch_ai", "huggingface_blog", "ars_technica"],
    "local LLM inference": ["ollama_blog", "huggingface_blog", "lesswrong_ai"],
}

# Harvester thresholds (must match .agents/harvester/HARVESTER_FEED_CRITERIA.md)
STALE_OVERRIDE_MAX_AGE_DAYS = 21        # N — keyword match overrides staleness if entry < N days old
UNDERREPRESENTED_KEYWORD_MAX_SIGNALS = 3  # K — keywords with < K signals in lookback window get boost
UNDERREPRESENTED_LOOKBACK_DAYS = 14     # M — lookback window for underrepresentation check

def canonicalize_url(url: str) -> str:
    """Strip tracking params and trailing slashes for dedup comparison."""
    url = url.split("?utm_")[0].split("&utm_")[0]
    url = url.split("?ref=")[0].split("&ref=")[0]
    url = url.rstrip("/")
    return url.lower()


def should_log_signal(item: dict, seen_urls: set) -> bool:
    """Check if signal should be logged (dedup gate). Returns True if unique."""
    url = canonicalize_url(item.get("link", "") or item.get("entry_id", ""))
    if not url:
        return True
    if url in seen_urls:
        return False
    seen_urls.add(url)
    return True


# Concept clusters for underrepresentation check (appear in external RSS content)
# An article fires the underrep boost only when it matches terms from
# AT LEAST TWO different clusters — catches phrasing variance while
# filtering out unrelated "memory" (hardware), "agent" (insurance), etc.
TOPICAL_CLUSTERS = {
    "subject": ["agent", "AI", "LLM", "model", "bot", "assistant", "chatbot"],
    "memory": ["memory", "context window", "recall", "state", "context overflow",
               "context management", "long-term memory", "working memory"],
    "local": ["local", "self-hosted", "on-device", "on-premise", "edge",
              "local inference", "local llm", "local model"],
    "evals": ["evals", "evaluation", "benchmark", "testing", "metrics", "scoring"],
    "governance": ["guardrail", "governance", "safety", "alignment", "drift",
                   "oversight", "audit", "compliance"],
    "training": ["fine-tune", "fine-tuning", "quantization", "optimization",
                 "training", "distillation", "gguf"],
    "open": ["open source", "open weights", "open-source", "free", "zero-cost",
             "open model", "open weights"],
    "orchestration": ["multi-agent", "orchestration", "coordination", "swarm",
                      "pipeline", "agent loop", "agent framework"],
}

# Flatten for backward-compatible get_keyword_counts
TOPICAL_KEYWORDS = sorted({kw for terms in TOPICAL_CLUSTERS.values() for kw in terms})

# Brand keywords for "Road4AI mentioned externally" monitor
BRAND_MENTIONS = [
    "skillopt", "hermes", "road4ai", "obsidian", "blotato",
    "skill optimization", "zero-cost",
]


def get_keyword_counts(log_path: Path, lookback_days: int = None,
                       keywords: list = None) -> dict:
    """Scan signal_log.jsonl and count unique signals per keyword in the lookback window."""
    if lookback_days is None:
        lookback_days = UNDERREPRESENTED_LOOKBACK_DAYS
    if keywords is None:
        keywords = TOPICAL_KEYWORDS

    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)
    counts = {kw: 0 for kw in keywords}

    if not log_path.exists():
        return counts

    seen_urls = set()
    for line in log_path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Only count deduped rows (skip if URL already seen)
        url = canonicalize_url(row.get("link", "") or row.get("entry_id", ""))
        if url in seen_urls:
            continue
        seen_urls.add(url)

        # Check recency
        harvested = row.get("harvested_at", "")
        if harvested:
            try:
                ts = datetime.fromisoformat(harvested.replace("Z", "+00:00"))
                if ts < cutoff:
                    continue
            except (ValueError, TypeError):
                continue

        # Count keyword matches
        text = (row.get("title", "") + " " + row.get("text", "")).lower()
        for kw in keywords:
            if kw in text:
                counts[kw] += 1

    return counts


def match_clusters(text: str, min_clusters: int = 2) -> list:
    """Check which concept clusters match the text. Returns matched cluster names.

    An article fires the underrep boost when it matches >= min_clusters clusters.
    This filters out false positives (hardware "memory", insurance "agent") by
    requiring topical convergence.
    """
    text_lower = text.lower()
    matched = []
    for cluster_name, terms in TOPICAL_CLUSTERS.items():
        for term in terms:
            if term.lower() in text_lower:
                matched.append(cluster_name)
                break
    return matched


def get_underrepresented_keywords(log_path: Path = None) -> list:
    """Return topical keywords with fewer than K signals in the last M days."""
    if log_path is None:
        log_path = Path("state/signal_log.jsonl")

    counts = get_keyword_counts(log_path, keywords=TOPICAL_KEYWORDS)
    threshold = UNDERREPRESENTED_KEYWORD_MAX_SIGNALS

    return [kw for kw, n in counts.items() if n < threshold]


def get_brand_mentions(log_path: Path = None) -> int:
    """Count how many times Road4AI brand terms appear in recent signals."""
    if log_path is None:
        log_path = Path("state/signal_log.jsonl")

    counts = get_keyword_counts(log_path, keywords=BRAND_MENTIONS)
    return sum(counts.values())


def strip_html(html_text: str) -> str:
    """Remove HTML tags and decode entities."""
    text = re.sub(r'<[^>]+>', ' ', html_text)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def fetch_rss_feed(url: str, timeout: int = 15) -> list:
    """Fetch and parse an RSS feed, return list of entries."""
    if not feedparser or not requests:
        return []

    try:
        headers = {"User-Agent": "Road4AI-Harvester/1.0"}
        resp = requests.get(url, timeout=timeout, headers=headers)
        if resp.status_code != 200:
            return []

        feed = feedparser.parse(resp.text)
        entries = []
        for entry in feed.entries[:20]:
            published = ""
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).isoformat()
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                published = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc).isoformat()

            entries.append({
                "id": entry.get("id", entry.get("link", "")),
                "title": entry.get("title", ""),
                "text": strip_html(entry.get("summary", entry.get("description", "")))[:500],
                "link": entry.get("link", ""),
                "author": entry.get("author", entry.get("source", {}).get("title", "unknown")),
                "published": published,
                "source_feed": url,
            })
        return entries
    except Exception as e:
        print(f"  RSS fetch failed for {url[:50]}: {e}")
        return []


def run_rss_search(query: str, limit: int = 5) -> list:
    """Search RSS feeds for query-relevant entries."""
    feed_keys = QUERY_TO_FEEDS.get(query, list(RSS_FEEDS.keys())[:3])

    all_entries = []
    for key in feed_keys:
        url = RSS_FEEDS.get(key)
        if not url:
            continue
        entries = fetch_rss_feed(url)
        all_entries.extend(entries)

    # Deduplicate by ID
    seen = set()
    unique = []
    for e in all_entries:
        eid = e.get("id", "")
        if eid and eid not in seen:
            seen.add(eid)
            unique.append(e)

    # Score and sort by relevance to query
    query_words = query.lower().split()
    for entry in unique:
        text_lower = (entry["title"] + " " + entry["text"]).lower()
        matched = sum(1 for w in query_words if w in text_lower)
        entry["_relevance"] = matched / len(query_words) if query_words else 0

    unique.sort(key=lambda x: x["_relevance"], reverse=True)
    return unique[:limit]


def extract_signals(entries: list, query: str) -> list:
    """Extract harvester signals from RSS entries."""
    signals = []
    for entry in entries:
        text = entry.get("title", "") + " " + entry.get("text", "")
        author = entry.get("author", "unknown")

        # Relevance score
        query_words = query.lower().split()
        text_lower = text.lower()
        matched = sum(1 for w in query_words if w in text_lower)
        relevance = matched / len(query_words) if query_words else 0.5

        # Road4AI keyword boost
        road4ai_keywords = ["skillopt", "hermes", "road4ai", "drift", "governance",
                            "local llm", "zero-cost", "multi-agent", "obsidian", "blotato",
                            "agent memory", "skill optimization", "guardrail"]
        keyword_boost = min(0.3, sum(0.1 for kw in road4ai_keywords if kw in text_lower))

        # Source authority boost (curated feeds are higher signal)
        authority_boost = 0.15 if "hackernews" in entry.get("source_feed", "") else 0.1

        confidence = min(1.0, relevance * 0.4 + keyword_boost + authority_boost + 0.2)

        signal = {
            "source": "rss",
            "query": query,
            "entry_id": entry.get("id", ""),
            "author": author,
            "title": entry.get("title", "")[:100],
            "text": entry.get("text", "")[:200],
            "link": entry.get("link", ""),
            "last_entry_date": entry.get("published", ""),
            "confidence": round(confidence, 3),
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

    # Step 2: RSS search
    print(f"\n[2/4] RSS search: '{query}' (limit={limit})...")
    entries = run_rss_search(query, limit)
    print(f"  Found: {len(entries)} entries")
    if not entries:
        print("  No entries found. Pipeline stopped.")
        return {"status": "no_data", "entries": 0}

    for i, e in enumerate(entries[:3]):
        title = e.get("title", "")[:60]
        print(f"  [{i+1}] {e.get('author', '?')}: {title}...")

    # Step 3: Extract signals
    print(f"\n[3/4] Extracting signals...")
    signals = extract_signals(entries, query)
    print(f"  Extracted: {len(signals)} signals")
    for s in signals[:3]:
        print(f"  [{s['source']}] conf={s['confidence']:.3f} — {s['title'][:50]}...")

    # Step 4: Route through drift gate
    print(f"\n[4/4] Routing through drift gate...")
    results = []
    for signal in signals:
        if dry_run:
            result = {"action": "dry-run", "signal": signal}
        else:
            result = process_signal(signal)
        results.append(result)
        print(f"  {result['action']:15s} conf={signal['confidence']:.3f} — {signal['title'][:50]}...")

    # Summary
    actions = {}
    for r in results:
        action = r.get("action", "unknown")
        actions[action] = actions.get(action, 0) + 1

    summary = {
        "status": "complete",
        "query": query,
        "entries_found": len(entries),
        "signals_extracted": len(signals),
        "actions": actions,
        "dry_run": dry_run,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    print(f"\n=== Summary ===")
    print(f"Entries: {summary['entries_found']}")
    print(f"Signals: {summary['signals_extracted']}")
    print(f"Actions: {json.dumps(actions)}")
    if dry_run:
        print("[DRY RUN — nothing logged]")

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Full harvester pipeline (RSS-based)")
    parser.add_argument("--query", default="AI agents", help="Search query")
    parser.add_argument("--limit", type=int, default=5, help="Number of entries to fetch")
    parser.add_argument("--dry-run", action="store_true", help="Don't log to state files")
    args = parser.parse_args()

    result = run_pipeline(args.query, args.limit, args.dry_run)
    return 0 if result["status"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
