---
title: "The Underrep Boost Works"
hook: "One config change and the harvester started surfacing signals it was silently dropping."
type: Win
platform: X
goal: Build in public
status: ready_for_publishing
karen_verdict: APPROVED
scheduled: true
---

## Tweet 1
One config change and the harvester started surfacing signals it was silently dropping.

The underrep boost went from 0 to 9 signals in a single day.

## Tweet 2
The fix: concept clusters. 8 clusters — subject, memory, local, evals, governance, training, open, orchestration. Article fires the boost when it matches >= 2 clusters. Filters false positives by requiring topical convergence.

## Tweet 3
Before the fix: everything below 0.5 confidence got discarded. Including relevant signals about AI agent memory that used different phrasing than the keyword list.

After: those signals get rescued. Routed to queue-for-review instead of thrown out.

## Tweet 4
The math: 21 signals in, 9 underrep-boosted, 11 queued for review. The harvester isn't just filtering — it's actively rescuing underrepresented topics.

9 signals that would have been silently dropped are now in the pipeline.

## Tweet 5
This is what governance looks like in practice. Not a policy doc. A config change that makes the system surface what it was missing, and a gate that ensures nothing gets through that shouldn't.
