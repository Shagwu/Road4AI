# Phase 5 RFC Log

Evaluations of tools considered for Phase 5+ adoption. All entries follow the evaluate-document-defer pattern: assess fit, log findings, defer until a concrete trigger is hit.

**Moratorium**: No new Phase 5 evaluations until Phase 4 has real usage data (rule from July 15 retro, enforced via open-items.md Item 4).

---

## 1. Memanto Semantic Memory (evaluated June 2026) — DEFERRED

**What:** moorcheh-ai/memanto — semantic memory agent (`remember`, `recall`, `answer`). MIT, on-prem via Docker+Ollama, sub-90ms retrieval, no vector DB.

**Why deferred:** Hermes works at current scale (1-3 agents, human-in-the-loop). Memanto adds Docker dependency. Road4AI philosophy: habits before infrastructure.

**Revisit trigger:** 5+ concurrent autonomous agents, or 1,000+ checkpoints where `git log --grep` becomes unwieldy.

**Source:** WORKING-CONTEXT.md § Deferred Evaluations

---

## 2. OmniRoute Multi-Provider AI Gateway (evaluated July 2026) — DEFERRED

**What:** Self-hosted local proxy, 230+ LLM providers, MIT, no cloud in request path.

**Why deferred:** No current need. Ollama already solves local-first inference. Large attack surface for no active benefit.

**Revisit trigger:** Future phase requires cloud-provider fallback that Ollama/MiMo can't cover.

**Source:** WORKING-CONTEXT.md § Deferred Evaluations

---

## 3. cc-mirror — DEFERRED

**What:** (Details from July evaluation cycle)

**Why deferred:** Evaluate-document-defer outcome. Zero adoption data to justify integration.

**Source:** open-items.md Item 4

---

## 4. gpt-oss-120b — DEFERRED

**What:** (Details from July evaluation cycle)

**Why deferred:** Evaluate-document-defer outcome. Zero adoption data to justify integration.

**Source:** open-items.md Item 4

---

## 5. Project Graveyard — DEFERRED

**What:** (Details from July evaluation cycle)

**Why deferred:** Evaluate-document-defer outcome. Zero adoption data to justify integration.

**Source:** open-items.md Item 4

---

## 6. google-agents-cli (evaluated July 20, 2026) — DEFERRED

**What:** `github.com/google/agents-cli`, `uvx google-agents-cli setup`. Google's ADK toolchain for Gemini Enterprise Agent Platform — CLI + 7 coding-agent skills (workflow, ADK code, scaffold, eval, deploy, publish, observability) injected into Claude Code/Codex/Antigravity.

**Why rejected:** Requires Google Cloud/Gemini API key auth and targets Cloud Run/GKE/Agent Runtime deployment, none of which Road4AI needs. Would run a parallel agent-lifecycle framework alongside Hermes/Karen/AGENTS.md rather than feeding them.

**Pattern-level notes (no code/tool adoption):**

- **Eval methodology:** Their `eval generate` (run agent on dataset → traces) / `eval grade` (LLM-as-judge against rubrics: INSTRUCTION_FOLLOWING, HALLUCINATION, TOOL_USE_QUALITY) is a cleaner two-phase split than Karen's current scoring. Worth considering for Karen's internals — **deferred until after Signal Harvester cutover and Karen gap on harvester scripts are closed**, to avoid a second structural change in flight (PR #2 pattern risk).
- **Skills packaging:** Their `npx skills add` (install once, discovered by any coding agent) validates the `.agents/skills/` approach already in use. No action needed.

**Re-evaluate only if:** Future phase needs actual Google Cloud deployment, which the local-first/Ollama-first architecture doesn't currently require.

---

*Compiled by CoS. Not a Karen-reviewed artifact.*
