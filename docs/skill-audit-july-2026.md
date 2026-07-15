# Skill Audit: July 2026

Audited all Road4AI-authored skills against the standard structure defined in the June 5 audit.

## Standard

- YAML frontmatter with `name`, `description`, `origin`, `tools`
- Sections: `## When to Activate`, `## The Mechanism`, `## Workflow`, `## Output Contract`
- Activation boundaries ("Do not use..." language)
- No em dashes in instructional text

## Tier 2 Runtime Skills

### hermes-checkpoint

- **Location:** `.agents/skills/hermes-checkpoint/SKILL.md`
- **Frontmatter:** name, description, origin, tools all present
- **Sections:** When to Activate, The Mechanism, Workflow all present. Output Contract missing (has "Commit Format" instead).
- **Boundaries:** Present ("Do not use this for broken mid-edit state...")
- **Em dashes:** None found
- **Verdict:** PASS with minor note (Output Contract section is absent but the commit format section serves the same purpose)

### voice-match

- **Location:** `.agents/skills/voice-match/SKILL.md`
- **Frontmatter:** name, description, origin, tools all present
- **Sections:** When to Activate, The Mechanism present. Workflow present as "8-Step Quality Filter". Output Contract present as "Output Contract" section.
- **Boundaries:** Present ("Do not use this for generic business writing...")
- **Em dashes:** None in instructional text (the skill explicitly prohibits them)
- **Verdict:** PASS

### ideation-orchestrator (.agents)

- **Location:** `.agents/skills/ideation-orchestrator/SKILL.md`
- **Frontmatter:** name, description present. origin and tools missing.
- **Sections:** When to Activate is inline text, not a `## When to Activate` heading. Has `## Workflow`. Has `## Output Schema` (not Output Contract). No `## The Mechanism`.
- **Boundaries:** Partial (governance lock section present, but no explicit "Do not use..." boundary)
- **Em dashes:** One found in the output schema example: `[Idea title — punchy, no em dashes]` (line 25, inside a code block showing what to avoid — technically acceptable)
- **Verdict:** FAIL. Missing origin/tools in frontmatter. Missing The Mechanism. Section naming inconsistent with standard.

### ideation-orchestrator (.gemini)

- **Location:** `.gemini/skills/ideation-orchestrator/SKILL.md`
- Same structure as the .agents version. Same gaps.
- **Verdict:** FAIL. Same issues as .agents copy.

### content-pipeline (.agents)

- **Location:** `.agents/skills/content-pipeline/SKILL.md`
- **Sync status:** DRIFT detected by sync_skills.py (differs from canonical `skills/content-pipeline/SKILL.md`)
- **Frontmatter:** name, description, origin, tools all present
- **Sections:** When to Activate, The Mechanism, Lifecycle (serves as Workflow) all present. Output Contract absent.
- **Boundaries:** Present ("Do not use this skill for final copy edits...")
- **Em dashes:** None found
- **Verdict:** FAIL on drift. Content diverged from canonical source. Needs resync.

### public-sanitization-review (.agents)

- **Location:** `.agents/skills/public-sanitization-review/SKILL.md`
- **Sync status:** OK per sync_skills.py
- **Frontmatter:** name, description, origin, tools present
- **Sections:** All four standard sections present
- **Boundaries:** Present
- **Em dashes:** None
- **Verdict:** PASS

## Unregistered Skills (in .agents/skills but not in manifest.json)

### subagent-driven-development

- **Location:** `.agents/skills/subagent-driven-development/SKILL.md`
- **Frontmatter:** name, description present. Uses `when_to_use` instead of `origin`/`tools`. Has `version` key.
- **Sections:** Has `## Overview` instead of standard sections. No When to Activate, Mechanism, or Output Contract headings.
- **Origin:** Not Road4AI (third-party skill pack)
- **Verdict:** Not a Road4AI governance source. Tier 3 vendor skill. No action needed beyond manifest classification.

### tdd

- **Location:** `.agents/skills/tdd/SKILL.md`
- **Frontmatter:** name, description present. Uses `when_to_use` instead of `origin`/`tools`. Has `version`, `languages`.
- **Sections:** Has `## Overview`, `## When to Use`. Non-standard structure.
- **Origin:** Not Road4AI (third-party)
- **Verdict:** Tier 3 vendor skill. No action needed.

### writing-plans

- **Location:** `.agents/skills/writing-plans/SKILL.md`
- **Frontmatter:** name, description present. Uses `when_to_use` instead of `origin`/`tools`. Has `version`.
- **Sections:** Has `## Overview`. Non-standard structure.
- **Origin:** Not Road4AI (third-party)
- **Verdict:** Tier 3 vendor skill. No action needed.

### using-git-worktrees

- **Location:** `.agents/skills/using-git-worktrees/SKILL.md`
- **Verdict:** Tier 3 vendor skill. Not audited in detail.

## Summary

| Skill | Tier | Status | Action |
|-------|------|--------|--------|
| hermes-checkpoint | 2 | PASS | None |
| voice-match | 2 | PASS | None |
| ideation-orchestrator (.agents) | 2 | FAIL | Add origin/tools to frontmatter, add The Mechanism section, rename Output Schema to Output Contract |
| ideation-orchestrator (.gemini) | 2 | FAIL | Same as .agents copy |
| content-pipeline (.agents) | 2 | DRIFT | Resync from canonical source |
| public-sanitization-review | 2 | PASS | None |
| subagent-driven-development | 3 | N/A | Add to manifest as Tier 3 |
| tdd | 3 | N/A | Add to manifest as Tier 3 |
| writing-plans | 3 | N/A | Add to manifest as Tier 3 |
| using-git-worktrees | 3 | N/A | Add to manifest as Tier 3 |

## Recommended Fixes

1. **Resync content-pipeline:** Run `python3 tools/sync_skills.py --sync` to pull the canonical version into `.agents/skills/`.
2. **Fix ideation-orchestrator:** Add `origin: Road4AI` and `tools:` to frontmatter. Add `## The Mechanism` section. Rename `## Output Schema` to `## Output Contract`. Apply to both .agents and .gemini copies.
3. **Update manifest.json:** Add the four unregistered Tier 3 skills (subagent-driven-development, tdd, writing-plans, using-git-worktrees) to the `vendor_tool_skills` section.
