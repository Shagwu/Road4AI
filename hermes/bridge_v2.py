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
