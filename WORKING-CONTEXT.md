# Road4AI Working Context

Last updated: 2026-07-22

## Current Sprint

Phase 4 POC: harvester runs on launchd, signal review brief bridges harvester to content pipeline, Phase 5 eval moratorium enforced.

Primary focus:

- Harvester proves value by informing a content decision (redefined POC gate — see approval-gates.md).
- Content pipeline continues with 7 posts scheduled through Jul 27.
- Weekly signal review brief surfaces candidates for ideation.

## v2.1 Timeline

### June 28
- v2.1.0 released, GitHub release published, X thread live.

### June 30
- LinkedIn post scheduled.

### July 1–10
- Drift monitoring started (daily runs), then stopped per operator decision (July 8). Scores accepted as-is: 0.788 (live Ollama), 0.871 (deterministic).
- Struggle ratio enforcement implemented (`check_struggle_ratio.py`).

### July 15
- v2.1 reveal posts published (X + LinkedIn).
- Phase 4 POC begins.

### July 16–20
- Harvester pivoted to RSS (Twitter CLI broken — API deprecation, 404).
- Harvester pipeline hardened: canonical-URL dedup, underrepresentation check, governance gate.
- Open items checkpoint compiled (6 governance/infra gaps).
- Harvester Karen review completed (post-commit).
- Sync-drift audit: 4 high-severity fixes, remaining debt documented.

### July 21–22 (today)
- Twitter reader fixed (broken import + JSON parser).
- Struggle stall detector built (`check_struggle_stall.py`).
- `.mimocode` tracked assets consolidated to `.agents/skills/`.
- Phase 5 eval moratorium enforced in approval-gates.md.
- Signal review brief built (`signal_review_brief.py` + skill) — bridges harvester to content pipeline.
- Phase 4 POC lift condition redefined: "signal → traceably informs content decision" (not "signal → post").
- All 6 open items resolved.

## Recent Checkpoints

- Jul 22: Gate redefined, signal review brief, stall detector, .mimocode consolidation, Twitter fix — 10 commits.
- Jul 20: Open items checkpoint compiled, sync-drift fixes (4 high-severity), Phase 5 RFC log.
- Jul 18: Queue sync fix, ratio script date-sort, harvester dead code cleanup.
- Jul 17: Harvester pipeline hardened (dedup, underrep, governance gate). Twitter CLI confirmed broken.
- Jul 15: v2.1 reveal published, Phase 4 POC begins.
- Jul 6–10: Struggle ratio enforcement implemented, content pipeline finalized.
- Jun 28: v2.1.0 released.

## Deferred Evaluations

### Memanto Semantic Memory (evaluated June 2026)

**Decision:** Defer to Phase 5 RFC. Blocked by Phase 5 eval moratorium.

**Revisit threshold:** 5+ concurrent autonomous agents, or 1,000+ checkpoints where `git log --grep` becomes unwieldy.

### OmniRoute Multi-Provider AI Gateway (evaluated July 2026)

**Decision:** Deferred, not adopted. Blocked by Phase 5 eval moratorium.

**Revisit trigger:** If a future phase requires cloud-provider fallback that Ollama/MiMo can't cover.

## Active Constraints

- `AGENTS.md` requires explicit human approval before edits.
- Queue writes must pass the four-check dedup gate.
- `state/current-queue.json` uses a top-level `queue` array; preserve this shape.
- Only the user moves content into `drafts/approved/`.
- Public posts must not include copy-pasteable exploit strings.
- X posts must be strictly under 280 characters each.
- Blotato scheduling confirmation is the terminal state. Do not verify whether posts appeared on platforms.
- Phase 5 eval moratorium: no new tool evaluations until Phase 4 POC lifts (see approval-gates.md).
- Harvester pipeline changes require Karen review before next unattended launchd run.

## Active Governance Backlog

1. ~~Audit Road4AI skills against the standardized `SKILL.md` structure.~~ (lower priority, maintenance)
2. ~~Consider filesystem-level protection for `AGENTS.md`.~~ (done — chmod 444 via `lock_agents_md.py`)
3. ~~Add broader hook coverage for publishing workflows.~~ (deterministic sanitizer + pre-commit hook in place)
4. ~~Decide whether to consolidate overlapping content pipeline skills.~~ (done — Phase 3 Consolidation)
5. Phase 5 RFC: evaluate Memanto if scale threshold reached (blocked by moratorium).
6. Phase 5 RFC: evaluate OmniRoute if cloud-provider fallback needed (blocked by moratorium).

## Content Pipeline Pattern

The five-agent content pipeline is the canonical Road4AI content workflow:

1. Chief of Staff selects and coordinates the work.
2. Trend Researcher gathers weak signals.
3. Voice-Match Ideator converts signals into Road4AI-native angles.
4. Format Selector maps ideas to platform and cadence.
5. Content Scout extracts structured knowledge from transcripts, URLs, or text.

**New input source (Jul 22):** Signal review brief (`tools/signal_review_brief.py`) surfaces queue-for-review candidates weekly. Selected signals become inbox entries for ideation.

Parallelize independent research and ideation work. Keep drafting, approval, and scheduling sequential because each step depends on the previous gate.

## Completed Archive

### Week of 2026-05-06

- Local Karen review pipeline established as an 8-step content/code audit path.
- `karen.py` became the local adversarial review reference for Road4AI content and PR safety.
- Early struggle-lane content documented the HNSW scale wall and the move from demo-scale to system-scale thinking.

### Week of 2026-05-13

- Hermes checkpointing upgraded to v2.0 with structured `[hermes-context]` commits.
- Modular Chief of Staff architecture and agent skill tracking finalized.
- Human Approval Gate and Strict Governance Lock added around `AGENTS.md`.
- Hermes-CrewAI bridge wired and self-knowledge RAG pivot locked.
- Self-knowledge index reached 200 high-signal chunks with sub-100ms target performance on most queries.
- Hermes v2.0 distributed substrate verified.

### Week of 2026-05-19

- Hermes v2.0 reveal strategy operationalized through runbook, reply strategy, script, fallback package, and public safety layers.
- Week 3 content gates passed and legacy draft/archive maintenance completed.
- June memory governance LinkedIn and X drafts approved.
- Struggle ratio and Self-Knowledge Loop trajectories verified.
- Content pipeline finalized for May 21.

### Week of 2026-05-26

- Hermes v2.0 reveal completed on May 26.
- `road4ai-hermes` standalone extraction scaffolded and completed.
- v0.1.0 changelog and Ecosystem Shift announcement added.
- Post-reveal retro sequence finalized and scheduled.
- Architecture hardening and state synchronization completed after reveal.
- Google Workspace plugin imported and agent spawn workflow launched.
- SkillOpt v2.1 direction defined with governance boundary, validation report, roadmap, benchmark foundation, and runner hardening.

### Week of 2026-06-01

- June 1 Road4AI posts confirmed published.
- Missed approved posts reconciled and May 27 posts filed as published.
- June 3 Catch-Up Checkpoint content scheduled/published.
- M Solo Agent Scout drop processed, drafted, scheduled, and marked published for June 4.
- GitNexus refresh policy batched.
- Token anxiety/fresh-idea capture logged as a current planning constraint.

### Phase 1 Governance Foundation

- Rules system added under `rules/`.
- `AGENTS.md` expanded with rules loading, autonomy levels, orchestration, workflow surface policy, public sanitization, security-before-commit, and queue-shape preservation.
- `WORKING-CONTEXT.md` added as live execution memory.
- `content-pipeline` and `public-sanitization-review` skills added.
- `hermes-checkpoint` skill standardized to the Road4AI skill template.

### Phase 2 Security and Sanitization

- Deterministic public sanitizer added under `tools/public_sanitizer.py`.
- Sanitizer wired into `tools/verify_content.py`.
- Security Theater Trap exploit phrase abstracted to `<INSTRUCTION_INJECTION_EXAMPLE>`.
- Sanitized draft moved to `drafts/ready/security-theater-abstraction.md`.
- Sanitizer tests added.

### Phase 3 Pattern Extraction

- `adversarial-review-karen` captures the local two-model Karen review gate.
- `content-pipeline` captures the weekly five-agent ideation flywheel and full content lifecycle.
- `hermes-checkpoint-patterns` captures cross-session state and handoff behavior.

### Phase 3 Consolidation

- Skill inventory policy added with Option B architecture: `skills/` is canonical source, runtime skill surfaces are install targets.
- `content-ideation-orchestrator` merged into `content-pipeline`.
- `.agents/marketing/` reference docs moved to `docs/marketing/`.
