---
name: wayfinder
description: Plan a chunk of work too big or too foggy for one session — a whole Phase, or a backlog like the Phase 5 tool evaluations — as a shared map of decision tickets, resolved one at a time until the way forward is clear. Use when the user has a loose idea, a new Phase, or a growing pile of "evaluate-document-defer" items with no shared map connecting them.
disable-model-invocation: false
---

# Wayfinder (Road4AI adaptation)

A loose idea, or a backlog of individually-fine-but-uncoordinated decisions (the OmniRoute / cc-mirror / Memanto / Project Graveyard pattern from the July 15 retrospective), doesn't get better by attacking it directly. It gets charted first, as a map, then worked one ticket at a time.

This is Road4AI's version of the upstream `wayfinder` skill: same shape, but the map lives as a markdown file instead of a GitHub issue tree, and closing a ticket writes a Hermes checkpoint instead of a tracker comment.

## The Map

One file per effort: `.agents/wayfinder/<effort-name>-map.md`.

The map is an **index, not a store** — it gists each ticket in one line and links out. Never restate a ticket's full reasoning in the map itself; that lives in the ticket's own section.

```markdown
# Wayfinder Map: <destination name>

## Destination
<what "done" looks like — one or two sentences, named before any ticket exists>

## Decisions so far
- <ticket-slug>: <one-line resolution> (resolved <date>)

## Frontier (open, unblocked, unclaimed)
- [ ] <ticket-slug> — <one-line question>

## Blocked
- [ ] <ticket-slug> — blocked by <ticket-slug>

## Fog of war (anticipated, not yet ticketed)
- <thing we can tell is coming but can't pin down yet>
```

## Tickets

Each ticket is its own file: `.agents/wayfinder/<effort-name>/<ticket-slug>.md`, sized to resolve in one session.

```markdown
## Question
<the decision or investigation this ticket resolves>

## Type
research | grilling | task

## Status
open | claimed | resolved

## Resolution
<filled in when closed>
```

**Claiming**: before doing any work on a ticket, mark it `claimed` in its own file and note the session in the map's Frontier line. This is the only coordination mechanism — if you didn't claim it, don't touch it, since another session (you, later, or a collaborator like Sharon) may be working it.

**Research tickets are the exception** to one-ticket-per-session: fire them in parallel since they're read-only investigation, not decisions with side effects.

## Working a ticket

1. Pick one from the Frontier (or run a research ticket in parallel batch).
2. If it's a real decision, not just a lookup — invoke `grilling` on the question.
3. Write the resolution into the ticket file, move its line from Frontier to Decisions so far, close it.
4. If closing it unblocks other tickets, move those into Frontier. If it reveals new fog, add it to Fog of war.
5. Write a `[hermes-context]` checkpoint for the resolution — this is what makes the map durable the same way everything else in Road4AI is durable.

## First use case: the Phase 5 backlog

Per the July 15 retrospective, OmniRoute, cc-mirror, Memanto, gpt-oss-120b, and Project Graveyard were each evaluated correctly but independently, with no shared view of the growing backlog. Stand up `.agents/wayfinder/phase-5-tools-map.md` with:

- **Destination**: a Phase 5 tool-adoption decision, or an explicit "not yet, re-evaluate after Phase 4 usage data" close-out
- Each already-evaluated tool becomes a **resolved** ticket (they're already decided — this is backfilling the map, not re-litigating them)
- New tool evaluations must open a ticket on this map *before* a CoS evaluation call happens, not after

This directly implements the retrospective's own recommendation to resist new Phase 5 evaluations until Phase 4 has real usage data — the map makes that a visible gate instead of a private resolution to remember.

## When to skip this

If a grilling session on the idea surfaces no real fog — the destination and the steps are already obvious — say so and skip the map. Wayfinder is for genuine multi-session uncertainty, not a formality to perform on every plan.
