"""ChromaDB integration for document embedding and retrieval."""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Dict, Any

import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHROMA_DIR = Path(__file__).resolve().parents[1] / "chroma_db"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)


class VectorService:
    """Manage document chunking, embedding, storage, and retrieval."""

    def __init__(self, collection_name: str = "documents") -> None:
        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embedder = None
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)

    def _get_embedder(self):
        """Load the embedding model lazily on first use."""
        if self.embedder is None:
            from sentence_transformers import SentenceTransformer

            self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        return self.embedder

    def add_document(self, document_id: str, content: str, metadata: Dict[str, Any] | None = None) -> None:
        """Split a document, embed chunks, and persist them in ChromaDB."""
        if not content.strip():
            raise ValueError("Empty document")

        chunks = self.splitter.split_text(content)
        if not chunks:
            raise ValueError("Empty document")

        embeddings = self._get_embedder().encode(chunks).tolist()
        ids = [f"{document_id}_{index}" for index in range(len(chunks))]
        chunk_metadata = []
        for index, chunk in enumerate(chunks):
            item_metadata = {"document_id": document_id, "chunk_index": index}
            if metadata:
                item_metadata.update(metadata)
            chunk_metadata.append(item_metadata)

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=chunk_metadata,
        )

    def delete_document(self, document_id: str) -> None:
        """Delete all stored chunks for a document id."""
        self.collection.delete(where={"document_id": document_id})

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search the vector store for the most relevant chunks."""
        if not query.strip():
            raise ValueError("Query cannot be empty")

        query_embedding = self._get_embedder().encode([query])[0].tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )
        matches: List[Dict[str, Any]] = []
        for document, metadata, distance in zip(
            results.get("documents", [[]])[0],
            results.get("metadatas", [[]])[0],
            results.get("distances", [[]])[0],
        ):
            matches.append({"content": document, "metadata": metadata, "distance": distance})
        return matches
