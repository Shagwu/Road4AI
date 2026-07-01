# Content Dedup Gate

No entry may be written to `state/current-queue.json` until the dedup gate passes.

## Required Checks

1. Title fuzzy match: scan existing queue entries for title similarity above `0.7`.
2. Hook semantic overlap: check whether hooks share the same scenario, reveal, metaphor, or inciting moment.
3. Published lookback: scan `published` entries updated within the last 30 days for topic or system component overlap.
4. Source story dedup: confirm the source capture or roadmap item does not already have a queue entry.

## Blocking Behavior

If any check fails, stop before writing. Report:

```text
DEDUP CONFLICT DETECTED
-----------------------------------------
Check failed : [1 | 2 | 3 | 4] - [Title | Hook | Published | Source]
New entry    : {new_entry.id} - "{new_entry.title}"
Conflicts with: {existing.id} - "{existing.title}" [{existing.status}]
Reason       : [one sentence plain-language explanation]
-----------------------------------------
Action required: Operator must confirm, merge, or cancel before queue write proceeds.
```

Do not merge, rename, or reframe automatically.

## Queue Shape

`state/current-queue.json` currently stores entries under a top-level `queue` key. Agents must preserve the existing file shape unless the user explicitly approves a schema migration.

## Platform Constraints

**Blog posts are disabled.** No blog platform is configured. All content must be routed to supported platforms only:
- X (Twitter)
- LinkedIn
- Instagram
- TikTok
- Threads
- Facebook

Any queue entry with `"platform": "Blog"` must be rejected at the dedup gate. This decision was made on 2026-07-01 and is permanent until a blog platform is explicitly configured and approved by the operator.
