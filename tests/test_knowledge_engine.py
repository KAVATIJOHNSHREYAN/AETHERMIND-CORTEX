"""
Unit tests for Document Processor and Knowledge Engine (Phase 4.2 Expanded)
"""

import os
import pytest
from core.document_processor import DocumentProcessor
from core.knowledge_engine import KnowledgeEngine
from database.connection import DBConnection
from database.init_db import initialize_database

@pytest.fixture
def temp_db(tmp_path):
    db_file = str(tmp_path / "test_knowledge_v42.db")
    db_conn = DBConnection(db_path=db_file)
    initialize_database(db_conn)
    return db_conn

def test_folder_scanner(tmp_path):
    dir_path = tmp_path / "docs_folder"
    dir_path.mkdir()
    (dir_path / "file1.txt").write_text("Text doc 1", encoding="utf-8")
    (dir_path / "file2.md").write_text("# MD doc 2", encoding="utf-8")
    (dir_path / "code.py").write_text("print('hello')", encoding="utf-8")
    
    files = DocumentProcessor.scan_directory(str(dir_path))
    assert len(files) == 3

def test_batch_ingest_and_confidence_score(temp_db, tmp_path):
    dir_path = tmp_path / "batch_folder"
    dir_path.mkdir()
    (dir_path / "docA.txt").write_text("AetherMind Cortex handles offline RAG document retrieval.", encoding="utf-8")
    (dir_path / "docB.txt").write_text("ChromaDB persists vector embeddings locally.", encoding="utf-8")

    ke = KnowledgeEngine(db_conn=temp_db)
    batch_res = ke.batch_ingest_directory(str(dir_path))
    assert batch_res["success"] is True
    assert batch_res["new_indexed"] == 2
    
    stats = ke.get_collection_stats()
    assert stats["total_documents"] >= 2
    
    chunks = ke.search_rag_chunks("offline RAG document retrieval")
    assert len(chunks) >= 1
    assert "confidence_score" in chunks[0]
    assert chunks[0]["confidence_score"] > 0
