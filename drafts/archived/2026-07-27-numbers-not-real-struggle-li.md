---
title: "The Numbers That Weren't Real"
hook: "Landing page update, five days before a public reveal. One of the metrics didn't exist in any report file."
type: Struggle
platform: LinkedIn
goal: Build in public
karen_verdict: APPROVED
scheduled: true
---

Landing page update, five days before a public reveal. Quick pass to add v2.1 content.

One of the metrics on there didn't exist in any report file. Not close, not rounded, just not there. A baseline number, an improvement percentage built on top of it, an audit mean pulled from nowhere.

Caught it before it shipped, not because a review gate flagged it, but because I asked for source-file verification and the agent that wrote the number couldn't find where it came from either.

That's the part that stuck with me. The gate that should've caught this didn't exist yet for public-facing content, only for code. Fixed that this week: any quantitative claim on a public surface now needs a source file cited in the commit, checkable by anyone with grep.

Small fix. Wouldn't have needed it if I hadn't gone looking.
