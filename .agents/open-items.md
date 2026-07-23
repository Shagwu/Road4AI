# Open Items

_Compiled 2026-07-23 by open-items-compiler skill. 32 findings across 6 categories._
_Updated 2026-07-23: 19 resolved, 13 remaining._

## Summary

| Category | Resolved | Remaining |
|----------|----------|-----------|
| Governance | 6 | 0 |
| Shared State | 4 | 3 |
| Tools Dead Code | 4 | 4 |
| Skills Drift | 2 | 3 |
| Launchd Agents | 2 | 2 |
| Cross-Cutting | 0 | 2 |
| Pending (distill) | 2 | 1 |
| **Totals** | **20** | **15** |

---

## Governance (6/6 resolved)

~~G-1 | HIGH | Duplicate item numbering~~ — Resolved via AGENTS.md edits.
~~G-2 | HIGH | Queue type enum diverges~~ — `Technical` added, casing documented.
~~G-3 | HIGH | Queue goal enum has 11 values vs 4 declared~~ — Widened to 7 values, compound values allowed.
~~G-4 | MEDIUM | Shared State table omits 12 files~~ — Table expanded to 19 entries.
~~G-5 | MEDIUM | Pre-commit hook no structural validation~~ — Added duplicate numbering + required section checks.
~~G-6 | LOW | Voice constraints not in rules/~~ — Hard non-negotiables codified in rules/content/voice-consistency.md.

---

## Shared State (4/7 resolved)

~~S-1 | HIGH | published-log status "scheduled"~~ — Fixed to "published" for v2.1-reveal-li.
~~S-2 | MEDIUM | published-log platform casing~~ — Normalized "x" to "X".
~~S-3 | MEDIUM | published-log schema drift~~ — Partial: normalized "note" to "notes" on 7 entries. Remaining drift (missing hook on 8 entries) is historical.
~~S-4 | MEDIUM | 7 phantom draft_path refs~~ — All patched. Step 8 in approve-and-schedule prevents recurrence.

### S-5 | LOW | harvester_gate signals_blocked always 0
**Status**: Working as designed. Field is wired (`harvester_drift_hook.py:95`), just hasn't triggered. No action needed.

### S-6 | LOW | current-queue updated field stale
**Status**: Fixed. Timestamp updated to 2026-07-23.

### S-7 | LOW | signal_log.jsonl mixes two schema types
**Status**: Informational. Batch schema (lines 1-6) is from old Twitter pipeline. Per-signal schema (lines 7+) is RSS pipeline. Not a bug, just historical.

---

## Tools Dead Code (4/8 resolved)

~~T-1 | HIGH | automate_content.py + content plist~~ — Script already deleted. Plist removed from ~/Library/LaunchAgents/.
~~T-2 | HIGH | index_self.py + verify_reveal.py~~ — Removed. Legacy Hermes v1.0 with broken imports.
~~T-3 | MEDIUM | sanitizer.py demo stub~~ — Removed. Superseded by public_sanitizer.py.
~~T-4 | MEDIUM | locker.py unused~~ — Removed. Only imported by dead automate_content.py.

### T-5 | MEDIUM | run_skillopt_benchmark_openai.py hardcodes model IDs
**Status**: Deferred. GPT model IDs in DEFAULT_PRICING will become stale. Externalize to config when next updated.

### T-6 | LOW | verify_content.py references nonexistent content/ directory
**Status**: Deferred. Function silently skips missing dirs. Cosmetic.

### T-7 | LOW | health_check.py checks .env as critical
**Status**: Deferred. Fresh clone triggers false alarms. Low impact.

### T-8 | LOW | daily_drift_check.py shadows sys import
**Status**: Deferred. Harmless duplicate import.

---

## Skills Drift (2/5 resolved)

~~K-4 | LOW | signal-review not in manifest~~ — Added to manifest.json as tier-1 canonical.

### K-1 | HIGH | 38 marketing skills have no canonical source
**Status**: By design. These are vendor pack (tier 4) in manifest. Documented as `kept_available`. No canonical source needed.

### K-2 | MEDIUM | hermes-checkpoint name mismatch
**Status**: Documented in manifest as intentional. Manual sync required.

### K-3 | MEDIUM | voice-match canonical/runtime can drift
**Status**: Documented in manifest. Benchmark-relevant — monitor during next benchmark cycle.

### K-5 | LOW | .gemini/skills/ doesn't exist
**Status**: Incorrect finding. Directory exists with content-pipeline. No action needed.

---

## Launchd Agents (2/4 resolved)

~~L-1 | HIGH | content plist runs stale script~~ — Unloaded and removed.
~~L-2 | MEDIUM | content plist lacks PATH~~ — Resolved with L-1 (plist removed).

### L-3 | MEDIUM | scheduled-harvester PATH includes stale venv
**Status**: Informational. PATH entry is harmless if venv doesn't exist. Verify on next harvester debugging session.

### L-4 | LOW | All plists use hardcoded absolute paths
**Status**: Known limitation. Documented. Fix requires symlink or env var indirection.

---

## Cross-Cutting (0/2 resolved)

### X-1 | MEDIUM | Pre-commit hook depends on non-portable shell script
**Status**: Deferred. commit_content_update.sh exists and is executable. Low risk.

### X-2 | LOW | No requirements.txt for tool dependencies
**Status**: Deferred. Stdlib-only tools work fine. Third-party tools (requests, openai) need docs.

---

## Pending from Previous Pass (2/3 resolved)

~~P-1 | HIGH | approve-and-schedule no canonical source~~ — Created, Karen-reviewed, committed.
~~P-2 | MEDIUM | approve-and-schedule not in manifest~~ — Added as tier-1 canonical.

### P-3 | MEDIUM | Karen-only gate vs Sharon sign-off
**Status**: Open design question. Skill checks karen_verdict but has no explicit operator sign-off step. Needs decision, not a code fix.

---

_Resolved items struck through with resolution date 2026-07-23._
