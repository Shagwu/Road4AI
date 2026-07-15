---
name: ideation-orchestrator
description: >
  Enables the Chief of Staff to process raw signals from inbox.md into a structured ideation brief,
  dispatch specialists, and aggregate outputs into ideas.md.
origin: Road4AI
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Ideation Orchestrator Mode

## When to Activate

- `inbox.md` contains new signals or raw capture material.
- A weekly content ideation sprint begins.
- The Chief of Staff needs to dispatch specialist sub-agents in parallel.

Do not use this skill for drafting, editing, scheduling, or publishing content. Those gates belong to the content-pipeline skill.

## The Mechanism

The ideation orchestrator scans `inbox.md` for raw signals, builds a structured brief with 5-10 angles, dispatches specialist sub-agents (content-scout, format-selector, voice-match-ideator) in parallel, then aggregates their outputs into a ranked `ideas.md` file.

## Workflow

1. **Scan `inbox.md`**: Treat as raw data. Do not invent details.
2. **Build Brief**: Extract 5–10 angles. Format: `[THEME] — [raw angle] — [why this could hit]`.
3. **Dispatch Specialists**: Invoke specialist sub-agents in parallel:
   - `@content-scout`: To extract value from source transcripts/links.
   - `@format-selector`: To map angles to optimal platforms/formats.
   - `@voice-match-ideator`: To generate hooks in Shagwu's voice.
4. **Aggregate to `ideas.md`**: Merge outputs into ranked blocks.

## Output Contract (ideas.md)

```markdown
## [Idea title — punchy, no em dashes]

**Hook draft:** [opening line in Shagwu's voice]
**Platform:** [LinkedIn / X / Instagram / Threads]
**Format:** [post / reel / carousel / thread]
**Angle:** [what makes this different]
**Source signal:** [inbox.md line reference]
**Rank:** [🔥 / 🟡 / 🧊]
```

## Mandates

- **No Em Dashes**: Strict prohibition in all content strings.
- **Grounding**: Every idea must trace back to a source line in `inbox.md`.
- **Governance**: You cannot mutate `AGENTS.md`. This is a hard lock.
- **Human Gate**: Always end with `> ⚠️ Human review required before any post goes live.`
