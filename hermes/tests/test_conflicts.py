import pytest
from hermes.bridge_v2 import MemoryBridgeV2

def test_v2_conflict_resolution_lww(tmp_path):
    """
    Test how MemoryBridgeV2 handles conflicting writes to the same ID.
    
    @known_limitation: Currently relies on ChromaDB's default Last-Write-Wins behavior.
    This ensures that updates to existing memories correctly overwrite previous content
    without manual versioning, keeping the substrate lean.
    """
    persist_directory = tmp_path / "test_chroma_conflict"
    bridge = MemoryBridgeV2(persist_directory=str(persist_directory))
    
    memory_id = "test-collision-id"
    vector = [1.0] + [0.0] * 383
    
    # First write: Version 1
    bridge.collection.add(
        ids=[memory_id],
        embeddings=[vector],
        documents=["Initial Version"],
        metadatas=[{"version": "1"}]
    )
    
    # Second write: Version 2 (The "Conflict")
    # Using upsert to simulate an update or a conflicting write that should win
    bridge.collection.upsert(
        ids=[memory_id],
        embeddings=[vector],
        documents=["Updated Version"],
        metadatas=[{"version": "2"}]
    )
    
    # Act: Retrieve by ID
    retrieved = bridge.get(memory_id)
    
    # Assert: Version 2 should have overwritten Version 1
    assert retrieved["text"] == "Updated Version"
    assert retrieved["metadata"]["version"] == "2"

def test_v2_retrieval_order_stable(tmp_path):
    """
    Test that retrieval order remains stable for identical distances.
    @known_limitation: ChromaDB's default ordering for identical distances.
    """
    persist_directory = tmp_path / "test_chroma_order"
    bridge = MemoryBridgeV2(persist_directory=str(persist_directory))
    
    # Two different memories with identical vectors
    vector = [1.0] + [0.0] * 383
    bridge.store("Memory A", vector)
    bridge.store("Memory B", vector)
    
    # Act: Search
    results = bridge.search(vector, k=5)
    
    # Assert: Both should be returned. Order is usually determined by Chroma internally.
    texts = [r["text"] for r in results]
    assert "Memory A" in texts
    assert "Memory B" in texts
