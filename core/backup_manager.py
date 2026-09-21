"""
AetherMind Cortex Backup & Restore Manager
Provides full zip archives of SQLite database state, settings, and memory vectors.
"""

import os
import zipfile
from typing import Dict, Any, Optional
from core.logger import get_logger

logger = get_logger("BackupManager")

class BackupManager:
    """Manages system backup ZIP generation and restoration."""

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def create_system_backup(self) -> Dict[str, Any]:
        """Creates a single zip archive of database, config, and logs."""
        backup_filename = "aethermind_system_backup.zip"
        backup_path = os.path.join(self.base_dir, "logs", backup_filename)
        
        db_path = os.path.join(self.base_dir, "database", "aethermind.db")
        config_path = os.path.join(self.base_dir, "config", "settings.yaml")

        try:
            with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                if os.path.exists(db_path):
                    zipf.write(db_path, arcname="database/aethermind.db")
                if os.path.exists(config_path):
                    zipf.write(config_path, arcname="config/settings.yaml")

            logger.info(f"Created system backup at {backup_path}")
            return {
                "success": True,
                "backup_path": backup_path,
                "message": f"Successfully created backup zip: {backup_filename}"
            }
        except Exception as e:
            logger.error(f"Failed to create backup zip: {e}")
            return {"success": False, "message": f"Backup failed: {e}"}
