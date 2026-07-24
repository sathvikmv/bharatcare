"""RAG retrieval service for extracting top context chunks without LLM orchestration."""

from __future__ import annotations

from typing import List
from backend.services.vector_service import VectorService


class RAGService:
    """Provides vector-based text context retrieval."""

    def __init__(self, vector_service: VectorService | None = None) -> None:
        self.vector_service = vector_service or VectorService()

    def retrieve_context(self, query: str, top_k: int = 5) -> List[str]:
        """Search ChromaDB and return the top matching text chunks.
        
        Args:
            query: User prompt or search question.
            top_k: Number of relevant chunks to retrieve (default: 5).

        Returns:
            List of string context chunks.
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        results = self.vector_service.search(query=query, top_k=top_k)
        return [item["content"] for item in results]
