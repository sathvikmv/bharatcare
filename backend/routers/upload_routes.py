"""FastAPI routes for document upload and retrieval."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.schemas.upload_schemas import DashboardResponse, UploadResponse
from backend.services.file_service import FileService
from backend.services.memory_service import MemoryService
from backend.services.vector_service import VectorService

router = APIRouter(prefix="/upload", tags=["documents"])


@router.post("", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Annotated[Session, Depends(get_db)] = None,
) -> UploadResponse:
    """Upload a supported document file (PDF, TXT, DOCX, CSV) and store metadata & vector embeddings."""
    if not file or not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing file")

    try:
        metadata, path = FileService.save_upload(file, file.filename)
        extracted_text = FileService.extract_text(path)
        if not extracted_text.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty document")

        vector_service = VectorService()
        vector_service.add_document(document_id=Path(path).name, content=extracted_text, metadata={"path": path})

        memory = MemoryService.load_memory()
        memory.setdefault("uploaded_documents", []).append({"filename": metadata["filename"], "path": path})
        MemoryService.save_memory(memory)
    except ValueError as exc:
        detail = str(exc)
        if detail == "Unsupported file format":
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=detail) from exc
        if detail == "Empty document":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from exc
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from exc
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error") from exc

    return UploadResponse(**metadata)

