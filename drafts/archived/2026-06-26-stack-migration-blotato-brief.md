---
karen_verdict: APPROVED (after audit)
status: approved
platform: linkedin
---

# Blotato Scheduling Brief

## Post Content (LinkedIn)

I just swapped out the engine of a live multi-agent system while it was running.

Not a refactor. Not a side project. The actual production stack that writes, schedules, and publishes Road4AI content across four platforms.

Here is what happened: my primary orchestration agent shut down. No warning, no migration path, no "we are sunsetting this feature" email. Just gone.

And I had two choices. Panic. Or treat it like any other engineering problem.

I chose the second one.

The old stack was Gemini CLI as the brain, with Ollama as a local fallback. The new stack is Claude Code as the brain, with Ollama still doing local inference. Same architecture. Same Hermes memory layer. Same Blotato scheduling pipeline. Different engine under the hood.

The part nobody tells you about migrating agent stacks: it is not about the new tool. It is about every reference, every config file, every workflow prompt, every governance rule that assumed the old tool was permanent.

I updated 22 files across the codebase. AGENTS.md, CLAUDE.md, project.yaml, state.yaml, five task files, three skill definitions, two README files, tool docs, marketing context. Every single one had a reference to the old engine hiding in a line I wrote months ago.

The lesson: your stack is only as resilient as the number of places you hardcoded a dependency name.

Zero-cost means zero lock-in. That was always the philosophy. This week I had to prove it.

---

Road4AI is the zero-cost, local-first AI operator blueprint.
If your agent stack breaks when one tool disappears, it was never really yours.

## Image Prompt (for Blotato image generation)

A clean before/after architecture diagram on a black background. Left side labeled "BEFORE" shows a vertical stack of four boxes connected by lines: "Gemini CLI (brain)" at top, "Ollama (fallback)" below it, "Hermes v2.0 (memory)" below that, and "Blotato (distribution)" at bottom. Right side labeled "AFTER" shows the same stack but the top box now reads "Claude Code (brain)" while the other three stay identical. Emerald green (#10B981) box outlines, white monospace text, dark background. Caption at bottom: "Same architecture. Different engine." Small text: "Zero-cost means zero lock-in. | Road4AI"

## Blotato Config

- Account ID: 2383 (LinkedIn)
- Platform: LinkedIn
- Queue ID: 2026-06-26-stack-migration-li
