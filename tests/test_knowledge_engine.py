"""
Unit tests for Document Processor and Knowledge Engine (RAG)
"""

import os
import pytest
from core.document_processor import DocumentProcessor
from core.knowledge_engine import KnowledgeEngine
from database.connection import DBConnection
from database.init_db import initialize_database

@pytest.fixture
def temp_db(tmp_path):
    db_file = str(tmp_path / "test_knowledge.db")
    db_conn = DBConnection(db_path=db_file)
    initialize_database(db_conn)
    return db_conn

def test_document_processor_chunking(tmp_path):
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("AetherMind Cortex is an offline AI reasoning engine platform built with Python.", encoding="utf-8")
    
    processor = DocumentProcessor(chunk_size=30, chunk_overlap=10)
    text, file_type = processor.extract_text(str(sample_file))
    assert file_type == "txt"
    assert "AetherMind" in text
    
    chunks = processor.chunk_text(text, {"file_name": "sample.txt"})
    assert len(chunks) > 1

def test_knowledge_engine_indexing(temp_db, tmp_path):
    sample_file = tmp_path / "rag_test.txt"
    sample_file.write_text("Python is a high-level programming language used extensively in AetherMind Cortex.", encoding="utf-8")
    
    ke = KnowledgeEngine(db_conn=temp_db)
    res = ke.ingest_file(str(sample_file))
    assert res["success"] is True
    assert res["chunk_count"] > 0
    
    docs = ke.list_indexed_documents()
    assert len(docs) >= 1
    assert docs[0]["file_name"] == "rag_test.txt"
    
    rag_context, citations = ke.get_rag_context_injection("What programming language does AetherMind use?")
    assert len(citations) >= 1
    assert citations[0]["source"] == "rag_test.txt"
    
    assert ke.remove_document(res["doc_id"]) is True
