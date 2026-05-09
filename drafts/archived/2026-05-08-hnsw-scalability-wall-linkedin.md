Local HNSW hit a wall at 100+ agents.

I didn't read about this in a paper.
I watched it happen in production.

Here's what the crash looked like:

↳ Query latency climbed from ~12ms to 400ms+
↳ Index rebuilds started locking the process
↳ Memory pressure spiked on every new agent registration
↳ The system that felt elegant at 20 agents became a liability at 120

The problem isn't HNSW. The algorithm is fine.

The problem is what "local-first" actually means at scale — it means you own the ceiling too.

At demo scale, local vector memory is a superpower.
No API keys. No recurring costs. No external dependencies.
It's fast, it's clean, it's yours.

But HNSW builds its index in RAM.
Every new agent registration mutates that index.
And at 100+ agents doing concurrent reads and writes, you don't have a memory system anymore. You have a contention problem.

We're not announcing a fix today.

We're documenting the crash before we ship the solution — because that's the part everyone skips.

Most "AI engineers" share the win. They skip the 3am moment when the thing they built stops working at the exact scale they were trying to reach.

This is that moment.

If you're building local-first multi-agent memory and you haven't hit this ceiling yet — you will. The question is whether you're surprised or prepared.

---

What we're exploring next: distributed HNSW sharding vs. a hybrid local/remote index strategy. Neither is clean. I'll share the tradeoffs when we have real data.

The sequence from local-first to distributed starts here.

#BuildingInPublic #AIEngineering #MultiAgentSystems #LocalFirst #VectorSearch
