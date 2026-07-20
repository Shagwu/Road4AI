---
title: "What We Let the Harvester Keep"
hook: "I almost let my harvester auto-publish. Then Karen intervened."
type: Behind-the-scenes
platform: LinkedIn
goal: Build in public
status: ready_for_publishing
karen_verdict: APPROVED
scheduled: true
---

I almost let my harvester auto-publish. Then Karen intervened.

Karen is the adversarial review gate — a two-model pipeline that catches what the primary model misses. It's been running on drafts, governance changes, and publishing decisions for months. But the harvester scripts had never gone through it.

I staged the four harvester files for review and ran Karen. She couldn't run — no staged diff, because the files hadn't been modified. So I did the review manually, applying the same criteria: real bugs, missing imports, race conditions, hallucinated claims.

Found three things.

One: dead code. Thirty-three lines after a return statement in match_clusters() — a copy-paste leftover from get_keyword_counts() that could never execute. Harmless but confusing.

Two: an unused constant. DEDUP_SAME_URL was defined, referenced in docs, but never actually used anywhere. Removed it.

Three: a race condition. Both harvester scripts write to shared state files without locking. Safe at the current 10-hour gap between automated runs, but a real risk if the schedule ever tightens.

The duplicated confidence scorer between harvester_pipeline.py and harvester_reader.py survived the review — flagged as a known risk with a revisit trigger, not a blocker.

Karen approved. The harvester scripts are now the first code in this project with a documented post-commit Karen review. Not because they're the most critical code, but because they run unattended — and unreviewed code running unattended is the exact pattern that caused PR #2.
