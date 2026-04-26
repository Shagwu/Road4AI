import sqlite3
import json
import os
import hnswlib
import numpy as np

class MemoryBridge:
    def __init__(self, db_path="memory.db", index_path="hnsw.index", dimension=384):
        self.db_path = db_path
        self.index_path = index_path
        self.dimension = dimension
        self.max_elements = 10000
        
        self._init_db()
        self._init_index()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    vector TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def _init_index(self):
        self.index = hnswlib.Index(space='cosine', dim=self.dimension)
        if os.path.exists(self.index_path):
            self.index.load_index(self.index_path, max_elements=self.max_elements)
        else:
            self.index.init_index(max_elements=self.max_elements, ef_construction=200, M=16)
        self.index.set_ef(50)

    def store(self, text, vector):
        vector_np = np.array(vector).astype('float32')
        vector_json = json.dumps(vector_np.tolist())
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO memories (text, vector) VALUES (?, ?)",
                (text, vector_json)
            )
            memory_id = cursor.lastrowid
            conn.commit()
            
            # Add to HNSW index
            self.index.add_items(vector_np, memory_id)
            self.index.save_index(self.index_path)
            
            return memory_id

    def get(self, memory_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT text, vector FROM memories WHERE id = ?",
                (memory_id,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    "text": row[0],
                    "vector": json.loads(row[1])
                }
            return None

    def search(self, query_vector, k=5):
        query_np = np.array(query_vector).astype('float32')
        labels, distances = self.index.knn_query(query_np, k=k)
        
        results = []
        for label, distance in zip(labels[0], distances[0]):
            memory = self.get(int(label))
            if memory:
                memory["distance"] = float(distance)
                results.append(memory)
        return results
