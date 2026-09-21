"""
Unit tests for Workflow Intelligence Engine
"""

import pytest
from core.workflow_engine import WorkflowEngine
from database.connection import DBConnection
from database.init_db import initialize_database

@pytest.fixture
def temp_db(tmp_path):
    db_file = str(tmp_path / "test_workflow.db")
    db_conn = DBConnection(db_path=db_file)
    initialize_database(db_conn)
    return db_conn

def test_task_intelligence_crud(temp_db):
    we = WorkflowEngine(db_conn=temp_db)
    task_id = we.add_task("Refactor RAG Pipeline", "AetherMind", "high", 3.5)
    assert task_id is not None
    
    tasks = we.list_tasks(status="todo")
    assert len(tasks) >= 1
    assert tasks[0]["title"] == "Refactor RAG Pipeline"
    assert tasks[0]["estimated_hours"] == 3.5
    
    assert we.update_task_status(task_id, "completed") is True
    assert len(we.list_tasks(status="completed")) >= 1
    
    summary = we.get_productivity_summary()
    assert summary["completed_tasks"] >= 1
    assert summary["completion_rate_pct"] > 0

def test_workflow_insights(temp_db):
    we = WorkflowEngine(db_conn=temp_db)
    insights = we.list_insights()
    assert isinstance(insights, list)
    assert len(insights) >= 1
