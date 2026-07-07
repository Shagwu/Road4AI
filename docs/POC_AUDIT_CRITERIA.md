# Phase 4 POC Audit Criteria

**Date defined:** 2026-07-07
**Deadline:** 2026-07-11 (hard gate before July 15 reveal)
**Owner:** Shagwu (human operator)

## Purpose

Define pass/fail criteria for the v2.1 SkillOpt POC before the July 15 public reveal. This document is the audit checklist. Every item is either a hard fail (delay reveal) or a soft fail (fix or disclose before July 15).

---

## Hard Fail — Delay reveal if ANY triggered

### HF-1: Score regression
Rerunning the skill against the benchmark produces a mean score below 0.64 (the pre-optimization baseline).
**Status:** Not yet tested (scheduled for July 11-12)

### HF-2: Protected file mutation
SkillOpt touched AGENTS.md, project.yaml, docs/brand-voice.md, or state files during optimization.
**Status:** PASS — V-002 confirmed no protected files were modified.

### HF-3: Rejection rule violation
Any optimized output contains em dashes, marketing hype words, or "AI-sounding" openers.
**Status:** PASS — Deterministic post-processor strips em dashes. V-002 showed zero failures.

### HF-4: Reveal post numbers don't match data
The LinkedIn post, X thread, or blog claims a number that can't be reproduced from the run artifacts in `execution/runs/` or `reports/skillopt/`.
**Status: ALREADY FLAGGED (2026-07-07)**

The original reveal posts cited 0.871 as the optimized score. This number comes from a deterministic evaluator (zero variance by design), which is a different execution path than the live Ollama runs that produced the 0.6447 baseline. The live optimized score is 0.788 (V-002, July 7, qwen2.5-coder:7b).

**Corrected claim:** 0.6447 → 0.788 live, local Ollama, zero API cost, zero failures. Deterministic 0.871 disclosed as separate methodology.

**Content already corrected:** `v2.1-benchmark-reveal-li-v2.md` (LinkedIn reveal)
**Content pending correction:** X reveal, LinkedIn Phase 4 teaser, X Phase 4 thread, blog post

---

## Soft Fail — Fix or disclose before July 15

### SF-1: Score reproducibility variance > 10%
Running the same skill + benchmark three times produces scores that vary by more than 10%.
**Benchmark:** June stability runs showed 0.26% variance (well within threshold).
**Status:** Not yet re-tested for July cycle. Schedule July 11.

### SF-2: Failed case overlap < 60%
Repeated runs produce different failing cases, meaning the benchmark isn't testing stable signal.
**Benchmark:** June runs hit 50% overlap (below 60% threshold). Already flagged in stability-test-june-2026.md.
**Status:** Known gap. The two consistently failing cases (001, 008) are strong optimization candidates; the swap cases (006, 009) are marginal.

### SF-3: Dedup logic gap
Asymmetric substring matching and no fuzzy match per AGENTS.md spec. V-003 documented this as a conditional pass.
**Status:** Known gap. Should be hardened before next content cycle but not a POC blocker.

### SF-4: Model version mismatch
The reveal claims results from a 14B model but the live validation (V-002) ran on 7B. If anyone asks "can I reproduce this?", the answer needs to be clear about which model produces which score.
**Status:** Needs disclosure in blog post. The corrected LinkedIn post already handles this by not specifying model size in the headline.

---

## Number Inventory (source of truth)

| Number | Source | Execution path | Date |
|--------|--------|---------------|------|
| 0.6447 | stability-run-1.md | Live Ollama qwen2.5-coder:14b | 2026-06-29 |
| 0.788 | V-002 / 2026-07-07-005 | Live Ollama qwen2.5-coder:7b | 2026-07-07 |
| 0.806 | stability-run-4-optimized.md | Post-processor + 14B | 2026-06-29 |
| 0.871 | deterministic-final-v2-july-2026.md | Deterministic evaluator | 2026-07-01 |
| 0.915 | memory_ops/2026-06-27-live-run.md | Live Ollama | 2026-06-27 |

**The reveal headline number is 0.788** (live, reproducible, zero failures). The deterministic 0.871 is disclosed as a separate methodology, not the headline.

---

## Audit Execution Plan

| Date | Action | Owner |
|------|--------|-------|
| 2026-07-07 | Define criteria (this doc) | Claude |
| 2026-07-07 | Fix content with wrong numbers | Claude |
| 2026-07-11 | Run reproducibility check (SF-1) | Codex or Claude |
| 2026-07-11 | Verify all content numbers match source of truth | Shagwu |
| 2026-07-12 | Execute hard fail checks (HF-1, HF-3 rerun) | Codex or Claude |
| 2026-07-13 | Fix or disclose soft fails | Shagwu + Claude |
| 2026-07-14 | Final gate review | Shagwu |
| 2026-07-15 | Publish (if all hard fails pass) | Shagwu |
