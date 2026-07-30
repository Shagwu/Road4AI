---
title: "The Harvester Governance Gap"
hook: "Karen never reviewed the harvester scripts before they went live."
type: Struggle
platform: LinkedIn
goal: Build in public
status: ready_for_publishing
karen_verdict: APPROVED
karen_rerun: "2026-07-25 — post-edit, content-mode review passed with minor fixes"
scheduled: true
source: operator_capture
created_at: 2026-07-24T00:00:00Z
---

Karen never reviewed the harvester scripts before they went live.

Same pattern as PR #2. Code ships, tests pass, and the adversarial review step gets skipped somewhere in the shuffle. 19 out of 19 tests green. Two governance docs committed. Everything looked rigorously tested.

Last time this happened with PR #2, it took a retroactive audit to catch the governance gaps after decision logic had already shipped. This time I caught it before the 18:00 UTC run went out unattended, not after.

So I ran Karen against harvester_pipeline.py, scheduled_harvester.py, and harvester_drift_hook.py. Post-commit, because the code was already live. Two rounds. Here's what she found:

Three dead imports that compiled fine but would have thrown at runtime under the right conditions. A confidence boost for "Hacker News" feeds that never fires because no feed key contains that string. A race condition on the signals_processed counter that would lose increments under concurrent runs. None of it broke anything today. All of it would have broken something later.

That's the actual point of building a governance layer. Not that mistakes stop happening. It's that you build enough friction into the process that you catch them before they ship instead of after.

The harvester now has a Karen gate. It runs before every unattended launchd cycle. The gap is closed. But the gap existed for three days, and nothing in the test suite would have caught it.
