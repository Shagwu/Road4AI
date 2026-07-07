# Hermes v2.1 Release Notes

**Release**: v2.1.0
**Date**: July 15, 2026
**Tag**: `v2.1.0`

## What Changed

Hermes v2.1 introduces SkillOpt, a governed self-improvement loop that lets skills evolve while staying inside a defined safety boundary. This is the first time a Road4AI skill has been benchmarked, optimized, and validated through an automated pipeline with human approval gates.

### SkillOpt (New)

SkillOpt is a three-part system:

1. **Benchmark runner** (`tools/run_skillopt_benchmark.py`) evaluates any allowlisted SKILL.md against a test suite. Each case checks for expected traits (what the output should have) and reject traits (what it must never have). The runner enforces a governance boundary: it only touches files in the allowlist, and it halts on any protected-file violation.

2. **Optimizer** proposes minimal edits to failing skills. It receives the skill text, the failure details, and returns a structured patch. The optimizer runs in-memory only. No files are mutated until a human approves.

3. **Voice-match benchmark** (`benchmarks/social_voice/`) is the test suite. Ten cases that verify Road4AI's social voice: conspiratorial tone, punchy hooks, no em dashes, no marketing hype, no corporate polish.

### Governance Boundary

SkillOpt operates under explicit constraints defined in `docs/plans/HERMES_V2_1_SKILLOPT_GOVERNANCE.md`:

- **Editable**: Only `skills/**/SKILL.md`, `marketing-skills/skills/**/SKILL.md`, and `rules/content/*.md`
- **Protected**: `AGENTS.md`, `project.yaml`, `docs/brand-voice.md`, `state/*.json`, `state/*.yaml`, `rules/common/*.md`, `rules/python/*.md`
- **Rejection rules**: Safety dilution, voice drift (buzzwords or em dashes), generic AI intros, transparency failure, data leaks
- **Human gate**: Every optimization requires explicit human approval before commit

### Benchmark Results

| Metric | Before | After |
|--------|--------|-------|
| Score (live Ollama) | 0.6447 | 0.788 |
| Score (deterministic) | — | 0.871 |
| Failed cases | 3 | 0 |
| Improvement (live) | — | +22% |

- Baseline: `qwen2.5-coder:14b` (local Ollama, zero API cost)
- Optimized: `qwen2.5-coder:7b` (local Ollama, zero API cost)
- Deterministic eval: separate execution path, zero variance by design, disclosed as distinct from live results
- Post-processor: deterministic em dash stripping (47-line Python script)
- Skill update: targeted rewrite of three rules (tone anchoring, reject list, hook section removal)
- Compute cost: $0.00 (local Ollama, zero-cost stack)

### Validation Infrastructure

- **Dry-run validation** (V-001): Confirms runner enforces governance boundary, rejects protected files, loads benchmark cases correctly
- **Live validation** (V-002): First full SkillOpt loop with all safety gates active. Baseline scored, optimizer called, optimized version evaluated, patch proposal written, human approval gate inserted
- **Daily drift monitoring**: Automated daily benchmark runs via launchd, alerting on score regression

## Safety Constraints

SkillOpt will never:
- Modify files outside the allowlist
- Auto-commit changes without human approval
- Weaken safety instructions or governance rules
- Bypass the voice benchmark validation

## What's Next

- Phase 4 POC: Signal harvester goes live on Twitter
- Governance gates are load-tested against real-world content signals
- All runs logged to Hermes checkpoints for full traceability

## Files Changed

- `tools/run_skillopt_benchmark.py` — Benchmark runner with governance enforcement
- `tools/run_skillopt_benchmark_openai.py` — OpenAI-compatible runner (Ollama support)
- `.agents/skills/voice-match/SKILL.md` — Optimized voice-match skill
- `benchmarks/social_voice/social_voice_cases.jsonl` — 10-case social voice benchmark
- `docs/plans/HERMES_V2_1_SKILLOPT_GOVERNANCE.md` — Governance boundary definition
- `verify/reports/V-001.md` — Dry-run validation report
- `verify/reports/V-002.md` — Live validation report
