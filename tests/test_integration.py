"""
Phase 12 End-to-End Integration & System Diagnostics Tests
"""

import os
import pytest
from app.controller import AppController
from core.diagnostics import DiagnosticsEngine
from utils.security import hash_secret, encode_local_payload, decode_local_payload

@pytest.fixture
def controller():
    ctrl = AppController()
    return ctrl

def test_security_crypto_utils():
    """Verify cryptographic hashing and local payload obfuscation."""
    raw = "cortex_secret_key"
    hashed = hash_secret(raw)
    assert len(hashed) == 64  # SHA-256 hex length
    
    payload = "Sensitive User Memory Data"
    encrypted = encode_local_payload(payload)
    assert encrypted != payload
    decrypted = decode_local_payload(encrypted)
    assert decrypted == payload

def test_diagnostics_engine(controller):
    """Verify system health diagnostic check across all subsystems."""
    engine = DiagnosticsEngine(controller.db_conn)
    report = engine.run_full_diagnostics()
    assert report["overall_status"] in ["PASS", "FAIL"]
    assert report["subsystems_checked"] == 12
    assert report["database_healthy"] is True

def test_diagnostics_self_healing(controller):
    """Verify database self-healing repair optimization."""
    engine = DiagnosticsEngine(controller.db_conn)
    res = engine.execute_self_healing_repair()
    assert res["success"] is True
    assert "optimized" in res["message"]

def test_end_to_end_controller_workflow(controller):
    """Verify end-to-end execution across multi-subsystem controller facade."""
    meta = controller.get_metadata()
    assert meta["version"] == "1.0.0-stable"
    
    # 1. Create chat session
    sess_id = controller.create_new_session(model_name="llama3")
    assert sess_id is not None
    
    # 2. Add memory & fetch memory
    controller.memory_manager.add_memory(category="user", key="Pref", content="Prefers Python over C++")
    mems = controller.memory_manager.list_memories(category="user")
    assert len(mems) > 0
    
    # 3. Decision Engine evaluation
    dec = controller.decision_engine.evaluate_decision(
        topic="Architecture Selection",
        options=["Monolith", "Modular Clean Architecture"]
    )
    assert "recommended_option" in dec
    
    # 4. Expert Skill Execution
    skills = controller.skill_manager.list_skills()
    assert len(skills) == 6
