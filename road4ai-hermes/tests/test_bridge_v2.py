import pytest
import os
import shutil
import numpy as np
from datetime import datetime, timedelta, timezone
from road4ai_hermes.bridge import MemoryBridgeV2


def _iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

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

def test_v2_search():
    persist_directory = "./test_chroma_search"
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
    
    bridge = MemoryBridgeV2(persist_directory=persist_directory)
    bridge.store("apple", [1.0] + [0.0]*383)
    bridge.store("banana", [0.0, 1.0] + [0.0]*382)
    
    results = bridge.search([0.1, 0.9] + [0.0]*382, k=1)
    assert len(results) == 1
    assert results[0]["text"] == "banana"
    
    shutil.rmtree(persist_directory)

def test_v2_v1_compatibility():
    persist_directory = "./test_chroma_v1_compat"
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
    
    bridge = MemoryBridgeV2(persist_directory=persist_directory)
    memory_id = bridge.store("compatibility test", [0.5] * 384)
    
    # Test alias
    retrieved = bridge.get_by_id(memory_id)
    assert retrieved["text"] == "compatibility test"
    
    shutil.rmtree(persist_directory)


def test_v2_writes_lifecycle_metadata(tmp_path):
    persist_directory = tmp_path / "test_chroma_lifecycle_metadata"
    bridge = MemoryBridgeV2(persist_directory=str(persist_directory))

    expires_at = "2026-05-01T12:00:00Z"
    memory_id = bridge.store(
        "Lifecycle metadata test",
        [0.2] * 384,
        metadata={"source": "test"},
        expires_at=expires_at,
    )

    retrieved = bridge.get(memory_id, include_archived=True)

    assert retrieved["metadata"]["source"] == "test"
    assert retrieved["metadata"]["status"] == "active"
    assert retrieved["metadata"]["expires_at"] == expires_at
    assert retrieved["metadata"]["archived_at"] is None


def test_v2_archive_expired_is_idempotent(tmp_path):
    persist_directory = tmp_path / "test_chroma_archive_expired"
    bridge = MemoryBridgeV2(persist_directory=str(persist_directory))
    now = datetime(2026, 5, 1, 12, 0, tzinfo=timezone.utc)

    expired_id = bridge.store(
        "expired memory",
        [1.0] + [0.0] * 383,
        expires_at=_iso_utc(now - timedelta(hours=1)),
    )
    active_id = bridge.store(
        "active memory",
        [0.0, 1.0] + [0.0] * 382,
        expires_at=_iso_utc(now + timedelta(hours=1)),
    )

    first_run = bridge.archive_expired(now=now)
    second_run = bridge.archive_expired(now=now)

    assert first_run == 1
    assert second_run == 0
    assert bridge.get(expired_id) is None
    archived = bridge.get(expired_id, include_archived=True)
    assert archived["metadata"]["status"] == "archived"
    assert archived["metadata"]["archived_at"] == _iso_utc(now)
    assert bridge.get(active_id)["text"] == "active memory"

    results = bridge.search([1.0] + [0.0] * 383, k=5)
    assert expired_id not in {result["id"] for result in results}


def test_v2_prune_archived_is_idempotent(tmp_path):
    persist_directory = tmp_path / "test_chroma_prune_archived"
    bridge = MemoryBridgeV2(persist_directory=str(persist_directory))
    archived_at = datetime(2026, 5, 1, 12, 0, tzinfo=timezone.utc)
    prune_at = archived_at + timedelta(hours=2)

    memory_id = bridge.store(
        "prune me",
        [0.3] * 384,
        expires_at=_iso_utc(archived_at - timedelta(hours=1)),
    )
    bridge.archive_expired(now=archived_at)

    first_run = bridge.prune_archived(now=prune_at, retention_seconds=1800)
    second_run = bridge.prune_archived(now=prune_at, retention_seconds=1800)

    assert first_run == 1
    assert second_run == 0
    assert bridge.get(memory_id, include_archived=True) is None
