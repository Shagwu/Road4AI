# Task T-003 Result: Add Benchmark Runner

## Summary
Hardened the `tools/run_skillopt_benchmark.py` utility to support governed SkillOpt runs. The runner now supports argument aliases (`--skill-path`, `--cases-path`), enforces governance allowlists, calculates costs based on OpenAI pricing, and produces structured markdown/JSON reports.

## Accomplishments
- Added `--skill-path` and `--cases-path` argument aliases.
- Implemented governance check that blocks any run targeting protected files (e.g., `AGENTS.md`) or files outside the allowed skill patterns.
- Verified dry-run mode functionality, which validates benchmarks and governance without making API calls.
- Integrated `gpt-4o` and `gpt-4.1` pricing models for cost estimation.
- Updated `benchmarks/social_voice/README.md` with explicit execution instructions.
- Implemented failure-aware exit codes (exit 1 on benchmark failure in live mode).

## Verification
- Dry-run validation: `python3 tools/run_skillopt_benchmark.py --dry-run --cases-path benchmarks/social_voice/social_voice_cases.jsonl` returned exit 0 and generated report.
- Argument alias test: Verified `--skill-path` and `--cases-path` work as expected.
