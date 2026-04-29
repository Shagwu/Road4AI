# CrewAI Hermes Integration Implementation Plan

> **For Claude:** Use `/Users/shagwu/Downloads/Road4AI-main/.agents/skills/writing-plans/SKILL.md` to implement this plan task-by-task.

**Goal:** Wire CrewAI agents to HermesBridge for semantic memory persistence.

**Architecture:** Create a `HermesStorage` class in `hermes/crewai_storage.py` that inherits from CrewAI's `BaseRAGStorage`. This class will wrap `MemoryBridge` to provide a persistent, SQLite+HNSW backed memory for CrewAI agents.

**Tech Stack:** Python, CrewAI, HermesBridge (SQLite, hnswlib, numpy).

---

### Task 1: Create HermesStorage Component

**Files:**
- Create: `hermes/crewai_storage.py`
- Test: `hermes/tests/test_crewai_integration.py`

**Step 1: Write the failing test**

```python
import pytest
import os
import numpy as np
from hermes.crewai_storage import HermesStorage
from crewai.agents.agent_builder.base_agent import PlanningConfig # placeholder if needed

def test_hermes_storage_save_and_search():
    # Setup
    db_path = "test_hermes_crewai.db"
    index_path = "test_hermes_crewai.index"
    if os.path.exists(db_path): os.remove(db_path)
    if os.path.exists(index_path): os.remove(index_path)

    storage = HermesStorage(
        type="short_term",
        db_path=db_path,
        index_path=index_path,
        dimension=3 # small for testing
    )

    # Act
    test_text = "CrewAI is awesome"
    # In a real scenario, BaseRAGStorage._generate_embedding would be called
    # For this test, we'll mock the embedder or verify the flow
    storage.save(test_text, metadata={"agent": "test_agent"})
    
    results = storage.search("CrewAI", limit=1)

    # Assert
    assert len(results) > 0
    assert results[0]["context"] == test_text
    assert results[0]["metadata"]["agent"] == test_agent

    # Cleanup
    if os.path.exists(db_path): os.remove(db_path)
    if os.path.exists(index_path): os.remove(index_path)
```

**Step 2: Run test to verify it fails**

Run: `pytest hermes/tests/test_crewai_integration.py`
Expected: FAIL with "ModuleNotFoundError: No module named 'hermes.crewai_storage'"

**Step 3: Write minimal implementation**

Implement `HermesStorage` in `hermes/crewai_storage.py` wrapping `MemoryBridge`.

**Step 4: Run test to verify it passes**

Run: `pytest hermes/tests/test_crewai_integration.py`
Expected: PASS

**Step 5: Commit**

```bash
git add hermes/crewai_storage.py hermes/tests/test_crewai_integration.py
git commit -m "feat(hermes): add HermesStorage for CrewAI integration"
```

### Task 2: Integration with CrewAI Agent

**Files:**
- Modify: `main.py` or create a new `integration_demo.py`
- Test: `hermes/tests/test_agent_memory.py`

**Step 1: Write the failing test**

Verify that an agent with `memory=True` and our custom storage correctly uses HermesBridge.

**Step 2: Run test to verify it fails**

**Step 3: Update Agent configuration**

**Step 4: Run test to verify it passes**

**Step 5: Commit**
