# Wayfinder Map: Phase 5 Tool Evaluations

## Destination
A Phase 5 tool-adoption decision, or an explicit "not yet, re-evaluate after Phase 4 usage data" close-out for each candidate.

## Decisions so far
- memanto: Deferred. Hermes works at current scale (1-3 agents, human-in-the-loop). Memanto adds Docker dependency. Revisit at 5+ concurrent autonomous agents or 1,000+ checkpoints. (resolved June 2026)
- omniroute: Deferred. Ollama already solves local-first inference. Large attack surface for no active benefit. Revisit if future phase needs cloud-provider fallback. (resolved July 2026)
- cc-mirror: Deferred. Evaluate-document-defer. Zero adoption data to justify integration. (resolved July 2026)
- gpt-oss-120b: Deferred. Evaluate-document-defer. Zero adoption data to justify integration. (resolved July 2026)
- project-graveyard: Deferred. Evaluate-document-defer. Zero adoption data to justify integration. (resolved July 2026)

## Frontier (open, unblocked, unclaimed)
(empty — moratorium active until Phase 4 has real usage data)

## Blocked
(empty)

## Fog of war (anticipated, not yet ticketed)
- Phase 4 POC lift condition: signal must traceably inform a content decision (not just signal → post). Traceability requires citation (title + brief date + confidence score). Positive decisions only. No retroactive credit. Until this lifts, no new tool evals.
- google-agents-cli was evaluated July 20, 2026 and rejected (requires Google Cloud/Gemini API key, targets Cloud Run/GKE deployment). Its eval methodology (two-phase LLM-as-judge) is worth revisiting for Karen internals, but deferred until Signal Harvester cutover and Karen gap on harvester scripts are closed.
