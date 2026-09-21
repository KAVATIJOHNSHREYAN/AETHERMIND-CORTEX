"""
AetherMind Cortex Plugin Manager
Handles dynamic plugin loading, plugin registration, permissions, and plugin marketplace architecture.
"""

import os
import json
import uuid
from typing import List, Dict, Any, Optional
from database.connection import DBConnection
from core.logger import get_logger

logger = get_logger("PluginManager")

class PluginManager:
    """Manages discovery, enablement, permissions, and registration of custom plugins."""

    def __init__(self, db_conn: Optional[DBConnection] = None):
        self.db_conn = db_conn or DBConnection()
        self._ensure_sample_plugins()

    def _ensure_sample_plugins(self):
        """Initializes default marketplace structure in SQLite if empty."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) as count FROM installed_plugins")
                if cursor.fetchone()["count"] == 0:
                    samples = [
                        ("plugin_git_integration", "Git Repository Assistant", "1.1.0", 1, "local_read_write"),
                        ("plugin_docker_monitor", "Docker Container Monitor", "1.0.0", 1, "local_process"),
                        ("plugin_latex_export", "LaTeX Math Formatter", "0.9.5", 0, "local_read")
                    ]
                    for pid, name, ver, en, perm in samples:
                        cursor.execute(
                            "INSERT INTO installed_plugins (id, name, version, enabled, permissions) VALUES (?, ?, ?, ?, ?)",
                            (pid, name, ver, en, perm)
                        )
        except Exception as e:
            logger.error(f"Error seeding default plugins: {e}")

    def list_plugins(self) -> List[Dict[str, Any]]:
        """Lists installed plugins."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, version, enabled, permissions, created_at FROM installed_plugins ORDER BY name ASC")
                rows = cursor.fetchall()
                return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"Failed to list plugins: {e}")
            return []

    def set_plugin_status(self, plugin_id: str, enabled: bool) -> bool:
        """Enables or disables an installed plugin."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE installed_plugins SET enabled = ? WHERE id = ?", (1 if enabled else 0, plugin_id))
            logger.info(f"Updated plugin [{plugin_id}] enabled = {enabled}")
            return True
        except Exception as e:
            logger.error(f"Failed to set plugin status: {e}")
            return False
