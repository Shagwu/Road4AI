# Signal Harvester — Feed Source Criteria

Governs which RSS feeds MiMo Auto (or any agent) can add to the Signal Harvester
without a human review gate, and which require Karen/Chief-of-Staff sign-off first.

## Hard gates (auto-reject, no judgment call)

A candidate feed is rejected outright if ANY of these are true:

1. **Zero entries on test pull.** `feedparser` returns 0 entries on a clean fetch.
   A feed that 200s with nothing in it is not a feed, it's a placeholder.
2. **Requires auth/OAuth/API key to read.** Matches the zero-cost/local-first
   principle already applied to OmniRoute/9Router/Memanto. Reddit's 403 on
   plain RSS falls here — PRAW/OAuth is a dependency decision, not a feed add.
3. **DNS/connection failure.** Domain doesn't resolve or refuses connection.
   Don't retry-loop a dead domain, log it dead and move on.
4. **Fewer than 1 update in the last 30 days**, based on the newest entry's
   published date. Stale feed = dead weight in the pipeline, not signal.
5. **ToS explicitly prohibits scraping/automated access.** Same posture as
   the 9Router rejection — don't build on a ToS-circumvention foundation.

### Soft staleness overrides (per-entry, not per-feed)

Default thresholds (mirrored in `harvester_pipeline.py`):
- N = 21 days (items older than this are considered stale)
- K = 3 recent signals per keyword
- M = 14 days recent-lookback window

By default, items from an approved feed that are older than N days
are treated as low-priority signal and may be skipped in harvesting.

MiMo Auto MAY override this soft staleness preference and keep a stale
item ONLY when ALL of the following are true:

- The item matches terms from at least two different concept clusters
  in `TOPICAL_CLUSTERS` (defined in `harvester_pipeline.py`):
  - **subject**: agent, AI, LLM, model, bot, assistant, chatbot
  - **memory**: memory, context window, recall, state, context overflow, long-term memory
  - **local**: local, self-hosted, on-device, on-premise, edge, local llm
  - **evals**: evals, evaluation, benchmark, testing, metrics
  - **governance**: guardrail, governance, safety, alignment, drift, oversight
  - **training**: fine-tune, quantization, optimization, training, gguf
  - **open**: open source, open weights, open-source, free, zero-cost
  - **orchestration**: multi-agent, orchestration, coordination, swarm, pipeline

  This filters out false positives (hardware "memory", insurance "agent")
  by requiring topical convergence — "memory crunch" alone won't fire,
  but an article about AI agent memory will match subject+memory.
- There are fewer than K signals for that keyword in the last M days
  of signal_log.jsonl, so the topic is currently underrepresented.
- "Keep" means the item is routed to `queue-for-review` regardless of
  its confidence score, bypassing the normal ≥0.5 confidence gate.
  This is implemented as an action override in `scheduled_harvester.py`:
  `if underrep_boost and action == "discard": action = "queue-for-review"`.
- MiMo Auto logs the underrep_keywords list in the signal row for audit
  trail (field: `underrep_keywords`).

Brand keywords (`BRAND_MENTIONS`: skillopt, hermes, road4ai, obsidian,
blotato, skill optimization, zero-cost) are tracked separately for the
"Road4AI mentioned externally" monitor and do NOT feed the underrep check.

MiMo Auto MUST NOT invent new override categories. Any new type of
override (beyond "stale + keyword-override") must be added to this
document by Sharon before it can be used.

### Deduplication gate (at ingest, before signal_log.jsonl)

Every signal is deduped by canonical URL before it reaches signal_log.jsonl.
`canonicalize_url()` strips UTM params, ref params, and trailing slashes,
then lowercases. Two URLs that differ only in tracking garbage are the same
article.

`should_log_signal(item, seen_urls_this_run)` returns False if the
canonical URL was already seen in the current run. Deduped items are logged
with reason `dedup_same_url` but never written to signal_log.jsonl.

This runs before the underrepresentation check (K/M logic), so keyword
counts in signal_log.jsonl reflect unique articles, not duplicate rows.

These don't auto-reject, but also don't auto-approve:

- **Relevance fit.** Is this actually AI/local-LLM/agent-infra content, or
  general tech noise that'll dilute ideation signal? (e.g. Synced AI News
  passed the hard gates but is broad industry news, not niche/local-LLM —
  worth asking if that's the lane you want.)
- **Volume sanity.** Extremely high entry counts (Hugging Face's 829) may
  need a "only look at last N days" filter downstream, not a rejection —
  flag for the harvester's ingestion logic, not the feed list itself.
- **Duplicate coverage.** If two feeds cover the same announcements (e.g. a
  vendor blog + a news aggregator both covering the same model release),
  keep the primary source, drop the aggregator.
- **Source credibility for a build-in-public brand.** Random blogspot-tier
  aggregators vs. vendor blogs (HF, Ollama, Anthropic) — the second builds
  more trust if content ever cites "saw this on X."

## Known accepted risks

- **Race condition on signal_log.jsonl (concurrent writes).** `scheduled_harvester.py` appends without file locking. Safe at current 10-hour gap between launchd runs (08:00 + 18:00 UTC). **Revisit trigger:** any change to the launchd schedule that tightens the gap to < 1 hour, or any manual run of `harvester_pipeline.py` alongside the automated schedule. [accepted 2026-07-17, expanded 2026-07-18]

- **Race condition on harvester_gate.json (read/write without locking).** `harvester_drift_hook.py` reads and writes `harvester_gate.json` without file locking. Same 10-hour gap mitigates this today. **Revisit trigger:** same as above — schedule tightening or concurrent manual+automated runs. [accepted 2026-07-18]

- **Duplicated confidence scorers.** `harvester_pipeline.py` (line ~320) and `harvester_reader.py` (line ~32) score signal confidence using different formulas. Same signal routed through different paths gets different scores. Not a bug today since they're used in different contexts, but will produce confusing discrepancies if the paths ever converge. **Revisit trigger:** any change that routes the same signal through both pipelines, or any investigation into confidence score drift. [flagged 2026-07-18]

## Karen review log

| Date | Script(s) | Method | Verdict | Notes |
|---|---|---|---|---|
| 2026-07-18 | harvester_pipeline.py, scheduled_harvester.py | Manual review (no staged diff; files already committed in 780f35b) | APPROVED | Dead code removal (33 lines after match_clusters return), unused constant DEDUP_SAME_URL removed (4 lines), unused import removed. Pure deletions, no behavioral change. Verified via AST analysis, import testing, compile checks, functional test of match_clusters(). Duplicated confidence scorer flagged as known risk above. |

## What MiMo Auto can do autonomously

- Run the test pull, apply hard gates, drop anything that fails them.
- Add feeds that pass hard gates AND are unambiguous vendor/project blogs
  (Ollama, Hugging Face, Anthropic, llama.cpp, etc.) — L8-autonomy tier,
  same spirit as Signal Harvester's existing AGENTS.md grant.
- Log every feed tested (pass/fail/reason) in a single running file, e.g.
  `harvester/FEED_LOG.md`, so nothing is silently dropped.

## What routes back to you (or Karen) before going live

- Anything in the soft-criteria bucket above.
- Any feed requiring a new dependency (OAuth libs, API clients) to fix a
  hard-gate failure — this is a scope decision, not a feed swap. Log as a
  Phase 5 RFC candidate if it comes up (matches the OmniRoute/cc-mirror
  pattern: don't add attack surface for a problem RSS already covers).
- Removing a feed that was previously approved (content pipeline shouldn't
  silently lose a source without you knowing why).

## Today's test results, sorted against these criteria

| Feed | Result | Verdict |
|---|---|---|
| Hugging Face Blog | 200, 829 entries | Pass hard gates → volume filter needed, otherwise auto-add candidate |
| Ollama Blog | 200, 54 entries | Pass hard gates → auto-add candidate |
| Synced AI News | 200, 10 entries | Pass hard gates → soft-criteria call (broad vs. niche) |
| Meta AI Blog | 404 | Hard reject (dead endpoint) |
| LangChain Blog | 200, 0 entries | Hard reject (empty) |
| LlamaIndex Blog | 404 | Hard reject (dead endpoint) |
| r/LocalLLaMA | 403 | Hard reject (auth required) → log as RFC candidate if OAuth ever pursued |
| r/MachineLearning | 403 | Hard reject (auth required) |
| Papers With Code | 200, 0 entries | Hard reject (empty, likely feed format changed) |
| Open Source AI | Connection error | Hard reject (dead domain) |
| AI Alignment Forum, LessWrong AI, The Batch, Anthropic Research | untested | Run through same test script before deciding |
