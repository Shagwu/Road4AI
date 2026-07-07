---
platform: x
status: ready_for_edit
type: Behind-the-scenes
goal: Build in public
karen_verdict: APPROVED
karen_date: 2026-07-07
karen_note: Deterministic review. All tweets under 280 chars (longest: 194). Zero em dashes, zero reject traits in voice, numbers match source data.
scheduled: true
---

# What the Audit Caught (X Thread)

## Tweet 1

I was about to publish a benchmark score I couldn't reproduce.

The reveal post claimed 0.871. My data showed 0.788. Same benchmark, different execution paths.

Here's how the POC audit caught it:

## Tweet 2

The 0.871 came from a deterministic evaluator. It checks em dashes and reject traits with pattern matching. Zero variance by design. You get the same number every time.

The 0.788 came from a live Ollama run. Real model inference. Same skill, same cases, but the model actually generates text and gets scored on it.

## Tweet 3

The problem: I was presenting both numbers as if they were the same kind of result.

0.6447 baseline (live Ollama) to 0.871 (deterministic) sounds like a 35% improvement. But you can't rerun the 0.871 the same way you reran the 0.6447. Different method. Different execution path.

## Tweet 4

The POC audit criteria had a hard fail gate: "reveal post numbers don't match data."

I defined it as a future check. Then I read my own reports and realized it was already failing. The number was in the post. The data said something different.

## Tweet 5

Fixed the reveal. Headline: 0.6447 to 0.788. Live. Reproducible. Zero failures.

Deterministic 0.871 disclosed as separate methodology. Not hidden. Just not the headline.

This is what audit gates are for.

---

## Publication Instructions

**Platform:** X/Twitter
**Time:** July 26, 09:00 WAT (10:00 UTC)
**Format:** 5-tweet thread
**Duration:** Pin thread to profile for 24 hours
