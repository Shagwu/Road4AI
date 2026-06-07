# Obsidian Workflow for Road4AI

Obsidian is the thinking and navigation layer for Road4AI. It helps connect themes, raw captures, source notes, and recurring ideas across the Markdown files already in the repo.

Obsidian is not the operational source of truth.

## What Obsidian Is For

- Navigate recurring themes with links like `[[Token Anxiety]]`, `[[Self-Knowledge Pivot]]`, and `[[System Integrity]]`.
- Review clusters after weekly planning to see what ideas are developing.
- Add backlinks when they clarify how a raw signal connects to Road4AI's larger narrative.
- Preserve learning-in-public context without moving content out of the repo workflow.

## What Obsidian Is Not For

- Scheduling posts.
- Approving content.
- Publishing content.
- Replacing queue state.
- Replacing draft folders.
- Replacing Hermes checkpoints.

Operational truth stays here:

- `state/current-queue.json` for queue and scheduling truth.
- `drafts/approved/` for human approval truth.
- `state/published-log.json` for publishing truth.
- `drafts/archived/` for completed content assets.

## Status Markers

Use plain-text markers when they help a human scan a note:

```md
Status: raw
Status: idea
Status: drafted
Status: approved
Status: scheduled
Status: filed
```

Status markers are for human navigation and reflection only. Automation scripts are forbidden from reading `Status:` markers. If a workflow needs automation, add the logic to `state/current-queue.json` or another explicit state file instead, then remove the status dependency from the note.

## Graph Guardrail

The graph visualizes themes and thinking, not workflow readiness. A well-connected idea is not automatically ready to draft. An orphaned idea is not failed. Trust `state/current-queue.json`, `drafts/approved/`, and `state/published-log.json` for workflow truth.

## Red Link Guardrail

Red links are possible future notes, not todos. A red link earns a file only when the theme has enough captured signal to justify a standalone note. If a red link stays unresolved for 30 days and is not helping navigation, delete the link.

## Weekly Ritual

Obsidian comes after the operational ideation sprint, not during it.

Recommended loop:

1. Sunday: capture raw signals in `inbox.md`, `TOKEN_ANXIETY_LOG.md`, or scout drops.
2. Monday: run the Road4AI ideation sprint and update `ideas.md` or `state/current-queue.json`.
3. After the sprint closes: open Obsidian, review the new clusters, and add only the backlinks that clarify thinking.
4. Drafting, review, approval, scheduling, and publishing continue through the normal Road4AI gates.

## Validation Checkpoint

After the next full Sunday/Monday content cycle, run a 15-minute reflection and document the result in this file or the relevant planning note.

Ask:

- Did Obsidian help the thinking process?
- Did the links feel natural or forced?
- Were `Status:` markers useful, or did they become noise?
- Did any `Status:` marker try to become automation?
- Did the graph reveal an unexpected theme cluster?
- Was Obsidian faster than grep for the question being asked?

Use the reflection to decide whether this layer should stay light, expand carefully, or be rolled back.

## Hermes Checkpoint Alignment

Hermes checkpoints save Markdown content and explicit state files. Obsidian UI metadata, graph position, and workspace state are ignored. If the Obsidian vault is deleted, git history plus checkpoint content should fully recover the thinking layer.

## Filing Used Ideas

Ideas that reach `Status: filed` stay in their original source file with the marker. Do not create separate Obsidian-only archive files.

For `TOKEN_ANXIETY_LOG.md`, the `FILED / USED IDEAS` section remains the canonical archive for used token-anxiety ideas.

## Link Style

Use semantic topic links instead of file-path links:

```md
[[Token Anxiety]]
[[Self-Knowledge Pivot]]
[[System Integrity]]
[[SkillOpt]]
[[Tireless Worker Trap]]
[[Context Windows]]
[[AI Agents]]
[[Text-to-Action Programming]]
[[Road4AI Content Pipeline]]
```

Keep links light. The goal is navigability, not formatting pressure.
