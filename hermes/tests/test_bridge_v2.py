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
