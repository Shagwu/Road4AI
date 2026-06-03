---
name: content-ideation-orchestrator
description: Use for Road4AI weekly ideation, inbox processing, or coordinating the parallel trend, format, voice, and scout workflow into ranked content candidates.
origin: Road4AI
tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Content Ideation Orchestrator

## When to Activate

- A weekly content ideation sprint begins.
- `inbox.md` contains new raw signals to process.
- The user asks for content ideas, a weekly slate, or pipeline orchestration.
- A Scout drop needs to become ranked ideas, queue candidates, or drafts.

Do not use this for final copy editing, publishing, or one-off posts that do not need pipeline coordination.

## The Mechanism

Road4AI ideation works as a gated content flywheel:

1. Sunday capture: raw notes, transcripts, links, and field observations land in `inbox.md`.
2. Monday ideation: independent agents analyze the raw material in parallel.
3. Human gate: the operator chooses which ideas deserve drafting.
4. Codex drafting: selected ideas become drafts.
5. Karen and sanitizer gates: quality and public-safety checks run before approval.
6. Scheduling: approved content moves through Gemini CLI and Blotato.

## Parallel Agents

Launch these workstreams in parallel when inputs are independent:

- Trend Researcher: identifies weak signals and timely market context.
- Format Selector: maps ideas to LinkedIn, X, Threads, Instagram, TikTok, or short-form video.
- Voice-Match Ideator: turns raw signals into Road4AI-native hooks.
- Content Scout: extracts structured knowledge from transcripts, URLs, or source text.

The Chief of Staff aggregates outputs and applies gates.

## Workflow

1. Read `AGENTS.md`, `WORKING-CONTEXT.md`, `state/current-queue.json`, `docs/brand-voice.md`, and `docs/content-strategy.md`.
2. Run the queue audit.
3. Read the source material and identify source provenance: inbox, roadmap, audience question, experiment, or scout drop.
4. Check `state/current-queue.json` and `state/published-log.json` before proposing queue writes.
5. Generate 3-5 ranked ideas.
6. For each idea, include:
   - title;
   - hook;
   - type: Struggle, Win, Tutorial, or Behind-the-scenes;
   - platform;
   - goal;
   - source;
   - priority;
   - why it fits now.
7. Run the dedup gate before any queue mutation.
8. Put selected drafts in `drafts/ideas/` or `drafts/ready/` according to user instruction.

## Output Contract

Return:

- queue audit summary;
- source summary;
- 3-5 ranked content candidates;
- dedup status for each candidate;
- recommended next gate: human review, drafting, Karen, sanitizer, or scheduling.

## Anti-Patterns

- Do not invent source details that are not in the raw material.
- Do not silently write queue entries that failed dedup checks.
- Do not flatten Road4AI into generic AI marketing content.
- Do not move content into `drafts/approved/`.

## Related Skills

- `content-pipeline`
- `public-sanitization-review`
- `adversarial-review-karen`

