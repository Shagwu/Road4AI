# Hermes v2.1 SkillOpt Integration Implementation Plan

> **For Claude:** Use `${SUPERPOWERS_SKILLS_ROOT}/skills/collaboration/executing-plans/SKILL.md` to implement this plan task-by-task.

**Goal:** Move SkillOpt from local validation into a governed Hermes v2.1 learning loop that can optimize selected Road4AI skills without mutating operating contracts or safety boundaries.

**Architecture:** Keep Hermes v2.0 focused on memory and treat SkillOpt as the v2.1 learning layer. The implementation uses benchmark fixtures, allowlisted editable skill files, before/after evaluation reports, and human review before any optimized instruction is accepted.

**Tech Stack:** Python, OpenAI SDK, Pytest, Markdown, JSON/JSONL benchmark fixtures, `tools/skillopt_openai.py`.

---

## Narrative Boundary

- **v2.0 — Hermes remembers:** distributed memory substrate, lifecycle controls, standalone package, and self-knowledge retrieval.
- **v2.1 — Hermes learns:** governed SkillOpt runs improve selected skills using measured benchmark failures.
- **v2.2 — Hermes scales:** community contribution workflows expand after memory and learning boundaries are proven.

The v2.0 reveal should not become a SkillOpt launch. SkillOpt is a proof asset for v2.1: “we validated the loop locally, then integrated it with governance.”

## Source Artifacts

**Files:**
- Read: `SKILLOPT_VALIDATION_REPORT.md`
- Read: `tools/skillopt_openai.py`
- Read: `docs/tool-docs/HERMES_V2.md`
- Read: `docs/brand-voice.md`
- Read: `docs/content-strategy.md`
- Do not modify: `AGENTS.md`

**Validation already completed:**
- SkillOpt training loop works locally.
- Standard OpenAI client path works without Azure lock-in.
- Early runs produced coherent, domain-aware edits.
- Estimated small-domain cost is roughly `$0.30-$0.60`.
- Safety assumption is promising, but must be enforced with explicit file allowlists before production use.

---

### Task 1: Define the Governance Boundary

**Files:**
- Create: `docs/plans/HERMES_V2_1_SKILLOPT_GOVERNANCE.md`

**Step 1: Create the governance document**

Add:

```markdown
# Hermes v2.1 SkillOpt Governance

## Editable Files

SkillOpt may only propose edits to files explicitly listed in a per-run allowlist.

Initial allowlist:
- `marketing-skills/skills/**/SKILL.md`
- `.agents/skills/**/SKILL.md`

## Protected Files

SkillOpt must never edit:
- `AGENTS.md`
- `state/current-queue.json`
- `state/published-log.json`
- `docs/brand-voice.md`
- `docs/content-strategy.md`
- release notes, launch plans, or operating contracts

## Review Gate

Every proposed edit must be written as a patch proposal first.
No optimized skill becomes active until a human accepts it.

## Rejection Rules

Reject any edit that:
- removes approval gates
- weakens safety language
- changes agent roles or operating contracts
- adds claims not supported by benchmark results
- optimizes for engagement by sacrificing technical accuracy
```

**Step 2: Review for boundary clarity**

Run:

```bash
rg -n "AGENTS.md|Protected Files|Review Gate|Rejection Rules" docs/plans/HERMES_V2_1_SKILLOPT_GOVERNANCE.md
```

Expected: each governance section is present.

**Step 3: Commit**

```bash
git add docs/plans/HERMES_V2_1_SKILLOPT_GOVERNANCE.md
git commit -m "docs: define SkillOpt governance boundary"
```

---

### Task 2: Build the Social Voice Benchmark

**Files:**
- Create: `benchmarks/social_voice/social_voice_cases.jsonl`
- Create: `benchmarks/social_voice/README.md`

**Step 1: Create 10-20 labeled cases**

Each JSONL record should use this shape:

```json
{"id":"sv-001","input":"Draft a LinkedIn hook about Hermes memory expiration.","expected_traits":["technical","direct","specific","no hype"],"reject_traits":["vague","buzzword-heavy","overpromising"],"reference":"If your agent remembers everything, it will eventually understand nothing."}
```

**Step 2: Add benchmark README**

Include:

```markdown
# Social Voice Benchmark

**Purpose:** Evaluate whether a Road4AI skill preserves Sharon's technical, direct, high-signal voice.

**Pass criteria:**
- Specific technical claim
- No generic AI marketing language
- No unsupported performance claims
- Clear build-in-public framing

**Fail criteria:**
- Hype without evidence
- Generic AI phrasing
- Weak or vague hook
- Safety or governance claim without proof
```

**Step 3: Validate JSONL**

Run:

```bash
python3 -c 'import json, pathlib; [json.loads(line) for line in pathlib.Path("benchmarks/social_voice/social_voice_cases.jsonl").read_text().splitlines() if line.strip()]'
```

Expected: command exits with status `0`.

**Step 4: Commit**

```bash
git add benchmarks/social_voice/social_voice_cases.jsonl benchmarks/social_voice/README.md
git commit -m "test: add social voice SkillOpt benchmark"
```

---

### Task 3: Add a Benchmark Runner

**Files:**
- Create: `tools/run_skillopt_benchmark.py`
- Create: `config/openai-pricing-2026-05.json`
- Test: `tests/test_run_skillopt_benchmark.py`

**Architecture decision:** Use Option B for v2.1: keep evaluator logic inside `tools/run_skillopt_benchmark.py` for faster validation. Do not create `tools/evaluate_skill_output.py` yet. Extract the evaluator into its own module in v2.2 if multiple evaluator providers become necessary.

**Pricing decision:** Do not hardcode OpenAI pricing in the runner. Prices change over time and differ by model. Store rates in `config/openai-pricing-2026-05.json`, require the runner to record the pricing config hash in every usage report, and update the config from the official OpenAI pricing page before live validation. The runner must require the pricing file to exist; do not auto-fetch pricing and do not fall back to embedded defaults.

Initial pricing config shape:

```json
{
  "refreshed_at": "2026-05-29T14:32:00Z",
  "source": "https://openai.com/api/pricing/",
  "models": {
    "gpt-4.1-2025-04-14": {
      "input_per_1m_tokens": 2.0,
      "output_per_1m_tokens": 8.0,
      "aliases": ["gpt-4.1"]
    },
    "gpt-4o-2024-11-20": {
      "input_per_1m_tokens": 2.5,
      "output_per_1m_tokens": 10.0,
      "aliases": ["gpt-4o"]
    }
  }
}
```

**Step 1: Write the failing tests**

Test that the runner:
- loads JSONL benchmark cases
- rejects protected skill files
- scores outputs against `expected_traits`, `reject_traits`, and `reference`
- treats cases below the configurable threshold as failures
- writes a before/after report
- exits cleanly when no API key is present and `--dry-run` is used
- makes zero API calls in `--dry-run` mode
- produces no real scores in `--dry-run` mode
- runs the live flow as target model → evaluator model → optimizer model → target model → evaluator model
- keeps optimized skill edits in memory until human approval
- requires `OPENAI_API_KEY` or `--openai-api-key` in live mode
- requires `--usage-output` in live mode
- records exact model IDs used for target, evaluator, and optimizer calls
- writes per-model call counts, token usage, pricing config hash, and cost estimates
- retries transient API failures, then exits non-zero if any case cannot be scored
- exits non-zero if usage data is missing or incomplete in live mode

**Step 2: Run tests to verify failure**

Run:

```bash
pytest tests/test_run_skillopt_benchmark.py -v
```

Expected: FAIL because the runner does not exist.

**Step 3: Implement minimal runner**

The runner should:
- accept `--skill-file`
- accept `--benchmark`
- accept `--output`
- accept `--dry-run`
- accept `--usage-output`, required in live mode
- accept `--openai-api-key`, falling back to `OPENAI_API_KEY`
- accept `--pricing-config`, required in live mode and optional in dry-run mode
- accept `--failure-threshold`, defaulting to `0.7`
- accept `--target-model`, requiring a specific model ID for live runs
- accept `--optimizer-model`, requiring a specific model ID for live runs
- accept `--evaluator-model`, requiring a specific model ID for live runs
- load cases from JSONL
- refuse protected files from the governance list
- run baseline evaluation by calling the target model with the current skill
- score each generated output with an evaluator model using a trait rubric
- collect failures where evaluator score is below `--failure-threshold`
- stop after structural validation in `--dry-run` mode
- in `--dry-run` mode, validate structure only: benchmark schema, governance checks, pricing config loading if provided, and report template rendering
- in `--dry-run` mode, output planned call counts only: target model once per case, evaluator model twice per case in live mode, and optimizer model once if failures exist
- call `tools.skillopt_openai.create_skillopt_client()` only during live optimization
- generate proposed edits from failures using the optimizer model
- apply proposed edits in memory only
- re-run the target model and evaluator against the optimized skill
- write a Markdown report with baseline score, optimized score, delta, token/cost details if available, sample cases, and proposed edits for human review
- retry transient API failures up to `3` times with backoff
- fail hard after retries if any benchmark case cannot be evaluated
- fail hard if a live response does not include usage data
- write usage JSON to `--usage-output`

Key implementation constraints:

- Always run dry-run first to validate structure, governance, pricing config, and report rendering.
- Dry-run mode must not call the target model, evaluator model, or optimizer model.
- Dry-run mode must not produce baseline scores, optimized scores, usage JSON, or cost estimates.
- Live mode requires `OPENAI_API_KEY` or `--openai-api-key`.
- Live mode requires exact model IDs, not aliases like `gpt-4`.
- Live mode requires `--pricing-config` pointing to a reviewed local pricing JSON file.
- Live mode requires `--usage-output`.
- Live mode retries transient errors up to `3` times with exponential backoff.
- Live mode fails hard on non-transient errors such as authentication failure, bad request, or model not found.
- Live mode exits non-zero if usage or cost cannot be computed.
- No live proof report may be produced without complete usage data.

Use this scoring model inside the runner:

```python
score = (
    expected_trait_score * 0.5
    + reject_trait_score * 0.3
    + reference_alignment_score * 0.2
)
```

Evaluator responses must be structured JSON:

```json
{
  "score": 0.82,
  "expected_traits_met": ["technical", "direct"],
  "expected_traits_missed": ["specific"],
  "reject_traits_present": [],
  "reference_alignment": 0.7,
  "reason": "Specific enough, but weaker than the reference hook."
}
```

The evaluator prompt should make the separation explicit:

```text
Evaluate this output against the rubric. You are the evaluator only. Do not optimize the skill and do not rewrite the output.

Output:
{output}

Expected traits that should be present:
{expected_traits}

Reject traits that should be absent:
{reject_traits}

Reference exemplar for alignment:
{reference}

Return JSON with:
- expected_traits_met
- expected_traits_missed
- reject_traits_present
- reject_traits_avoided
- reference_alignment from 0.0 to 1.0
- reason
```

Usage JSON must use this shape:

```json
{
  "run_id": "2026-05-29-social-voice",
  "benchmark": "social_voice",
  "pricing_config": {
    "path": "config/openai-pricing-2026-05.json",
    "sha256": "<hash>",
    "source": "https://openai.com/api/pricing/"
  },
  "models": {
    "target_model": "gpt-4.1-2025-04-14",
    "evaluator_model": "gpt-4.1-2025-04-14",
    "optimizer_model": "gpt-4.1-2025-04-14"
  },
  "calls": {
    "target_model": 20,
    "evaluator_model": 20,
    "optimizer_model": 1
  },
  "tokens": {
    "target_model": {"prompt": 0, "completion": 0, "total": 0},
    "evaluator_model": {"prompt": 0, "completion": 0, "total": 0},
    "optimizer_model": {"prompt": 0, "completion": 0, "total": 0}
  },
  "estimated_cost_usd": {
    "target_model": 0.0,
    "evaluator_model": 0.0,
    "optimizer_model": 0.0,
    "total": 0.0
  }
}
```

**Step 4: Run tests to verify pass**

Run:

```bash
pytest tests/test_run_skillopt_benchmark.py -v
```

Expected: PASS.

**Step 5: Commit**

```bash
git add tools/run_skillopt_benchmark.py config/openai-pricing-2026-05.json tests/test_run_skillopt_benchmark.py
git commit -m "feat: add three-model benchmark runner with cost tracking"
```

---

### Task 4: Run First Dry-Run Validation

**Files:**
- Create: `reports/skillopt/social_voice/README.md`
- Create: `reports/skillopt/social_voice/2026-05-29-dry-run-validation.md`

**Step 1: Run dry-run against protected file**

Run:

```bash
python3 tools/run_skillopt_benchmark.py \
  --skill-file docs/brand-voice.md \
  --benchmark benchmarks/social_voice/social_voice_cases.jsonl \
  --output reports/skillopt/social_voice/2026-05-29-dry-run-protected.txt \
  --dry-run
```

Expected:
- runner rejects `docs/brand-voice.md` as protected
- exits non-zero
- message includes `Error: docs/brand-voice.md is in protected files list`

**Step 2: Run dry-run against allowed skill**

Pick one allowed skill file under `marketing-skills/skills/**/SKILL.md` and run:

```bash
python3 tools/run_skillopt_benchmark.py \
  --skill-file marketing-skills/skills/<skill-name>/SKILL.md \
  --benchmark benchmarks/social_voice/social_voice_cases.jsonl \
  --output reports/skillopt/social_voice/2026-05-29-dry-run-validation.md \
  --dry-run
```

Expected:
- loads all benchmark cases
- validates case structure: `input`, `expected_traits`, `reject_traits`, and `reference`
- validates report template rendering
- makes no API calls
- produces no real scores
- output includes `Dry-run validation passed. Ready for live mode.`
- output includes planned calls: target model once per case, evaluator model twice per case in live mode, optimizer model once if failures exist
- exits `0`

**Step 3: Validate pricing config loads**

Run:

```bash
python3 tools/run_skillopt_benchmark.py \
  --skill-file marketing-skills/skills/<skill-name>/SKILL.md \
  --benchmark benchmarks/social_voice/social_voice_cases.jsonl \
  --output reports/skillopt/social_voice/2026-05-29-dry-run-pricing.md \
  --dry-run \
  --pricing-config config/openai-pricing-2026-05.json
```

Expected:
- pricing config loads without error
- output shows the loaded model rates
- exits `0`

**Step 4: Commit**

```bash
git add reports/skillopt/social_voice
git commit -m "docs: record dry-run validation for SkillOpt social voice"
```

---

### Task 5: Run One Live Controlled Optimization

**Files:**
- Create: `reports/skillopt/social_voice/2026-<date>-live-run.md`
- Create: `reports/skillopt/social_voice/2026-<date>-usage.json`
- Create: `reports/skillopt/social_voice/2026-<date>-approval.md`
- Modify only by human approval: selected skill file from allowlist

**Step 1: Confirm prerequisites**

Check:

```bash
test -n "$OPENAI_API_KEY" && echo "OPENAI_API_KEY present"
```

Expected: key is present. If absent, stop.

**Step 2: Run the live benchmark**

Run:

```bash
python3 tools/run_skillopt_benchmark.py \
  --skill-file marketing-skills/skills/<skill-name>/SKILL.md \
  --benchmark benchmarks/social_voice/social_voice_cases.jsonl \
  --output reports/skillopt/social_voice/2026-<date>-live-run.md \
  --usage-output reports/skillopt/social_voice/2026-<date>-usage.json \
  --pricing-config config/openai-pricing-2026-05.json \
  --target-model gpt-4.1-2025-04-14 \
  --evaluator-model gpt-4.1-2025-04-14 \
  --optimizer-model gpt-4.1-2025-04-14
```

Expected:
- report contains baseline scores, proposed edits, optimized scores, and delta
- usage JSON contains per-model call counts, token usage, pricing config hash, and cost estimate
- report includes all benchmark cases in baseline and optimized evaluation
- no edits are applied to disk yet
- transient errors such as rate limit, timeout, or `5xx` are retried up to `3` times
- non-transient errors such as auth failure, bad request, or model not found fail hard immediately

If any benchmark case cannot be evaluated after retries, the runner must exit non-zero and avoid producing a proof report.

**Step 3: Review usage and cost**

Run:

```bash
jq '.estimated_cost_usd' reports/skillopt/social_voice/2026-<date>-usage.json
```

Expected: total cost is acceptable for the validation budget. Do not rely on a fixed dollar estimate unless the pricing config is current.

**Step 4: Human review**

Do not apply edits automatically. Shagwu is the reviewer for v2.1 validation unless another reviewer is explicitly named in the run report.

The reviewer must choose one decision:
- `APPROVED`: accepted edits may be applied to the skill file.
- `REJECTED`: no skill file changes may be applied; report stays as evidence.
- `REVISION_REQUESTED`: update the benchmark, prompt, or proposed edit set and run again.

Record the decision in `reports/skillopt/social_voice/2026-<date>-approval.md`:

```markdown
# SkillOpt Review Decision

**Reviewer:** Shagwu
**Decision:** APPROVED | REJECTED | REVISION_REQUESTED
**Benchmark:** social_voice
**Skill file:** marketing-skills/skills/<skill-name>/SKILL.md
**Run report:** reports/skillopt/social_voice/2026-<date>-live-run.md
**Usage report:** reports/skillopt/social_voice/2026-<date>-usage.json
**Before score:** 0.72
**After score:** 0.89
**Delta:** +0.17
**Cost:** $0.27

## Approved Edits

- [plain-language summary of accepted edit 1]
- [plain-language summary of accepted edit 2]

## Rejected Edits

- [plain-language summary of rejected edit, or "None"]

## Review Notes

[Why the decision is safe and useful.]
```

If the decision is `REJECTED`, commit only the run report and approval file. Do not modify the skill file.

If the decision is `REVISION_REQUESTED`, commit the run report and approval file, then create a new run report after changes are made.

**Step 5: Apply accepted patch**

Only after approval:

```bash
git add marketing-skills/skills/<skill-name>/SKILL.md reports/skillopt/social_voice/2026-<date>-live-run.md
git add reports/skillopt/social_voice/2026-<date>-usage.json reports/skillopt/social_voice/2026-<date>-approval.md
git commit -m "feat: apply reviewed SkillOpt social voice improvement

Reviewed by: Shagwu
Benchmark: social_voice
Before score: 0.72
After score: 0.89
Delta: +0.17
Cost: $0.27
Approval record: reports/skillopt/social_voice/2026-<date>-approval.md"
```

**Step 6: Verify disk state**

Run:

```bash
git log --oneline -- reports/skillopt/social_voice/ | head -5
```

Expected: the approval commit is the latest change to the domain report path.

---

### Task 6: Prepare the v2.1 Launch Proof Package

**Files:**
- Create: `docs/plans/HERMES_V2_1_LAUNCH_PROOF.md`
- Read: `SKILLOPT_VALIDATION_REPORT.md`
- Read: `reports/skillopt/social_voice/*.md`

**Step 1: Create the proof package**

Include:
- what was validated locally
- what changed after governance was added
- benchmark domain and sample size
- before/after metrics
- accepted edits
- rejected edits
- safety boundary evidence
- total cost

**Step 2: Add launch narrative**

Use:

```markdown
Hermes v2.0 remembered.
Hermes v2.1 learned under supervision.

We did not let the optimizer rewrite the constitution.
We gave it a narrow sandbox, measured its output, and reviewed every change.
```

**Step 3: Commit**

```bash
git add docs/plans/HERMES_V2_1_LAUNCH_PROOF.md
git commit -m "docs: prepare Hermes v2.1 SkillOpt proof package"
```

---

## Launch Readiness Criteria

Hermes v2.1 is ready to reveal when:

- At least one real Road4AI skill has a measured before/after benchmark.
- Protected files are technically blocked by the runner.
- No SkillOpt edit bypasses human review.
- Reports include cost, model, benchmark size, and accepted/rejected edits.
- Public claims are limited to observed benchmark results.
- `SKILLOPT_VALIDATION_REPORT.md` and live-run reports agree on the core story.

## Recommended First Public Post

**Working title:** We Tested SkillOpt Locally Before Letting Hermes Learn

**Hook:** I didn’t want Hermes to learn until I knew it could stay inside the guardrails.

**Core argument:**
- v2.0 gave Hermes memory.
- v2.1 gives Hermes a learning loop.
- The hard part is not generating better instructions.
- The hard part is preventing the optimizer from rewriting the rules it is supposed to obey.
