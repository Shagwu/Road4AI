# Terminal Reveal Script: Road4AI Self-Knowledge (May 26)

**Narration Anchor:** 
"Most people build RAG on someone else's data. I built mine on my voice — so even if the model has no integrity, the system does."

---

## The Demo Flow (No Cuts)

### [PROMPT 1: The Code Meta-Awareness]
**Command:** `ask "How does the HermesStorage class bridge CrewAI's knowledge system with our internal memory layer?"`

**Terminal Output:**
```text
ROAD4AI SELF-KNOWLEDGE SYSTEM [ONLINE]
--------------------------------------
> QUERY: How does the HermesStorage class bridge CrewAI's knowledge system...
> LATENCY: 54ms
> SOURCE: hermes/crewai_storage.py | CATEGORY: implementation

HermesStorage is the integration bridge. It inherits from CrewAI's BaseKnowledgeStorage 
and wraps our MemoryBridgeV2 (ChromaDB). It maps the 'save' and 'search' methods 
directly to the Road4AI substrate, ensuring that every agent in the swarm 
persists context to the same distributed brain.
```

### [PROMPT 2: The Architectural Intent]
**Command:** `ask "Why did we move from local HNSW to a distributed ChromaDB substrate for Hermes v2.0?"`

**Terminal Output:**
```text
ROAD4AI SELF-KNOWLEDGE SYSTEM [ONLINE]
--------------------------------------
> QUERY: Why did we move from local HNSW to a distributed ChromaDB substrate...
> LATENCY: 58ms
> SOURCE: docs/plans/2026-05-01-hermes-v2-distributed-vector-layer.md | CATEGORY: plan

We migrated to solve the 'Scale Wall.' While SQLite + local HNSW worked for 5 agents, 
it hit a WAL-mode lock bottleneck at 100+ concurrent write-heavy agents. ChromaDB 
provides the distributed substrate needed for swarm-scale coordination without 
sacrificing retrieval speed.
```

### [PROMPT 3: The Governance Guardrail]
**Command:** `ask "What is the 'Governance Lock' on AGENTS.md and how does it prevent agent-to-agent negotiation?"`

**Terminal Output:**
```text
ROAD4AI SELF-KNOWLEDGE SYSTEM [ONLINE]
--------------------------------------
> QUERY: What is the 'Governance Lock' on AGENTS.md...
> LATENCY: 48ms
> SOURCE: AGENTS.md | CATEGORY: governance

The Governance Lock is the system's 'Manual Approval Gate.' It establishes 
AGENTS.md as a protected constitution. It explicitly prohibits agents from 
negotiating or mutating their own operating contracts without a per-session 
human confirmation, preventing autonomous drift in system-wide rules.
```

---

## Capture Aesthetic (The Brand)
- **Theme**: Dark Mode (Obsidian/High-Contrast).
- **Font**: JetBrains Mono or Fira Code.
- **Colors**: Background #0D1117 (Dark Blue/Black), Text #50C878 (Emerald Green).
- **Chrome**: Clean terminal (no zsh themes, no plugins). Just the prompt and the signal.

## Technical Verification (No-Fake Zone)
1. **Reset**: Clear warm cache before first take (`rm -rf ~/.cache/huggingface` - optional, but be honest about cold load).
2. **Timing**: Ensure the `ask` script's internal timer is accurate (`time.time()` around the encode/search block).
3. **Environment**: Use a clean repo state (no uncommitted files, no staged hacks).

