---
name: signal-review
description: Weekly review of harvester signals — surfaces top candidates from queue-for-review for content ideation. Use when the user asks to review signals, run a weekly brief, or see what the harvester found.
origin: Road4AI
tools:
  - Read
  - Bash
  - Grep
---

# Signal Review

## When to Activate

- The user asks "what did the harvester find?" or "review signals"
- A weekly content planning session begins
- The user wants to see what signals are waiting for review
- Ideation needs external input beyond inbox.md

Do not use this for harvester configuration, feed management, or confidence scoring changes.

## The Mechanism

The signal harvester runs twice daily via launchd, surfacing signals from RSS feeds and scoring them by confidence. Signals scoring 0.5-0.8 land in `queue-for-review` status in `state/signal_log.jsonl`. This skill surfaces the best candidates from that pile for human review.

## Workflow

1. Run `python3 tools/signal_review_brief.py` to generate the brief.
2. Read `state/signal-review-brief.md`.
3. Present the top candidates to the user.
4. For each candidate the user selects, add a line to `inbox.md` with the signal source, link, and a one-line angle.
5. Selected signals become input for `content-pipeline` ideation.

## Output Contract

Return:
- number of candidates found;
- top candidates with title, source, confidence, and link;
- recommended next step: select candidates for ideation.

## Anti-Patterns

- Do not auto-draft from signals without user selection.
- Do not modify the confidence scoring or harvester configuration.
- Do not treat the brief as content — it's a selection menu, not a draft.
