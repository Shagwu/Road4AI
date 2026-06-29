# Voice-Match Measured Ceiling — June 2026

## Configuration
- Skill: `.agents/skills/voice-match/SKILL.md`
- Model: `qwen2.5-coder:14b` (Ollama, local, zero-cost)
- Post-processor: `tools/voice_postprocess.py`
- Benchmark: `benchmarks/social_voice/social_voice_cases.jsonl` (10 cases)

## Compliance Metrics
- Em dash compliance: 100% (deterministic removal via post-processor)
- Reject trait compliance: 100% (deterministic replacement via post-processor)

## Score Range
- Measured range: 0.79-0.81 across 3+ runs
- Baseline (no optimization): 0.6447
- Post-optimization + post-processor: 0.806 (+25%)
- Failed cases (pre-optimization): case-001 (0.09), case-008 (0.09), case-009 (0.09)
- Failed cases (post-optimization + post-processor): case-002 (0.09, regression resolved), case-001/008 at 0.793

## Known Limitations
Trait generation depth capped by model size:
- "Manual friction focus" trait: model doesn't emphasize friction angle without explicit prompting
- "No marketing hype" trait: model generates positive-sounding language despite rules
- Score ceiling of ~0.81 is a model capability limit, not a post-processing or skill definition issue

## Recommendation
Use as-is for July 2026 cycle. Revisit with 32B model or prompt restructuring in Phase 5.

## Artifacts
- `tools/voice_postprocess.py` — deterministic post-processor
- `.agents/skills/voice-match/SKILL.md` — consolidated 6-rule skill
- `reports/skillopt/social_voice/stability-run-*.md` — benchmark runs
- `reports/skillopt/social_voice/stability-runs.json` — recorded stability data
