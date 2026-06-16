# Social Voice Benchmark (Road4AI)

This benchmark evaluates whether an optimized skill or agent preserves Sharon's specific technical voice and brand mandates.

## Ground Truth Rules (from docs/brand-voice.md)
1. **No Em Dashes**: Never use `—`. Use periods or short sentences.
2. **No Marketing Hype**: Reject "revolutionary," "game-changing," "unprecedented," etc.
3. **High Signal**: No filler like "In today's fast-paced world" or "I am thrilled to share."
4. **Technical Integrity**: Own the friction (e.g., latency) rather than hiding it.
5. **Senior Persona**: Authoritative, humble, opinionated, and transparent.

## Schema
Each record in `social_voice_cases.jsonl` contains:
- `id`: Unique case ID.
- `input`: A draft or instruction containing "bad" traits (hype, filler, em dashes).
- `expected_traits`: What the output SHOULD demonstrate after optimization.
- `reject_traits`: Specific words or patterns that MUST be removed.
- `reference`: A target "Gold Standard" output in Sharon's voice.

## Evaluation Criteria
- **PASS**: Output removes all `reject_traits`, contains `expected_traits`, and matches the tone of the `reference`.
- **FAIL**: Output preserves any `reject_traits` or uses generic AI language.

## How to Run

### 1. Dry-Run Validation
Verify the governance allowlist and benchmark case loading without making API calls.
```bash
python3 tools/run_skillopt_benchmark.py \
  --skill-path marketing-skills/skills/email-sequence/SKILL.md \
  --cases-path benchmarks/social_voice/social_voice_cases.jsonl \
  --output reports/skillopt/social_voice/dry-run.md \
  --dry-run
```

### 2. Live Baseline Scoring
Run cases against the current skill to get a baseline score.
```bash
python3 tools/run_skillopt_benchmark.py \
  --skill-path marketing-skills/skills/email-sequence/SKILL.md \
  --cases-path benchmarks/social_voice/social_voice_cases.jsonl \
  --output reports/skillopt/social_voice/baseline.md \
  --usage-output reports/skillopt/social_voice/baseline.json \
  --baseline-only
```

### 3. Full Optimization Loop
Run baseline, generate edits, apply them in-memory, and score the optimized version.
```bash
python3 tools/run_skillopt_benchmark.py \
  --skill-path marketing-skills/skills/email-sequence/SKILL.md \
  --cases-path benchmarks/social_voice/social_voice_cases.jsonl \
  --output reports/skillopt/social_voice/opt-run.md \
  --usage-output reports/skillopt/social_voice/opt-run.json
```
