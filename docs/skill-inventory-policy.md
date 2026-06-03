# Road4AI Skill Inventory Policy

Version: 1.0
Last updated: 2026-06-03

## Tier Classification

### Tier 1: Canonical Road4AI Operating IP

**Location:** `skills/` (top-level)
**Ownership:** Road4AI-authored, maintained, evolved
**Runtime Status:** Source of truth; installed into runtime locations when needed

Examples:

- `skills/content-pipeline/SKILL.md`
- `skills/adversarial-review-karen/SKILL.md`
- `skills/public-sanitization-review/SKILL.md`
- `skills/hermes-checkpoint-patterns/SKILL.md`

Policy:

- Single source of truth for Road4AI operating IP.
- Governed by Road4AI rules, approval gates, and security gates.
- Subject to skill-health audits.
- Authored in `skills/` first, then mirrored into runtime locations only when needed.

### Tier 2: Runtime Road4AI Operational Skills

**Location:** `.agents/skills/` or `.gemini/skills/`
**Ownership:** Road4AI-authored, actively invoked
**Runtime Status:** Currently visible to one or more harnesses

Examples:

- `.agents/skills/hermes-checkpoint/SKILL.md`
- `.gemini/skills/ideation-orchestrator/SKILL.md`

Policy:

- Keep when currently activated by a harness.
- Document which harness depends on the skill.
- If a matching Tier 1 source exists, keep the runtime copy synchronized or consolidate.
- Do not treat runtime location as the canonical source for Road4AI operating IP.

### Tier 3: Vendor or Tool-Specific Skills

**Location:** `.agents/skills/`
**Ownership:** External tools, plugins, or third-party packs
**Runtime Status:** Available on demand, not a Road4AI governance source

Examples:

- `.agents/skills/google-agents-cli-*`
- `.agents/skills/ask-docs`
- `.agents/skills/design-agent`
- `.agents/skills/skill-creator`

Policy:

- Keep for capability access.
- Do not modify without understanding tool dependencies.
- Do not treat as Road4AI governance source.
- Archive only if the underlying tool is deprecated or unused.

### Tier 4: Marketing Vendor or Generic Pack

**Location:** `.agents/skills/` or `.agents/marketing/`
**Ownership:** Generic marketing templates, vendor packs, or lightly adapted references
**Runtime Status:** Not part of current Road4AI operating workflow unless explicitly adopted

Examples:

- `.agents/skills/ai-seo`
- `.agents/skills/content-strategy`
- `.agents/skills/copywriting`
- `.agents/skills/social-content`
- `.agents/marketing/content-calendar-30-days.md`
- `.agents/marketing/homepage-copy.md`
- `.agents/marketing/launch-plan.md`

Policy:

- Keep only if Road4AI has adapted or actively uses them.
- Move reference documents to `docs/marketing/`.
- Do not load into `AGENTS.md` or `WORKING-CONTEXT.md`.
- Archive if unused for two or more sprints.

### Tier 5: Archive or Reference

**Location:** `docs/`, `docs/marketing/`, or `archive/`
**Ownership:** Historical context and superseded workflows
**Runtime Status:** Never activated

Policy:

- Keep for historical or teaching value only.
- Do not load or reference in current workflows unless explicitly revived.
- Record why the artifact is kept.

## Runtime Loading Status

Current evidence as of 2026-06-03:

- `skills/`: canonical Road4AI source of truth.
- `.agents/skills/`: runtime-visible in the current Codex session.
- `.gemini/skills/`: Gemini-specific runtime skill surface.

## Architecture Decision

Road4AI uses Option B: `skills/` is canonical source; runtime locations are install surfaces.

- `skills/` is the canonical Road4AI source of truth.
- `.agents/skills/` is a runtime install surface.
- `.gemini/skills/` is a Gemini-specific runtime install surface.
- Vendor and tool skills may live directly in `.agents/skills/`.
- Road4AI-authored skills should be authored in `skills/` first, then mirrored into runtime locations only when needed.

`tools/sync_skills.py` installs canonical skills into runtime targets and reports source/runtime drift.

Use:

```bash
python3 tools/sync_skills.py --check
python3 tools/sync_skills.py --sync
```

## Consolidation Rules

Before deleting or merging any skill:

1. Verify it is not required by a runtime harness.
2. Check whether another Tier 1 or Tier 2 skill subsumes it.
3. If subsumed, merge useful material into the canonical skill.
4. Update `WORKING-CONTEXT.md` and the manifest.
5. Commit as a consolidation or refactor checkpoint.

## Immediate Consolidation Targets

1. Keep `skills/content-pipeline` as the single canonical content lifecycle skill.
2. Keep `.agents/skills/hermes-checkpoint` as operational runtime.
3. Keep `skills/hermes-checkpoint-patterns` as teaching/audit unless later merged.
4. Classify `.agents/skills/*` by tier in `skills/manifest.json`.
5. Keep `.agents/marketing/` reference docs in `docs/marketing/`.

## Inventory Review Cadence

- Per sprint: record which skills are actually invoked.
- Per quarter: consolidate overlaps and archive dead weight.
- Every six months: audit runtime loading and source/runtime drift.
