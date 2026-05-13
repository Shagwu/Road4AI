---
name: hermes-checkpoint
description: |
  Hermes v2.0 distributed memory checkpoint system for Road4AI. Use this skill
  whenever you complete a logical unit of work, before a long-running command,
  after a bug fix, or when switching context between agents or sessions. Triggers
  on phrases like "save progress", "checkpoint", "commit this", "save context",
  "switching agents", or "picking this up later". Also auto-triggers before any
  install, build, test, or deploy command. This is the memory backbone of the
  Chief of Staff agent — use it proactively, not just when asked.
---

# Hermes Checkpoint

The distributed memory layer for Road4AI. Every checkpoint is a structured git
commit that any agent in the system can read, parse, and resume from — across
sessions, across tools, across context resets.

---

## When to checkpoint

Commit a checkpoint after:
- A new file is created intentionally
- A function, module, or feature is complete
- A bug is verified fixed
- A content piece moves from draft to ready
- A decision is made that affects architecture or direction

Commit a checkpoint before:
- Any long-running command (`npm install`, `bun run build`, deploys)
- Switching from one agent to another
- Ending a session you plan to resume

**Never checkpoint:**
- Broken or mid-edit state
- Failed tests
- Exploratory scratch work you don't intend to keep

---

## Commit format

```
CHECKPOINT: <one-line description of what changed>

[hermes-context]
Decisions: <what was locked in — architecture choice, content direction, system config>
Remaining: <what's next in this logical unit>
Tried: <what failed and why — omit if nothing failed>
Confidence: high | medium | low
Context_type: build | content | system | research
Agent: <gemini-cli | claude | codex | cos (Chief of Staff)>
[/hermes-context]
```

### Field guide

| Field | Required | Purpose |
|-------|----------|---------|
| `Decisions` | Yes | What got locked in. Stops agents re-litigating settled choices. |
| `Remaining` | Yes | What's next. Lets any agent pick up without asking you to recap. |
| `Tried` | No | Failed approaches. Prevents the agent looping on dead ends next session. |
| `Confidence` | Yes | How solid is this state. Low = needs human review before continuing. |
| `Context_type` | Yes | Routes the checkpoint to the right memory layer in Hermes. |
| `Agent` | Yes | Which agent wrote this. Helps trace decisions back to their source. |

---

## Staging rules

- Stage only intentional files — **never `git add -A`**
- List files explicitly: `git add src/agent.md inbox.md`
- Do not push unless `HERMES_PUSH=true` is set — default is local only
- Do not announce the checkpoint commit in conversation — just do it silently

---

## Context restore

When starting a session or resuming work, run:

```bash
git log --oneline -10 | grep "CHECKPOINT:"
```

Then read the most recent relevant checkpoint body to reconstruct state. The
`[hermes-context]` block is machine-parseable — the Chief of Staff agent reads
it directly to brief you on where things stand.

For a full session restore:

```bash
git log --grep="CHECKPOINT:" --format="%H %s" -5
git show <commit-hash>
```

---

## Context types explained

| Type | Use for |
|------|---------|
| `build` | Code, agent architecture, system config, Hermes internals |
| `content` | Posts, scripts, hooks, content pipeline decisions |
| `system` | Road4AI infrastructure, tool integrations, workflow changes |
| `research` | Findings, tool evaluations, competitor analysis |

---

## Example checkpoints

**After finishing a Hermes memory module:**
```
CHECKPOINT: Add distributed memory write layer to Hermes v2.0

[hermes-context]
Decisions: Using JSONL over SQLite for portability across zero-cost stack
Remaining: Wire read layer to Chief of Staff context restore flow
Tried: SQLite worked locally but broke on Codex environment — dropped it
Confidence: high
Context_type: build
Agent: gemini-cli
[/hermes-context]
```

**Before switching to Claude for content work:**
```
CHECKPOINT: Inbox capture habit live — 3 days validated

[hermes-context]
Decisions: inbox.md is single capture point, no sub-folders until habit is solid
Remaining: Sunday ritual to batch-process inbox into content queue
Tried: Tried tagging system in first pass — too much friction, removed it
Confidence: high
Context_type: content
Agent: cos
[/hermes-context]
```

**Low confidence state needing human review:**
```
CHECKPOINT: Social Remix Agent architecture draft — needs review

[hermes-context]
Decisions: Agent reads from inbox.md, drafts platform variants, human approves before post
Remaining: Define approval gate mechanism — manual vs Blotato webhook
Tried: None yet — first pass
Confidence: low
Context_type: system
Agent: claude
[/hermes-context]
```

---

## Integration with Chief of Staff

The Chief of Staff agent reads `[hermes-context]` blocks on session start and
produces a briefing. To trigger this, add to your `cos` system prompt:

```
On session start, run:
git log --grep="CHECKPOINT:" --format="%B" -3

Parse each [hermes-context] block and brief the operator on:
- What was last completed
- What's remaining
- Any low-confidence states needing review
- Which agent last touched each context type
```

---

## Confidence guide

**high** — state is clean, tested, and ready for the next agent to build on
**medium** — works but has known rough edges; note them in `Remaining`
**low** — incomplete, untested, or a decision that needs human sign-off before continuing
