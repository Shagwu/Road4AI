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
            metadatas=[metadata] if metadata else None,
            ids=[memory_id]
        )
        return memory_id

    def get(self, memory_id):
        result = self.collection.get(ids=[memory_id])
        if result["ids"]:
            return {
                "text": result["documents"][0],
                "vector": result["embeddings"][0] if result["embeddings"] else None,
                "metadata": result["metadatas"][0] if result["metadatas"] else None
            }
        return None

    def search(self, query_vector, k=5):
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=k
        )
        
        output = []
        if results["ids"] and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                output.append({
                    "id": results["ids"][0][i],
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else None,
                    "distance": results["distances"][0][i]
                })
        return output

    # V1 Aliases
    def get_by_id(self, memory_id):
        return self.get(memory_id)
