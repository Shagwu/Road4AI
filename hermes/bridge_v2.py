from datetime import datetime, timedelta, timezone
import uuid
import math

import chromadb


class MemoryBridgeV2:
    ACTIVE_STATUS = "active"
    ARCHIVED_STATUS = "archived"

    def __init__(self, persist_directory="./chroma_db", collection_name="memories"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        
        # Verify distance metric to safeguard Task 2 scoring (1.0 - sqrt(dist))
        # Chroma defaults to 'l2' (squared L2). If this changes, scoring fails.
        metadata = self.collection.metadata or {}
        hnsw_space = metadata.get("hnsw:space", "l2")
        if hnsw_space != "l2":
            # We don't hard fail to maintain 'Degraded Mode' philosophy, but we log the risk
            print(f"WARNING: Collection space is '{hnsw_space}', but scoring assumes 'l2'. Relevance signals may be inaccurate.")

    def store(self, text, vector, metadata=None, expires_at=None, ttl_seconds=None):
        if expires_at is not None and ttl_seconds is not None:
            raise ValueError("Provide either expires_at or ttl_seconds, not both")

        current_time = self._utcnow()
        resolved_expires_at = expires_at
        if ttl_seconds is not None:
            resolved_expires_at = current_time + timedelta(seconds=ttl_seconds)

        memory_id = str(uuid.uuid4())
        self.collection.add(
            embeddings=[vector],
            documents=[text],
            metadatas=[self._build_active_metadata(metadata, current_time, resolved_expires_at)],
            ids=[memory_id],
        )
        return memory_id

    def get(self, memory_id, include_archived=False):
        result = self.collection.get(
            ids=[memory_id],
            include=["documents", "metadatas", "embeddings"],
        )
        if not result["ids"]:
            return None

        metadata = self._hydrate_metadata(result["metadatas"][0] if result["metadatas"] else None)
        if not include_archived and metadata["status"] == self.ARCHIVED_STATUS:
            return None

        return {
            "id": result["ids"][0],
            "text": result["documents"][0],
            "vector": result["embeddings"][0].tolist() if result["embeddings"] is not None else None,
            "metadata": metadata,
        }

    def search(self, query_vector, k=5, include_archived=False, threshold=0.7):
        total_memories = self.collection.count()
        if total_memories == 0:
            return []

        query_limit = total_memories if not include_archived else min(k, total_memories)
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=query_limit,
        )

        output = []
        if results["ids"] and results["ids"][0]:
            for index, memory_id in enumerate(results["ids"][0]):
                metadata = self._hydrate_metadata(
                    results["metadatas"][0][index] if results["metadatas"] else None
                )
                if not include_archived and metadata["status"] == self.ARCHIVED_STATUS:
                    continue

                distance = results["distances"][0][index]
                # Chroma uses squared L2 by default. Use sqrt for linear score.
                score = 1.0 - math.sqrt(distance)
                
                status = "relevant" if score >= threshold else "irrelevant"
                if status == "irrelevant" and score >= (threshold - 0.15):
                    status = "borderline"
                
                reason = f"Score {score:.2f} vs Threshold {threshold:.2f}"
                
                output.append(
                    {
                        "id": memory_id,
                        "text": results["documents"][0][index],
                        "metadata": metadata,
                        "distance": distance,
                        "relevance_signal": {
                            "status": status,
                            "reason": reason,
                            "score": round(score, 4),
                            "threshold": threshold,
                        }
                    }
                )
                if len(output) == k:
                    break
        return output

    def archive_expired(self, now=None):
        current_time = self._coerce_timestamp(now) if now is not None else self._utcnow()
        snapshot = self.collection.get(include=["metadatas"])
        if not snapshot["ids"]:
            return 0

        ids_to_archive = []
        metadatas_to_archive = []
        archived_at = self._format_timestamp(current_time)

        for memory_id, metadata in zip(snapshot["ids"], snapshot["metadatas"] or []):
            hydrated_metadata = self._hydrate_metadata(metadata)
            expires_at = hydrated_metadata["expires_at"]
            if hydrated_metadata["status"] != self.ACTIVE_STATUS or expires_at is None:
                continue

            if self._coerce_timestamp(expires_at) <= current_time:
                updated_metadata = dict(hydrated_metadata)
                updated_metadata["status"] = self.ARCHIVED_STATUS
                updated_metadata["archived_at"] = archived_at
                ids_to_archive.append(memory_id)
                metadatas_to_archive.append(self._persistable_metadata(updated_metadata))

        if ids_to_archive:
            self.collection.update(ids=ids_to_archive, metadatas=metadatas_to_archive)
        return len(ids_to_archive)

    def prune_archived(self, now=None, retention_seconds=0):
        if retention_seconds < 0:
            raise ValueError("retention_seconds must be non-negative")

        current_time = self._coerce_timestamp(now) if now is not None else self._utcnow()
        retention_window = timedelta(seconds=retention_seconds)
        snapshot = self.collection.get(include=["metadatas"])
        if not snapshot["ids"]:
            return 0

        ids_to_delete = []
        for memory_id, metadata in zip(snapshot["ids"], snapshot["metadatas"] or []):
            hydrated_metadata = self._hydrate_metadata(metadata)
            archived_at = hydrated_metadata["archived_at"]
            if hydrated_metadata["status"] != self.ARCHIVED_STATUS or archived_at is None:
                continue

            if self._coerce_timestamp(archived_at) + retention_window <= current_time:
                ids_to_delete.append(memory_id)

        if ids_to_delete:
            self.collection.delete(ids=ids_to_delete)
        return len(ids_to_delete)

    # V1 Aliases
    def get_by_id(self, memory_id, include_archived=False):
        return self.get(memory_id, include_archived=include_archived)

    def _build_active_metadata(self, metadata, created_at, expires_at):
        merged_metadata = dict(metadata or {})
        merged_metadata["status"] = self.ACTIVE_STATUS
        merged_metadata["created_at"] = self._format_timestamp(created_at)
        if expires_at is not None:
            merged_metadata["expires_at"] = self._format_timestamp(self._coerce_timestamp(expires_at))
        return merged_metadata

    def _hydrate_metadata(self, metadata):
        hydrated = dict(metadata or {})
        hydrated.setdefault("status", self.ACTIVE_STATUS)
        hydrated.setdefault("expires_at", None)
        hydrated.setdefault("archived_at", None)
        return hydrated

    def _persistable_metadata(self, metadata):
        return {key: value for key, value in metadata.items() if value is not None}

    def _coerce_timestamp(self, value):
        if isinstance(value, datetime):
            timestamp = value
        elif isinstance(value, str):
            try:
                timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError as exc:
                raise ValueError(f"Invalid timestamp: {value}") from exc
        else:
            raise TypeError("Timestamp values must be datetime or ISO 8601 strings")

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        else:
            timestamp = timestamp.astimezone(timezone.utc)
        return timestamp.replace(microsecond=0)

    def _format_timestamp(self, value):
        return self._coerce_timestamp(value).isoformat().replace("+00:00", "Z")

    def _utcnow(self):
        return datetime.now(timezone.utc).replace(microsecond=0)
