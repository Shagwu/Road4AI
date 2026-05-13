---
name: ideation-orchestrator
description: >
  Enables the Chief of Staff to process raw signals from inbox.md into a structured ideation brief,
  dispatch specialists, and aggregate outputs into ideas.md.
---

# Ideation Orchestrator Mode

Activate this mode when `inbox.md` contains new signals or when a weekly content ideation sprint begins.

## Workflow

1. **Scan `inbox.md`**: Treat as raw data. Do not invent details.
2. **Build Brief**: Extract 5–10 angles. Format: `[THEME] — [raw angle] — [why this could hit]`.
3. **Dispatch Specialists**: Invoke specialist sub-agents in parallel:
   - `@content-scout`: To extract value from source transcripts/links.
   - `@format-selector`: To map angles to optimal platforms/formats.
   - `@voice-match-ideator`: To generate hooks in Shagwu's voice.
4. **Aggregate to `ideas.md`**: Merge outputs into ranked blocks.

## Output Schema (ideas.md)

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
