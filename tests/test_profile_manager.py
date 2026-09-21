"""
Unit tests for Human Profile Manager
"""

import pytest
import json
from core.profile_manager import ProfileManager
from database.connection import DBConnection
from database.init_db import initialize_database

@pytest.fixture
def temp_db(tmp_path):
    db_file = str(tmp_path / "test_profile.db")
    db_conn = DBConnection(db_path=db_file)
    initialize_database(db_conn)
    return db_conn

def test_profile_attributes(temp_db):
    pm = ProfileManager(db_conn=temp_db)
    
    # Check default
    assert pm.get_profile_attribute("user_name") == "User"
    
    # Update single attribute
    assert pm.set_profile_attribute("user_name", "Shreyan") is True
    assert pm.get_profile_attribute("user_name") == "Shreyan"
    
    # Bulk update
    pm.update_profile_bulk({
        "profession": "AI Architect",
        "coding_style": "Clean Architecture"
    })
    prof = pm.get_full_profile()
    assert prof["profession"] == "AI Architect"
    assert prof["coding_style"] == "Clean Architecture"

def test_goals_engine(temp_db):
    pm = ProfileManager(db_conn=temp_db)
    goal_id = pm.add_goal("Master Rust", "learning", "high")
    assert goal_id is not None
    
    goals = pm.list_goals(status="active")
    assert len(goals) >= 1
    assert goals[0]["title"] == "Master Rust"
    
    prompt = pm.get_personalized_prompt_context()
    assert "Shreyan" in prompt or "Master Rust" in prompt or "User" in prompt
    
    assert pm.delete_goal(goal_id) is True

def test_profile_json_export_and_reset(temp_db):
    pm = ProfileManager(db_conn=temp_db)
    pm.set_profile_attribute("user_name", "TestUser")
    
    export_json = pm.export_profile_json()
    data = json.loads(export_json)
    assert "profile" in data
    assert data["profile"]["user_name"] == "TestUser"
    
    assert pm.reset_profile() is True
    assert pm.get_profile_attribute("user_name") == "User"
