# Week 3: First SkillOpt Training Run

**Domain:** Social Voice
**Target:** Week 3 post-v2.0 launch
**Status:** PLANNED

---

## Prerequisites

Before the training run, ensure:

- [ ] 10-20 labeled benchmark cases in `benchmarks/social_voice/social_voice_cases.jsonl`
- [ ] Ground truth labels verified (see `docs/GROUND_TRUTH_LABELING_GUIDE.md`)
- [ ] `skillopt_openai.py` cleaned up and tested
- [ ] `run_skillopt_benchmark_openai.py` functional
- [ ] `OPENAI_API_KEY` available for live mode
- [ ] Pricing config current (`config/openai-pricing-2026-05.json`)

---

## Training Run Plan

### Step 1: Dry-Run Validation

```bash
python tools/run_skillopt_benchmark_openai.py \
  --skill-file skills/social-voice/SKILL.md \
  --benchmark benchmarks/social_voice/social_voice_cases.jsonl \
  --output reports/skillopt/social_voice/week3-dry-run.md \
  --dry-run \
  --pricing-config config/openai-pricing-2026-05.json
```

**Expected:**
- Loads all benchmark cases
- Validates case structure
- No API calls made
- Exits 0

### Step 2: Baseline Evaluation

```bash
python tools/run_skillopt_benchmark_openai.py \
  --skill-file skills/social-voice/SKILL.md \
  --benchmark benchmarks/social_voice/social_voice_cases.jsonl \
  --output reports/skillopt/social_voice/week3-baseline.md \
  --usage-output reports/skillopt/social_voice/week3-usage.json \
  --pricing-config config/openai-pricing-2026-05.json \
  --target-model gpt-4.1-2025-04-14 \
  --evaluator-model gpt-4.1-2025-04-14 \
  --optimizer-model gpt-4.1-2025-04-14 \
  --baseline-only
```

**Expected:**
- Baseline scores for all cases
- Usage JSON with token counts and cost estimates
- No optimization applied yet

### Step 3: Full Optimization Run

```bash
python tools/run_skillopt_benchmark_openai.py \
  --skill-file skills/social-voice/SKILL.md \
  --benchmark benchmarks/social_voice/social_voice_cases.jsonl \
  --output reports/skillopt/social_voice/week3-live-run.md \
  --usage-output reports/skillopt/social_voice/week3-usage.json \
  --pricing-config config/openai-pricing-2026-05.json \
  --target-model gpt-4.1-2025-04-14 \
  --evaluator-model gpt-4.1-2025-04-14 \
  --optimizer-model gpt-4.1-2025-04-14
```

**Expected:**
- Baseline scores
- Proposed edits from optimizer
- Optimized scores
- Delta (improvement percentage)
- Usage JSON with cost estimates

### Step 4: Human Review

Review the run report and decide:

- **APPROVED:** Apply edits to skill file
- **REJECTED:** Keep as evidence only
- **REVISION_REQUESTED:** Update benchmark and run again

Record decision in `reports/skillopt/social_voice/week3-approval.md`.

### Step 5: Apply Accepted Edits

Only after approval:

```bash
git add skills/social-voice/SKILL.md reports/skillopt/social_voice/week3-*
git commit -m "feat: apply reviewed SkillOpt social voice improvement

Reviewed by: Shagwu
Benchmark: social_voice
Before score: [baseline]
After score: [optimized]
Delta: [delta]
Cost: [cost]"
```

---

## Success Criteria

The training run is successful if:

- [ ] Baseline evaluation completes without errors
- [ ] Optimizer produces coherent, reviewable edits
- [ ] Protected files remain untouched
- [ ] Cost is within budget ($0.30-$0.60 estimated)
- [ ] Human review completes with clear decision
- [ ] Results documented in reports/

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| API rate limits | Retry logic with exponential backoff (3 attempts) |
| High cost | Baseline-only mode first, then full run |
| Bad edits | Human review gate, protected files list |
| Governance breach | Protected files technically blocked by runner |

---

## Deliverables

After Week 3:

1. `reports/skillopt/social_voice/week3-baseline.md` — Baseline scores
2. `reports/skillopt/social_voice/week3-live-run.md` — Full optimization run
3. `reports/skillopt/social_voice/week3-usage.json` — Cost and token usage
4. `reports/skillopt/social_voice/week3-approval.md` — Human review decision
5. Updated `skills/social-voice/SKILL.md` (if approved)

---

## Timeline

| Day | Activity |
|-----|----------|
| Day 1 | Dry-run validation |
| Day 2 | Baseline evaluation |
| Day 3 | Full optimization run |
| Day 4 | Human review and decision |
| Day 5 | Apply edits (if approved), document results |

---

## Next Steps

After Week 3:

1. Document learnings from the training run
2. Update validation report with real-world results
3. Plan Week 6 blog post and v2.1 release
4. Consider expanding to additional domains (memory_ops, QA)
