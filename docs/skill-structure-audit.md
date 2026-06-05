# Road4AI Skill Structure Audit

Last updated: 2026-06-05

## Scope

Audited the canonical Road4AI skills under `skills/*/SKILL.md` against the standardized Road4AI `SKILL.md` structure.

This audit does not treat vendor, Google ADK, CrewAI, or generic marketing skills under `.agents/skills/` as Road4AI governance sources. Those remain classified by `docs/skill-inventory-policy.md` and `skills/manifest.json`.

## Prior Audit Check

A prior partial audit existed.

- Commit `754ec676c54aeb8b63da32c7b4b385d5d14a71d1` promoted `voice-match` and `ideation-orchestrator` toward Tier 1 canonical status.
- `docs/skill-inventory-policy.md` already defined the tier model and Option B architecture: top-level `skills/` is canonical, runtime skill directories are install surfaces.
- `skills/manifest.json` already classified most canonical, runtime, vendor, and generic marketing skills.

What was not complete:

- `skills/voice-match` and `skills/ideation-orchestrator` existed as canonical skill directories but were missing from `canonical_skills` in `skills/manifest.json`.
- Three canonical `SKILL.md` files did not fully match the standard section structure.
- Two canonical skills still contained em dashes inside instructional text or schemas.

## Standard Checked

Each canonical Road4AI skill should include:

- YAML frontmatter delimited by `---`.
- Frontmatter keys: `name`, `description`, `origin`, and `tools`.
- Body sections:
  - `## When to Activate`
  - `## The Mechanism`
  - `## Workflow`
  - `## Output Contract`
  - `## Related Skills` where adjacent Road4AI skills exist
- Explicit activation boundaries, such as "Do not use..." guidance.
- No em dashes in instructional prose or output schemas.

## Results

| Skill | Status | Notes |
| --- | --- | --- |
| `skills/adversarial-review-karen/SKILL.md` | Pass | Already matched the standard structure. |
| `skills/content-pipeline/SKILL.md` | Pass | Already matched the standard structure. |
| `skills/hermes-checkpoint-patterns/SKILL.md` | Pass | Already matched the standard structure. |
| `skills/ideation-orchestrator/SKILL.md` | Fixed | Renamed `Output Schema` to `Output Contract`; removed em dashes from workflow/schema text. |
| `skills/public-sanitization-review/SKILL.md` | Fixed | Renamed `Output Format` to `Output Contract`. |
| `skills/voice-match/SKILL.md` | Fixed | Added `The Mechanism`; removed em dashes from persona and anti-AI-tell text. |

## Manifest Updates

Added these canonical entries to `skills/manifest.json`:

- `ideation-orchestrator`
- `voice-match`

Both are marked as `canonical_runtime_source` with empty `runtime_targets` for now. Their runtime copies remain protected in `runtime_road4ai` because they are active harness surfaces. This avoids breaking `tools/sync_skills.py`, which refuses to overwrite protected runtime skills.

## Remaining Work

No remaining canonical `SKILL.md` structure gaps were found.

Future consolidation work can decide whether to expand `tools/sync_skills.py` so active Tier 2 runtime installs can be intentionally synchronized from Tier 1 canonical sources without being treated as protected overwrite targets.
