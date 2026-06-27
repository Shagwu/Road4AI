# CLAUDE.md — Road4AI

This file is read by every agent that opens this repo: Claude Code, Codex, and the Chief of Staff (CoS). Read it fully before doing anything. It is the source of truth for how to behave in this project.

---

## 1. What this project is

**Road4AI** is an open-source, zero-cost AI operator blueprint for solo builders.

It is a layered multi-agent system built on local-first, CLI-native tools. No paid APIs required to run the core stack. No bloated frameworks. The goal is to give anyone, especially women building with AI, a real, working reference for how to operate as an indie AI builder using agents that actually talk to each other.

**The operator:** Shagwu (@Shagwu on GitHub, @road4ai on Instagram). Active content creator, practitioner, and the human-in-the-loop for every output this system produces.

**The stack:**
- Claude Code — ideation, research, first-pass drafts, content strategy, long-context reasoning
- Codex — structured coding and refactoring
- Ollama — local model inference, zero-cost fallback
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
- **Approval-to-archive rule:** Once Shagwu moves a draft into `drafts/approved/`, that is the final human approval for scheduling. After Blotato scheduling is confirmed, move the draft to `drafts/archived/` immediately and update queue paths. Do not leave scheduled content in `drafts/approved/`, because visible approved files create human duplicate-approval and duplicate-posting risk.

### Architecture decisions

These are locked. Don't re-litigate them:
- Zero-cost stack is non-negotiable for the core blueprint
- Local-first, CLI-native, no cloud-only dependencies in the main path
- Multi-agent coordination via Hermes memory layer, not hardcoded handoffs
- Human-in-the-loop before any public output, this is infrastructure, not a preference
- Obsidian is a thinking/navigation layer only. Recovery flows rebuild it from Markdown and git history; Obsidian workspace state, graph position, and UI metadata are not Hermes checkpoint inputs.
- v2.1 scope does not include the Visual Memory Loop. v2.1 is the governed SkillOpt learning layer: benchmarks, allowlisted skill optimization, review gates, and proof package. Visual Memory Loop is a Phase 5+ candidate because it adds a new product surface, storage/retrieval semantics, media governance, and UX decisions that would blur the v2.1 learning-loop boundary.

### V2.1 Benchmark Proof Plan (July 2026)

**Reveal date target:** Wednesday, July 15, 2026.

**Skill under test:**
- Skill: `.agents/skills/voice-match/SKILL.md`
- Test suite: `benchmarks/social_voice/social_voice_cases.jsonl`
- Size: 15 cases: 12 tightened base cases plus 3 real June runway cases
- Rationale: `voice-match` is high-signal for the audience, already has a test suite, and is safe to improve without touching governance, queue, or publishing contracts. Benchmark the runtime skill under `.agents/skills/`, not the repo teaching copy under `skills/`.

**Execution flow:**
1. Baseline: run the current skill against the suite, recording mean score, failures, and failure types.
2. Optimization: run SkillOpt against failed cases only.
3. Review gate: inspect the proposed patch against governance and voice constraints. Do not auto-apply.
4. After score: rerun the benchmark against the improved skill, recording mean score and delta.
5. Artifacts: write `docs/benchmarks/voice-match-skillopt-july-2026.md`, raw outputs under `reports/skillopt/social_voice/`, and the accepted skill-improvement commit hash only after approval.

**Stability proof execution:**
- Executor: Codex or Claude may run the June 24-25 stability task.
- Runner engine: the current benchmark runner uses Claude Code for target generation and evaluator scoring.
- Required artifacts: `reports/skillopt/social_voice/stability-test-june-2026.md` and `reports/skillopt/social_voice/stability-runs.json`.
- Pass condition: repeated baseline-only live scoring runs must keep mean score within +/-5%, failed case overlap above 80%, and stable standard deviation.
- If the stability proof needs an alternative scoring backend, add that backend explicitly before the July benchmark cycle instead of treating Codex execution as a different model engine.

**Evaluation engine:**
- Platform: Claude Code + Ollama (local, zero-cost).
- Rate limit: none (local inference).
- Risk level: low for baseline-only stability runs, medium for full optimization runs until measured. A baseline-only run over 15 cases uses roughly 30 LLM calls. A full live runner pass can use roughly 61 LLM calls when failures trigger optimization and after-score evaluation.
- Reveal transparency: state that `voice-match` was scored with Claude Code + Ollama judgment, not hosted API models.

**June 24-25 stability playbook:**
- Run 1: June 24 morning. Use `--baseline-only`. Record timestamp, exact command, Claude Code version, Ollama model version, environment notes, mean score, standard deviation, and failed case IDs.
- Run 2: June 25 morning. Use the same command, skill, benchmark, and environment. Record the same fields.
- Save raw data from each run's `--usage-output` into `reports/skillopt/social_voice/stability-runs.json`.
- Baseline-only command template:

```bash
python3 tools/run_skillopt_benchmark.py \
  --skill-path .agents/skills/voice-match/SKILL.md \
  --cases-path benchmarks/social_voice/social_voice_cases.jsonl \
  --output reports/skillopt/social_voice/stability-run-1.md \
  --usage-output reports/skillopt/social_voice/stability-run-1-usage.json \
  --baseline-only
```

- Record each run:

```bash
python3 tools/record_stability_run.py \
  --usage-report reports/skillopt/social_voice/stability-run-1-usage.json \
  --stability-runs reports/skillopt/social_voice/stability-runs.json \
  --run-label run_1 \
  --executor codex \
  --command "python3 tools/run_skillopt_benchmark.py --skill-path .agents/skills/voice-match/SKILL.md --cases-path benchmarks/social_voice/social_voice_cases.jsonl --output reports/skillopt/social_voice/stability-run-1.md --usage-output reports/skillopt/social_voice/stability-run-1-usage.json --baseline-only" \
  --environment-notes "June 24 morning stability run"
```

- Write a 2-3 sentence summary to `reports/skillopt/social_voice/stability-test-june-2026.md`.
- Validation: mean score variance within +/-5% is acceptable. Greater than +/-10% requires investigation. Failed case overlap above 80% passes. Between 60-80% requires review. Below 60% is a signal to debug before July 1.
- Pass means ready for SkillOpt optimization. Fail means debug the runner before the July benchmark cycle.

**Timeline:**
- Budget: 1 week nominal, plus 2-3 day buffer for runner or benchmark cleanup.
- Start: July 1, 2026, after June runway posts land.
- Complete: July 8, 2026, leaving one week for reveal draft and Karen gate before July 15.

**Risk mitigation:**
- Runner stability: before July 1, validate that the runner produces consistent scores on `voice-match`.
- Benchmark quality: review the current 12 cases for breadth and flag cases that are too vague.
- Overclaiming guard: reveal language must say "`voice-match` improved X%" rather than "Hermes got smarter."
- Governance review: self-review against `docs/plans/HERMES_V2_1_SKILLOPT_GOVERNANCE.md` before Karen.

**Pre-reveal checklist:**
- [ ] Dry-run runner on `voice-match` by June 24-25.
- [ ] Review benchmark cases for quality by June 25-26.
- [ ] Execute benchmark cycle July 1-8.
- [ ] Draft reveal with actual numbers July 8-12.
- [ ] Karen gate review July 12-14.
- [ ] Final polish and publish July 15.

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
Agent: <claude | codex | cos>
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
- Never run `/caveman-compress` on any Road4AI file without explicit operator approval and a manual backup first.
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
