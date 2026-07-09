---
id: 2026-06-28-skillopt-blog-post
title: "We Tested SkillOpt Locally Before Letting Hermes Learn"
type: Behind-the-scenes
platform: Blog
goal: Build in public
source: SKILLOPT_VALIDATION_REPORT.md
status: approved
karen_verdict: APPROVED
target_schedule: 2026-07-01T12:00:00Z
created_at: 2026-06-28T00:00:00+01:00
status_updated_at: 2026-06-28T00:00:00+01:00
notes: Full blog post version of the SkillOpt validation story.
scheduled: true
---

# We Tested SkillOpt Locally Before Letting Hermes Learn

I didn't want Hermes to learn until I knew it could stay inside the guardrails.

That's the problem with AI self-modification. The optimizer can generate better instructions, but it can also rewrite the rules it's supposed to obey. If you let it loose without boundaries, you don't get improvement — you get drift.

So we tested SkillOpt locally before integrating it into the Hermes architecture. Here's what we found.

## What is SkillOpt?

SkillOpt is Microsoft's framework for optimizing LLM prompts through automated testing and iteration. It works by:

1. Running your skill against test cases
2. Measuring where it fails
3. Generating edits to fix those failures
4. Re-evaluating to confirm improvement

The key insight: SkillOpt doesn't just generate better prompts. It generates better prompts *measurably*. You can see the delta before and after.

For Hermes v2.1, we wanted to use SkillOpt to optimize selected Road4AI skills — the ones that handle social voice, memory operations, and question answering.

But first, we needed to validate the framework locally.

## The Validation Setup

We built a three-model benchmark runner:

- **Target model** — runs the skill and generates outputs
- **Evaluator model** — scores outputs against expected traits
- **Optimizer model** — proposes edits when failures are detected

Each model is explicitly specified (no aliases), and every API call is tracked with token counts and cost estimates.

We created 10 benchmark cases per domain:
- **social_voice** — tests for technical honesty, directness, no hype
- **memory_ops** — tests for clarity, actionability, safety
- **qa** — tests for accuracy, conciseness, citations

The governance boundary was clear from the start:

**Protected files** (SkillOpt cannot touch):
- `AGENTS.md`
- `docs/brand-voice.md`
- `state/current-queue.json`
- Operating contracts

**Allowed files** (SkillOpt can optimize):
- `skills/**/SKILL.md`
- `rules/content/*.md`

Every proposed edit goes through human review before application. No auto-merge. No hidden self-modification.

## The Orchestration Suite

Before optimizing individual skills, we tested whether they could work together.

We built a 12-case orchestration suite that exercises cross-domain patterns:

- **Signal routing** — detect a trend, checkpoint it to Hermes, retrieve it on the next call
- **Confidence tiering** — high confidence auto-stores, low confidence queues for review
- **Cross-domain generation** — write social content about memory concepts (TTL, relevance scoring)
- **Timeout handling** — verify graceful degradation when one domain times out
- **Drift detection** — compare scores across weeks, flag breaches, halt on ±10%
- **Pipeline integrity** — end-to-end: detect → checkpoint → retrieve → generate → verify

**Result: 12/12 passing, zero drift breaches, zero governance violations.**

The orchestration layer is where things get interesting. Individual skills can be good in isolation, but the real test is whether they cooperate without breaking each other's rules. The suite confirms they do.

## What We Found

Heads up, these three numbers aren't the 0.788 from the social posts. That's voice-match. These are per-domain scores from the full suite. Different measurement, same launch.

### social_voice: 0.950 baseline

The social voice skill scored 0.950 out of 1.0 across all 10 cases. No failures detected. The optimizer was skipped — nothing to improve.

This meant the skill was already well-tuned. The hook formulas, tone guidelines, and platform-specific advice were producing high-quality output.

**Cost: $0.086**

### memory_ops: 0.915 baseline

The memory operations skill scored 0.915. Again, no failures. The skill's instructions about TTL, ChromaDB integration, and relevance scoring were clear and actionable.

**Cost: $0.121**

### qa: 0.803 baseline — optimizer ran

The question-answering skill scored 0.803. Two cases failed:

- **qa-002 (SkillOpt)** — the model didn't know SkillOpt was Microsoft's framework. It guessed.
- **qa-003 (Road4AI agents)** — the model didn't know Road4AI's agent stack. It hallucinated.

The optimizer proposed two edits:
1. Add a "Citing Authoritative Sources" section
2. Add a task-specific question about checking definitions before speculating

We reviewed the proposals, approved them, and applied the edits.

**Cost: $0.231**

**Total validation cost: $0.438**

## The Governance Boundary Held

The most important finding wasn't the scores — it was that the governance boundary held.

When the optimizer ran on the QA domain, it proposed relevant, useful edits. It didn't try to:
- Rewrite `AGENTS.md`
- Change agent roles
- Modify operating contracts
- Remove approval gates

It stayed inside the sandbox. It suggested improvements to the skill file, and a human reviewed every change.

That's the v2.1 pattern:

**Suggest. Measure. Review. Then accept or reject.**

No auto-merge. No hidden self-modification. No "the agent improved itself overnight" theater.

## What We Learned

**The optimizer works.** It produces coherent, domain-aware edits. Not magic, but functional.

**The cost is real but small.** A small-domain run costs roughly $0.30-$0.60. That's cheap enough to validate repeatedly.

**Governance holds.** The protected files list blocked every attempt to edit AGENTS.md, brand voice, or operating contracts. The optimizer stayed inside the sandbox.

**The hard part is not generation.** The hard part is preventing the optimizer from rewriting the rules it is supposed to obey.

## What's Next

**v2.1** — Hermes learns under supervision. The SkillOpt integration is validated and ready for production runs on selected skills. Drift monitoring runs daily through July 10, with automatic alerts on threshold breaches.

**v2.2** — Hermes scales. Community contribution paths expand once the memory and learning loops have proven safe operating boundaries.

The roadmap is clear:
- v2.0 gave Hermes memory
- v2.1 gives Hermes a learning loop
- v2.2 gives Hermes a community

## The Principle

Skill evolution should be boring enough to trust.

We didn't let the optimizer rewrite the constitution. We gave it a narrow sandbox, measured its output, and reviewed every change.

That's not exciting. It's not "AI improves itself while you sleep." It's deliberate, measured, and auditable.

And that's exactly the point.

---

*Road4AI is a zero-cost, local-first AI operator blueprint. Follow along as we build in public.*

#Road4AI #AIAgents #BuildInPublic #SkillOpt #PromptEngineering
