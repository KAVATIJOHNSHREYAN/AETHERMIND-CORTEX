"""
Unit tests for Safe Local Automation Engine
"""

import os
import pytest
from core.automation_engine import AutomationEngine
from database.connection import DBConnection
from database.init_db import initialize_database

@pytest.fixture
def temp_db(tmp_path):
    db_file = str(tmp_path / "test_automation.db")
    db_conn = DBConnection(db_path=db_file)
    initialize_database(db_conn)
    return db_conn

def test_script_execution(temp_db):
    ae = AutomationEngine(db_conn=temp_db)
    code = 'print("Hello from AetherMind Automation Test")'
    res = ae.execute_python_script(code)
    assert res["success"] is True
    assert "Hello from AetherMind" in res["output"]
    
    jobs = ae.list_automation_jobs()
    assert len(jobs) >= 1
    assert jobs[0]["type"].lower() == "script"

def test_project_template_creation(temp_db, tmp_path):
    ae = AutomationEngine(db_conn=temp_db)
    res = ae.create_project_template("TestAutomationProj", str(tmp_path))
    assert res["success"] is True
    assert os.path.exists(os.path.join(tmp_path, "TestAutomationProj", "app"))
    assert os.path.exists(os.path.join(tmp_path, "TestAutomationProj", "main.py"))

def test_reminder_system(temp_db):
    ae = AutomationEngine(db_conn=temp_db)
    rem_id = ae.add_reminder("Test Reminder")
    assert rem_id is not None
    
    rems = ae.list_reminders()
    assert len(rems) >= 1
    assert rems[0]["message"] == "Test Reminder"
