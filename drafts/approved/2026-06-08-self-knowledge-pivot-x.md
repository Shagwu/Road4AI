# X Thread Draft: The Self-Knowledge Pivot

**Source:** drafts/ready/2026-06-08-self-knowledge-pivot-li.md
**Platform:** X
**Type:** Struggle
**Goal:** Build in public
**Target schedule:** 2026-06-08
**Status:** Ready for human review

---

1/ I just deleted 10,000 chunks of high-quality RAG data.

To be honest, I thought I was making my agent smarter.

I was actually teaching it to drown.

2/ Everyone tells you to index more data.

More docs.
More transcripts.
More repos.
More context.

So I did the obvious thing. I fed Hermes a giant external knowledge base and expected it to become useful.

It got louder.

Not smarter.

3/ On paper, it looked impressive:

10,000 chunks indexed.
HNSW search working.
Facts coming back from a pile of technical material.

Can you believe it still felt wrong?

Retrieval worked.

Usefulness did not.

4/ The agent knew too much about other people's systems and not enough about mine.

It could explain a framework pattern.

It could not reliably explain why I made a decision three weeks ago.

That is not memory.

That is a search box with confidence.

5/ The ugly part:

I had built a very efficient noise machine.

The first query came back at 181ms cold.

I wanted a sub-100ms benchmark.

But latency was not the real failure.

The real failure was 10,000 chunks of context and no understanding of the build.

6/ It did not understand:

The roadmap.
The tradeoffs.
Why Hermes exists.
The commits.
The checkpoints.
The "we tried this and it broke" moments.

That is when the RAG story cracked.

More data does not make an agent better.

Better memory does.

7/ So I stopped indexing the internet.

I started indexing the build history.

Git commits.
Hermes checkpoints.
Architecture notes.
Working context.
The decisions I made while tired, blocked, annoyed, or halfway through ripping something out.

8/ The index got smaller.

About 200 high-signal chunks instead of 10,000 generic ones.

And the agent finally started sounding less like a search box and more like a collaborator who had been in the room.

This is the self-knowledge pivot.

9/ This is shaping v2.1.

Not more memory.

Better skills.

Skills that know what matters, what expires, what needs a human gate, and what should never be optimized just because the model feels confident.

10/ I wish someone told me this before I built the first version:

Your agent does not need to know everything.

It needs to know what you learned the hard way.

Memory without governance becomes a hoard.

And I have already built the hoard once.
