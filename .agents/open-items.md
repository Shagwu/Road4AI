# Open Items

_Compiled 2026-07-23 by open-items-compiler skill. 32 findings across 6 categories._

## Summary

| Category | HIGH | MEDIUM | LOW | Total |
|----------|------|--------|-----|-------|
| Governance | 3 | 2 | 1 | 6 |
| Shared State | 1 | 3 | 3 | 7 |
| Tools Dead Code | 2 | 3 | 3 | 8 |
| Skills Drift | 1 | 2 | 2 | 5 |
| Launchd Agents | 1 | 2 | 1 | 4 |
| Cross-Cutting | 0 | 1 | 1 | 2 |
| **Totals** | **8** | **13** | **11** | **32** |

## Highest-Priority Fixes

1. Disable or remove `com.road4ai.content.plist` + `automate_content.py` (stale April automation running daily)
2. Archive drafts still referenced as `drafts/approved/` in queue `draft_path` fields (7 phantom references)
3. Add `Technical` to the type enum and normalize casing across both state files
4. Normalize the `goal` field across queue entries (11 values vs. 4 declared)
5. Update `published-log.json` entry `2026-07-15-v2-1-reveal-li` from `"status": "scheduled"` to `"published"` or remove it

---

## Governance (6 findings)

### G-1 | HIGH | Duplicate item numbering in AGENTS.md
AGENTS.md lines 76-77 both carry the number `5`. The "Traceability" rule should be item 6, pushing subsequent items to 7-10. Currently items 6 and 7 are also mislabeled.
**Evidence**: AGENTS.md:76-82
**Fix**: Renumber all ten items sequentially.

### G-2 | HIGH | Queue schema `type` enum diverges from actual data
AGENTS.md line 91 lists four allowed types: `Struggle`, `Win`, `Tutorial`, `Behind-the-scenes`. The queue contains `"Technical"` (current-queue.json line 402; published-log.json line 498) and lowercase `"behind-the-scenes"` (current-queue.json line 1002; published-log.json line 624).
**Evidence**: AGENTS.md:91, current-queue.json:402/1002, published-log.json:498/624
**Fix**: Add `Technical` to the enum, enforce casing, or migrate existing entries.

### G-3 | HIGH | Queue schema `goal` enum has 11 distinct values; schema lists 4
AGENTS.md line 93 defines four goal values. Actual queue contains `"build_in_public"` (snake_case), `"Build in Public"`, `"Build in Public / Architectural integrity"`, `"Brand Nurture"`, `"Build Anticipation"`, `"Build Trust"`, `"Teach / Nurture"`. No enforcement exists.
**Evidence**: AGENTS.md:93, current-queue.json (multiple entries)
**Fix**: Widen the enum to match reality or add a normalization step in the dedup gate.

### G-4 | MEDIUM | Shared State Architecture table omits 12 state files
AGENTS.md lines 59-68 list only `current-queue.json` and `published-log.json` under `state/`. The directory contains 12+ additional files. Agents have no guidance on which are canonical versus ephemeral.
**Evidence**: AGENTS.md:59-68, ls state/
**Fix**: Update the table or add a legend distinguishing governance-critical state from operational artifacts.

### G-5 | MEDIUM | Pre-commit hook has no structural validation of AGENTS.md
`.git/hooks/pre-commit` checks for AGENTS.md staging and JSON integrity but has no structural validation (heading hierarchy, sequential numbering, required sections).
**Evidence**: .git/hooks/pre-commit
**Fix**: Add a lightweight linter or CI check for formatting regressions.

### G-6 | LOW | Voice constraints not codified in rules/
The em-dash prohibition and six "hard non-negotiables" from CLAUDE.md are not captured in any `rules/` file. They live only in prose inside CLAUDE.md.
**Evidence**: CLAUDE.md "Hard non-negotiables" section, rules/content/
**Fix**: Create `rules/content/voice-non-negotiables.md` or add enforcement hooks.

---

## Shared State (7 findings)

### S-1 | HIGH | `published-log.json` has entry with `status: "scheduled"`
Line 699 shows `2026-07-15-v2-1-reveal-li` with `"status": "scheduled"`. A published log should only record confirmed publications.
**Evidence**: published-log.json:699
**Fix**: Update to `"published"` or remove until confirmation exists.

### S-2 | MEDIUM | `published-log.json` uses inconsistent `platform` casing
Line 706 has `"platform": "x"` (lowercase). Every other entry uses title-case (`"X"`, `"LinkedIn"`, `"Instagram"`). No normalization at write time.
**Evidence**: published-log.json:706 vs other entries
**Fix**: Normalize platform casing in existing entries and add validation to write path.

### S-3 | MEDIUM | `published-log.json` schema drift between early and late entries
Early entries use `{id, title, type, platform, hook, scheduled_time, published_at, blotato_id, notes}`. Later entries drop `hook`, `scheduled_time`, `blotato_id`, rename `notes` to `note`, add `status`.
**Evidence**: published-log.json:1-180 vs 674-720
**Fix**: Define and enforce a canonical published-log schema.

### S-4 | MEDIUM | 7 queue entries reference `drafts/approved/` but files are in `drafts/archived/`
Per AGENTS.md rule 5, scheduled content should be in `drafts/archived/`. Queue `draft_path` values were never updated after archival. `drafts/approved/` is empty on disk.
**Evidence**: current-queue.json lines 1128, 1147, 1166, 1418, 1507, 1563, 1582
**Fix**: Update draft_path values to point to `drafts/archived/`.

### S-5 | LOW | `harvester_gate.json` `signals_blocked` is always 0
598 signals processed, zero blocked. Either the counter is unused or the gate logic never increments it.
**Evidence**: harvester_gate.json
**Fix**: Verify whether `signals_blocked` is wired into the pipeline or is a dead field.

### S-6 | LOW | `current-queue.json` `updated` field is stale
Line 1759: `"updated": "2026-07-18"`. Five days of mutations without updating this timestamp.
**Evidence**: current-queue.json:1759
**Fix**: Update timestamp on next queue mutation, or remove the field if it provides no value.

### S-7 | LOW | `signal_log.jsonl` mixes two schema types
Lines 1-6 use batch-processing schema. Lines 7+ use per-signal schema. No discriminator field.
**Evidence**: signal_log.jsonl:1-6 vs 7+
**Fix**: Add `schema_version` or `pipeline_stage` field, or split into separate log files.

---

## Tools Dead Code (8 findings)

### T-1 | HIGH | `automate_content.py` references stale April plan, runs daily
Line 7 hardcodes `PLAN_FILE = "CONTENT_PLAN_APRIL.md"`. Launchd plist runs it daily at 05:00. Script either no-ops or processes stale data.
**Evidence**: tools/automate_content.py:7, com.road4ai.content.plist
**Fix**: Unload launchd agent, remove or update script.

### T-2 | HIGH | `index_self.py` and `verify_reveal.py` depend on missing packages
Both import `sentence_transformers` and `road4ai_hermes.bridge` — not in any requirements file. Will raise ImportError immediately. Legacy Hermes v1.0 scripts.
**Evidence**: tools/index_self.py:5-6, tools/verify_reveal.py:5-6
**Fix**: Mark as deprecated or remove.

### T-3 | MEDIUM | `sanitizer.py` is a demo stub superseded by `public_sanitizer.py`
Contains hardcoded keyword lists and simple substring matching. No file imports it.
**Evidence**: tools/sanitizer.py, no imports found
**Fix**: Remove or archive.

### T-4 | MEDIUM | `locker.py` is not imported by any active tool
Only imported by `automate_content.py` (itself dead code per T-1). `schedule_post.py` explicitly documents it has no file locking.
**Evidence**: tools/locker.py, tools/automate_content.py:5
**Fix**: Remove or archive.

### T-5 | MEDIUM | `run_skillopt_benchmark_openai.py` hardcodes model IDs
Lines 50-58 hardcode `"gpt-4.1-2025-04-14"` in `DEFAULT_PRICING`. Will become stale. Lazy OpenAI import surfaces errors only at runtime.
**Evidence**: tools/run_skillopt_benchmark_openai.py:50-58
**Fix**: Externalize model pricing to a config file.

### T-6 | LOW | `verify_content.py` references nonexistent `content/` directory
Line 88: `check_public_sanitization(["drafts/ideas", "drafts/ready", "drafts/approved", "content"])`. The `content/` directory doesn't exist.
**Evidence**: tools/verify_content.py:88
**Fix**: Remove `content` from the list.

### T-7 | LOW | `health_check.py` checks for `.env` as critical file
Line 32: `.env` is listed as critical. Fresh clone will report SYSTEM ISSUES. Does not check `project.yaml`, `state.yaml`, or AGENTS.md permissions.
**Evidence**: tools/health_check.py:32
**Fix**: Update critical file list to match actual governance files.

### T-8 | LOW | `daily_drift_check.py` shadows `sys` import
Line 6 imports `sys`, line 25 imports `sys` again. Harmless but signals copy-paste. Lines 55-56 set Ollama env vars that could be mistaken for hardcoded secrets.
**Evidence**: tools/daily_drift_check.py:6,25,55-56
**Fix**: Remove duplicate import, add comment clarifying Ollama config.

---

## Skills Drift (5 findings)

### K-1 | HIGH | 38 skills in `.agents/skills/` have no canonical source in `skills/`
The marketing pack skills live only in `.agents/skills/` with no `skills/` counterpart. If runtime is deleted, no canonical source to restore from.
**Evidence**: `.agents/skills/` has 46 SKILL.md files; `skills/` has 7 canonical + 2 runtime + vendor symlinks
**Fix**: Decide which are canonical (add to `skills/`) vs. vendor-pack (document as intentionally runtime-only).

### K-2 | MEDIUM | `hermes-checkpoint-patterns` vs `hermes-checkpoint` name mismatch
Canonical is `hermes-checkpoint-patterns`, runtime is `hermes-checkpoint`. Manifest documents this intentionally but `sync_skills.py` cannot sync between them.
**Evidence**: manifest.json:28-31, skills/hermes-checkpoint-patterns/, .agents/skills/hermes-checkpoint/
**Fix**: Align names or document manual sync requirement.

### K-3 | MEDIUM | `voice-match` canonical and runtime copies can drift independently
Manifest: `runtime_targets: []` for canonical, separate runtime entry. Any divergence could invalidate benchmark results.
**Evidence**: manifest.json:47-52, 77-82
**Fix**: Add runtime targets to canonical entry, or document drift-check procedure.

### K-4 | LOW | `signal-review` not listed in manifest
Both `skills/` and `.agents/skills/` have the file. Manifest has no entry.
**Evidence**: skills/signal-review/SKILL.md, .agents/skills/signal-review/SKILL.md, manifest.json (no entry)
**Fix**: Add to `canonical_skills` with appropriate `runtime_targets`.

### K-5 | LOW | `.gemini/skills/` doesn't exist despite manifest declaring it
Manifest line 5 lists it as a runtime target. Directory doesn't exist.
**Evidence**: manifest.json:5, ls .gemini/ (not found)
**Fix**: Remove from manifest targets or create the directory.

---

## Launchd Agents (4 findings)

### L-1 | HIGH | `com.road4ai.content.plist` runs stale script daily
Invokes `automate_content.py` which hardcodes `CONTENT_PLAN_APRIL.md`. Runs at 05:00 UTC daily.
**Evidence**: ~/Library/LaunchAgents/com.road4ai.content.plist:10
**Fix**: Unload (`launchctl unload`), remove plist, or update script.

### L-2 | MEDIUM | `com.road4ai.content.plist` lacks PATH environment variable
Unlike the other three plists, content plist has no `EnvironmentVariables` section. Will fail silently if script shells out.
**Evidence**: com.road4ai.content.plist (no EnvironmentVariables)
**Fix**: Add PATH like the other plists: `/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin`.

### L-3 | MEDIUM | `com.road4ai.scheduled-harvester.plist` PATH includes stale venv
Line 37: PATH includes `.agent-reach-venv/bin` — from pre-RSS Twitter era. May no longer exist.
**Evidence**: com.road4ai.scheduled-harvester.plist:37
**Fix**: Verify venv is still needed. If not, remove from PATH.

### L-4 | LOW | All plists use hardcoded absolute paths
Every plist references `/Users/shagwu/Downloads/Road4AI-main/...`. Repo move breaks all agents.
**Evidence**: All four plists
**Fix**: Use symlink or environment variable indirection, or document the path dependency.

---

## Cross-Cutting (2 findings)

### X-1 | MEDIUM | Pre-commit hook depends on non-portable shell script
`.git/hooks/pre-commit` line 11 runs `./tools/commit_content_update.sh dry-run`. May not be executable on all environments.
**Evidence**: .git/hooks/pre-commit:11
**Fix**: Ensure script is executable, add fallback, or document the dependency.

### X-2 | LOW | No requirements.txt or pyproject.toml for tool dependencies
Multiple tools import third-party packages (`requests`, `openai`, `sentence_transformers`, `fcntl`). No dependency manifest exists.
**Evidence**: Multiple tools, no requirements.txt found
**Fix**: Create `requirements.txt` listing all tool dependencies.

---

## Pending from Previous Pass

### P-1 | HIGH | `approve-and-schedule` has no canonical `skills/` source
Only runtime copy at `.agents/skills/approve-and-schedule/SKILL.md` exists. Violates option_b architecture.
**Evidence**: skills/approve-and-schedule/ (does not exist)
**Fix**: Create canonical source. **Prerequisite: Karen adversarial review before manifest entry** (tier-1 skill, PR #2 precedent).

### P-2 | MEDIUM | `approve-and-schedule` not listed in manifest.json
No manifest registration. `sync_skills.py` can't see it.
**Evidence**: manifest.json (no approve-and-schedule entry)
**Fix**: Add to `canonical_skills` after Karen review.

### P-3 | MEDIUM | Karen-only gate vs. Sharon sign-off in approve-and-schedule
Skill checks `karen_verdict` but has no explicit step for operator sign-off. Design question: should Sharon's approval be an explicit step?
**Evidence**: .agents/skills/approve-and-schedule/SKILL.md:44-47
**Fix**: Design decision needed — not a drift fix.

---

_Resolved items will be marked with strikethrough and resolution date._
