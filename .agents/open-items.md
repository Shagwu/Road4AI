# Open Items Checkpoint

Date: 2026-07-20
Context: Compiled during review of .mimocode distill work (commit 588cf99). Captures outstanding governance/infra items so they don't get lost the way the Phase 5 eval backlog did.

---

## 1. Signal Harvester Karen review gap — RESOLVED (2026-07-20)

**Status:** Closed, commit `ed6524a`
**Resolution:**
- Karen review: APPROVED (manual, post-commit — ordering noted honestly in commit message per retroactive-audit convention)
- 3 dead imports removed: `load_gate`, `TOPICAL_KEYWORDS`, `DRIFT_LOG`
- 2 known risks documented in `HARVESTER_FEED_CRITERIA.md`: dead `authority_boost` branch, `signals_processed` race condition (accepted for sequential launchd execution)
- Plist cleaned: stale `TWITTER_AUTH_TOKEN`/`TWITTER_CT0` removed, job reloaded, verified via manual `launchctl start`
- 19/19 tests passing
- Next unattended run (08:00 UTC July 21) will execute with the cleaned/reviewed code

---

## 2. Twitter/X RSS 404

**Status:** Broken, blocking Phase 4 POC
**Owner:** TBD
**Issue:** Agent-Reach CLI → Twitter test → Harvester integration (targeted July 16+) can't proceed until this is resolved.
**Action:** Determine whether this is an API/auth change on Twitter's side or a bug in the fetch logic. If not fixable soon, log it explicitly as a blocker with a re-check date rather than letting Harvester run silently degraded on that source.

---

## 3. 72-hour stall detector (missing guardrail)

**Status:** Not implemented
**Owner:** TBD
**Issue:** The June 2 Struggle-content cliff-break (16 consecutive non-Struggle posts) was traced to a missing automated ratio enforcement guardrail. Ratio has been managed manually since (e.g. July 20-31 skeleton hand-balanced).
**Action:** Build the stall detector so ratio drift is caught automatically instead of retrospectively during content audits.

---

## 4. Phase 5 eval backlog — enforce a moratorium

**Status:** Pattern identified, not yet enforced
**Owner:** TBD
**Issue:** Five tool evaluations (OmniRoute, cc-mirror, Memanto, gpt-oss-120b, Project Graveyard) completed with correct evaluate-document-defer outcomes but zero adoption — backlog growing without usage data to justify further evaluation.
**Action:** Add an explicit rule (AGENTS.md line item or Karen gate) blocking new Phase 5 tool evaluations until Phase 4 has real usage data. Turn the intention into an enforced constraint.

---

## 5. Recurring sync-drift bug class — PARTIALLY RESOLVED (2026-07-20)

**Status:** 4 high-severity mismatches fixed, remaining debt documented
**Owner:** Shagwu (for remaining decisions)
**Resolution (commit TBD):**
- **M1 FIXED**: `approve-and-schedule/SKILL.md` read `blotato` but field is `blotato_id` — queue sync verification always returned "none"
- **M11 FIXED**: `get_keyword_counts()` couldn't dedup Twitter signals (`tweet_id` not checked) — inflated keyword counts
- **M13 FIXED**: `signal_server.py` imported dead `run_twitter_search` (removed when pipeline switched to RSS) — would crash on import. Updated to `run_rss_search`.
- **Dead import cleaned**: `load_gate` removed from `signal_server.py` (unused)

**Remaining tech debt (not fixed, documented):**
- M2: Queue data has type enum violations (`"Technical"`, lowercase `"behind-the-scenes"`) not in AGENTS.md enum — no script validates the enum
- M3: `rituals/CONTENT_AGENT.md` uses status values (`"drafting"`, `"outlined"`) not in AGENTS.md enum
- M5: `codex_daily_check.py` treats `ready` as valid status (groups with `ready_for_publishing`)
- M7: `published-log.json` has no automated writer — structural drift risk
- M10: `signal_log.jsonl` has 3 schemas (request summaries, Twitter signals, RSS signals) with no discriminator
- M6 (reclassified): `sync_queue_status()` raises RuntimeError for entries without `draft_path` — this is correct behavior (surfacing real errors), not a bug

**Structural fix deferred:** A shared state module (single source of truth for queue/status schema) was evaluated but deferred. The 4 fixes address the concrete bugs; the remaining debt is enum consistency and published-log automation, which are lower urgency. Revisit if drift incidents recur.

---

## 6. `.mimocode` tracking decision

**Status:** Open, low urgency
**Owner:** Shagwu (explicitly your call)
**Issue:** `.mimocode` is gitignored; `queue-inspect.md` and `approve-and-schedule/SKILL.md` are committed via `git add -f`, so `git status` will keep showing them as untracked.
**Options:**
- **A — Un-ignore `.mimocode`:** keeps assets in MiMo's native discovery path; add a scoped `.mimocode/.gitignore` to avoid pulling in local-only cache/log files.
- **B — Move to `.agents/skills/`:** consistent with existing tracked-skill locations (`.agents/harvester/`), but requires confirming MiMo Auto can still discover/invoke skills from a non-`.mimocode/` path — check this before moving anything, to avoid a silent discovery failure.
**Action:** Decide, verify MiMo's discovery mechanism if choosing B, note the decision in a Hermes checkpoint.

---

*Compiled by Claude at Shagwu's request. Not a Karen-reviewed artifact — this is a tracking doc, not code/pipeline content.*
