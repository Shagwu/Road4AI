---
id: 2026-06-12-indexing-the-builder-x
title: Indexing the Builder
type: Technical
platform: X
goal: Build in public
target_schedule: 2026-06-12
source: tools/index_self.py; drafts/archived/2026-06-08-self-knowledge-pivot-li.md; docs/tool-docs/HERMES_V2.md
status: approved
created_at: 2026-06-06T00:00:00+01:00
status_updated_at: 2026-06-06T00:00:00+01:00
notes: Approved for scheduling.
---

# X Thread Draft: Indexing the Builder

1/ Stop indexing documentation.

Start indexing yourself.

That sounds like a slogan, but it is the biggest change I made to Hermes after the self-knowledge pivot.

The useful context was not in more docs.

It was in the build history.

2/ The first version looked impressive:

10,000 chunks indexed.
External material everywhere.
Semantic search working.

And the agent still could not explain why I made a decision three weeks ago.

That is when I realized the index was pointed at the wrong world.

3/ Most RAG systems optimize for coverage.

I needed memory.

Coverage asks:

"Can the system retrieve the fact?"

Memory asks:

"Can the system explain why this project is shaped this way?"

4/ So I rebuilt ingestion around four signal types:

1. governance
2. plans
3. implementation signals
4. temporal history

Not everything in the repo.

Only the parts that help an agent understand the build.

5/ The proof layer comes first:

- `AGENTS.md`
- roadmap files
- planning docs
- manifesto-level context

This tells Hermes what the system is allowed to do, what it is trying to become, and which boundaries should not be optimized away.

6/ Then the implementation layer:

- core Hermes code
- orchestration code
- class definitions
- function definitions
- docstrings

Not full source dumps.

Just code-as-docs signal.

The goal is shape, not token landfill.

7/ Then the temporal layer:

- recent Hermes checkpoints
- git commits tagged with `[hermes-context]`
- published history
- decisions recorded during actual work

This is where the "why" lives.

Not in the polished docs.

In the scars.

8/ The indexing rule is simple:

Do not ask "can this be embedded?"

Ask "will this help a future agent resume the work correctly?"

That one question deletes most of the junk.

9/ The chunking changed too.

For governance and plans:

- split by markdown sections
- split oversized sections by paragraph
- keep source/category metadata attached

For code:

- extract docstrings
- extract class and function signatures
- skip tests and init files

10/ Every stored chunk gets context in the text itself:

`SOURCE: ... | CATEGORY: ...`

That is not decoration.

It lets retrieval return an answer with provenance baked in.

Hermes should not just give an answer.

It should say where the memory came from.

11/ The practical pattern:

Start with governance.
Add plans.
Extract code structure, not every line.
Index checkpoints and commit messages.
Store source/category metadata.
Query for decisions, not just facts.

Index the builder, not just the build.
