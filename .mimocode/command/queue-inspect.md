---
description: Inspect Road4AI content queue state — trailing-10, type breakdown, Struggle ratio, status summary, upcoming posts, or full queue dump.
---

# Queue Inspector

Read-only inspection of `state/current-queue.json`. No mutations.

## Replaces

The inline python queue-peek pattern that appeared 89+ times across 12 sessions:
```python
python3 -c "
import json
data = json.load(open('state/current-queue.json'))
# ... ad hoc filtering, counting, printing
"
```
This command consolidates those ad hoc calls into documented subcommands with consistent output.

## Usage

```
/queue-inspect                    # Default: trailing-10 with ratio
/queue-inspect ratio              # Struggle ratio only
/queue-inspect trailing           # Full trailing-10 detail
/queue-inspect types              # Type breakdown across all non-published
/queue-inspect upcoming           # Next 7 days of scheduled posts
/queue-inspect status             # Status distribution (published/scheduled/idea/etc)
/queue-inspect <date>             # Trailing-10 as of a specific date (YYYY-MM-DD)
/queue-inspect find <keyword>     # Search queue entries by title or hook
```

## What It Does

1. Reads `state/current-queue.json`
2. Filters to relevant entries based on the subcommand
3. Outputs a clean, formatted summary
4. For ratio checks, uses date-based sorting (posts by scheduled_time, not queue array order)

## Output Format

### Default (trailing-10)
```
TRAILING-10 as of YYYY-MM-DD
─────────────────────────────────────
Date       Type          Title
2026-08-09 Struggle      The Post That Was Scheduled...
2026-08-08 Struggle      The Guardrail That Gave Wrong...
...

Struggles: N/10 = NN% (threshold: 25-30%)
Status: PASS | FAIL
```

### Ratio
```
Struggle ratio: N/10 = NN% (threshold: 25%)
Status: PASS | FAIL
[If FAIL: Deficit: N percentage points, Action: generate at least N Struggle post(s)]
```

### Types
```
Type breakdown (non-published entries):
  Struggle:           N (NN%)
  Behind-the-scenes:  N (NN%)
  Win:                N (NN%)
  Tutorial:           N (NN%)
  Idea:               N (NN%)
```

### Upcoming
```
Next 7 days:
2026-08-01  LinkedIn  Win      OpenJarvis Runs on Ollama
2026-08-02  LinkedIn  Struggle The Twitter CLI Broke
...
```

## Implementation

```python
#!/usr/bin/env python3
"""Queue inspector — read-only views of state/current-queue.json."""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

QUEUE_PATH = Path(__file__).resolve().parent.parent.parent / "state" / "current-queue.json"

def load_queue():
    if not QUEUE_PATH.exists():
        return []
    data = json.loads(QUEUE_PATH.read_text())
    return data.get("queue", [])

def post_date(e):
    if not isinstance(e, dict):
        return datetime.min.replace(tzinfo=None)
    for field in ("published_at", "scheduled_time", "status_updated_at"):
        val = e.get(field, "")
        if val:
            try:
                return datetime.fromisoformat(str(val).replace("Z", "+00:00"))
            except (ValueError, TypeError):
                continue
    return datetime.min.replace(tzinfo=None)

def trailing_10(queue, as_of=None):
    active_statuses = {"published", "scheduled", "ready_for_drafting", "ready_for_edit", "ready_for_publishing"}
    active = [e for e in queue if e.get("status") in active_statuses]
    if as_of:
        cutoff = datetime.fromisoformat(as_of + "T23:59:59+00:00")
        active = [e for e in active if post_date(e) <= cutoff]
    active.sort(key=post_date, reverse=True)
    return active[:10]

def ratio(entries):
    if not entries:
        return 0, 0, 0.0
    struggles = sum(1 for e in entries if e.get("type") == "Struggle")
    return struggles, len(entries), (struggles / len(entries) * 100) if entries else 0

def main():
    args = sys.argv[1:]
    subcmd = args[0] if args else "trailing"
    keyword = " ".join(args[1:]) if len(args) > 1 else None
    as_of = args[1] if len(args) > 1 and args[1].count("-") == 2 else None

    queue = load_queue()
    if not queue:
        print("No queue found at", QUEUE_PATH)
        sys.exit(1)

    if subcmd == "ratio" or subcmd == "trailing" or as_of:
        entries = trailing_10(queue, as_of)
        s, total, pct = ratio(entries)
        if subcmd == "ratio":
            status = "PASS" if pct >= 25 else "FAIL"
            print("Struggle ratio: %d/%d = %.1f%% (threshold: 25%%)" % (s, total, pct))
            print("Status: %s" % status)
            if pct < 25:
                needed = max(1, int(0.25 * total) - s + 1)
                print("Deficit: %.1f percentage points" % (25 - pct))
                print("Action: generate at least %d Struggle post(s) before next queue write" % needed)
        else:
            date_str = as_of or datetime.now().strftime("%Y-%m-%d")
            print("TRAILING-10 as of %s" % date_str)
            print()
            for e in entries:
                st = e.get("published_at") or e.get("scheduled_time") or e.get("status_updated_at") or "?"
                print("  %s  %-12s  %-12s  %s" % (st[:10], e.get("status", "?"), e.get("type", "?"), e.get("title", "")[:40]))
            print()
            print("Struggles: %d/%d = %.0f%%" % (s, total, pct))
            status = "PASS" if pct >= 25 else "FAIL"
            print("Status: %s" % status)

    elif subcmd == "types":
        non_pub = [e for e in queue if e.get("status") not in ("published",)]
        types = {}
        for e in non_pub:
            t = e.get("type", "unknown")
            types[t] = types.get(t, 0) + 1
        print("Type breakdown (non-published):")
        for t, count in sorted(types.items(), key=lambda x: -x[1]):
            print("  %-20s %d" % (t, count))

    elif subcmd == "upcoming":
        now = datetime.now(timezone.utc) if hasattr(datetime, 'utcnow') else datetime.utcnow()
        # Use a simple approach
        now = datetime.now()
        cutoff = now + timedelta(days=7)
        upcoming = []
        for e in queue:
            st = e.get("scheduled_time", "")
            if not st:
                continue
            try:
                ts = datetime.fromisoformat(st.replace("Z", "+00:00"))
                if ts >= datetime.now(ts.tzinfo) and ts <= cutoff.replace(tzinfo=ts.tzinfo):
                    upcoming.append(e)
            except:
                continue
        upcoming.sort(key=lambda x: x.get("scheduled_time", ""))
        print("Next 7 days:")
        for e in upcoming:
            st = e.get("scheduled_time", "?")[:10]
            print("  %s  %-12s  %-12s  %s" % (st, e.get("platform", "?"), e.get("type", "?"), e.get("title", "")[:40]))

    elif subcmd == "status":
        statuses = {}
        for e in queue:
            s = e.get("status", "unknown")
            statuses[s] = statuses.get(s, 0) + 1
        print("Status distribution:")
        for s, count in sorted(statuses.items(), key=lambda x: -x[1]):
            print("  %-20s %d" % (s, count))

    elif subcmd == "find" and keyword:
        kw = keyword.lower()
        matches = [e for e in queue if kw in e.get("title", "").lower() or kw in e.get("hook", "").lower() or kw in e.get("id", "").lower()]
        print("Matches for '%s': %d" % (keyword, len(matches)))
        for e in matches:
            print("  %-50s  %-12s  %s" % (e.get("id", "?")[:50], e.get("status", "?"), e.get("title", "")[:40]))

    else:
        print("Usage: /queue-inspect [ratio|trailing|types|upcoming|status|find <keyword>|YYYY-MM-DD]")

if __name__ == "__main__":
    main()
```

## Notes

- Uses date-based sorting (posts by scheduled_time), not queue array order.
- Includes `ready_for_publishing` in active set (the status that caused silent exclusion before the fix).
- No mutations — read-only by design.
- The `as_of` parameter lets you simulate the trailing-10 at any future date.
