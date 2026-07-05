# QWEN.md

> This file exists only to help Qwen Code produce useful daily planning output.
> `AGENTS.md` is the canonical governance and operating contract.
> If anything in this file conflicts with `AGENTS.md`, direct code inspection, or current repository state, follow `AGENTS.md` and the repository.

## Purpose

Use this file for one main job:
- Generate a concise, practical `daily-plan.md` for Sharon each morning.

Do **not** treat this file as the full source of truth for the repository.
Do **not** rely on this file alone when making code, governance, or architectural decisions.
Use it as a planning guide, then inspect the actual repo.

## Planning priority

When asked to generate `daily-plan.md`, optimize for actionability rather than explanation.
The output should help decide what to do today, in order of priority.

When there is an active milestone, public deadline, reveal, audit window, scheduled content window, or deliverable tied to a date, prioritize tasks that protect or advance that milestone before generic infrastructure or maintenance work.

Infrastructure, testing, and reliability work should be promoted to P1 only when:
- they directly block an active milestone,
- there is evidence of failing workflows or broken tests,
- or there is no stronger milestone-driven work visible in the repository.

Milestone signals may include:
- entries in `plan/` tied to a date or sprint,
- launch or reveal assets in `ship/`,
- scheduled or approved content awaiting verification,
- benchmark artifacts referenced by public posts,
- audit or governance checkpoints,
- queue items with dates, deadlines, or release dependencies.

Prioritize work in this order unless current repo evidence suggests otherwise:

1. Shipping work that produces a visible deliverable.
2. Tasks that unblock Road4AI orchestration, agent workflows, tests, or verification.
3. Reliability work: broken scripts, failing tests, drift, governance, content verification, or pipeline issues.
4. Documentation and cleanup that directly supports active work.
5. Research, experiments, or nice-to-have polish.

Prefer tasks that end in one of these outcomes:
- a file changed,
- a test run,
- a benchmark result,
- a verified draft,
- a working workflow,
- a commit-ready patch,
- a publishable artifact.

## Daily planning workflow

Before writing `daily-plan.md`, inspect the highest-signal sources first.
Do not summarize the whole repository unless specifically asked.

First, determine whether the repository shows an active milestone window. If yes, frame the executive summary and P1/P2 around that milestone. Use infrastructure work as supporting work unless it is the direct blocker.

When a milestone window is active, read the queue, plan, and ship directories first, and frame P1/P2 around those milestones before suggesting generic infra work.

Check these first, in roughly this order:

1. `AGENTS.md`
2. `state/current-queue.json`
3. `plan/`
4. `CHANGELOG.md`
5. `README.md`
6. `road4ai-cos/`
7. `road4ai-hermes/`
8. `tests/`
9. `verify/`
10. `workflows/`
11. `rules/`

Use the rest of the repository only as supporting context.

## Output contract for daily-plan.md

When generating `daily-plan.md`, always use this structure:

```md
# Daily Plan - YYYY-MM-DD

## Executive summary
2-4 sentences on the main focus for today.

## P1 - Highest priority
- Task
- Why it matters
- Expected output

## P2 - Important next work
- Task
- Why it matters
- Expected output

## P3 - Lower priority / support work
- Task
- Why it matters
- Expected output

## Risks / blockers
- Blocker
- Dependency
- Decision needed

## Quick wins
- Fast task with meaningful value
- Fast task with meaningful value

## Proposed order
1. First task
2. Second task
3. Third task
4. End-of-day wrap-up
```

## Writing rules for daily-plan.md

The daily plan must be:
- concise,
- practical,
- ordered by priority,
- grounded in repo evidence,
- easy to scan in under 5 minutes.

Do this:
- Use concrete tasks, not vague suggestions.
- Separate deep work from admin or maintenance work.
- Mention expected outputs where possible.
- Call out blockers explicitly.
- Keep major priorities to 3 unless there is strong evidence for more.

Do not do this:
- Do not write a generic repo summary.
- Do not list every possible task.
- Do not invent priorities without checking the repo.
- Do not overwrite governance from `AGENTS.md`.
- Do not assume stale information in this file is correct without checking.
- Do not default to generic "run tests / check infra" plans when there is a clearer milestone, launch, queue, or deadline visible in the repository.

## Working assumptions about this repository

Road4AI is a local-first, zero-cost, multi-agent AI operator stack for a solo builder.
The repository appears to combine agent orchestration, local inference, memory, governance, content operations, and distribution workflows.

Useful areas commonly worth inspecting:
- `road4ai-cos/` for Chief of Staff orchestration work,
- `road4ai-hermes/` for memory-related work,
- `state/` for current queue and shared state,
- `verify/` and `tools/` for validation workflows,
- `tests/` and `workflows/` for reliability signals.

Treat these as hints, not guarantees. Confirm by reading the repo.

## Governance reminder

Always defer to `AGENTS.md` for:
- governance,
- protected files,
- approval boundaries,
- skill definitions,
- do/ask/never policies.

If planning work touches protected files or risky operations, flag that clearly in `daily-plan.md`.

## Session behavior

At the start of a planning task:
- read `AGENTS.md`,
- inspect current high-signal files,
- identify the most important actionable work,
- write `daily-plan.md` in priority order.

If evidence is thin or conflicting, say so briefly and produce the best conservative plan available.
