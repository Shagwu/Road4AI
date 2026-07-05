# Daily Plan - 2026-07-05

## Executive summary
The v2.1 Benchmark Reveal is locked for July 15 — 10 days out. Four posts are scheduled (Phase 4 teasers at 08:00/12:00 UTC, v2.1 X thread at 15:30, LinkedIn at 16:00 UTC), plus a manual blog publish at 18:00 UTC. The `drafts/approved/` directory has the reveal assets. The `ship/` directory is empty — no proof package exists yet. Today's focus: fill the proof package gap, verify the last week's scheduled posts actually landed, and confirm reveal assets are finalized.

## P1 - Highest priority
- **Write the v2.1 proof package in `ship/`.** The reveal posts (X thread, LinkedIn) reference benchmark results (0.871 deterministic, +35% improvement) but no proof artifact exists in `ship/`. Draft a `ship/v2.1-benchmark-proof.md` summarizing: baseline score, optimized score, test methodology, governance boundary results, and a link to the raw data in `reports/skillopt/social_voice/`. Why: the blog post and social posts cite numbers that need a source artifact. Expected output: one markdown file in `ship/` that the blog post can link to.

- **Verify late-June/early-July scheduled posts published.** Queue shows 5+ entries with `status: scheduled` and `scheduled_time` between June 28 and July 4, but no `published_at` timestamps or live URLs. Check Blotato dashboard or API for these posts. Update queue entries to `published` with URLs, or flag if any were dropped. Why: content pipeline traceability; phantom entries break the published-log. Expected output: queue entries updated or blockers flagged.

## P2 - Important next work
- **Review reveal draft quality.** Read `drafts/approved/v2.1-benchmark-reveal-x.md` and `drafts/approved/v2.1-benchmark-reveal-li.md`. Verify all numbers match the actual benchmark data in `reports/skillopt/social_voice/`. Confirm X thread posts are under 280 characters. Confirm no em dashes. Why: these go public in 10 days; a number error or governance violation here is high-visibility. Expected output: confirmation or corrections.

- **Confirm Phase 4 teaser assets.** The `drafts/approved/phase4_teaser_linkedin.md` is scheduled for July 15 12:00 UTC. Verify it references the correct v2.1 results and doesn't conflict with the v2.1 reveal posts that follow at 15:30/16:00 UTC. Why: the Phase 4 teaser sets up the reveal; timing and messaging must be coherent. Expected output: confirmation or edits.

## P3 - Lower priority / support work
- **Run drift check.** Verify the July 3 baseline is still stable. Quick sanity check against `state/drift_log.jsonl`. Why: ongoing reliability, but not a blocker for the reveal. Expected output: drift status logged.

- **Move scheduled content from `drafts/approved/` to `drafts/archived/`** for any posts that Blotato confirms are live. Prevents duplicate-approval risk. Why: governance hygiene. Expected output: approved/ contains only pre-July-15 assets.

## Risks / blockers
- **Blog manual publish on July 15 at 18:00 UTC.** No Blotato automation exists for the blog. Dependency: operator must be available at that time. If unavailable, the blog post must be rescheduled or pre-staged.
- **Blotato post verification.** If Blotato silently dropped a June 28-July 4 post, we lose a scheduled window with no retry. Dependency: Blotato dashboard access or API.
- **Proof package is empty.** The `ship/` directory has nothing in it. This is the gap between "scheduled posts" and "verifiable claims." P1 today.

## Quick wins
- Run `rg '"published_at"' state/current-queue.json` to see how many posts have confirmed publish timestamps vs. how many are still in limbo.
- Check `drafts/approved/v2.1-benchmark-reveal-x.md` for em dashes (governance violation) — takes 30 seconds.

## Proposed order
1. Verify July 1-4 posts in Blotato, update queue entries.
2. Write `ship/v2.1-benchmark-proof.md` using benchmark data.
3. Review reveal drafts for number accuracy and governance compliance.
4. Confirm Phase 4 teaser timing coherence with v2.1 reveal.
5. Run drift check, archive confirmed-published content.
6. Commit with Hermes checkpoint.
