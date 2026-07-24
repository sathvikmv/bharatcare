"""Service layer for document upload and text extraction."""

from __future__ import annotations

import csv
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple

import pandas as pd
from docx import Document as DocxDocument
from PyPDF2 import PdfReader

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx", ".csv"}


class FileService:
    """Handles file uploads and document parsing."""

    @staticmethod
    def ensure_upload_directory() -> Path:
        """Create the upload directory if it does not exist."""
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        return UPLOAD_DIR

    @staticmethod
    def _safe_filename(filename: str) -> str:
        """Sanitize filenames to avoid path traversal issues."""
        return os.path.basename(filename)

    @staticmethod
    def _file_size(path: Path) -> int:
        """Return the size of a file in bytes."""
        return path.stat().st_size if path.exists() else 0

    @classmethod
    def save_upload(cls, uploaded_file, filename: str) -> Tuple[dict, str]:
        """Persist an uploaded file and return metadata."""
        safe_name = cls._safe_filename(filename)
        extension = Path(safe_name).suffix.lower()
        if extension not in SUPPORTED_EXTENSIONS:
            raise ValueError("Unsupported file format")

        upload_dir = cls.ensure_upload_directory()
        destination = upload_dir / safe_name
        if destination.exists():
            suffix = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
            destination = upload_dir / f"{Path(safe_name).stem}_{suffix}{Path(safe_name).suffix}"

        with destination.open("wb") as handle:
            shutil.copyfileobj(uploaded_file.file, handle)

        metadata = {
            "filename": destination.name,
            "path": str(destination),
            "size": cls._file_size(destination),
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
        }
        return metadata, str(destination)

    @staticmethod
    def extract_text(path: str) -> str:
        """Extract textual content from a supported document type."""
        extension = Path(path).suffix.lower()
        if extension == ".pdf":
            return FileService.extract_pdf_text(path)
        if extension == ".txt":
            return FileService.extract_txt_text(path)
        if extension == ".docx":
            return FileService.extract_docx_text(path)
        if extension == ".csv":
            return FileService.extract_csv_text(path)
        raise ValueError("Unsupported file format")

    @staticmethod
    def extract_pdf_text(path: str) -> str:
        """Extract text from a PDF document."""
        reader = PdfReader(path)
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages).strip()

    @staticmethod
    def extract_txt_text(path: str) -> str:
        """Read plain text from a .txt file."""
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read().strip()

    @staticmethod
    def extract_docx_text(path: str) -> str:
        """Extract paragraphs from a .docx document."""
        document = DocxDocument(path)
        paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
        return "\n".join(paragraphs)

    @staticmethod
    def extract_csv_text(path: str) -> str:
        """Read a CSV file into a DataFrame and serialize it to text."""
        dataframe = pd.read_csv(path)
        return dataframe.to_string(index=False)
