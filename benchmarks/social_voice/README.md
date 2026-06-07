# Social Voice Benchmark

This benchmark evaluates whether an agent or skill preserves the Road4AI social voice as defined in `docs/brand-voice.md` and `.agents/skills/voice-match/SKILL.md`.

## Structure
The benchmark consists of JSONL records in `social_voice_cases.jsonl`.

Current suite size: 15 cases.

Each record contains:
- `id`: Unique identifier for the case.
- `input`: The prompt or task given to the agent.
- `expected_traits`: Key traits that must be present in the output.
- `reject_traits`: Traits that, if present, should cause the output to fail.
- `reference`: A ground-truth example of a high-signal response.

## Execution
Use the `run_skillopt_benchmark.py` tool to execute this benchmark.

```bash
python3 tools/run_skillopt_benchmark.py \
  --skill-path .agents/skills/voice-match/SKILL.md \
  --cases-path benchmarks/social_voice/social_voice_cases.jsonl \
  --output reports/skillopt/social_voice/$(date +%Y%m%d)-run.md \
  --usage-output reports/skillopt/social_voice/$(date +%Y%m%d)-usage.json \
  --pricing-config config/openai-pricing-2026-05.json \
  --target-model gpt-4o-2024-11-20 \
  --evaluator-model gpt-4o-2024-11-20 \
  --optimizer-model gpt-4o-2024-11-20
```

For a safe dry-run (no API calls, governance check only):
```bash
python3 tools/run_skillopt_benchmark.py \
  --skill-path .agents/skills/voice-match/SKILL.md \
  --cases-path benchmarks/social_voice/social_voice_cases.jsonl \
  --output reports/skillopt/social_voice/dry_run.md \
  --dry-run
```

## Pass Criteria
An output passes if:
1. It contains all `expected_traits`.
2. It contains zero `reject_traits`.
3. It maintains technical accuracy for the specific domain mentioned.
4. (For X/Twitter) It is strictly under 280 characters.

## Fail Criteria
An output fails if:
1. It uses prohibited buzzwords (revolutionary, game-changing, etc.).
2. It starts with generic AI filler ("In today's fast-paced world...").
3. It uses em dashes (prohibited by brand voice).
4. It is vague or lacks architectural reasoning.
5. It sounds like marketing hype rather than engineering experience.

## Case Quality Review: 2026-06-07

Review outcome:
- V-001 through V-012: tightened. These remain the base suite, but the expected and reject traits now target Road4AI-specific voice markers instead of generic good-writing traits.
- V-013 through V-015: added from the June runway posts to test the v2.1 reveal arc directly.

New runway coverage:
- V-013: Self-Knowledge Pivot, memory without build context becomes noise.
- V-014: System Integrity, governance belongs in the system, not the model.
- V-015: Tireless Worker Trap, speed without human oversight is not alignment.

Do not expand past 17 cases before the July 2026 v2.1 proof cycle unless a real June failure exposes a missing voice risk. The benchmark should stay small enough to rerun under the Gemini CLI free-tier budget.
