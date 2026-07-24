"""FastAPI router for Dashboard metrics."""

from __future__ import annotations

from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.schemas.upload_schemas import DashboardResponse
from backend.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
@router.get("/", response_model=DashboardResponse)
def get_dashboard_metrics(db: Annotated[Session, Depends(get_db)]) -> DashboardResponse:
    """Return overall metrics: total chats, total messages, uploaded files, and vector document chunks."""
    service = DashboardService(db)
    metrics = service.get_metrics()
    return DashboardResponse(**metrics)
