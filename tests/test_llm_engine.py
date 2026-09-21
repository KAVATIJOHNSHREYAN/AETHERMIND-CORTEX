"""
Unit tests for Local LLM Engine
"""

import pytest
from core.llm_engine import OllamaEngine

def test_ollama_service_check():
    engine = OllamaEngine()
    status = engine.check_service_status()
    assert isinstance(status, dict)
    assert "online" in status

def test_list_available_models():
    engine = OllamaEngine()
    models = engine.list_available_models()
    assert isinstance(models, list)
