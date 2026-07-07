---
platform: li
status: ready_for_edit
type: Behind-the-scenes
goal: Build in public
karen_verdict: APPROVED
karen_date: 2026-07-07
karen_note: Deterministic review (mistral-nemo unavailable). Zero em dashes, zero reject traits in voice, no AI-sounding openers, numbers match source data.
scheduled: true
---

# The Number That Didn't Add Up (LinkedIn)

I was about to publish a benchmark score I couldn't reproduce.

The v2.1 reveal post claimed 0.871 as the optimized score. Clean number. Sounds impressive. But when I traced it back to the actual run, 0.871 came from a deterministic evaluator, a separate execution path from the live Ollama run that produced the 0.6447 baseline.

The live optimized score was 0.788.

Same benchmark. Same skill. Different method of running it. One number was reproducible by anyone with Ollama installed. The other required a specific Python script that checks em dashes and reject traits deterministically.

I was about to present these as if they were the same kind of number. They are not.

The instinct to lead with 0.871 is worth being suspicious of. It's the flattering number. The one that makes the improvement look bigger. But a build-in-public brand lives or dies on whether someone can rerun your claim and get the same answer.

So I rewrote the reveal. 0.6447 to 0.788, live, local Ollama, zero API cost. Deterministic 0.871 disclosed as a separate methodology, not the headline.

This is the part of building in public that doesn't make the highlight reel. Figuring out which number actually means what you think it means, before you publish it.

---

## Links to Include

In the first comment:

v2.1.0 Release:
https://github.com/Shagwu/Road4AI/releases/tag/v2.1.0

POC Audit Criteria:
https://github.com/Shagwu/Road4AI/blob/main/docs/POC_AUDIT_CRITERIA.md

---

## Publication Instructions

**Platform:** LinkedIn
**Time:** July 20, 09:00 WAT (10:00 UTC)
**Format:** Single post with comment links
**Engagement:** Pin to profile for 48 hours
