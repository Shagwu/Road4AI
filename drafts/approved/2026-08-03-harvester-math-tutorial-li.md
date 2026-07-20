---
title: "How the Harvester Decides What Matters"
hook: "21 signals in, 10 thrown out. Here's the math behind the cut."
type: Tutorial
platform: LinkedIn
goal: Teach
status: ready_for_publishing
karen_verdict: APPROVED
scheduled: true
---

21 signals in, 10 thrown out. Here's the math behind the cut.

The harvester runs every morning at 08:00 UTC. It pulls RSS feeds, extracts signals, and routes each one through three gates before anything gets logged.

**Gate 1: Dedup.** Canonical URL matching. Strip UTM params, trailing slashes, lowercase. Two URLs that differ only in tracking garbage are the same article. If it's been seen before, it's out.

**Gate 2: Confidence scoring.** Each signal gets a score from 0 to 1 based on keyword relevance (does the title/text match Road4AI topics?), keyword boost (does it mention hermes, skillopt, local LLM, governance?), and source authority. Green (>= 0.8) auto-stores. Yellow (0.5-0.8) queues for review. Blue (< 0.5) discards.

**Gate 3: Underrepresentation boost.** This is the one that changed everything. Eight concept clusters — subject, memory, local, evals, governance, training, open, orchestration. An article fires the boost only when it matches terms from at least two different clusters. "Memory crunch" alone won't fire. "AI agent memory with local inference" will.

If a signal gets discarded but hits the underrep boost, it gets rescued. Routed to queue-for-review instead. The system doesn't just filter — it actively rescues signals that are underrepresented in the recent window.

Last run: 21 signals, 9 deduped, 11 queued for review, 10 discarded, 9 underrep-boosted. The harvester isn't just finding signal. It's deciding what matters.
