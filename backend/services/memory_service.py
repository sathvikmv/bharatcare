"""Simple in-memory persistence for recent conversation and uploaded documents."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

MEMORY_FILE = Path(__file__).resolve().parents[1] / "memory.json"


class MemoryService:
    """Store and load lightweight memory snapshots for the backend."""

    @staticmethod
    def _default_payload() -> Dict[str, Any]:
        return {
            "last_conversation": [],
            "uploaded_documents": [],
            "recent_chats": [],
        }

    @classmethod
    def save_memory(cls, payload: Dict[str, Any] | None = None) -> None:
        """Persist the supplied memory payload to disk."""
        memory_path = MEMORY_FILE
        memory_path.parent.mkdir(parents=True, exist_ok=True)
        data = cls._default_payload()
        if payload:
            data.update(payload)
        with memory_path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)

    @classmethod
    def load_memory(cls) -> Dict[str, Any]:
        """Load the stored memory payload, returning defaults if absent."""
        if not MEMORY_FILE.exists():
            return cls._default_payload()
        with MEMORY_FILE.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    @classmethod
    def clear_memory(cls) -> None:
        """Remove the persisted memory file."""
        if MEMORY_FILE.exists():
            MEMORY_FILE.unlink()
