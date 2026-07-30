---
title: "The Guardrail That Gave Wrong Answers"
hook: "My ratio script was returning 2/10. The real number was 3/10. The guardrail was wrong and nobody noticed."
type: Struggle
platform: LinkedIn
goal: Build in public
status: ready_for_publishing
karen_verdict: APPROVED
scheduled: true
---

My ratio script was returning 2/10. The real number was 3/10. The guardrail was wrong and nobody noticed.

The script sorted queue entries by array position instead of by post date. As the queue grew, older entries drifted out of the "recent" window by insertion order, not by when they were actually scheduled. A post that went live two days ago was counted as older than one scheduled for next week, just because it was added to the JSON array first.

The ratio still looked plausible at 2/10. That's what made it dangerous. If it had returned 0/10, someone would have flagged it immediately. But 2/10 is close enough to the 25% threshold that it looked like a tight-but-passing grade instead of a miscount.

Found it by doing the date math by hand for an unrelated scheduling decision. Traced the trailing-10 manually, got a different number than the script, and spent four messages figuring out which one was wrong.

The script was. Fixed it to sort by scheduled_time instead of array index. The ratio jumped to 3/10.

The part that sticks with me: the guardrail existed, was running, was returning answers, and was wrong about the one number it was built to protect. Not because the logic was bad, but because the input ordering was. A guardrail that silently gives you the wrong answer is worse than no guardrail at all, because you trust it.
