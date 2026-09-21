"""
AetherMind Cortex Central Application Controller
Serves as the main orchestrator binding Core business logic, Database operations, and UI state.
"""

from typing import Dict, Any, Optional
from core.config_manager import ConfigManager
from core.logger import get_logger
from core.settings import SettingsManager
from core.version import get_app_metadata, get_version_string
from database.connection import DBConnection
from database.init_db import initialize_database

logger = get_logger("AppController")

class AppController:
    """Central Application Controller managing application lifecycle and state."""
    _instance: Optional["AppController"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        logger.info("Initializing AetherMind Cortex Central Controller...")
        self.config_manager = ConfigManager()
        self.db_conn = DBConnection()
        self.settings_manager = SettingsManager(self.db_conn)
        
        # Initialize SQLite DB
        self.db_initialized = initialize_database(self.db_conn)
        self._initialized = True
        logger.info("AetherMind Cortex Controller successfully initialized.")

    def get_system_status(self) -> Dict[str, Any]:
        """Gathers system status indicators for UI display."""
        db_healthy = self.db_conn.check_health()
        current_theme = self.settings_manager.get_setting("app.theme", "dark")
        return {
            "status": "Online" if db_healthy else "Degraded",
            "db_healthy": db_healthy,
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
