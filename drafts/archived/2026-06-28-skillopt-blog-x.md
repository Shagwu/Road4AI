---
id: 2026-06-28-skillopt-blog-x
title: "We Tested SkillOpt Locally (Thread)"
type: Behind-the-scenes
platform: X
goal: Build in public
source: SKILLOPT_VALIDATION_REPORT.md
status: approved
karen_verdict: APPROVED
target_schedule: 2026-06-30T18:00:00Z
created_at: 2026-06-28T00:00:00+01:00
status_updated_at: 2026-06-28T00:00:00+01:00
notes: Twitter/X thread version of the SkillOpt validation blog post.
scheduled: true
---

# Twitter/X Thread: We Tested SkillOpt Locally

**Post 1/8:**
I didn't want Hermes to learn until I knew it could stay inside the guardrails.

So we tested SkillOpt locally before integrating it.

Here's what we found:

**Post 2/8:**
What is SkillOpt?

Microsoft's framework for optimizing LLM prompts through automated testing.

It runs your skill against test cases, measures failures, generates fixes, then re-evaluates.

Key: it doesn't just generate better prompts. It generates them measurably.

**Post 3/8:**
The validation setup:

Three models:
- Target: runs the skill
- Evaluator: scores outputs
- Optimizer: proposes fixes

10 cases per domain. 3 domains. Every API call tracked.

Governance: protected files blocked from optimization.

**Post 4/8:**
Results:

social_voice: 0.950/1.0
- No failures. Optimizer skipped.
- The skill was already strong.

memory_ops: 0.915/1.0
- No failures. Same story.

Cost: $0.207 for both.

**Post 5/8:**
qa: 0.803/1.0

Two failures:
- Model didn't know SkillOpt = Microsoft's framework
- Model didn't know Road4AI's agent stack

The optimizer proposed citation instructions.

We reviewed, approved, applied.

**Post 6/8:**
Total cost: $0.438

The governance boundary held. Protected files untouched. Human review gate worked.

No auto-merge. No hidden self-modification.

**Post 7/8:**
What we learned:

1. The optimizer works — coherent, domain-aware edits
2. Cost is real but small — $0.30-$0.60 per run
3. Governance holds — sandbox enforced
4. The hard part is trust, not generation

**Post 8/8:**
The v2.1 pattern:

Suggest. Measure. Review. Accept or reject.

Skill evolution should be boring enough to trust.

Full writeup: [link to blog post]

#Road4AI #AIAgents #BuildInPublic
