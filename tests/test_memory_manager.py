"""
Unit tests for Long-Term Memory Manager (SQLite & ChromaDB)
"""

import pytest
from core.memory_manager import MemoryManager
from database.connection import DBConnection
from database.init_db import initialize_database

@pytest.fixture
def temp_db(tmp_path):
    db_file = str(tmp_path / "test_memories.db")
    db_conn = DBConnection(db_path=db_file)
    initialize_database(db_conn)
    return db_conn

def test_memory_crud(temp_db):
    mm = MemoryManager(db_conn=temp_db)
    
    # 1. Add memory
    mem_id = mm.add_memory(
        category="user",
        key="Favorite Language",
        content="Prefers Python for AI applications",
        importance=9,
        is_pinned=True
    )
    assert mem_id is not None
    
    # 2. List memories
    memories = mm.list_memories(category="user")
    assert len(memories) >= 1
    assert memories[0]["key"] == "Favorite Language"
    assert memories[0]["importance"] == 9
    
    # 3. Status updates (archive & pin)
    assert mm.update_memory_status(mem_id, is_archived=True) is True
    assert len(mm.list_memories(category="user", include_archived=False)) == 0
    assert len(mm.list_memories(category="user", include_archived=True)) >= 1
    
    # 4. Delete memory
    assert mm.delete_memory(mem_id) is True
    assert len(mm.list_memories(category="user", include_archived=True)) == 0

def test_memory_semantic_retrieval(temp_db):
    mm = MemoryManager(db_conn=temp_db)
    mm.add_memory(
        category="project",
        key="Architecture Choice",
        content="AetherMind uses Gradio UI and SQLite local database",
        importance=8
    )
    
    prompt_context = mm.get_context_prompt_injection("What is the UI framework?")
    assert "AetherMind" in prompt_context or "Architecture Choice" in prompt_context
