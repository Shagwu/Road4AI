# Post: The Struggle of Scale (Hermes v2.0 Transition)

**Platform:** X (Twitter) / LinkedIn
**Type:** Struggle
**Goal:** Build in public / Nurture

**Hook:** Local HNSW is a lie once you hit 100+ agents. I thought I had the memory substrate solved until I tried to scale the swarm.

---

## The Content

I’ve been preaching the "Shared Brain" for weeks. SQLite + local HNSW worked perfectly for 5 agents. It was fast, simple, and zero-cost.

Then I pushed it to 100 concurrent agents.

The "Shared Memory Substrate" turned into a massive bottleneck.
- SQLite WAL mode cannot handle 100+ concurrent write-heavy agents without significant lock contention.
- Incremental HNSW indexing in a local file-backed store leads to severe graph fragmentation at high churn.
- Memory overhead for the shared HNSW index began competing with the agent runtimes themselves.

The reality? Demo-tier architecture doesn't survive contact with production workloads.

We’re currently mid-migration to a distributed vector layer. It’s painful. We’re losing the "zero-config" simplicity I loved, but gaining the ability to run a swarm that doesn't choke on its own state.

The lesson: Don't optimize for scale you don't have yet. But don't lie to yourself that a local file is a "database" once the agent count hits triple digits.

Hermes v2.0 isn't just a version bump. It's an admission that we outgrew our own infrastructure.

---

## Metadata
- **Voice Check:** Zero em dashes. No "AI-sounding" intros. High signal.
- **Visual Suggestion:** Terminal screenshot showing "database is locked" or memory consumption metrics.
- **CTA:** Are you building for 5 agents or 500? Let's talk about the scaling wall in the comments.
- **Tags:** #AI #Engineering #Hermes #VectorDB #BuildInPublic
