import pytest
import os
import sys
import numpy as np

# Add the project root to sys.path to allow importing from hermes
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from road4ai_hermes.legacy import MemoryBridge
except ImportError:
    # This is expected to fail initially in TDD
    MemoryBridge = None

def test_memory_persistence_lifecycle():
    if MemoryBridge is None:
        pytest.fail("MemoryBridge class not implemented or cannot be imported")

    # Setup
    db_path = "test_memory.db"
    index_path = "test_hnsw.index"
    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(index_path):
        os.remove(index_path)
    
    bridge = MemoryBridge(db_path=db_path, index_path=index_path, dimension=3)
    
    # Act
    memory_text = "This is a test memory"
    memory_vector = [0.1, 0.2, 0.3]
    memory_id = bridge.store(memory_text, memory_vector)
    retrieved = bridge.get(memory_id)
    
    # Assert
    assert retrieved["text"] == memory_text
    # HNSW stores vectors as float32, so we need to compare with some tolerance or cast
    assert np.allclose(retrieved["vector"], memory_vector, atol=1e-6)
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(index_path):
        os.remove(index_path)

def test_memory_semantic_search():
    if MemoryBridge is None:
        pytest.fail("MemoryBridge class not implemented or cannot be imported")

    # Setup
    db_path = "test_search.db"
    index_path = "test_search.index"
    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(index_path):
        os.remove(index_path)
    
    bridge = MemoryBridge(db_path=db_path, index_path=index_path, dimension=3)
    
    # Act
    bridge.store("apple", [1.0, 0.0, 0.0])
    bridge.store("banana", [0.0, 1.0, 0.0])
    bridge.store("cherry", [0.0, 0.0, 1.0])
    
    # Search for something close to banana
    results = bridge.search([0.1, 0.9, 0.1], k=1)
    
    # Assert
    assert len(results) == 1
    assert results[0]["text"] == "banana"
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(index_path):
        os.remove(index_path)
