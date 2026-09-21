"""
AetherMind Cortex Settings Manager
Provides persistent settings storage synchronized between runtime memory, YAML, and SQLite DB.
"""

from typing import Any, Optional, Dict
from core.config_manager import ConfigManager
from database.connection import DBConnection
from core.logger import get_logger

logger = get_logger("SettingsManager")

class SettingsManager:
    """Manages application settings with SQLite persistence and fallback to ConfigManager."""

    def __init__(self, db_conn: Optional[DBConnection] = None):
        self.config_manager = ConfigManager()
        self.db_conn = db_conn or DBConnection()

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Retrieves a setting value from DB, falling back to Config YAML."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM app_settings WHERE key = ?", (key,))
                row = cursor.fetchone()
                if row:
                    return row["value"]
        except Exception as e:
            logger.warning(f"Error querying setting '{key}' from DB: {e}")

        # Fallback to ConfigManager dictionary
        config_dict = self.config_manager.get_dict()
        parts = key.split(".")
        val = config_dict
        for part in parts:
            if isinstance(val, dict) and part in val:
                val = val[part]
            else:
                return default
        return val

    def set_setting(self, key: str, value: Any) -> bool:
        """Sets a setting value in SQLite database and updates runtime memory."""
        str_val = str(value)
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO app_settings (key, value) VALUES (?, ?) "
                    "ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=CURRENT_TIMESTAMP",
                    (key, str_val),
                )
            logger.info(f"Setting updated: {key} = {str_val}")
            return True
        except Exception as e:
            logger.error(f"Failed to update setting '{key}' in DB: {e}")
            return False

    def get_all_settings(self) -> Dict[str, Any]:
        """Returns merged dictionary of file config and DB settings."""
        settings = self.config_manager.get_dict()
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT key, value FROM app_settings")
                rows = cursor.fetchall()
                for row in rows:
                    settings[row["key"]] = row["value"]
        except Exception as e:
            logger.error(f"Failed to fetch DB settings: {e}")
        return settings
