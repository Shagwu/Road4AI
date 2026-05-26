import os
import time
from typing import List
from sentence_transformers import SentenceTransformer
from road4ai_hermes.bridge import MemoryBridgeV2

# Constants
MODEL_NAME = "all-MiniLM-L6-v2"
PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "self_knowledge"

class RevealVerifier:
    def __init__(self):
        print(f"Loading embedding model for verification: {MODEL_NAME}...")
        self.model = SentenceTransformer(MODEL_NAME)
        self.bridge = MemoryBridgeV2(persist_directory=PERSIST_DIR, collection_name=COLLECTION_NAME)

    def ask(self, question: str):
        print(f"\n--- QUERY: {question} ---")
        start_time = time.time()
        
        # Generate embedding
        vector = self.model.encode(question).tolist()
        
        # Search Hermes
        results = self.bridge.search(query_vector=vector, k=3, threshold=0.4)
        latency_ms = (time.time() - start_time) * 1000
        
        if not results:
            print("No relevant context found.")
            return

        print(f"Latency: {latency_ms:.2f}ms")
        for i, res in enumerate(results):
            source = res["metadata"].get("source", "unknown")
            category = res["metadata"].get("category", "unknown")
            score = res["relevance_signal"]["score"]
            print(f"\n[Result {i+1}] (Score: {score:.4f}, Source: {source}, Category: {category})")
            print(f"CONTENT PREVIEW: {res['text'][:300]}...")

    def run_reveal_tests(self):
        questions = [
            "Why did we move from local HNSW to a distributed ChromaDB substrate for Hermes v2.0?",
            "What is the 'Governance Lock' on AGENTS.md and how does it prevent agent-to-agent negotiation?",
            "How does the HermesStorage class bridge CrewAI's knowledge system with our internal memory layer?"
        ]
        for q in questions:
            self.ask(q)

if __name__ == "__main__":
    verifier = RevealVerifier()
    verifier.run_reveal_tests()
