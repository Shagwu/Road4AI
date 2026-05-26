# Announcement: The Road4AI Ecosystem Shift

**"The bridge is open. Now, build with it."** 🔧

Today marks a fundamental pivot in the Road4AI architecture. We are moving from a single-repo "builder" model to a modular "ecosystem" model.

## 🏗️ From Internal Tool to Standalone Plugin

Until now, **Hermes v2.0**—the distributed memory layer that powers our 100+ agent swarms—was an internal component. It was the "secret sauce" for our zero-cost stack.

As of today, we have extracted Hermes into its own standalone Python package: `road4ai-hermes`.

### Why this matters:
1. **Democratization:** You no longer need to clone the entire Road4AI repo to use our memory substrate. You can now `pip install road4ai-hermes` into any agentic project.
2. **Modular Integrity:** By separating the memory layer from the orchestration layer, we ensure that both can evolve independently without breaking your local workflows.
3. **Open Collaboration:** This shift lowers the barrier for contributors. You can now help us harden the memory layer or build new adapters for different agent frameworks (Autogen, LangChain, etc.) in a focused package.

## 🚀 How to Participate

- **Use the Plugin:** Install `road4ai-hermes` and drop a distributed, ChromaDB-backed brain into your own swarm.
- **Read the Guide:** Our new `CONTRIBUTING.md` is live. We have identified specific gaps in the memory substrate and Gemini CLI that we need your help to close.
- **Join the Community:** We are hosting a technical deep-dive on the extraction and the new modular roadmap in the [Skool Community](https://www.skool.com/road4ai).

## 🔧 What's Next?

The "Ecosystem Shift" isn't just a rename; it’s a commitment to building infrastructure for the autonomous era that is **owned by the people who use it.**

Modular. Local-first. Zero-cost. Forever.

---
© 2026 Road4AI. Built, not just prompted. 🔧
