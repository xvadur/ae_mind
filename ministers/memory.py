"""Memory ministry with introspective logging."""

import os
import uuid
from typing import Any, Dict, List

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from memory.shared_memory import SharedMemory
from agents.base_minister import BaseMinister


class MinisterOfMemory(BaseMinister):
    """Handle storage and retrieval operations."""

    def __init__(self, shared_memory: SharedMemory):
        # AETH: initialize minister with shared and personal memory
        super().__init__("MinisterOfMemory", shared_memory)
        self.personal_log: Dict[str, Any] = {}
        # AETH: setup persistent vector database for RAG
        persist_dir = os.path.join("memory", "chroma_db")
        self.chroma_client = chromadb.PersistentClient(path=persist_dir)
        embed_fn = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-3-small",
        )
        self.collection = self.chroma_client.get_or_create_collection(
            "aethero_mem", embedding_function=embed_fn
        )

    def activate(self) -> None:
        """Activate memory services."""
        # AETH: confirm operational status for audits
        print(f"[{self.name}] activated")

    def report_capabilities(self) -> str:
        """Return description of memory competencies."""
        # AETH: provide mandate summary
        return "Stores and retrieves shared data"

    def archive(self, key: str, value: Any) -> None:
        """Store value in shared and personal memory."""
        # AETH: persist data for system-wide access
        self.shared_memory.data[key] = value
        self.personal_log[key] = value

    def process_request(self, key: str) -> Any:
        """Retrieve value from shared memory."""
        # AETH: fetch information, record repeated lookups
        feedback = self._register_task(key)
        result = self.shared_memory.data.get(key)
        if feedback:
            result = {"value": result, "poser": feedback}
        return result

    def add_to_knowledge_base(
        self, text: str, source: str, metadata: Dict[str, Any] | None = None
    ) -> None:
        """Add text to vector store with metadata."""
        # AETH: convert text to embedding and store for retrieval
        metadata = metadata or {}
        self.collection.add(
            documents=[text],
            metadatas=[{"source": source, **metadata}],
            ids=[str(uuid.uuid4())],
        )

    def retrieve_relevant_info(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve related entries from knowledge base."""
        # AETH: query vector store for semantic matches
        result = self.collection.query(query_texts=[query], n_results=top_k)
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        return [
            {"text": doc, "metadata": meta} for doc, meta in zip(docs, metas)
        ]

    def introspect(self) -> Dict[str, Any]:
        """Return basic introspective statistics."""
        # AETH: expose internal memory status for audits
        return {
            "stored_keys": list(self.personal_log.keys()),
            "shared_keys": list(self.shared_memory.data.keys()),
        }


class AssistantOfMemory:
    """Assistant performing auxiliary memory tasks."""

    def __init__(self, shared_memory: SharedMemory):
        # AETH: rely on same shared memory reference
        self.name = "AssistantOfMemory"
        self.shared_memory = shared_memory

    def activate(self) -> None:
        """Signal assistant readiness."""
        # AETH: confirm assistant activation
        print(f"[{self.name}] activated")

    def log(self, message: str) -> None:
        """Simple log placeholder."""
        # AETH: introspective placeholder for advanced logging
        print(f"[AssistantOfMemory] {message}")
