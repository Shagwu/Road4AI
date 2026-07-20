---
title: "The Harvester's First Month"
hook: "274 signals. 8 feeds. One month of watching the harvester learn what matters."
type: Behind-the-scenes
platform: LinkedIn
goal: Build in public
status: ready_for_drafting
karen_verdict: null
---

274 signals. 8 feeds. One month of watching the harvester learn what matters.

June 29: first run. Twitter CLI, single source, no dedup. 25 signals, 13 queued for review. The harvester was a search tool with a confidence score.

July 17: the Twitter CLI broke. Pivoted to 8 RSS feeds in a day. Added canonical URL dedup — two URLs differing only in tracking params are now recognized as the same article. Signal count dropped. Quality went up.

July 18: cluster matching landed. 8 concept clusters requiring >= 2 matches to fire the underrep boost. Same day, the boost went from 0 to 9 signals. The harvester started finding things it was silently dropping before.

July 18: Karen reviewed the harvester scripts. Found dead code, an unused constant, a race condition on shared state files. Approved with known risks documented. The harvester now has a governance trail.

July 18: the ratio script got fixed — it was sorting by queue array position instead of post date, giving wrong answers for a week without anyone noticing.

One month. The harvester went from a Twitter search wrapper to a gated, deduped, cluster-matched, Karen-reviewed signal pipeline. Not because I planned it that way, but because each failure demanded the next improvement.

The pattern I keep seeing: the system that works is the one that broke and got fixed, not the one that never ran.
