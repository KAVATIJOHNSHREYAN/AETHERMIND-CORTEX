"""
AetherMind Cortex Local Automation Engine
Handles file organization, template creation, safe Python script execution, reminder scheduling, and automation logging.
"""

import os
import uuid
import subprocess
import shutil
from typing import List, Dict, Any, Optional
from database.connection import DBConnection
from core.logger import get_logger

logger = get_logger("AutomationEngine")

class AutomationEngine:
    """Safe Local Automation Engine for file tasks, project templates, script execution, and reminders."""

    def __init__(self, db_conn: Optional[DBConnection] = None):
        self.db_conn = db_conn or DBConnection()

    def log_job(self, name: str, job_type: str, status: str, logs: str = "") -> str:
        """Logs an automation job execution in SQLite."""
        job_id = str(uuid.uuid4())
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO automation_jobs (id, name, type, status, logs) VALUES (?, ?, ?, ?, ?)",
                    (job_id, name, job_type, status, logs)
                )
            return job_id
        except Exception as e:
            logger.error(f"Failed to log automation job: {e}")
            return job_id

    def list_automation_jobs(self) -> List[Dict[str, Any]]:
        """Lists historical automation jobs."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, type, status, logs, created_at FROM automation_jobs ORDER BY created_at DESC")
                rows = cursor.fetchall()
                return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"Failed to list automation jobs: {e}")
            return []

    # Project Template Automation
    def create_project_template(self, project_name: str, target_dir: str) -> Dict[str, Any]:
        """Creates a standardized clean architecture project folder structure."""
        if not target_dir or not os.path.exists(target_dir):
            return {"success": False, "message": f"Target directory does not exist: {target_dir}"}

        proj_path = os.path.join(target_dir, project_name)
        folders = ["app", "core", "config", "database", "ui", "utils", "logs", "tests", "docs"]
        
        try:
            os.makedirs(proj_path, exist_ok=True)
            for folder in folders:
                os.makedirs(os.path.join(proj_path, folder), exist_ok=True)

            # Create default README and main.py
            with open(os.path.join(proj_path, "README.md"), "w", encoding="utf-8") as f:
                f.write(f"# {project_name}\n\nProject initialized by AetherMind Cortex Automation Engine.\n")
            
            with open(os.path.join(proj_path, "main.py"), "w", encoding="utf-8") as f:
                f.write('if __name__ == "__main__":\n    print("AetherMind Cortex Project Active.")\n')

            msg = f"Project template '{project_name}' created at {proj_path}"
            self.log_job(f"Template: {project_name}", "template", "completed", msg)
            return {"success": True, "message": msg, "path": proj_path}
        except Exception as e:
            msg = f"Failed to create project template: {e}"
            self.log_job(f"Template: {project_name}", "template", "failed", msg)
            return {"success": False, "message": msg}

    # Safe Python Script Executor
    def execute_python_script(self, script_code: str) -> Dict[str, Any]:
        """Executes a Python code string locally in a safe subprocess and captures stdout/stderr."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        temp_script = os.path.join(base_dir, "logs", "_temp_execution.py")
        
        try:
            with open(temp_script, "w", encoding="utf-8") as f:
                f.write(script_code)

            res = subprocess.run(
                ["python", temp_script],
                capture_output=True,
                text=True,
                timeout=15
            )

            output = res.stdout if res.returncode == 0 else f"STDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"
            status = "completed" if res.returncode == 0 else "failed"

            self.log_job("Local Script Execution", "script", status, output)
            return {
                "success": res.returncode == 0,
                "output": output,
                "returncode": res.returncode
            }
        except Exception as e:
            err_msg = f"Script execution error: {e}"
            self.log_job("Local Script Execution", "script", "failed", err_msg)
            return {"success": False, "output": err_msg, "returncode": -1}

    # Reminder System
    def add_reminder(self, message: str) -> str:
        """Adds a local scheduled reminder record."""
        rem_id = str(uuid.uuid4())
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO reminders (id, message, status) VALUES (?, ?, 'pending')",
                    (rem_id, message)
                )
            self.log_job(f"Reminder: {message[:30]}", "reminder", "completed", f"Set reminder: {message}")
            return rem_id
        except Exception as e:
            logger.error(f"Failed to add reminder: {e}")
            return rem_id

    def list_reminders(self) -> List[Dict[str, Any]]:
        """Lists local reminders."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, message, scheduled_time, status, created_at FROM reminders ORDER BY created_at DESC")
                rows = cursor.fetchall()
                return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"Failed to list reminders: {e}")
            return []
