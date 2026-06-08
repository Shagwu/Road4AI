---
title: Why I Added Obsidian to Road4AI (And Why It Can't Control Me)
date: 2026-06-24
type: behind-the-scenes
platform: linkedin
status: working-draft
---

## Hook

I added Obsidian to Road4AI.

Then I immediately made sure it could not become the system.

That sounds backwards until you have watched a note app quietly turn into a second operating layer.

Hermes v2.1 is about the learning layer.
Obsidian is only the thinking layer.
The repo stays the operational layer.

That separation matters more than the tool.

## Act 1: The Problem (Tool Sprawl)

Most solo builders do not lose control all at once.

They lose it one convenience at a time.

First, the note app is just a place to think.

Then it becomes the place where ideas live.

Then it starts holding status.

Then links become todos.

Then a graph starts feeling like progress.

Then the builder has two systems:

One system where the work actually happens.

Another system where the work feels organized.

That split is dangerous because both layers look useful.

The repo has the real workflow:

Queue state.
Approved drafts.
Published logs.
Hermes checkpoints.

Obsidian has the thinking surface:

Themes.
Backlinks.
Clusters.
Reflection.

Both are useful.

But if both start claiming operational truth, the system starts lying.

Not because Obsidian is bad.

Because any tool that is easier to update than the source of truth will eventually tempt you to treat convenience as correctness.

That is where tool sprawl begins.

Not with too many tools.

With unclear boundaries.

## Act 2: The Solution (Three Guardrails)

So I added Obsidian with constraints already attached.

The rule is simple:

Obsidian can help me think.

It cannot decide what is true.

### Guardrail 1: Status markers are reflection, not automation

I can write markers like:

```md
Status: raw
Status: idea
Status: drafted
Status: approved
Status: scheduled
Status: filed
```

But those markers are for human scanning only.

No automation is allowed to read them.

If a workflow needs real status, that logic belongs in an explicit state file.

For Road4AI, that means `state/current-queue.json`, not a loose Markdown marker.

The marker can help me remember where an idea is emotionally or narratively.

It cannot become the workflow gate.

### Guardrail 2: The graph is navigation, not readiness

Obsidian graphs are useful because they show theme clusters.

Token anxiety can connect to context windows.

System integrity can connect to governance.

Self-knowledge can connect to Hermes.

That helps me see the narrative.

But a connected idea is not automatically ready to draft.

An orphaned idea is not automatically weak.

The graph can show relationships.

It cannot approve content.

It cannot schedule content.

It cannot replace the queue.

### Guardrail 3: The queue stays in the repo

Road4AI already has operational truth.

`state/current-queue.json` holds queue and scheduling truth.

`drafts/approved/` holds human approval truth.

`state/published-log.json` holds publishing truth.

`drafts/archived/` holds completed content assets.

Obsidian does not replace any of that.

It sits after capture and planning, not inside the execution gates.

Sunday is for raw capture.

Monday is for the ideation sprint.

After the sprint closes, Obsidian can help me review clusters and add useful backlinks.

Drafting, review, approval, scheduling, and publishing still move through the Road4AI gates.

That is the boundary:

Obsidian helps me navigate thought.

Hermes v2.1 handles the learning layer.

The repo runs operations.

## Act 3: Why It Matters

[PLACEHOLDER FOR CLAUDE]

## CTA

[PLACEHOLDER FOR CLAUDE]

---

## Karen Gate Checklist

- [ ] Does this confuse readers into thinking Obsidian is part of Hermes v2.1?
- [ ] Is the spine clear: thinking (Obsidian) | learning (Hermes v2.1) | operations (repo)?
- [ ] Does it avoid sounding like a tool announcement?
- [ ] Does voice match Road4AI (insider, pragmatic, no em dashes)?
