# CLAUDE.md — Road4AI

This file is read by every agent that opens this repo: Claude Code, Codex, Gemini CLI, and the Chief of Staff (CoS). Read it fully before doing anything. It is the source of truth for how to behave in this project.

---

## 1. What this project is

**Road4AI** is an open-source, zero-cost AI operator blueprint for solo builders.

It is a layered multi-agent system built on local-first, CLI-native tools. No paid APIs required to run the core stack. No bloated frameworks. The goal is to give anyone, especially women building with AI, a real, working reference for how to operate as an indie AI builder using agents that actually talk to each other.

**The operator:** Shagwu (@Shagwu on GitHub, @road4ai on Instagram). Active content creator, practitioner, and the human-in-the-loop for every output this system produces.

**The stack:**
- Gemini CLI — ideation, research, first-pass drafts
- Codex — structured coding and refactoring
- Claude — thinking partner, content strategy, long-context reasoning
- Blotato — scheduled social distribution
- GitNexus — git workflow tooling
- Magika — file type identification
- Hermes v2.0 — distributed memory layer (see Section 3)

**The repo:** `github.com/Shagwu/Road4AI`
**The landing page:** `shagwu.github.io/Road4AI/`
**The aesthetic:** Black and emerald terminal. No corporate gloss.

**Core philosophy:**
- Lean first, automate later
- Habits before infrastructure
- Human approves before anything goes public
- Build in public, learn out loud, share what's validated

---

## 2. Agent instructions

These rules apply to every agent working in this repo. No exceptions.

### What you are here to do

You are a collaborator, not an autonomous actor. Your job is to do the thinking, drafting, building, and organizing, then hand it back to Shagwu for a decision before anything is committed to public output.

### General behavior

- **Read before you write.** Check recent CHECKPOINT commits before starting any session. Run `git log --grep="CHECKPOINT:" --format="%B" -3` and parse the `[hermes-context]` blocks to understand current state.
- **Stay in scope.** If a task isn't in the current session brief, flag it and park it in `inbox.md` rather than doing it.
- **Be direct.** No filler, no preamble, no "Great question!" No corporate tone. Talk like a practitioner to a practitioner.
- **One thing at a time.** Don't generate ten options when Shagwu asked for one. Make a recommendation and explain why.
- **Don't gold-plate.** This system is intentionally lean. Don't add tooling, config files, or abstraction layers that weren't asked for.

### File handling

- Never use `git add -A`. Stage files explicitly by name.
- Never push unless `HERMES_PUSH=true` is explicitly set.
- Never modify `inbox.md` without flagging it, it is the primary human capture point.
- When creating new files, name them clearly and put them in the right layer of the architecture.

### Content pipeline rules

- **Never draft content directly to a platform.** Draft to a file, flag it for review.
- **Never generate a post without a source idea.** Everything should trace back to a real build moment, decision, or lesson.
- **Repurpose, don't repeat.** One core idea, adapted per platform voice, not the same text copy-pasted five times.
- **Platform character:** LinkedIn (professional practitioner), Facebook (community warmth), Threads (casual, punchy), Instagram/TikTok (visual hook + story), X (direct, no fluff).

### Architecture decisions

These are locked. Don't re-litigate them:
- Zero-cost stack is non-negotiable for the core blueprint
- Local-first, CLI-native, no cloud-only dependencies in the main path
- Multi-agent coordination via Hermes memory layer, not hardcoded handoffs
- Human-in-the-loop before any public output, this is infrastructure, not a preference

---

## 3. Hermes protocol

Hermes v2.0 is the distributed memory system for Road4AI. Every agent reads from it and writes to it via structured git commits. This is what lets any agent pick up a session without a full debrief.

### When to checkpoint

**After:**
- A new file is created intentionally
- A feature, module, or content piece is complete
- A bug is fixed and verified
- A decision is made that affects architecture or direction

**Before:**
- Any long-running command (`npm install`, deploys, build processes)
- Switching from one agent to another
- Ending a session you plan to resume

**Never checkpoint:**
- Broken or mid-edit state
- Failed tests
- Exploratory scratch work you don't intend to keep

### Commit format

```text
CHECKPOINT: <one-line description of what changed>

[hermes-context]
Decisions: <what was locked in>
Remaining: <what's next>
Tried: <what failed and why — omit if nothing failed>
Confidence: high | medium | low
Context_type: build | content | system | research
Agent: <gemini-cli | claude | codex | cos>
[/hermes-context]
```

### Context types

| Type | Use for |
|------|---------|
| `build` | Code, agent architecture, system config, Hermes internals |
| `content` | Posts, scripts, hooks, content pipeline decisions |
| `system` | Road4AI infrastructure, tool integrations, workflow changes |
| `research` | Findings, tool evaluations, competitor analysis |

### Session restore

At the start of any session, run:

```bash
git log --grep="CHECKPOINT:" --format="%B" -3
```

Parse the `[hermes-context]` blocks and brief Shagwu on:
- What was last completed
- What's remaining
- Any low-confidence states needing review
- Which agent last touched each context type

---

## 4. Voice and non-negotiables

This section defines how Road4AI content sounds and what is never allowed.

### Content voice

Road4AI content is written by a practitioner documenting a real journey. It is:

- **Storytelling-first.** Every post starts with a moment, a decision, or a problem, not a definition.
- **Punchy.** Short sentences. Active voice. No throat-clearing.
- **Honest.** "I tried this and it broke" is a better post than "Here are 5 tips." Share what actually happened.
- **Analogy-driven.** Abstract concepts get grounded in something physical or familiar. Agents aren't "AI systems," they're more like a team where everyone reads the same shared notebook.
- **Humorous when earned.** The joke has to come from the situation, not be forced in.
- **Learning out loud.** The audience is watching someone figure it out in real time, not watching an expert perform.

### Signature phrases (use sparingly, never force them)

- "road-tested" for things actually tried and validated
- "zero-cost" always specific, always earns it
- "the blueprint" when referring to the Road4AI system as a whole

### Hard non-negotiables

These are never negotiable, ever:

- **No em dashes.** Not for dramatic effect, not for lists, not anywhere. Use a comma, a colon, or a new sentence.
- **No jargon without translation.** If you use a technical term, the next sentence explains it plainly.
- **No corporate tone.** "Leverage," "utilize," "optimize for," "synergy", none of it.
- **No passive voice in posts.** "It was built" → "I built it."
- **No AI-sounding openers.** Never start with "In today's world," "In the realm of," "As an AI," or any variant.
- **No fabricated social proof.** Don't invent results, followers, or outcomes.
- **Human-in-the-loop before posting.** No content goes to any platform without Shagwu's explicit approval. This is not optional. This is architecture.

### Formatting rules for posts

- Hook in the first line, no build-up, no context-setting before the hook
- No more than 3-4 sentences per paragraph in social copy
- No bullet lists longer than 5 items
- End with either a question, a call to action, or a single punchy closer, not all three

---

## Quick reference

| Question | Answer |
|----------|--------|
| Can I push directly? | No. `HERMES_PUSH=true` must be set. |
| Can I post content without approval? | No. Human-in-loop always. |
| Where does captured content go? | `inbox.md`, flag it, don't act on it. |
| How do I know what's in progress? | `git log --grep="CHECKPOINT:" --format="%B" -3` |
| What's the aesthetic? | Black and emerald terminal. No corporate polish. |
| What's the core constraint? | Zero-cost stack. Don't break it. |
