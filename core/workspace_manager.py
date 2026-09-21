"""
AetherMind Cortex Workspace Manager
Manages multi-workspace switching, session restoration, and workspace template creation.
"""

import uuid
from typing import List, Dict, Any, Optional
from database.connection import DBConnection
from core.logger import get_logger

logger = get_logger("WorkspaceManager")

class WorkspaceManager:
    """Manages workspace state and session restoration across environments."""

    def __init__(self, db_conn: Optional[DBConnection] = None):
        self.db_conn = db_conn or DBConnection()
        self._ensure_default_workspaces()

    def _ensure_default_workspaces(self):
        """Initializes default workspaces in SQLite if empty."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) as count FROM workspaces")
                if cursor.fetchone()["count"] == 0:
                    samples = [
                        ("ws_default", "Default Workspace", "General AI reasoning workspace.", 1),
                        ("ws_research", "Research Lab", "Dedicated workspace for academic document RAG.", 0),
                        ("ws_development", "Software Engineering Studio", "Coding, refactoring, and debugging workspace.", 0)
                    ]
                    for wid, name, desc, act in samples:
                        cursor.execute(
                            "INSERT INTO workspaces (id, name, description, is_active) VALUES (?, ?, ?, ?)",
                            (wid, name, desc, act)
                        )
        except Exception as e:
            logger.error(f"Error seeding default workspaces: {e}")

    def list_workspaces(self) -> List[Dict[str, Any]]:
        """Lists stored workspaces."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, description, is_active, created_at FROM workspaces ORDER BY is_active DESC, name ASC")
                rows = cursor.fetchall()
                return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"Failed to list workspaces: {e}")
            return []

    def set_active_workspace(self, workspace_id: str) -> bool:
        """Sets active workspace and restores workspace environment state."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE workspaces SET is_active = 0;")
                cursor.execute("UPDATE workspaces SET is_active = 1 WHERE id = ?", (workspace_id,))
            logger.info(f"Switched active workspace to [{workspace_id}]")
            return True
        except Exception as e:
            logger.error(f"Failed to set active workspace [{workspace_id}]: {e}")
            return False

    def create_workspace(self, name: str, description: str = "") -> str:
        """Creates a new workspace."""
        wid = str(uuid.uuid4())
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO workspaces (id, name, description, is_active) VALUES (?, ?, ?, 0)",
                    (wid, name, description)
                )
            logger.info(f"Created workspace [{wid}]: {name}")
            return wid
        except Exception as e:
            logger.error(f"Failed to create workspace: {e}")
            return wid
