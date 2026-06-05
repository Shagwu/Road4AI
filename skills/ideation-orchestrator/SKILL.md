---
name: ideation-orchestrator
description: Enables the Chief of Staff to process raw signals from inbox.md into a structured ideation brief, dispatch specialists, and aggregate outputs into ideas.md.
origin: Road4AI
tools:
  - Read
  - Edit
  - Grep
  - Glob
---

# Road4AI Ideation Orchestrator

## When to Activate

- `inbox.md` contains new signals (Struggles, Wins, Consumed, Questions).
- A weekly content ideation sprint begins.
- The user asks to "process the inbox," "plan the week," or "find content ideas."
- High-level orchestration is needed to coordinate Trend Researcher, Voice-Match, and Format specialists.

Do not use this for one-off drafting or final scheduling. This is a strategy and orchestration layer.

## The Mechanism

The Orchestrator processes raw signals into structured briefs and manages parallel specialist workstreams to fill the content queue.

## Workflow

1. **Scan `inbox.md`**: Treat as raw data. Do not invent details.
2. **Build Brief**: Extract 5–10 candidate angles. Format: `[THEME] — [raw angle] — [strategic rationale]`.
3. **Dispatch Specialists**: Invoke specialist sub-agents in parallel:
   - `content-scout`: Extract value from source transcripts/links.
   - `format-selector`: Map angles to optimal platforms/formats.
   - `voice-match-ideator`: Generate hooks in the Road4AI voice.
4. **Aggregate to `ideas.md`**: Merge outputs into ranked blocks.
5. **Human Gate**: End with `> ⚠️ Human review required before any post goes live.`

## Output Schema (`ideas.md`)

```markdown
## [Idea title — punchy, no em dashes]

**Hook draft:** [opening line in Road4AI voice]
**Platform:** [LinkedIn / X / Instagram / Threads]
**Format:** [post / reel / carousel / thread]
**Angle:** [what makes this different]
**Source signal:** [inbox.md line reference]
**Rank:** [🔥 / 🟡 / 🧊]
```

## Governance Mandates

- **No Em Dashes:** Strict prohibition in all hook drafts and content strings.
- **Grounding:** Every idea must trace back to a source line in `inbox.md`.
- **Governance Lock:** You are prohibited from mutating `AGENTS.md`. This is a non-delegable constraint.
- **Authenticity:** Prioritize Struggle-lane content (25-30% of queue).

## Related Skills

- `content-pipeline`
- `voice-match`
- `adversarial-review-karen`
