"""
AetherMind Cortex Central Application Controller (Phase 9 Expanded)
Orchestrates Config, DB, Ollama Engine, Sessions, Memory, RAG, Profile, Reasoning Engine, Workflow Engine, Decision Engine, and Skill Manager.
"""

from typing import Dict, Any, Optional, List
from core.config_manager import ConfigManager
from core.logger import get_logger
from core.settings import SettingsManager
from core.version import get_app_metadata, get_version_string
from database.connection import DBConnection
from database.init_db import initialize_database
from core.llm_engine import OllamaEngine
from core.session_manager import SessionManager
from core.memory_manager import MemoryManager
from core.knowledge_engine import KnowledgeEngine
from core.profile_manager import ProfileManager
from core.reasoning_engine import ReasoningEngine
from core.workflow_engine import WorkflowEngine
from core.decision_engine import DecisionEngine
from core.skill_manager import SkillManager

logger = get_logger("AppController")

class AppController:
    """Central Application Controller managing all sub-systems."""
    _instance: Optional["AppController"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        logger.info("Initializing AetherMind Cortex Central Controller (Phase 9)...")
        self.config_manager = ConfigManager()
        self.db_conn = DBConnection()
        self.settings_manager = SettingsManager(self.db_conn)
        
        # Initialize SQLite DB
        self.db_initialized = initialize_database(self.db_conn)
        
        # Initialize Engines
        self.llm_engine = OllamaEngine()
        self.session_manager = SessionManager(self.db_conn)
        self.memory_manager = MemoryManager(self.db_conn)
        self.knowledge_engine = KnowledgeEngine(self.db_conn)
        self.profile_manager = ProfileManager(self.db_conn)
        self.reasoning_engine = ReasoningEngine()
        self.workflow_engine = WorkflowEngine(self.db_conn)
        self.decision_engine = DecisionEngine(self.db_conn)
        self.skill_manager = SkillManager(self.db_conn)
        
        # Active session state
        self.current_session_id: Optional[str] = None
        self.ensure_active_session()

        self._initialized = True
        logger.info("AetherMind Cortex Controller Phase 9 initialized successfully.")

    def ensure_active_session(self) -> str:
        """Ensures there is an active session loaded."""
        sessions = self.session_manager.list_sessions()
        if sessions:
            self.current_session_id = sessions[0]["id"]
        else:
            models = self.get_available_models()
            default_model = models[0] if models else "default"
            self.current_session_id = self.session_manager.create_session("New Session", default_model)
        return self.current_session_id

    def get_available_models(self) -> List[str]:
        """Retrieves installed Ollama models."""
        return self.llm_engine.list_available_models()

    def get_ollama_status(self) -> Dict[str, Any]:
        """Checks Ollama connection health."""
        return self.llm_engine.check_service_status()

    def get_system_status(self) -> Dict[str, Any]:
        """Gathers system status indicators for UI display."""
        db_healthy = self.db_conn.check_health()
        ollama_status = self.get_ollama_status()
        current_theme = self.settings_manager.get_setting("app.theme", "dark")
        memory_count = len(self.memory_manager.list_memories(include_archived=True))
        doc_count = len(self.knowledge_engine.list_indexed_documents())
        task_count = len(self.workflow_engine.list_tasks(status="all"))
        decision_count = len(self.decision_engine.list_saved_decisions())
        active_skills_count = len([s for s in self.skill_manager.list_skills() if s["enabled"] == 1])
        user_name = self.profile_manager.get_profile_attribute("user_name", "User")
        
        return {
            "status": "Online" if (db_healthy and ollama_status["online"]) else "Degraded",
            "db_healthy": db_healthy,
            "ollama_online": ollama_status["online"],
            "ollama_models": ollama_status["model_count"],
            "memory_count": memory_count,
            "doc_count": doc_count,
            "task_count": task_count,
            "decision_count": decision_count,
            "active_skills": active_skills_count,
            "user_name": user_name,
            "version": get_version_string(),
            "theme": current_theme,
            "app_name": self.config_manager.config.app.name,
        }

    def update_theme(self, new_theme: str) -> str:
        """Updates theme in runtime settings and database."""
        success = self.settings_manager.set_setting("app.theme", new_theme)
        if success:
            logger.info(f"Theme changed to: {new_theme}")
            return f"Theme changed to {new_theme} successfully."
        return "Failed to update theme."

    def get_metadata(self) -> Dict[str, Any]:
        """Returns metadata detailing application configuration and versioning."""
        return get_app_metadata()

    # Session CRUD Delegates
    def create_new_session(self, model_name: Optional[str] = None) -> str:
        self.current_session_id = self.session_manager.create_session("New Chat", model_name)
        return self.current_session_id

    def switch_session(self, session_id: str) -> List[Dict[str, Any]]:
        self.current_session_id = session_id
        return self.session_manager.get_session_messages(session_id)

    def get_active_messages(self) -> List[Dict[str, Any]]:
        if not self.current_session_id:
            self.ensure_active_session()
        return self.session_manager.get_session_messages(self.current_session_id)

    def add_user_message(self, content: str) -> bool:
        if not self.current_session_id:
            self.ensure_active_session()
        return self.session_manager.add_message(self.current_session_id, "user", content)

    def add_assistant_message(self, content: str, tokens: int = 0) -> bool:
        if not self.current_session_id:
            self.ensure_active_session()
        return self.session_manager.add_message(self.current_session_id, "assistant", content, tokens)

    def clear_active_session(self) -> bool:
        if self.current_session_id:
            return self.session_manager.clear_session_messages(self.current_session_id)
        return False

    def export_active_session(self, format_type: str = "markdown") -> str:
        if self.current_session_id:
            return self.session_manager.export_session(self.current_session_id, format_type)
        return ""
