---
name: hermes-checkpoint-patterns
description: Use to explain, apply, or audit Road4AI Hermes checkpoint behavior across sessions, agents, commits, context recovery, and handoffs.
origin: Road4AI
tools:
  - Bash
  - Read
  - Grep
---

# Hermes Checkpoint Patterns

## When to Activate

- The user asks to save progress, checkpoint, hand off, resume, or recover context.
- A logical unit of work is complete and should be preserved.
- A long-running command, install, build, test, deploy, or agent switch is about to happen.
- You need to audit whether a checkpoint captured decisions, blockers, and remaining work clearly.

Do not use this for trivial one-line changes, failed experiments, or broken mid-edit state.

## The Mechanism

Hermes checkpoints are structured git commits with `[hermes-context]` blocks. They turn repo history into shared memory that Gemini CLI, Codex, and other agents can parse after context resets.

The checkpoint records:

- decisions locked in;
- remaining work;
- failed approaches;
- confidence level;
- context type;
- responsible agent.

## Workflow

1. Run `git status --short`.
2. Identify the completed logical unit.
3. Stage only intentional files.
4. Run relevant validation.
5. Commit with:

```text
CHECKPOINT: <one-line description>

[hermes-context]
Decisions: <what was locked in>
Remaining: <what is next>
Tried: <what failed and why, or omit if none>
Confidence: high | medium | low
Context_type: build | content | system | research
Agent: <gemini-cli | claude | codex | cos>
[/hermes-context]
```

6. At session start, restore context with:

```bash
git log --grep="CHECKPOINT:" --format="%B" -3
```

7. Brief the operator on completed work, remaining work, low-confidence states, and the agent that last touched each context.

## Output Contract

Return:

- checkpoint subject;
- files staged;
- validation run;
- `[hermes-context]` summary;
- remaining work;
- confidence.

For recovery, return:

- most recent relevant checkpoint;
- decisions already locked;
- next action;
- low-confidence states.

## Anti-Patterns

- Do not checkpoint unrelated user changes.
- Do not use `git add -A`.
- Do not checkpoint failed tests as if they are complete.
- Do not omit the decision rationale.
- Do not use checkpoints to bypass human approval gates.

## Related Skills

- `hermes-checkpoint`
- `content-ideation-orchestrator`
- `adversarial-review-karen`

