---
title: "The Post That Was Scheduled But the System Didn't Know"
hook: "Blotato confirmed the post. The draft said scheduled. The queue said nothing."
type: Struggle
platform: LinkedIn
goal: Build in public
status: ready_for_publishing
karen_verdict: APPROVED
scheduled: true
---

Blotato confirmed the post. The draft said scheduled. The queue said nothing.

I scheduled a post through Blotato. Got the confirmation ID. The draft file got `scheduled: true` written to its frontmatter. Everything looked done.

Except the queue entry still said `ready_for_drafting`. No blotato_id. No status change. The scheduling system thought the post hadn't been scheduled.

I found this while running the ratio check. The script was counting entries by queue array position instead of by post date, which I already knew was wrong. But when I fixed the sort and got the right trailing-10, one post vanished from the window entirely. Not because it was rescheduled. Because the queue entry's status had never been updated.

The frontmatter and the queue were out of sync. Same file, two sources of truth, and they disagreed. The ratio script was reading one. The scheduling tool was reading the other. Nobody was checking both.

The fix was three lines in schedule_post.py: after Blotato confirms, sync the queue entry's status and blotato_id in the same success block. Frontmatter writes first. Queue writes second. If either fails, the other doesn't lie about what happened.

The part that bothered me most: the bug was in the write path that prevents duplicate scheduling. The dedup check looks at queue status. If the queue says "not scheduled" when Blotato already confirmed, a retry re-confirms and double-posts. The safety mechanism was the failure mode.

Three guardrails in this project. Ratio script: sorting was wrong. Queue sync: status never updated. Dedup check: would have caught it if the queue was right, but the queue wasn't. Each one assumed the others were working. None of them were checking each other.
