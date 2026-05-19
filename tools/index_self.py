import os
import subprocess
import re
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from hermes.bridge_v2 import MemoryBridgeV2

# Constants
MODEL_NAME = "all-MiniLM-L6-v2"
PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "self_knowledge"

class SelfIndexer:
    def __init__(self):
        print(f"Loading embedding model: {MODEL_NAME}...")
        self.model = SentenceTransformer(MODEL_NAME)
        self.bridge = MemoryBridgeV2(persist_directory=PERSIST_DIR, collection_name=COLLECTION_NAME)
        # Clear existing self-knowledge for a clean build
        self.bridge.client.delete_collection(COLLECTION_NAME)
        self.bridge.collection = self.bridge.client.get_or_create_collection(name=COLLECTION_NAME)

    def run(self):
        print("Starting surgical ingestion for Road4AI Self-Knowledge...")
        
        # 1. The Proof Layer (Plans & Governance)
        self.index_markdown_files("docs/plans/*.md", category="plan")
        self.index_file("AGENTS.md", category="governance")
        self.index_file("MAY_ROADMAP.md", category="roadmap")
        self.index_file("manifesto.md", category="philosophy")

        # 2. The Implementation Layer (Code-as-Docs)
        self.index_code_files("hermes/*.py", category="implementation")
        self.index_code_files("road4ai-cos/app/*.py", category="orchestration")

        # 3. The Contextual Layer (Temporal History)
        self.index_checkpoints(limit=20)
        self.index_file("state/published-log.json", category="history")

        print("Ingestion complete.")

    def index_file(self, file_path: str, category: str):
        if not os.path.exists(file_path):
            print(f"Skipping missing file: {file_path}")
            return
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        print(f"Indexing {file_path}...")
        self.chunk_and_store(content, metadata={"source": file_path, "category": category})

    def index_markdown_files(self, pattern: str, category: str):
        import glob
        for file_path in glob.glob(pattern):
            self.index_file(file_path, category)

    def index_code_files(self, pattern: str, category: str):
        import glob
        for file_path in glob.glob(pattern):
            if "test" in file_path or "__init__" in file_path:
                continue
                
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # Extract docstrings and class/fn definitions only (Signal over Noise)
            relevant_lines = []
            in_docstring = False
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    in_docstring = not in_docstring
                    relevant_lines.append(line)
                    continue
                if in_docstring:
                    relevant_lines.append(line)
                    continue
                if stripped.startswith("class ") or stripped.startswith("def "):
                    relevant_lines.append(line)
            
            if relevant_lines:
                print(f"Indexing code signal from {file_path}...")
                content = "".join(relevant_lines)
                self.chunk_and_store(content, metadata={"source": file_path, "category": category})

    def index_checkpoints(self, limit: int = 20):
        print(f"Indexing latest {limit} git checkpoints...")
        try:
            output = subprocess.check_output(
                ["git", "log", "--grep=\\[hermes-context\\]", "--format=%B", f"-n {limit}"],
                text=True
            )
            # Split into individual checkpoints
            checkpoints = re.split(r'CHECKPOINT:', output)
            for cp in checkpoints:
                if cp.strip():
                    self.chunk_and_store("CHECKPOINT:" + cp, metadata={"source": "git_log", "category": "history"})
        except Exception as e:
            print(f"Error reading checkpoints: {e}")

    def chunk_and_store(self, text: str, metadata: Dict[str, Any]):
        # Add source context directly into the text for 'Self-Awareness'
        source = metadata.get("source", "unknown")
        category = metadata.get("category", "unknown")
        header = f"SOURCE: {source} | CATEGORY: {category}\n\n"
        
        # Surgical chunking for core files
        if category in ["governance", "plan"]:
            # Initial split by any header level (H1-H6)
            raw_chunks = re.split(r'\n(?=#+ )', text)
            chunks = []
            for rc in raw_chunks:
                # If a chunk is still too fat (> 2000 chars), split by paragraph
                if len(rc) > 2000:
                    chunks.extend([p.strip() for p in rc.split("\n\n") if len(p.strip()) > 50])
                else:
                    if len(rc.strip()) > 50:
                        chunks.append(rc.strip())
        else:
            # Simple chunking by paragraph/section
            chunks = [c.strip() for c in text.split("\n\n") if len(c.strip()) > 50]
            
        if not chunks:
            chunks = [text.strip()]

        for chunk in chunks:
            # Final safety check: if chunk is still massive, truncate or split (rare)
            # Prepend context header to the indexed text
            final_text = header + chunk
            vector = self.model.encode(final_text).tolist()
            self.bridge.store(final_text, vector, metadata=metadata)

if __name__ == "__main__":
    indexer = SelfIndexer()
    indexer.run()
