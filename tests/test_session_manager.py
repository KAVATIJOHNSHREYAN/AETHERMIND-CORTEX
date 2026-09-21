"""
Unit tests for Session Manager
"""

import pytest
from core.session_manager import SessionManager
from database.connection import DBConnection
from database.init_db import initialize_database

@pytest.fixture
def temp_db(tmp_path):
    db_file = str(tmp_path / "test_sessions.db")
    db_conn = DBConnection(db_path=db_file)
    initialize_database(db_conn)
    return db_conn

def test_session_lifecycle(temp_db):
    sm = SessionManager(db_conn=temp_db)
    session_id = sm.create_session("Test Session", "llama3")
    assert session_id is not None
    
    assert sm.add_message(session_id, "user", "Hello model!") is True
    assert sm.add_message(session_id, "assistant", "Hello human!") is True
    
    messages = sm.get_session_messages(session_id)
    assert len(messages) == 2
    assert messages[0]["content"] == "Hello model!"
    
    export_md = sm.export_session(session_id, "markdown")
    assert "User" in export_md
    assert "Hello model!" in export_md

    assert sm.clear_session_messages(session_id) is True
    assert len(sm.get_session_messages(session_id)) == 0
