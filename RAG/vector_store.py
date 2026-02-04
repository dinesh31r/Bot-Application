import os
import time
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

class KnowledgeBase:
    def __init__(self):
        # Initialize Pinecone
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.env = os.getenv("PINECONE_ENV", "us-east-1")
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "jarvis-knowledge")
        
        if not self.api_key:
            print("WARNING: Pinecone API Key not found. Vector DB features will be disabled.")
            self.pc = None
            self.index = None
        else:
            try:
                self.pc = Pinecone(api_key=self.api_key)
                self.index = self.pc.Index(self.index_name)
                print(f"Connected to Pinecone Index: {self.index_name}")
            except Exception as e:
                print(f"Error connecting to Pinecone: {e}")
                self.pc = None
                self.index = None

        # Initialize Embedding Model
        # using all-MiniLM-L6-v2 for speed and efficiency
        try:
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Error loading embedding model: {e}")
            self.encoder = None

    def get_embedding(self, text: str) -> List[float]:
        if not self.encoder:
            return []
        return self.encoder.encode(text).tolist()

    def search(self, query: str, top_k: int = 3) -> str:
        if not self.index or not self.encoder:
            return ""
        
        try:
            query_embedding = self.get_embedding(query)
            results = self.index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
            
            contexts = []
            for match in results.matches:
                if match.score > 0.7:  # Threshold for relevance
                    text = match.metadata.get('text', '')
                    contexts.append(text)
            
            return "\n".join(contexts)
        except Exception as e:
            print(f"Error querying Pinecone: {e}")
            return ""

# Global instance
knowledge_base = KnowledgeBase()
