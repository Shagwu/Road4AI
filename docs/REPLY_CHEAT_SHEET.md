# Hermes v2.0: Reveal Day Reply Cheat Sheet

Use these high-signal replies for technical engagement on LinkedIn and X. 🔧

---

### 1. The "How it works" (General Technical)
**Context:** For users asking about the underlying stack or the bridge to CrewAI.
> **Reply:** "We're running local HNSW via SQLite for individual agent working memory, but the Hermes v2.0 substrate uses ChromaDB for distributed coordination across the swarm. The bridge logic inherits from CrewAI's `BaseKnowledgeStorage` (check `hermes/crewai_storage.py` for the implementation). This ensures every agent hits the same distributed brain without database locks."

### 2. The "Scale Wall" (Why ChromaDB?)
**Context:** For users asking why we moved away from simple local files or SQLite.
> **Reply:** "We hit the 'Scale Wall' at 5+ agents. SQLite + local HNSW is great until you have 100+ concurrent write-heavy agents hitting WAL-mode lock bottlenecks. ChromaDB provides the distributed substrate needed for swarm coordination without sacrificing retrieval speed. It’s the difference between a single-user demo and a production swarm."

### 3. The "Self-Knowledge" (Privacy/Data)
**Context:** For users asking if we're just indexing documentation or something more.
> **Reply:** "Most RAG setups index the internet. I indexed myself—specifically the Road4AI build history, architectural decisions, and git commits. The goal is 'System Meta-Awareness.' The agents don't just know 'AI'; they know exactly how *this* system was built and why. All storage remains local-first and private."

### 4. The "Governance Lock" (Safety/Control)
**Context:** For users asking about agent drift or instructions being bypassed.
> **Reply:** "That's why we revealed the 'Governance Lock.' `AGENTS.md` acts as the system constitution. It's filesystem-protected (chmod 444) and agents are strictly prohibited from mutating their own operating contracts without a manual human gate. System integrity is enforced by the architecture, not just the model's 'ethics'."

### 5. The "181ms Honesty" (Performance)
**Context:** For users asking about the latency shown in the demo.
> **Reply:** "We're hitting sub-60ms on warm queries, but the 181ms cold query in the demo is the reality of loading a distributed HNSW index from disk. Most demos hide the cold-start cost with selective editing; we’re keeping it in to show what real-world production friction looks like."

---
© 2026 Road4AI. Built, not just prompted. 🔧