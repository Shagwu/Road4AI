# Voice-Match Stability Test: June 2026

Status: pending

## Purpose

Prove that repeated live scoring runs on `voice-match` are stable enough to trust before/after SkillOpt deltas.

## Executor

Executor may be Codex or Gemini.

Runner engine: `tools/run_skillopt_benchmark.py` currently uses Gemini CLI for both target generation and evaluator scoring.

## Inputs

- Skill: `.agents/skills/voice-match/SKILL.md`
- Benchmark: `benchmarks/social_voice/social_voice_cases.jsonl`
- Cases: 12
- Raw run log: `reports/skillopt/social_voice/stability-runs.json`

## Test Plan

1. Run 1: execute live scoring against the current `voice-match` skill.
2. Run 2: repeat with the same skill, same benchmark, and same runner configuration.
3. Compare mean score, failed case IDs, and standard deviation.

## Pass Criteria

- Mean score variance is within +/-5%.
- Failed case overlap is above 80%.
- Standard deviation is stable.

## Results

Pending June 24-25 execution.

## Notes

Record timestamp, executor, git commit, command, environment notes, mean score, failed case IDs, and variance notes for each run.
