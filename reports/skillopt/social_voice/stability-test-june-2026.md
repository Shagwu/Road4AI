# Stability Test Summary — June 2026

**Run 1**: June 29, 2026. Baseline-only via Ollama `qwen2.5-coder:14b` (local, zero-cost). Mean score: 0.6447, standard deviation: 0.3709. Failed cases: case-001, case-008, case-009 (all scoring 0.09 due to reject-trait violations). 10 cases loaded from benchmark file (documented spec says 15; discrepancy flagged).

**Run 2**: June 29, 2026. Same config. Mean score: 0.6430, standard deviation: 0.3705. Failed cases: case-001, case-006, case-008.

**Stability evaluation**:
- Score variance: 0.26% — passes (+/-5% threshold)
- Stddev: stable (0.3709 → 0.3705)
- Failed case overlap: 50% (2/4 unique) — below 60% threshold

**Verdict**: Partial pass. Score and variance are stable. Failed case overlap is low due to case-006/case-009 swap near the 0.7 threshold. The two consistently failing cases (001, 008) are strong candidates for SkillOpt optimization. Recommend proceeding with optimization on the consistent failures; the marginal swap does not indicate runner instability.

**SkillOpt optimization (June 29)**: Consolidated rules targeting case-001 (marketing hype), case-008 (perfection claims), and case-002 (input reject traits). Results:
- case-001: 0.09 → 0.793 (slight regression from 0.96 due to input quoting in output section)
- case-002: 0.96 → 0.96 (maintained, regression from earlier iteration resolved)
- case-008: 0.09 → 0.96 (fixed)
- Mean score: 0.6447 → 0.806 (+25%)

**Known limitations (document for July cycle)**:
1. **Em dash compliance**: Model generates em dashes despite Rule 1. This is a model compliance issue, not solvable by rule wording alone. Consider post-processing filter or stronger prompt anchoring.
2. **Input quoting**: Output section quotes the input verbatim, which contains reject traits. Evaluator sometimes flags this. Consider removing the "Original Hook" section from output contract or adding instruction to paraphrase.
3. **Case count**: Benchmark file has 10 cases, CLAUDE.md documents 15 (12 base + 3 June runway). Discrepancy needs resolution before July benchmark.

**Post-processing filter (June 29)**: Built `tools/voice_postprocess.py` to deterministically strip em dashes and replace known reject phrases.

Test results (3 iterations, case-001 + case-008):
- Em dashes: 0 in all runs (deterministic removal)
- Reject traits: consistently absent from humanized drafts
- case-001: 0.09 → 0.793 (stable across runs)
- case-008: 0.09 → 0.793 (stable across runs)

Score ceiling with 14B model + post-processing: ~0.79-0.81. Remaining gap is model capability (missing "Manual friction focus" and "no marketing hype" traits), not post-processing. The key deliverable is deterministic compliance: zero em dashes, zero reject traits.

For July benchmark: post-processor is ready for integration into the benchmark runner pipeline.
