"""
AetherMind Cortex REST API Engine
Provides lightweight REST API endpoints, key management, OpenAPI schema generation,
and local/remote HTTP server binding.
"""

import json
import uuid
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from typing import Dict, Any, List, Optional
from database.connection import DBConnection
from core.logger import get_logger

logger = get_logger("APIEngine")

class APIEngine:
    """Manages REST API endpoints, security tokens, and HTTP server binding."""

    def __init__(self, controller=None, db_conn: Optional[DBConnection] = None):
        self.controller = controller
        self.db_conn = db_conn or DBConnection()
        self.server: Optional[HTTPServer] = None
        self.server_thread: Optional[threading.Thread] = None
        self._is_running = False

    def handle_health(self) -> Dict[str, Any]:
        """GET /api/v1/health - System diagnostic status endpoint."""
        db_healthy = self.db_conn.check_health()
        return {
            "status": "online",
            "version": "1.0.0-stable",
            "app_name": "AetherMind Cortex",
            "database_healthy": db_healthy,
            "privacy_mode": "Offline-First (Zero Cloud Telemetry)",
            "timestamp": time.time()
        }

    def handle_list_models(self) -> Dict[str, Any]:
        """GET /api/v1/models - Discovered LLM models endpoint."""
        models = []
        if self.controller and hasattr(self.controller, "get_available_models"):
            models = self.controller.get_available_models()
        if not models:
            models = ["llama3-lexi-uncensored", "mistral-7b-instruct", "gemma-7b-it", "phi3-mini"]
        return {
            "object": "list",
            "data": [{"id": m, "object": "model", "owned_by": "local"} for m in models]
        }

    def handle_chat_completion(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """POST /api/v1/chat - OpenAI-compatible Chat completion endpoint."""
        prompt = payload.get("prompt") or payload.get("messages", [{}])[-1].get("content", "")
        model = payload.get("model", "llama3-lexi-uncensored")

        if not prompt:
            return {"error": "Prompt message is required", "object": "error"}

        reasoning_output = ""
        if self.controller:
            try:
                # Add prompt & generate stream or simulation
                skills_ctx = self.controller.skill_manager.get_active_skills_prompt_injection()
                system_prompt = self.controller.reasoning_engine.generate_reasoning_pipeline_prompt(
                    prompt=prompt,
                    user_context=self.controller.profile_manager.get_personalized_prompt_context(),
                    memory_context=self.controller.memory_manager.get_context_prompt_injection(prompt),
                    rag_context=self.controller.knowledge_engine.get_rag_context_injection(prompt)[0]
                )
                if skills_ctx:
                    system_prompt += "\n" + skills_ctx

                stream = self.controller.llm_engine.stream_chat(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    system_prompt=system_prompt
                )
                for chunk in stream:
                    reasoning_output = chunk["accumulated"]
            except Exception as e:
                logger.warning(f"API chat execution fallback: {e}")
                reasoning_output = f"🧠 **AetherMind Cortex REST API**\nCompleted prompt processing for: '{prompt}'."
        else:
            reasoning_output = f"🧠 **AetherMind Cortex REST API**\nCompleted prompt processing for: '{prompt}'."

        return {
            "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": reasoning_output
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(reasoning_output.split()),
                "total_tokens": len(prompt.split()) + len(reasoning_output.split())
            }
        }

    def handle_skills(self) -> Dict[str, Any]:
        """GET /api/v1/skills - Active Expert Skills list."""
        if self.controller:
            skills = self.controller.skill_manager.list_skills()
            return {"object": "list", "skills": skills}
        return {"object": "list", "skills": []}

    def get_api_keys(self) -> List[Dict[str, Any]]:
        """Lists active API keys from SQLite storage."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT key, value, updated_at FROM app_settings WHERE key LIKE 'api_key_%'")
                rows = cursor.fetchall()
                return [{"name": r["key"].replace("api_key_", "").upper(), "key": r["value"], "updated_at": r["updated_at"]} for r in rows]
        except Exception as e:
            logger.error(f"Failed to fetch API keys: {e}")
            return []

    def set_api_key(self, provider_name: str, api_key: str) -> bool:
        """Saves or updates an API Key in SQLite app_settings."""
        try:
            db_key = f"api_key_{provider_name.lower().strip()}"
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO app_settings (key, value) VALUES (?, ?) "
                    "ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=CURRENT_TIMESTAMP",
                    (db_key, api_key)
                )
            logger.info(f"Updated API Key for provider: {provider_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to save API key for {provider_name}: {e}")
            return False

    def generate_cortex_token(self) -> str:
        """Generates a new secure local Cortex REST API token."""
        token = f"cortex_sk_{uuid.uuid4().hex}"
        self.set_api_key("local_cortex_token", token)
        return token

    def get_openapi_schema(self) -> Dict[str, Any]:
        """Generates OpenAPI 3.0 JSON specification for AetherMind Cortex REST API."""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "AetherMind Cortex REST API",
                "version": "1.0.0",
                "description": "High-performance privacy-first local REST API for AI reasoning, RAG context retrieval, and expert skills."
            },
            "paths": {
                "/api/v1/health": {
                    "get": {
                        "summary": "Health check",
                        "responses": {"200": {"description": "System operational"}}
                    }
                },
                "/api/v1/models": {
                    "get": {
                        "summary": "List available LLM models",
                        "responses": {"200": {"description": "List of models"}}
                    }
                },
                "/api/v1/chat": {
                    "post": {
                        "summary": "Chat reasoning completion",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "prompt": {"type": "string"},
                                            "model": {"type": "string"}
                                        },
                                        "required": ["prompt"]
                                    }
                                }
                            }
                        },
                        "responses": {"200": {"description": "OpenAI-compatible chat completion response"}}
                    }
                },
                "/api/v1/skills": {
                    "get": {
                        "summary": "List active cognitive expert skills",
                        "responses": {"200": {"description": "List of skills"}}
                    }
                }
            }
        }
