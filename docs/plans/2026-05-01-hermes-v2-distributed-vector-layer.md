# Hermes v2.0 Distributed Vector Layer Implementation Plan

> **For Claude:** Use `${SUPERPOWERS_SKILLS_ROOT}/skills/collaboration/executing-plans/SKILL.md` to implement this plan task-by-task.

**Goal:** Migrate Hermes from local HNSW to ChromaDB for distributed vector storage while maintaining V1 compatibility.

**Architecture:** Implement `MemoryBridgeV2` using ChromaDB as the backend. It will support both local persistence (file-based) and a distributed server-client model (HTTP). A thin compatibility layer will ensure V1 callers can migrate seamlessly.

**Tech Stack:** ChromaDB, NumPy, Pydantic, Pytest.

---

### Task 1: Environment Setup & Dependency Verification

**Files:**
- Modify: `requirements.txt`

**Step 1: Update dependencies**

Add `chromadb>=0.4.0` to `requirements.txt`.

```text
chromadb>=0.4.0
chroma-hnswlib==0.7.6
hnswlib==0.8.0
sentence-transformers==5.1.0
```

**Step 2: Commit**

```bash
git add requirements.txt
git commit -m "chore: add chromadb dependency for Hermes v2.0"
```

---

### Task 2: Implement MemoryBridgeV2 Core

**Files:**
- Create: `hermes/bridge_v2.py`
- Test: `hermes/tests/test_bridge_v2.py`

**Step 1: Write the failing test for initialization and storage**

```python
import pytest
import os
import shutil
import numpy as np
from hermes.bridge_v2 import MemoryBridgeV2

def test_v2_lifecycle():
    persist_directory = "./test_chroma_db"
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
    
    bridge = MemoryBridgeV2(persist_directory=persist_directory, collection_name="test_memories")
    
    memory_text = "Distributed intelligence is the goal."
    memory_vector = [0.1] * 384
    
    memory_id = bridge.store(memory_text, memory_vector, metadata={"source": "test"})
    
    retrieved = bridge.get(memory_id)
    assert retrieved["text"] == memory_text
    assert retrieved["metadata"]["source"] == "test"
    
    # Cleanup
    shutil.rmtree(persist_directory)
```

**Step 2: Run test to verify it fails**

Run: `pytest hermes/tests/test_bridge_v2.py -v`
Expected: FAIL (Module not found)

**Step 3: Implement minimal MemoryBridgeV2**

```python
import chromadb
from chromadb.config import Settings
import uuid

class MemoryBridgeV2:
    def __init__(self, persist_directory="./chroma_db", collection_name="memories"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def store(self, text, vector, metadata=None):
        memory_id = str(uuid.uuid4())
        self.collection.add(
            embeddings=[vector],
            documents=[text],
            metadatas=[metadata or {}],
            ids=[memory_id]
        )
        return memory_id

    def get(self, memory_id):
        result = self.collection.get(ids=[memory_id])
        if result["ids"]:
            return {
                "text": result["documents"][0],
                "vector": result["embeddings"][0] if result["embeddings"] else None,
                "metadata": result["metadatas"][0]
            }
        return None
```

**Step 4: Run test to verify it passes**

Run: `pytest hermes/tests/test_bridge_v2.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add hermes/bridge_v2.py hermes/tests/test_bridge_v2.py
git commit -m "feat: implement core MemoryBridgeV2 with ChromaDB"
```

---

### Task 3: Implement Semantic Search in V2

**Files:**
- Modify: `hermes/bridge_v2.py`
- Modify: `hermes/tests/test_bridge_v2.py`

**Step 1: Write the failing search test**

```python
def test_v2_search():
    persist_directory = "./test_chroma_search"
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
    
    bridge = MemoryBridgeV2(persist_directory=persist_directory)
    bridge.store("apple", [1.0] + [0.0]*383)
    bridge.store("banana", [0.0] + [1.0]*383)
    
    results = bridge.search([0.1, 0.9] + [0.0]*382, k=1)
    assert len(results) == 1
    assert results[0]["text"] == "banana"
    
    shutil.rmtree(persist_directory)
```

**Step 2: Run test to verify it fails**

Run: `pytest hermes/tests/test_bridge_v2.py::test_v2_search -v`
Expected: FAIL (AttributeError: 'MemoryBridgeV2' object has no attribute 'search')

**Step 3: Implement search method**

```python
    def search(self, query_vector, k=5):
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=k
        )
        
        output = []
        for i in range(len(results["ids"][0])):
            output.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })
        return output
```

**Step 4: Run test to verify it passes**

Run: `pytest hermes/tests/test_bridge_v2.py::test_v2_search -v`
Expected: PASS

**Step 5: Commit**

```bash
git add hermes/bridge_v2.py hermes/tests/test_bridge_v2.py
git commit -m "feat: add semantic search to MemoryBridgeV2"
```

---

### Task 4: Implementation of V1 Compatibility Layer

**Files:**
- Modify: `hermes/bridge_v2.py`

**Step 1: Add V1-style method aliases**

Ensure `MemoryBridgeV2` can be used as a drop-in replacement for `MemoryBridge` where possible.

```python
    # V1 Aliases
    def get_by_id(self, memory_id):
        return self.get(memory_id)
```

**Step 2: Commit**

```bash
git add hermes/bridge_v2.py
git commit -m "feat: add V1 compatibility aliases to MemoryBridgeV2"
```

---

### Task 5: Integration Check with Road4AI-COS

**Files:**
- Modify: `road4ai-cos/app/tools.py`

**Step 1: Update triage_queue to use V2 if available**

**Step 2: Commit**

```bash
git add road4ai-cos/app/tools.py
git commit -m "feat: integrate MemoryBridgeV2 into road4ai-cos triage"
```
