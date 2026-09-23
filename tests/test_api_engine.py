"""
Unit tests for AetherMind Cortex REST API Engine module.
"""

import pytest
from app.controller import AppController
from core.api_engine import APIEngine

@pytest.fixture
def api_engine():
    controller = AppController()
    return controller.api_engine

def test_api_engine_health(api_engine):
    """Verify GET /api/v1/health status output."""
    health = api_engine.handle_health()
    assert health["status"] == "online"
    assert health["version"] == "1.0.0-stable"
    assert health["database_healthy"] is True

def test_api_engine_models(api_engine):
    """Verify GET /api/v1/models list output."""
    models = api_engine.handle_list_models()
    assert models["object"] == "list"
    assert isinstance(models["data"], list)
    assert len(models["data"]) > 0

def test_api_engine_chat_completion(api_engine):
    """Verify POST /api/v1/chat completion output."""
    res = api_engine.handle_chat_completion({"prompt": "Hello REST API"})
    assert res["object"] == "chat.completion"
    assert len(res["choices"]) > 0
    assert "content" in res["choices"][0]["message"]

def test_api_engine_key_management(api_engine):
    """Verify API key storage and generation."""
    success = api_engine.set_api_key("OpenAI", "sk-test-12345")
    assert success is True
    
    keys = api_engine.get_api_keys()
    assert len(keys) > 0
    
    token = api_engine.generate_cortex_token()
    assert token.startswith("cortex_sk_")

def test_api_engine_openapi_schema(api_engine):
    """Verify OpenAPI 3.0 schema generation."""
    schema = api_engine.get_openapi_schema()
    assert schema["openapi"] == "3.0.0"
    assert "/api/v1/chat" in schema["paths"]
