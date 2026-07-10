# Retroactive Audit Entry: Landing Page v2.1 Update

**Date:** 2026-07-10
**Related gap:** PR #2 merged without a Karen adversarial review gate (flagged for retroactive audit)
**Status:** Content shipped. Process gap logged for fix.

## What happened

MiMo Auto updated `index.html` with v2.1 content (SkillOpt scores, Hermes v2.0, benchmark proof cards). First pass included fabricated or misattributed numbers: a 0.6447 baseline that didn't exist in any report file, a +22% improvement derived from that baseline, a 0.7504 audit mean with no source, and a "zero em dashes" claim pulled from the deterministic evaluator and mislabeled as a live Ollama result.

## How it was caught

Not by the review gate. Manual instruction to verify claims against source files triggered MiMo to grep its own report files and confirm or remove each number. Karen's pass returned REQUEST_CHANGES, but on inspection this was a false positive from deterministic fallback confusion, flagging CSS/nav lines rather than the content claims. No real adversarial review ran against the actual numbers.

## What shipped

Final version kept only claims with a matching source file:
- 0.788 live Ollama (`execution/runs/2026-07-07-005/live-report.md`)
- 0.871 deterministic (`deterministic-final-v2-july-2026.md`)
- 10 benchmark cases (confirmed in report headers)
- "No protected file mutations" replacing the unverified "zero governance violations"

## The gap

Verification was performed by the same agent that produced the original fabricated numbers. This is self-verification, not independent review. It happened to work here because a human caught the pattern and asked for source-file grounding, not because the pipeline has a gate that would catch this by default. This is the same shape as the PR #2 gap: content moved to a public-facing surface without a real adversarial checkpoint in the loop.

## Fix to fold into the PR #2 retroactive audit

- Landing page / public-facing content changes need a review step that isn't the authoring agent grepping its own outputs.
- Karen's false-positive-on-CSS behavior here is a second, smaller finding worth a line in `POC_AUDIT_CRITERIA.md`: the deterministic fallback is flagging structural lines instead of content, which means REQUEST_CHANGES can't currently be trusted as a signal without manual inspection of what actually got flagged.
