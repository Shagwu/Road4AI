# road4ai-hermes

**The high-performance, distributed memory substrate for agent swarms.**

`road4ai-hermes` is a standalone memory bridge extracted from the [Road4AI](https://github.com/Shagwu/Road4AI) project. It provides a scalable, ChromaDB-backed architecture capable of supporting 100+ concurrent agents with sub-60ms retrieval speeds.

## 🏗️ Core Features
- **Distributed Scale:** Move past SQLite WAL-mode lock bottlenecks.
- **Linear Relevance Scoring:** Built-in `1.0 - sqrt(dist)` logic for intuitive agent signals.
- **Lifecycle Management:** Automatic TTL, archiving, and idempotent pruning.
- **CrewAI Native:** First-class support for `crewai.knowledge.storage`.

## 🚀 Installation

```bash
pip install road4ai-hermes
```

For local embedding support:
```bash
pip install "road4ai-hermes[local]"
```

## 📖 Quick Start

```python
from road4ai_hermes.bridge import MemoryBridgeV2

# Initialize (Default: ./chroma_db)
bridge = MemoryBridgeV2()

# Store a memory
memory_id = bridge.store(
    text="Architectural decision: Use ChromaDB.",
    vector=[0.1, 0.2, ...],
    metadata={"type": "decision"}
)

# Search
results = bridge.search(query_vector=[...], k=1)
```

## ⚖️ License
MIT. Built by the Road4AI movement. 🔧
