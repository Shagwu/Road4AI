# Stack Migration X Thread

My primary orchestration agent shut down last week. No warning.

I had to swap the engine of a live multi-agent system while it was running.

Here is what I learned. 🧵

---

The old stack: Gemini CLI as the brain, Ollama for local inference.

The new stack: Claude Code as the brain, Ollama still doing local inference.

Same architecture. Same memory layer. Same scheduling pipeline. Different engine.

---

The hard part was not the new tool.

It was 22 files across the codebase that had a hardcoded reference to the old one.

AGENTS.md. CLAUDE.md. project.yaml. state.yaml. Five task files. Three skill definitions. Two READMEs.

---

Here is the rule I am adding to my architecture decisions:

Zero-cost means zero lock-in.

If your stack breaks when one tool disappears, it was never really yours.

---

The real test of a local-first stack is not whether it runs.

It is whether you can rip out a layer and replace it without rebuilding everything above it.

Road4AI passed that test this week.

---

If you are building with agents, write your configs like you will replace every tool eventually.

Because you will.

---

Road4AI: zero-cost, local-first, CLI-native.

The blueprint is at github.com/Shagwu/Road4AI.
