---
name: hermes-checkpoint
description: Hermes v2.0 distributed memory checkpoint system for Road4AI. Use whenever a logical unit of work is complete, before long-running install/build/test/deploy commands, after bug fixes, after queue writes, or when switching context between agents or sessions.
origin: Road4AI
tools:
  - Bash
  - Read
  - Edit
  - Grep
---

# Hermes Checkpoint

## When to Activate

- A logical unit of work is complete.
- A new intentional file was created.
- A function, module, feature, or governance change is complete.
- A bug is verified fixed.
- A content item moves lifecycle stage.
- `state/current-queue.json` is successfully written.
- A long-running install, build, test, or deploy command is about to run.
- The session is ending or switching agents.
- The user says "save progress", "checkpoint", "commit this", "save context", "switching agents", or "picking this up later".

Do not use this for broken mid-edit state, failed tests, or exploratory scratch work that should not be preserved.

## The Mechanism

Hermes checkpoints are structured git commits that preserve machine-readable context for other agents. The Chief of Staff reads recent `[hermes-context]` blocks at session start and briefs the operator on completed work, remaining work, and low-confidence states.

## Workflow

1. Run `git status --short`.
2. Review changed files and identify only the files that belong to the completed logical unit.
3. Do not stage unrelated user changes.
4. Run any relevant validation before checkpointing.
5. Stage explicit files only.
6. Commit with a `CHECKPOINT:` subject and a `[hermes-context]` block.
7. Do not push unless `HERMES_PUSH=true` is explicitly set.

## Staging Rules

- Use explicit `git add <file>` commands.
- Never use `git add -A`.
- Do not stage unrelated draft, queue, tool metadata, or generated files.
- Do not revert changes you did not make.
- If `AGENTS.md` was changed, confirm the session included explicit human approval and the governance lock was restored.

## Commit Format

```text
CHECKPOINT: <one-line description of what changed>

[hermes-context]
Decisions: <what was locked in: architecture, content direction, governance, or system config>
Remaining: <what is next in this logical unit>
Tried: <what failed and why, or omit if nothing failed>
Confidence: high | medium | low
Context_type: build | content | system | research
Agent: <gemini-cli | claude | codex | cos>
[/hermes-context]
```

## Field Guide

| Field | Required | Purpose |
|-------|----------|---------|
| `Decisions` | Yes | Records what was locked in so agents do not re-litigate settled choices. |
| `Remaining` | Yes | Lets another agent resume without asking for a recap. |
| `Tried` | No | Captures failed approaches to prevent repeated loops. |
| `Confidence` | Yes | Signals whether the state is clean or needs human review. |
| `Context_type` | Yes | Routes the checkpoint to the right memory layer. |
| `Agent` | Yes | Traces the decision to the agent that wrote it. |

## Context Restore

At session start or when resuming work, run:

```bash
git log --grep="CHECKPOINT:" --format="%B" -3
```

Parse each `[hermes-context]` block and brief the operator on:

- what was last completed;
- what remains;
- any low-confidence states needing review;
- which agent last touched each context type.

## Output Contract

When checkpointing is requested and a commit is created, return:

- checkpoint subject;
- files staged;
- validation run;
- remaining work;
- confidence.

If checkpointing is unsafe, return the blocker instead of committing.

## Related Skills

- `content-pipeline`
- `public-sanitization-review`

