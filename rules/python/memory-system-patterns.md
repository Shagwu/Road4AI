# Memory System Patterns

Road4AI memory work should preserve human control and traceability.

## Principles

- Memory is a substrate, not an authority.
- Retrieval should be inspectable.
- Forgetting and expiration are product features, not defects.
- Agent autonomy must remain bounded by explicit contracts.

## Required Boundaries

- Do not let memory mutate operating contracts automatically.
- Do not let agents approve their own governance changes.
- Treat self-healing rules as human-review events unless explicitly authorized.
- Log memory-driven decisions when they affect queue state, content approval, or publishing.

