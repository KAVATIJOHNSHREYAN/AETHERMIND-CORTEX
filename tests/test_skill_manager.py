"""
Unit tests for Skill Manager and Modular Expert Skills System
"""

import pytest
from core.skill_manager import SkillManager
from database.connection import DBConnection
from database.init_db import initialize_database

@pytest.fixture
def temp_db(tmp_path):
    db_file = str(tmp_path / "test_skills.db")
    db_conn = DBConnection(db_path=db_file)
    initialize_database(db_conn)
    return db_conn

def test_skill_registration(temp_db):
    sm = SkillManager(db_conn=temp_db)
    skills = sm.list_skills()
    assert len(skills) == 6
    
    skill_ids = [s["skill_id"] for s in skills]
    assert "coding_expert" in skill_ids
    assert "research_expert" in skill_ids
    assert "writing_expert" in skill_ids
    assert "data_expert" in skill_ids
    assert "learning_expert" in skill_ids
    assert "project_planner" in skill_ids

def test_skill_toggle_and_prompt_injection(temp_db):
    sm = SkillManager(db_conn=temp_db)
    assert sm.set_skill_status("coding_expert", False) is True
    
    skills = sm.list_skills()
    coding_skill = [s for s in skills if s["skill_id"] == "coding_expert"][0]
    assert coding_skill["enabled"] == 0
    
    prompt = sm.get_active_skills_prompt_injection()
    assert "Research" in prompt or "Writing" in prompt
    assert "EXPERT SKILL" in prompt
