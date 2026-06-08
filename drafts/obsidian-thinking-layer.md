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

Obsidian is not part of Hermes v2.1.

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

Obsidian is not the product.

It is the boundary test.

## Act 3: Why It Matters

You are doom scrolling, you hit a repo, and something in your brain lights up:

This is it.

This is the missing piece.

This will change everything for Road4AI.

You read the README.

You skim the code.

You start imagining integrations it was not even built for.

By the time you are done, you are not just evaluating a repo.

You are emotionally committed to a possible future where this thing fixes your system.

And because it feels that big, your first instinct is to pull it into your world fast.

You grab a summary.

You feed it into your mentor.

You start asking:

How do we use this?

Not:

Should we?

Not:

Where does this live?

Just:

How do we plug this in?

That is the moment where boundaries matter.

In a boundaryless system, this repo quietly becomes:

Yet another place that defines how content should move.

Yet another opinion about state, memory, or workflow.

Yet another game changer sitting half-integrated, half-abandoned, still taking up mental RAM.

In a system with boundaries, you run a different script:

Which domain is this allowed to touch: memory, state, publishing, or orchestration?

What, if anything, does it replace?

If I adopt this, what do I explicitly not allow it to control?

Same excitement.

Same repo.

Completely different impact.

So the move is not to stop doom scrolling.

It is not to be more careful before you get excited.

The move is this:

Even when you are excited, the repo still has to pass through the boundary filter.

Your mentor does not just answer:

How can we use this?

It also has to answer:

Where, if anywhere, does this belong?

And what power are we giving it?

## CTA

If you take anything from this, do not copy my Obsidian setup.

Copy the boundary question.

Before you add the next tool, ask yourself:

What is this allowed to control?

What is it forbidden from controlling?

And where does operational truth live when the excitement wears off?

You do not need my stack.

You need a contract.

The tools can change.

The boundaries stay.

---

## Karen Gate Checklist

- [ ] Does this confuse readers into thinking Obsidian is part of Hermes v2.1?
- [ ] Is the spine clear: thinking (Obsidian) | learning (Hermes v2.1) | operations (repo)?
- [ ] Does it avoid sounding like a tool announcement?
- [ ] Does voice match Road4AI (insider, pragmatic, no em dashes)?
