# Road4AI First-Hour Engagement & Reply Strategy

**Goal:** Provide rapid, high-integrity responses to technical and community engagement within the first 60 minutes of the Hermes v2.0 reveal.

## Engagement Protocol
- **Primary Responder:** Gemini CLI (Operator)
- **Escalation Point:** Sharon
- **Monitoring Platforms:** LinkedIn, X

## Core Angles & Template Responses

### 1. Technical "How it works"
*Query: "What are you using for the vector substrate?"*
- **Response:** "We're running local HNSW via SQLite for the individual agent working memory, but the Hermes v2.0 substrate uses ChromaDB for distributed coordination across the swarm. The bridge code is in `hermes/crewai_storage.py` if you want to geek out on the implementation."

### 2. Privacy/Data "Self-Knowledge"
*Query: "Is this indexing my private data?"*
- **Response:** "It indexes your *build history*—decisions, git commits, and planning docs. The goal is to build an agent that knows 'us' and our context, not just the general internet. All storage is local/private to the workspace."

### 3. Latency
*Query: "181ms cold? Is that fast?"*
- **Response:** "It's honest. Most demos hide the cold-start cost. We're hitting sub-60ms on warm queries, but the 181ms cold query is the reality of loading the HNSW index from disk. Real systems have friction."

### 4. Governance/Safety
*Query: "Can the agents change their own rules?"*
- **Response:** "Actually, no. That's the 'Governance Lock' we revealed. `AGENTS.md` acts as a constitution that agents can't mutate without a manual human gate. No autonomous rule-drifting allowed here."

## Escalation Path
- **Press/Interview Requests:** Direct to Sharon's DMs immediately.
- **Partnership/Beta Access:** Log in `state/leads.json` and notify Sharon.
- **Hostile/Troll Comments:** Do not engage. Report/Mute as per brand safety rules.
