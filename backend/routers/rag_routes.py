"""FastAPI router for RAG context retrieval."""

from __future__ import annotations

from typing import Dict, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from backend.services.rag_service import RAGService

router = APIRouter(prefix="/rag", tags=["rag"])


class RAGQueryRequest(BaseModel):
    """Request schema for RAG context retrieval."""
    query: str = Field(..., min_length=1, description="Search query string")


class RAGContextResponse(BaseModel):
    """Response schema containing retrieved top context chunks."""
    context: List[str]


@router.post("/retrieve", response_model=RAGContextResponse)
def retrieve_context_endpoint(payload: RAGQueryRequest) -> RAGContextResponse:
    """Retrieve top 5 relevant document chunks for a query from ChromaDB without invoking any LLM."""
    service = RAGService()
    try:
        chunks = service.retrieve_context(payload.query, top_k=5)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return RAGContextResponse(context=chunks)
