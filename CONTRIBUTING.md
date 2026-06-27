# Contributing to Road4AI

Welcome to the revolt. 🔧

Road4AI is a movement for builders who want to own their intelligence. We are building a zero-cost, local-first, CLI-native AI operator stack. By contributing, you are helping indie hackers, technical founders, and engineers break free from the SaaS tax and build high-integrity agent systems.

## 🏗️ Our Core Pillars

- **Zero-Cost First:** If it requires a subscription, it’s not for us. We prioritize local models and free-tier APIs (Claude Code + Ollama).
- **High Signal, No Fluff:** We build systems, not slogans. Every line of code and every post must deliver value.
- **Local-First Ownership:** Your data, your voice, your infrastructure.
- **Human-in-the-Loop:** Agents are collaborators, not autonomous actors. Governance is enforced by architecture.

## 🚀 Getting Started

1. **Fork and Clone:**
   ```bash
   git clone https://github.com/Shagwu/Road4AI.git
   cd Road4AI
   ```

2. **Setup Environment:**
   ```bash
   # Install Magika for repo verification
   python3 -m pip install magika
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Verify the Repo:**
   ```bash
   python3 verify_repo.py .
   ```

## 🛠️ How to Contribute

### 1. Identify a Gap
Check `plan/index.yaml`, `WORKING-CONTEXT.md`, or `state/current-queue.json` for planned tasks. We prioritize:
- Bug fixes in the Hermes memory bridge.
- New zero-cost tool integrations.
- Improvements to the Karen validation filter.
- Technical documentation and tutorials.

### 2. Follow the Engineering Standards
We maintain a strict "Plan -> Act -> Validate" lifecycle.

- **TDD (Test-Driven Development):** Always write the failing test first. A change is incomplete without verification logic.
- **The Karen Filter:** All content drafts must pass the 8-step adversarial audit (Type Safety, Architectural Alignment, Signal-to-Noise, etc.).
- **Hermes Protocol:** Use structured commit messages for cross-agent memory synchronization.

### 3. Submit a Pull Request
- Create a feature branch.
- Stage files explicitly (avoid `git add .`).
- Follow the Hermes checkpoint format in your commits.
- Ensure all tests pass.

## 📜 Commit Message Format (Hermes v2.0)

Every major change must include a `[hermes-context]` block to keep the swarm synchronized.

```text
feat(scope): short imperative description

[hermes-context]
Decisions: <what was locked in>
Remaining: <what's next>
Tried: <what failed and why>
Confidence: high | medium | low
Context_type: build | content | system | research
Agent: <name>
[/hermes-context]
```

## ⚖️ Governance & Integrity

- **AGENTS.md:** This is our constitution. Any changes to agent operating contracts require explicit human approval.
- **Voice Match:** We follow the Road4AI brand voice—authoritative but humble, storytelling-driven, and **strictly no em dashes**.

## 💬 Join the Community
For deep dives, architectural walkthroughs, and peer support, join the [Road4AI Skool Community](https://www.skool.com/road4ai).

---
© 2026 Road4AI. Built, not just prompted. 🔧