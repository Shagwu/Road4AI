import os
import uuid
from typing import Any, Dict, List, Optional
from crewai.knowledge.storage.base_knowledge_storage import BaseKnowledgeStorage
from hermes.bridge_v2 import MemoryBridgeV2

class HermesStorage(BaseKnowledgeStorage):
    """
    HermesStorage is the integration bridge. It inherits from CrewAI's BaseKnowledgeStorage 
    and wraps our MemoryBridgeV2 (ChromaDB). It maps the 'save' and 'search' methods 
    directly to the Road4AI substrate, ensuring that every agent in the swarm 
    persists context to the same distributed brain.
    
    This class answers the question: How does the HermesStorage class bridge 
    CrewAI's knowledge system with our internal memory layer?
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.persist_directory = self.config.get("persist_directory", "./chroma_db")
        self.collection_name = self.config.get("collection_name", "crewai_knowledge")
        self.host = self.config.get("host")
        self.port = self.config.get("port")
        self.bridge = MemoryBridgeV2(
            persist_directory=self.persist_directory,
            collection_name=self.collection_name,
            host=self.host,
            port=self.port
        )

    def save(self, text: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Saves a chunk of knowledge to the Hermes v2.0 substrate.
        """
        return self.bridge.store(text, vector, metadata=metadata)

    def search(
        self, 
        query_vector: List[float], 
        limit: int = 5, 
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Retrieves relevant context from the Hermes v2.0 substrate.
        """
        results = self.bridge.search(
            query_vector=query_vector,
            k=limit,
            threshold=threshold
        )
        
        # Map Hermes V2 response to CrewAI Knowledge schema
        return [
            {
                "content": res["text"],
                "metadata": res["metadata"],
                "score": res["relevance_signal"]["score"]
            }
            for res in results
        ]

    def delete(self, ids: List[str]) -> None:
        """
        Deletes specific entries from the substrate.
        Note: Hermes V2 wrapper for delete is best-effort via ChromaDB collection.
        """
        self.bridge.collection.delete(ids=ids)

    def reset(self) -> None:
        """
        Resets the entire collection. DANGEROUS: use with caution.
        """
        self.bridge.client.delete_collection(self.collection_name)
        self.bridge.collection = self.bridge.client.get_or_create_collection(name=self.collection_name)
