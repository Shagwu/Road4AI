---
title: "The Twitter CLI Broke"
hook: "My harvester lost its only data source mid-build."
type: Struggle
platform: LinkedIn
goal: Build in public
status: ready_for_publishing
karen_verdict: APPROVED
scheduled: true
---

My harvester lost its only data source mid-build.

The Twitter CLI returned a 404. Not rate-limited, not auth-gated — just gone. The build system was broken upstream, and I had no fallback. One morning the harvester was searching Twitter for Road4AI-relevant signals. The next morning it had nothing to search.

I tried OpenCLI. Missing dependency. Reddit. 403 — OAuth required. Three attempts, three dead ends, same afternoon.

The only thing that worked was RSS. Eight feeds I'd already tested for the feed criteria doc. TechCrunch, Ars Technica, Hugging Face, Ollama, AI Alignment Forum, LessWrong, Synced AI, MIT Tech Review. I'd written them off as "broad" — too general, not niche enough for Road4AI's lane.

They were the only lane left.

Pivoted the entire harvester from Twitter CLI to RSS in a day. Added canonical URL dedup, cluster-based underrepresentation checks, and a Karen gate on the signal routing. The harvester that went down was a single-source tool. The one that came back was a pipeline.

The lesson I didn't expect: the best fallback wasn't a better version of the same thing. It was a different architecture entirely. RSS feeds don't need auth, don't break when a CLI maintainer disappears, and don't rate-limit at the worst possible moment.

The Twitter CLI is still broken. The harvester doesn't care anymore.
