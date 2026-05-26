import pytest
import os
import shutil
import numpy as np
from road4ai_hermes.crewai import HermesStorage

def test_hermes_storage_lifecycle():
    persist_directory = "./test_chroma_crewai"
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
    
    config = {
        "persist_directory": persist_directory,
        "collection_name": "test_crewai_knowledge"
    }
    
    storage = HermesStorage(config=config)
    
    # Test Data
    text = "Road4AI uses Hermes for persistent memory."
    vector = [0.1] * 384
    metadata = {"category": "architecture"}
    
    # Save
    storage.save(text, vector, metadata=metadata)
    
    # Search
    # Using a similar vector to ensure retrieval
    results = storage.search(query_vector=[0.11] * 384, limit=1, threshold=0.5)
    
    assert len(results) == 1
    assert results[0]["content"] == text
    assert results[0]["metadata"]["category"] == "architecture"
    assert "score" in results[0]
    
    # Delete
    # Note: We need the ID. In the real flow, save() returns the ID.
    # But since we're using uuid inside store(), let's verify save returns it.
    
    # Cleanup
    shutil.rmtree(persist_directory)

def test_hermes_storage_reset():
    persist_directory = "./test_chroma_reset"
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
    
    config = {"persist_directory": persist_directory}
    storage = HermesStorage(config=config)
    
    storage.save("Test reset", [0.1]*384)
    storage.reset()
    
    # Verify collection is empty
    results = storage.search([0.1]*384, limit=1)
    assert len(results) == 0
    
    shutil.rmtree(persist_directory)
