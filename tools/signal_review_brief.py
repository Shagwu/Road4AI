#!/usr/bin/env python3
"""Weekly signal review brief — surfaces top queue-for-review candidates.

Usage:
    python tools/signal_review_brief.py              # last 7 days, top 10
    python tools/signal_review_brief.py --days 14    # custom window
    python tools/signal_review_brief.py --top 5      # custom count
    python tools/signal_review_brief.py --json       # machine-readable output

Writes to state/signal-review-brief.md (human) or stdout (JSON).
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIGNAL_LOG = ROOT / "state" / "signal_log.jsonl"
BRIEF_PATH = ROOT / "state" / "signal-review-brief.md"


def load_signals(days: int) -> list:
    """Load queue-for-review signals from the last N days."""
    if not SIGNAL_LOG.exists():
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    signals = []

    with open(SIGNAL_LOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                s = json.loads(line)
            except json.JSONDecodeError:
                continue

            if s.get("action") != "queue-for-review":
                continue

            harvested = s.get("harvested_at", "")
            if harvested:
                try:
                    ts = datetime.fromisoformat(harvested.replace("Z", "+00:00"))
                    if ts < cutoff:
                        continue
                except (ValueError, TypeError):
                    continue

            signals.append(s)

    return signals


def rank_signals(signals: list) -> list:
    """Rank by confidence (desc), then recency (desc), then underrep_boost."""
    def score(s):
        conf = s.get("confidence", 0)
        underrep = 1 if s.get("underrep_boost") else 0
        # Recency: newer = higher (use harvested_at as tiebreaker)
        harvested = s.get("harvested_at", "")
        try:
            ts = datetime.fromisoformat(harvested.replace("Z", "+00:00"))
            recency = ts.timestamp()
        except (ValueError, TypeError):
            recency = 0
        return (conf, recency, underrep)

    signals.sort(key=score, reverse=True)
    return signals


def dedup(signals: list) -> list:
    """Remove duplicate entries by entry_id."""
    seen = set()
    result = []
    for s in signals:
        eid = s.get("entry_id", "")
        if eid in seen:
            continue
        seen.add(eid)
        result.append(s)
    return result


def format_brief(signals: list, top_n: int) -> str:
    """Format signals as a markdown brief."""
    lines = [
        "# Signal Review Brief",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"Candidates: {len(signals)} (showing top {min(top_n, len(signals))})",
        "",
        "---",
        "",
    ]

    for i, s in enumerate(signals[:top_n], 1):
        title = s.get("title", s.get("text", "Untitled"))[:80]
        source = s.get("query", "unknown")
        conf = s.get("confidence", 0)
        link = s.get("link", "")
        clusters = s.get("underrep_clusters", [])
        underrep = " (underrepresented)" if s.get("underrep_boost") else ""

        lines.append(f"## {i}. {title}")
        lines.append("")
        lines.append(f"- **Source:** {source}")
        lines.append(f"- **Confidence:** {conf:.2f}{underrep}")
        if clusters:
            lines.append(f"- **Topics:** {', '.join(clusters)}")
        if link:
            lines.append(f"- **Link:** {link}")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Next steps",
        "",
        "1. Pick candidates with a Road4AI angle",
        "2. Add selected signals as entries to `inbox.md`",
        "3. Run content-pipeline to draft from selected signals",
        "",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Weekly signal review brief")
    parser.add_argument("--days", type=int, default=7,
                        help="Look back N days (default: 7)")
    parser.add_argument("--top", type=int, default=10,
                        help="Show top N candidates (default: 10)")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON instead of markdown")
    args = parser.parse_args()

    signals = load_signals(args.days)
    if not signals:
        print(f"No queue-for-review signals in last {args.days} days.", file=sys.stderr)
        if args.json:
            print(json.dumps({"signals": [], "count": 0}))
        sys.exit(0)

    signals = dedup(signals)
    signals = rank_signals(signals)

    if args.json:
        result = {
            "count": len(signals),
            "top": args.top,
            "signals": [
                {
                    "title": s.get("title", s.get("text", ""))[:80],
                    "source": s.get("query", ""),
                    "confidence": s.get("confidence", 0),
                    "link": s.get("link", ""),
                    "underrep_boost": s.get("underrep_boost", False),
                    "clusters": s.get("underrep_clusters", []),
                }
                for s in signals[: args.top]
            ],
        }
        print(json.dumps(result, indent=2))
    else:
        brief = format_brief(signals, args.top)
        BRIEF_PATH.parent.mkdir(parents=True, exist_ok=True)
        BRIEF_PATH.write_text(brief)
        print(f"Brief written to {BRIEF_PATH}")
        print(f"Found {len(signals)} candidates, showing top {min(args.top, len(signals))}")


if __name__ == "__main__":
    main()
