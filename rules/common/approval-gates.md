# Approval Gates

Road4AI uses manual approval for actions that change public output or operating authority.

## Content Lifecycle

- `drafts/ideas/`: rough ideas and early drafts.
- `drafts/ready/`: drafted and ready for user review.
- `drafts/approved/`: user-approved content only.
- `drafts/archived/`: published or retired drafts.

Only the user moves content into `drafts/approved/`.

## Publishing

Once content is approved, Claude Code may schedule via Blotato without a second scheduling confirmation, subject to:

- dedup gate passed;
- public sanitization passed;
- platform constraints passed;
- published log and queue status will be updated after Blotato confirms scheduling. Platform-side verification is not required.

## Governance

Changes to operating contracts require explicit human approval in the active session. This includes:

- `AGENTS.md`;
- rules that weaken or bypass approval gates;
- agent specs that change who may publish, approve, or mutate shared state.

## Public-Facing Content Gate

Changes to public-facing surfaces (`index.html`, `SYSTEM.md`, `manifesto.md`, `CONTRIBUTING.md`, or any file served to external users) require a source citation check before merge.

**Rule:** Any claim containing a number, metric, benchmark score, or quantitative result must include a source file path in the commit message or PR description. Example: "0.788 live Ollama (execution/runs/2026-07-07-005/live-report.md)".

**Why this exists:** PR #2 merged without adversarial review on public-facing content. The landing page update (2026-07-10) included fabricated numbers (0.6447, +22%, 0.7504) that had no matching source file. A mechanical source-citation check would have caught this without relying on an LLM review gate.

**What this is not:** This is not a Karen gate. Karen reviews code diffs. This is a commit-message-level check that any human or agent can verify by grepping the cited source file. If the source file doesn't exist or doesn't contain the claimed number, the commit fails the gate.

**Enforcement:** Manual. The committing agent must include source citations for quantitative claims. The reviewing agent (or human) must verify the cited file exists and contains the claimed value before merge.

## Harvester Pipeline Gate

Changes to `tools/harvester_pipeline.py` or `tools/scheduled_harvester.py` that add or modify decision logic (dedup, keyword lists, staleness overrides, confidence gate overrides, underrep routing) MUST go through Karen adversarial review before the next unattended launchd run.

**Why this exists:** PR #2 precedent — governance gaps found retroactively after decision logic shipped. The harvester runs unattended at 08:00 + 18:00 UTC. Decision logic changes (discard→queue overrides, keyword-based routing, dedup filtering) affect what gets surfaced for content ideation without human review. Adversarial pass catches edge cases, logic inversion, and silent failure modes that unit tests miss.

**Scope:** Any commit that touches the `if underrep_boost` override path, `TOPICAL_KEYWORDS`, `BRAND_MENTIONS`, `should_log_signal`, `get_keyword_counts`, `get_underrepresented_keywords`, or the confidence tier routing in `process_signal`.

**Enforcement:** Manual. The committing agent must flag the change. Karen review must complete before the affected launchd cycle.

## Phase 5 Eval Moratorium

New Phase 5 tool evaluations are blocked until Phase 4 has real usage data.

**Blocked evaluations:** OmniRoute, cc-mirror, Memanto, gpt-oss-120b, Project Graveyard (all evaluated, none adopted).

**What this blocks:** Any new evaluation, benchmark, or integration attempt for tools outside the core stack (Claude Code, Codex, Ollama, Blotato, GitNexus, Magika, Hermes).

**What this allows:** Bug fixes, maintenance, and iteration on tools already in use. Phase 4 harvester and drift monitoring work continues.

**Why this exists:** Five evaluations completed with correct evaluate-document-defer outcomes but zero adoption. The backlog grew without usage data to justify further evaluation. The moratorium turns "we should wait" into an enforced constraint.

**Enforcement:** Manual. Any agent proposing a new tool evaluation must check this rule first. If Phase 4 usage data is insufficient, the evaluation is deferred — not skipped, deferred.

**Lift condition:** Phase 4 POC has demonstrated measurable value (signals surfaced → content published, or drift detection → corrective action). Operator decision to lift.

