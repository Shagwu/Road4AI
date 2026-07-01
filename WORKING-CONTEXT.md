# Road4AI Working Context

Last updated: 2026-06-28

## Current Sprint

Governance foundation after the Hermes v2.0 reveal.

Primary focus:

- Make governance explicit through `rules/`.
- Preserve `AGENTS.md` as the operating contract.
- Formalize the five-agent content pipeline as a reusable skill.
- Add public sanitization rules before security/autonomy content is published.
- Extract working Road4AI operating patterns into reusable skills.

## v2.1 Timeline

### June 28 (Today)
- v2.1.0 released ✅
- GitHub release published ✅
- X thread live ✅

### June 30 (Sun)
- LinkedIn post scheduled ✅

### July 1 (Mon)
- Blog post scheduled ✅
- Drift monitoring starts (daily runs, 12-case orchestration suite)
- First checkpoint to Hermes (baseline comparison)
- COS daily review (5 min: check alerts, approve next run)

### July 2–10 (Tue–Sun)
- Daily drift monitoring (same pattern)
- Zero blue incidents expected (local model variance within ±5%)
- Any yellow incidents logged, investigated same day
- Hermes checkpoint history accumulates

### July 11–12 (Mon–Tue)
- Phase 4 POC readiness audit
  - Harvester CLI confirmed working (Agent-Reach integration)
  - MiMo backend confirmed working (OpenAI-compatible API)
  - Harvester → Drift Monitor hook wired (pause/resume gates configured)
- AGENTS.md final update (drift monitoring section + Phase 4 reference)

### July 15 (Fri)
- v2.1 reveal narrative locked (ready for July 16 Phase 4 POC start)

### July 16+ (Sat+)
- Phase 4 POC begins
- Harvester detects trends (Twitter platform test)
- Signals route through social_voice → memory_ops → Hermes
- Drift monitor watches live (real-time or batched, TBD)
- v2.1 reveal posts publish (pre-scheduled or live thread, TBD)

## Recent Checkpoints

- June 8 content scheduled: 'Self-Knowledge Pivot' series for LinkedIn and X.
- Blotato account IDs updated in `config/blotato-accounts.json`.
- June 4 content scheduled/published: M Solo Agent series.
- M Solo Agent Scout drop processed into three drafts, then moved to published queue status.
- June 3 content scheduled/published: Catch-Up Checkpoint series.
- June 2 GitNexus refresh policy batched and fresh-idea token anxiety captured.
- June 1 Road4AI posts confirmed published, missed approved posts reconciled, and May 27 posts filed as published.
- May 30 SkillOpt benchmark runner hardened, free-tier Gemini runner swapped in, and T-001/T-002 governance tasks approved.
- May 29 SkillOpt validation report, v2.1 roadmap, and standard OpenAI implementation added.
- May 28 Google Workspace plugin imported and agent spawn command launched.
- May 27 post-reveal retro sequence scheduled, telemetry initialized, and architecture hardening synchronized.
- May 26 Hermes standalone extraction shipped into `road4ai-hermes`, v0.1.0 changelog added, and reveal-day content promoted/scheduled.
- May 21 content pipeline finalized, struggle ratio verified, and Self-Knowledge Loop trajectories checked.
- May 19 reveal runbook, reply strategy, safety layers, and final reveal momentum added.
- May 13-14 Hermes v2.0 distributed substrate, self-knowledge index, Hermes-CrewAI bridge, strict governance lock, and checkpoint v2.0 flow established.

## Deferred Evaluations

### Memanto Semantic Memory (evaluated June 2026)

**Decision:** Defer to Phase 5 RFC. Do not integrate until Harvester CLI + MiMo POC is validated and shipped.

**What it is:** Memanto (moorcheh-ai/memanto) is a semantic memory agent that provides `remember`, `recall`, and `answer` operations. Built on Moorcheh, an information-theoretic search engine with sub-90ms retrieval, no vector DB, no indexing delay. 1,472 stars, MIT, Python. Supports Claude Code, Cursor, Codex, and 14+ other agents.

**Why defer:**
- Hermes is working. Git checkpoints are adequate for 1-3 agents with human-in-the-loop.
- Road4AI philosophy: "habits before infrastructure." Hermes is a habit. Memanto is infrastructure (Docker container, running service).
- Phase 4 has a hard deadline (July 15, 2026). Ship the POC first, then measure whether semantic memory is a bottleneck.
- The locked architectural decisions say "no cloud-only dependencies in the main path." Memanto on-prem respects this, but adds a Docker dependency.

**Revisit threshold:** 5+ concurrent autonomous agents, or 1,000+ checkpoints where `git log --grep` becomes unwieldy.

**Shorter-term alternative if grep becomes slow before Phase 5:** Add a lightweight metadata index to Hermes (JSON summary of each checkpoint's agents, timestamp, outcome) rather than swapping engines. Keeps the habit intact.

**Project health:** Active maintenance (1.4k stars, MIT, 413 forks). No risk of disappearance if wanted in 6 months.

---

### OmniRoute Multi-Provider AI Gateway (evaluated July 2026)

**Decision:** Deferred, not adopted.

**What it is:** Self-hosted local proxy, one OpenAI-compatible endpoint routing across 230+ LLM providers (50+ free tiers), auto-fallback, MIT licensed, no cloud in request path.

**Why defer:**
- No current need. MiMo/qwen2.5-coder:14b via Ollama already solves local-first inference for Phase 4.
- OmniRoute solves a cloud-API rate-limit problem Road4AI doesn't have.
- Large, fast-moving, single-maintainer-heavy codebase (MITM proxy, OAuth, credential storage). More attack surface than current stack for no active benefit.

**Revisit trigger:** If a future phase requires cloud-provider fallback that Ollama/MiMo can't cover, or multi-provider routing becomes a real need.

**Source:** github.com/diegosouzapw/OmniRoute (npm install -g omniroute)

---

## Active Constraints

- `AGENTS.md` requires explicit human approval before edits.
- Queue writes must pass the four-check dedup gate.
- `state/current-queue.json` currently uses a top-level `queue` array; preserve that shape.
- Only the user moves content into `drafts/approved/`.
- Public posts must not include copy-pasteable exploit strings.
- X posts must be strictly under 280 characters each.

## Active Governance Backlog

1. Audit Road4AI skills against the standardized `SKILL.md` structure.
2. Consider filesystem-level protection for `AGENTS.md`.
3. Add broader hook coverage for publishing workflows if the deterministic sanitizer needs stronger enforcement.
4. Decide whether to consolidate overlapping content pipeline skills after Phase 3 extraction.
5. Phase 5 RFC: evaluate Memanto semantic memory if scale threshold is reached (5+ concurrent agents, 1k+ checkpoints).
6. Phase 5 RFC: evaluate OmniRoute multi-provider AI gateway if cloud-provider fallback or multi-provider routing becomes a real need.

## Content Pipeline Pattern

The five-agent content pipeline is the canonical Road4AI content workflow:

1. Chief of Staff selects and coordinates the work.
2. Trend Researcher gathers weak signals.
3. Voice-Match Ideator converts signals into Road4AI-native angles.
4. Format Selector maps ideas to platform and cadence.
5. Content Scout extracts structured knowledge from transcripts, URLs, or text.

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
