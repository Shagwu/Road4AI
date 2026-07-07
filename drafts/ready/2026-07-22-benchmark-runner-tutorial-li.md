---
platform: li
status: ready_for_edit
type: Tutorial
goal: Teach
karen_verdict: PENDING
---

# How the Benchmark Runner Works (LinkedIn)

After the v2.1 reveal, a few people asked: how does the benchmark actually score a skill?

The short version: `run_skillopt_benchmark.py` takes a SKILL.md file and a test suite (10 social voice cases), runs the skill against each case, then scores the output on two axes.

First, expected traits. Each case defines what the output should have: conspiratorial tone, punchy hooks, technical honesty, no marketing hype. The scorer checks whether those traits appear in the generated output.

Second, reject traits. Each case also defines what must never appear: em dashes, "game-changer," "In today's fast-paced world," "thrilled to share." If any reject trait shows up, the score drops.

The runner also enforces a governance boundary. It only touches files in an allowlist (SKILL.md files in specific directories). If you point it at AGENTS.md or state files, it rejects the request and flags a security violation.

Every optimization must pass this benchmark before a human reviews it. No auto-apply. No silent edits. The runner halts, writes a patch proposal, and waits.

This is what "skills evolve" looks like when you add guardrails. Not vague promises. A test suite, a scorer, and a human gate.

---

## Links to Include

In the first comment:

Benchmark Runner:
https://github.com/Shagwu/Road4AI/blob/main/tools/run_skillopt_benchmark.py

Voice-Match Skill:
https://github.com/Shagwu/Road4AI/blob/main/.agents/skills/voice-match/SKILL.md

Social Voice Benchmark:
https://github.com/Shagwu/Road4AI/blob/main/benchmarks/social_voice/social_voice_cases.jsonl

---

## Publication Instructions

**Platform:** LinkedIn
**Time:** July 22, 09:00 WAT (10:00 UTC)
**Format:** Single post with comment links
**Engagement:** Pin to profile for 48 hours
