"""
AetherMind Cortex Database Connection Manager
Provides thread-safe SQLite connection handling and context management.
"""

import os
import sqlite3
from contextlib import contextmanager
from typing import Generator, Optional
from core.logger import get_logger
from core.config_manager import ConfigManager

logger = get_logger("DatabaseConnection")

class DBConnection:
    """SQLite Database Connection Manager."""

    def __init__(self, db_path: Optional[str] = None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if not db_path:
            config = ConfigManager().config
            rel_path = config.database.path
            db_path = os.path.join(base_dir, rel_path) if not os.path.isabs(rel_path) else rel_path

        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager yielding a database connection with auto-commit/rollback."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database transaction error: {e}")
            raise e
        finally:
            conn.close()

    def check_health(self) -> bool:
        """Verifies database accessibility and connectivity."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1;")
                return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
