"""
AetherMind Cortex Document Processor
Parses PDF, DOCX, TXT, Markdown, and source code files, chunking text for RAG indexing.
"""

import os
import hashlib
from typing import List, Dict, Any, Tuple
from core.logger import get_logger

logger = get_logger("DocumentProcessor")

class DocumentProcessor:
    """Document Ingestion Engine handling text extraction and chunking."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    @staticmethod
    def calculate_file_hash(file_path: str) -> str:
        """Calculates SHA-256 hash of a file for duplicate detection."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def extract_text(self, file_path: str) -> Tuple[str, str]:
        """
        Extracts plain text content and identifies file type.
        Supports PDF, DOCX, TXT, Markdown, and Code files.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        extracted_text = ""

        if ext == ".pdf":
            import pypdf
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
            file_type = "pdf"

        elif ext == ".docx":
            import docx
            doc = docx.Document(file_path)
            extracted_text = "\n".join([p.text for p in doc.paragraphs if p.text])
            file_type = "docx"

        else:
            # TXT, Markdown, Python, JS, SQL, JSON, etc.
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                extracted_text = f.read()
            file_type = ext.lstrip(".") or "text"

        return extracted_text.strip(), file_type

    def chunk_text(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Splits extracted text into overlapping chunks with attached metadata.
        """
        if not text:
            return []

        chunks = []
        start = 0
        text_len = len(text)
        chunk_idx = 0

        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            chunk_content = text[start:end]

            chunk_meta = metadata.copy()
            chunk_meta["chunk_index"] = chunk_idx
            chunk_meta["start_char"] = start
            chunk_meta["end_char"] = end

            chunks.append({
                "content": chunk_content,
                "metadata": chunk_meta
            })

            chunk_idx += 1
            start += self.chunk_size - self.chunk_overlap
            if start >= text_len or self.chunk_size <= self.chunk_overlap:
                break

        logger.info(f"Chunked document [{metadata.get('file_name')}] into {len(chunks)} chunks.")
        return chunks
