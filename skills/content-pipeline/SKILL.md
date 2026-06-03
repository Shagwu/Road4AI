---
name: content-pipeline
description: Use for Road4AI content planning, weekly queue selection, scout drops, or orchestrating the five-agent content workflow across trend research, voice ideation, format selection, drafting, approval, and publishing.
origin: Road4AI
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Road4AI Content Pipeline

## When to Activate

- The user asks to process `inbox.md`, transcripts, URLs, or raw notes into content.
- The user asks for weekly planning, queue selection, or content prioritization.
- A Scout drop needs to become drafts or queue entries.
- Multiple content agents should work in parallel.

Do not use this skill for one-off copy edits that do not touch queue state or content strategy.

## The Mechanism

Road4AI uses a five-agent content pipeline:

- Chief of Staff: selects priorities and coordinates gates.
- Trend Researcher: finds weak signals and current market context.
- Voice-Match Ideator: converts signals into Road4AI-native ideas.
- Format Selector: chooses platform, format, and cadence.
- Content Scout: extracts structured knowledge from raw source material.

Independent research and ideation can run in parallel. Drafting, approval, scheduling, and queue mutation remain sequential because each depends on a gate.

## Workflow

1. Read the required coordination files: `AGENTS.md`, `state/current-queue.json`, `docs/brand-voice.md`, and `docs/content-strategy.md`.
2. Run the queue audit.
3. Identify the source material and whether it is inbox-derived, roadmap-derived, or experimental.
4. Run the dedup gate before any queue write.
5. Generate candidate ideas with title, hook, type, platform, goal, source, status, and priority.
6. Draft selected content into `drafts/ideas/` or `drafts/ready/` based on user instruction.
7. Preserve manual approval: only the user moves content into `drafts/approved/`.
8. After a successful queue write, create a Hermes checkpoint commit.

## Output Contract

Return:

- queue audit summary;
- selected content items and why they fit the strategy;
- dedup result;
- draft file paths if drafts were created;
- remaining approval or publishing gates.

## Related Skills

- `public-sanitization-review`

