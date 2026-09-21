"""
Unit tests for Decision Intelligence Engine
"""

import pytest
from core.decision_engine import DecisionEngine
from database.connection import DBConnection
from database.init_db import initialize_database

@pytest.fixture
def temp_db(tmp_path):
    db_file = str(tmp_path / "test_decision.db")
    db_conn = DBConnection(db_path=db_file)
    initialize_database(db_conn)
    return db_conn

def test_mcda_evaluation(temp_db):
    de = DecisionEngine(db_conn=temp_db)
    res = de.evaluate_decision(
        topic="Database Architecture Choice",
        options=["SQLite", "PostgreSQL", "ChromaDB Vector"]
    )
    assert res["recommended_option"] is not None
    assert len(res["ranked_options"]) == 3
    assert res["ranked_options"][0]["score"] > 0
    
    saved = de.list_saved_decisions()
    assert len(saved) >= 1
    assert saved[0]["topic"] == "Database Architecture Choice"
    
    assert de.update_decision_feedback(res["decision_id"], 5) is True
