---
name: hermes-checkpoint
description: >
  Enforces structured commit metadata for the Road4AI project using the [hermes-context] block.
  Used to track decisions, remaining tasks, and confidence across agent sessions.
---

# Hermes Checkpoint Protocol

Use this skill when preparing a git commit to ensure architectural alignment and context preservation.

## Commit Metadata Schema

Every commit should include a `[hermes-context]` block in the body:

```
[hermes-context]
Decisions: [Key architectural or strategic choices made]
Remaining: [Immediate next steps or pending tasks]
Tried: [What was attempted that failed or was discarded]
Confidence: [low | medium | high]
Context_type: [build | content | system | research]
Agent: [agent-id]
[/hermes-context]
```

## Field Definitions

- **Decisions**: Why we chose X over Y.
- **Remaining**: What the next agent needs to do immediately.
- **Tried**: Failed experiments to prevent work duplication.
- **Context_type**:
    - `build`: Code changes, refactors, new features.
    - `content`: `inbox.md`, `ideas.md`, drafting, marketing.
    - `system`: Environment config, MCP setup, infrastructure.
    - `research`: Speculative investigation, deep dives.
- **Agent**: The ID of the agent performing the task.
