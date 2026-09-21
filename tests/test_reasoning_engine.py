"""
Unit tests for Cognitive Reasoning Engine
"""

import pytest
from core.reasoning_engine import ReasoningEngine

def test_intent_detection():
    re = ReasoningEngine()
    
    res1 = re.analyze_intent("Hi")
    assert res1["is_ambiguous"] is True
    assert res1["clarification_needed"] is not None
    
    res2 = re.analyze_intent("How do I design a microservice architecture?")
    assert res2["is_complex"] is True
    assert res2["intent"] == "System Architecture & Design"

def test_reasoning_prompt_generation():
    re = ReasoningEngine()
    prompt = re.generate_reasoning_pipeline_prompt("Optimize SQL query performance")
    assert "INTENT & OBJECTIVE" in prompt
    assert "MULTI-STEP REASONING PIPELINE" in prompt
    assert "Trade-off Analysis" in prompt

def test_developer_inspection_log():
    re = ReasoningEngine()
    log = re.build_developer_inspection_log("Design high-throughput cache", 1.25, 340)
    assert log["developer_mode"] is True
    assert len(log["reasoning_steps"]) == 5
    assert "confidence_score" in log
