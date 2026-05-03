import pytest
import numpy as np
import math
from datetime import datetime, timezone
from hermes.bridge_v2 import MemoryBridgeV2

def test_v2_relevance_signal_logic(tmp_path):
    persist_directory = tmp_path / "test_chroma_relevance"
    bridge = MemoryBridgeV2(persist_directory=str(persist_directory))
    
    dim = 384
    
    # Case 1: Score 1.0 (Distance 0.0)
    v_perfect = [1.0] + [0.0] * (dim - 1)
    bridge.store("Perfect", v_perfect)
    
    # Case 2: Score 0.8 (Distance 0.04 because squared L2)
    # 1.0 - sqrt(0.04) = 1.0 - 0.2 = 0.8
    v_good = [0.8] + [0.0] * (dim - 1)
    bridge.store("Good", v_good)
    
    # Case 3: Score 0.6 (Distance 0.16)
    # 1.0 - sqrt(0.16) = 1.0 - 0.4 = 0.6
    v_weak = [0.6] + [0.0] * (dim - 1)
    bridge.store("Weak", v_weak)
    
    # Case 4: Score 0.4 (Distance 0.36)
    v_none = [0.4] + [0.0] * (dim - 1)
    bridge.store("None", v_none)
    
    query = [1.0] + [0.0] * (dim - 1)
    
    # Search with threshold 0.7
    # Relevant: score >= 0.7
    # Borderline: 0.55 <= score < 0.7
    # Irrelevant: score < 0.55
    results = bridge.search(query, k=10, threshold=0.7)
    
    perfect = next(r for r in results if r["text"] == "Perfect")
    assert perfect["relevance_signal"]["status"] == "relevant"
    assert perfect["relevance_signal"]["score"] == pytest.approx(1.0)
    
    good = next(r for r in results if r["text"] == "Good")
    assert good["relevance_signal"]["status"] == "relevant"
    assert good["relevance_signal"]["score"] == pytest.approx(0.8)
    
    weak = next(r for r in results if r["text"] == "Weak")
    assert weak["relevance_signal"]["status"] == "borderline"
    assert weak["relevance_signal"]["score"] == pytest.approx(0.6)
    
    none = next(r for r in results if r["text"] == "None")
    assert none["relevance_signal"]["status"] == "irrelevant"
    assert none["relevance_signal"]["score"] == pytest.approx(0.4)

def test_v2_relevance_signal_threshold_override(tmp_path):
    persist_directory = tmp_path / "test_chroma_threshold"
    bridge = MemoryBridgeV2(persist_directory=str(persist_directory))
    
    dim = 384
    v = [0.6] + [0.0] * (dim - 1)
    bridge.store("Target", v)
    
    query = [1.0] + [0.0] * (dim - 1)
    
    # Default threshold is 0.7. Score 0.6 is borderline.
    res1 = bridge.search(query, threshold=0.7)
    assert res1[0]["relevance_signal"]["status"] == "borderline"
    
    # Override threshold to 0.5. Score 0.6 is relevant.
    res2 = bridge.search(query, threshold=0.5)
    assert res2[0]["relevance_signal"]["status"] == "relevant"
    
    # Override threshold to 0.8. Score 0.6 is irrelevant.
    res3 = bridge.search(query, threshold=0.8)
    assert res3[0]["relevance_signal"]["status"] == "irrelevant"
