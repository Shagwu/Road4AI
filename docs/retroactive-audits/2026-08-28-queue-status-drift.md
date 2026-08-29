# Retroactive Audit Entry: Queue Status Drift (Recurrence)

**Date:** 2026-08-28
**Related gap:** Recurrence of the Aug 7-9 queue/Blotato sync drift (21 entries stuck at `scheduled`, resolved in commit `db20f8f`)
**Status:** 6 entries reconciled to `published`. 16 entries tagged `stuck-in-progress`, unresolved at Blotato's end.

## What happened

Routine status check on `state/current-queue.json` found 22 entries with `status: "scheduled"` whose `scheduled_time` values were all in the past (Jul 17 - Aug 9), while today's date is Aug 28. This is the same failure shape as the Aug 7-9 sync gap: `schedule_post.py`'s `sync_queue_status()` did not update the queue's status field to reflect what actually happened at Blotato.

## How it was caught

Manual queue audit prompted by a status-update review, not an automated gate. `check_publish_drift.py` (wired into `verify_content.py` after the Aug 7-9 fix) did not catch this batch — worth checking whether it's actually running, or running against the right field.

## Verification

Looked up all 22 `blotato_id`s directly via `blotato_get_post_status`:

- **6 confirmed published** (had real `publicUrl`s returned) — reconciled to `status: "published"` in the queue.
- **16 returned `in-progress`** — per Blotato's own tool semantics, this status means the original `blotato_create_post` call timed out and never got a definitive published/scheduled/failed confirmation. For submissions from 3-7 weeks ago, indefinite `in-progress` is itself an anomaly, not a transient state.
- **0 returned `failed`.**

## The gap

Two separate issues, same root cause (queue status not reflecting Blotato ground truth):
1. The 6 published-but-unmarked entries are a plain sync miss — the same bug class as Aug 7-9, recurring after the fix.
1. The 16 `in-progress` entries are unresolved at the source. Either the original `blotato_create_post` calls never got a callback, or `blotato_get_post_status` has a gap for older submissions. This needs investigation at the Blotato integration layer, not just a queue-side fix.

## Fix / follow-up

- 6 reconciled entries appended to `published-log.json`-equivalent status (`published` in queue).
- 16 unresolved entries tagged `stuck-in-progress` (a new explicit status, not `scheduled` or `archived`) with a note pointing to this audit, so they stop surfacing under normal `scheduled`-status queries without being silently hidden.
- Open question for next session: why did `check_publish_drift.py` not flag this batch? Worth re-running it manually against current queue state to see if it reproduces the miss.
- Open question: are the 16 `in-progress` posts actually stuck, or is this a `blotato_get_post_status` limitation for submissions past some age threshold? Worth one direct check with Blotato support or docs before assuming queue-side blame.
