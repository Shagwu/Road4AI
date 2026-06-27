---
name: content-pipeline
description: Use for Road4AI content planning, weekly ideation, queue selection, scout drops, drafting, review gates, approval, scheduling, and lifecycle orchestration.
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
- A weekly content ideation sprint begins.
- A Scout drop needs to become drafts or queue entries.
- Multiple content agents should work in parallel.
- The user asks for a content slate, ranked ideas, or pipeline orchestration.

Do not use this skill for final copy edits, one-off posts that do not touch content strategy, or publishing actions that have not passed approval.

## The Mechanism

Road4AI uses a five-agent content pipeline:

- Chief of Staff: selects priorities and coordinates gates.
- Trend Researcher: finds weak signals and current market context.
- Voice-Match Ideator: converts signals into Road4AI-native ideas.
- Format Selector: chooses platform, format, and cadence.
- Content Scout: extracts structured knowledge from raw source material.

Independent research and ideation can run in parallel. Dedup, drafting, review, approval, scheduling, and queue mutation remain sequential because each depends on a gate.

## Lifecycle

1. Capture: raw notes, transcripts, links, and observations land in `inbox.md` or a scout drop.
2. Ideation: Trend Researcher, Format Selector, Voice-Match Ideator, and Content Scout work in parallel when inputs are independent.
3. Dedup: candidates are checked against `state/current-queue.json` and `state/published-log.json`.
4. Drafting: Codex drafts selected items into `drafts/ideas/` or `drafts/ready/`.
5. Karen review: `adversarial-review-karen` checks quality, logic, platform limits, and false confidence.
6. Sanitizer: `public-sanitization-review` checks exploit strings, paths, secrets, private account names, and unsafe examples.
7. Approval: only the user moves content into `drafts/approved/`.
8. Scheduling: Claude Code schedules approved content through Blotato and updates shared state.
9. Filing: after Blotato confirms scheduling, move scheduled drafts from `drafts/approved/` to `drafts/archived/` and update queue paths. The approved folder is a scheduling inbox, not storage; leaving scheduled files there creates duplicate-approval and repost risk.

## Parallel Ideation Workstreams

Launch these workstreams in parallel when the inputs are independent:

- Trend Researcher: identifies weak signals and timely market context.
- Format Selector: maps ideas to LinkedIn, X, Threads, Instagram, TikTok, or short-form video.
- Voice-Match Ideator: turns raw signals into Road4AI-native hooks.
- Content Scout: extracts structured knowledge from transcripts, URLs, or source text.

The Chief of Staff aggregates the outputs, applies Road4AI strategy, and routes each candidate to the next gate.

## Workflow

1. Read the required coordination files: `AGENTS.md`, `state/current-queue.json`, `docs/brand-voice.md`, and `docs/content-strategy.md`.
2. Run the queue audit.
3. Identify the source material and whether it is inbox-derived, roadmap-derived, or experimental.
4. Generate 3-5 ranked candidate ideas.
5. For each idea, include title, hook, type, platform, goal, source, priority, and why it fits now.
6. Run the dedup gate before any queue write.
7. Draft selected content into `drafts/ideas/` or `drafts/ready/` based on user instruction.
8. Run Karen and public sanitizer gates before approval or scheduling.
9. Preserve manual approval: only the user moves content into `drafts/approved/`.
10. After scheduling in Blotato, archive the scheduled draft and update queue references away from `drafts/approved/`.
11. After a successful queue write, create a Hermes checkpoint commit.

## Output Contract

Return:

- queue audit summary;
- source summary;
- selected content items and why they fit the strategy;
- dedup result for each candidate;
- draft file paths if drafts were created;
- recommended next gate: human review, drafting, Karen, sanitizer, approval, or scheduling.

## Anti-Patterns

- Do not invent source details that are not in the raw material.
- Do not silently write queue entries that failed dedup checks.
- Do not flatten Road4AI into generic AI marketing content.
- Do not move content into `drafts/approved/`.
- Do not publish or schedule content before approval.

## Related Skills

- `adversarial-review-karen`
- `public-sanitization-review`
