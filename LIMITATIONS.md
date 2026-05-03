# Known Limitations

This document tracks known architectural tradeoffs, edge cases, and design choices in the Road4AI system.

## Hermes Memory Layer (v2.0)

### Last-Write-Wins (LWW) Resolution
Conflicting updates to the same memory ID (collision or intentional update) are resolved using a Last-Write-Wins strategy. 
- **Tradeoff:** No built-in version history for individual memory entries.
- **Benefit:** Keeps the vector substrate lean and prevents state bloating during long-running swarm sessions.

### Retrieval Order Stability
For memories with identical similarity distances (e.g., duplicate embeddings or identical vectors), retrieval order is stable within a session but is determined by ChromaDB's internal indexing rather than semantic priority.

### Local-First File Locks
In persistent mode, Hermes relies on local filesystem locks.
- **Risk:** Accessing the same `persist_directory` from multiple uncoordinated OS processes may cause temporary degradation or initialization errors.
- **Mitigation:** Use the `MemoryBridgeV2` graceful degradation logic implemented in Task 4.

## System Hooks

### Path Sensitivity
The context-mode hook system (`beforetool.mjs`) is sensitive to global npm installation paths. If hooks fail, ensure paths in `.gemini/settings.json` point to the `dist/hooks` directory of the installed `context-mode` package.

## Content Orchestration System (COS)

### Degraded Memory Mode
If the Hermes memory layer is unreachable, the COS tool falls back to "Degraded Mode."
- **Effect:** Semantic recall is disabled, but metadata-based triage and drafting remain functional.
