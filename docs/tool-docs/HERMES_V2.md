# Hermes v2.0: Distributed Memory Substrate

Hermes v2.0 is the high-performance, distributed memory substrate for the Road4AI agent stack. It replaces the local-only HNSW setup from V1 with a scalable ChromaDB-backed architecture capable of supporting 100+ concurrent agents.

## Narrative Positioning

- **v2.0 — Hermes remembers:** distributed memory, lifecycle controls, and a standalone substrate.
- **v2.1 — Hermes learns:** SkillOpt integration moves from local validation into governed optimization runs for selected Road4AI skills.
- **v2.2 — Hermes scales:** community contribution paths expand once the memory and learning loops have safe operating boundaries.

SkillOpt validation is intentionally treated as a v2.1 proof point, not the v2.0 headline. The v2.0 reveal should stay focused on memory; the validation report is preserved separately for the v2.1 launch narrative.

## 🏗️ Architecture

Hermes v2.0 follows a "Distributed Pivot" strategy:
- **Local Persistence:** Uses ChromaDB's `PersistentClient` for zero-cost, local-first storage.
- **Distributed Ready:** Supports `HttpClient` for multi-node agent coordination.
- **Linear Scoring:** Implements `1.0 - sqrt(L2_distance)` to provide intuitive relevance signals.
- **Lifecycle Management:** Built-in support for TTL (Time-to-Live), archiving, and pruning.

## 🚀 Getting Started

### Installation
Ensure you have the required dependencies:
```bash
pip install road4ai-hermes
```

### Basic Usage (Python)
```python
from road4ai_hermes.bridge import MemoryBridgeV2

# Initialize (Default: ./chroma_db)
bridge = MemoryBridgeV2()

# Store a memory (requires a 384-dim vector for all-MiniLM-L6-v2)
memory_id = bridge.store(
    text="The architectural decision to use ChromaDB was made on 2026-05-01.",
    vector=[0.1, 0.2, ...],
    metadata={"category": "decision", "source": "docs/plans/..."}
)

# Search with relevance signal
results = bridge.search(query_vector=[...], k=1, threshold=0.7)
for res in results:
    print(f"Match: {res['text']}")
    print(f"Score: {res['relevance_signal']['score']}")
```

## 🛠️ The `ask` CLI Tool

The `ask` command is a high-signal terminal interface for querying the system's self-knowledge index.

### Usage
```bash
./ask "Why did we move to ChromaDB?"
```

### Output Format
```text
ROAD4AI SELF-KNOWLEDGE SYSTEM [ONLINE]
--------------------------------------
> QUERY: Why did we move to ChromaDB?
> LATENCY: 54ms
> SOURCE: docs/plans/2026-05-01-hermes-v2-distributed-vector-layer.md | CATEGORY: plan

We migrated to solve the 'Scale Wall.' While SQLite + local HNSW worked for 5 agents, 
it hit a WAL-mode lock bottleneck at 100+ concurrent write-heavy agents.
```

## 📚 API Reference

### `MemoryBridgeV2`

#### `__init__(persist_directory="./chroma_db", collection_name="memories", host=None, port=None)`
Initializes the bridge. If `host` and `port` are provided, it connects to a remote ChromaDB server.

#### `store(text, vector, metadata=None, expires_at=None, ttl_seconds=None)`
Persists a memory.
- `expires_at`: `datetime` object or ISO 8601 string.
- `ttl_seconds`: Duration in seconds before the memory is eligible for archiving.

#### `search(query_vector, k=5, include_archived=False, threshold=0.7)`
Performs a semantic search.
- Returns a list of matches with a `relevance_signal` object.
- `threshold`: Minimum score (0.0 to 1.0) to be considered "relevant".

#### `archive_expired(now=None)`
Moves memories with passed expiration dates to `archived` status.

#### `prune_archived(now=None, retention_seconds=0)`
Permanently deletes archived memories that have exceeded the retention window.

---
© 2026 Road4AI. Built, not just prompted. 🔧
