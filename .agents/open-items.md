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

## 5. Recurring sync-drift bug class

**Status:** Pattern identified across 3 incidents, not structurally fixed
**Owner:** TBD
**Issue:** Same root cause has now surfaced three times: harvester's `last_entry_date` dropping between stages, the `queue-inspect` / `check_struggle_ratio.py` field-compatibility question (verified OK this time, but only by manual check), and the sync-drift bug documented in the `approve-and-schedule` skill's troubleshooting section. All stem from independently-evolving scripts assuming a shared schema/state without a shared source of truth.
**Action:** Evaluate whether a shared state module (single source of truth for queue/status schema) is worth building, rather than continuing to catch drift case-by-case.

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
