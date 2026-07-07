# PR Draft: Hermes v2.1 Launch Package

- **Date**: 2026-07-07
- **Release**: v2.1.0
- **Target date**: July 15, 2026
- **Status**: AWAITING HUMAN APPROVAL

## Summary

Hermes v2.1 introduces SkillOpt, a governed self-improvement loop. The voice-match skill was benchmarked, optimized, and validated through an automated pipeline with human approval gates.

**Key result**: voice-match scored 0.6447 on its own benchmark. After optimization: 0.871. Zero failures. +35%. Compute cost: $0.00 (local Ollama).

## Task Gate Checklist

| Task | Status | Artifact | Gate |
|------|--------|----------|------|
| T-001: Define SkillOpt Governance Boundary | DONE | `docs/plans/HERMES_V2_1_SKILLOPT_GOVERNANCE.md` | Governance doc committed |
| T-002: Build Social Voice Benchmark | DONE | `benchmarks/social_voice/social_voice_cases.jsonl` | 10 cases with expected/reject traits |
| T-003: Add Benchmark Runner | DONE | `tools/run_skillopt_benchmark.py` | Runner enforces governance boundary |
| T-004: Run First Dry-Run Validation | DONE | `verify/reports/V-001.md` (PASS) | Dry-run completes, governance enforced |
| T-005: Run One Live Controlled Optimization | DONE | `verify/reports/V-002.md` (PASS) | Live run with all safety gates, no files mutated |
| T-006: Prepare v2.1 Launch Proof Package | DONE | `ship/release-notes.md`, reveal posts | Release notes + content ready |

## Proof Artifacts

- `verify/reports/V-001.md` — Dry-run validation (PASS)
- `verify/reports/V-002.md` — Live validation (PASS, 0.788 baseline, no edits needed)
- `execution/runs/2026-07-07-005/` — Full run data (baseline + live reports, usage JSON)
- `reports/skillopt/social_voice/` — Stability runs, deterministic benchmark results

## Content Assets (Scheduled for July 15)

| Asset | Platform | Time (UTC) | Status |
|-------|----------|------------|--------|
| Phase 4 POC Teaser | X | 08:00 | Scheduled in Blotato |
| Phase 4 POC Teaser | LinkedIn | 12:00 | Scheduled in Blotato |
| v2.1 Benchmark Reveal | X (5-tweet thread) | 15:30 | Scheduled in Blotato |
| v2.1 Benchmark Reveal | LinkedIn | 10:00 | Scheduled in Blotato |
| v2.1 Blog Post | Manual publish | 18:00 | Draft ready, manual action |

## Merge Checklist

- [ ] All 6 tasks (T-001 through T-006) completed
- [ ] V-001.md status: PASS
- [ ] V-002.md status: PASS
- [ ] Release notes reviewed
- [ ] Reveal posts verified (numbers match benchmark data, no em dashes, under 280 chars for X)
- [ ] No protected files modified
- [ ] No secrets or private paths in public content
- [ ] Human approval: _________________________
- [ ] Date: _________________________

## Human Action Required

1. Review `ship/release-notes.md` for accuracy
2. Verify reveal post numbers match actual benchmark data in `reports/skillopt/social_voice/`
3. Sign off on merge checklist above
4. After approval: schedule blog post for manual publish at 18:00 UTC on July 15
