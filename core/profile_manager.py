"""
AetherMind Cortex Human Profile Manager
Manages User Identity, Preferences, Goals, Working Style, and Adaptive System Prompt Generation.
"""

import uuid
import json
from typing import Dict, Any, List, Optional
from database.connection import DBConnection
from core.logger import get_logger

logger = get_logger("ProfileManager")

DEFAULT_PROFILE = {
    "user_name": "User",
    "profession": "Developer / Architect",
    "experience_level": "Intermediate",  # Beginner, Intermediate, Expert
    "preferred_language": "English",
    "time_zone": "UTC+05:30",
    "coding_style": "Clean Modular Architecture",
    "writing_style": "Technical & Concise",
    "explanation_depth": "Balanced",  # Brief, Balanced, Deep-Dive
    "working_style": "Structured Planner",
    "personalization_enabled": "true"
}

class ProfileManager:
    """Manages User Persona, Preferences, Goals, and Adaptive Context Injections."""

    def __init__(self, db_conn: Optional[DBConnection] = None):
        self.db_conn = db_conn or DBConnection()
        self._ensure_default_profile()

    def _ensure_default_profile(self):
        """Initializes default profile parameters in SQLite if missing."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                for k, v in DEFAULT_PROFILE.items():
                    cursor.execute(
                        "INSERT INTO user_profile (key, value) VALUES (?, ?) ON CONFLICT(key) DO NOTHING",
                        (k, v)
                    )
        except Exception as e:
            logger.error(f"Error initializing profile defaults: {e}")

    def get_profile_attribute(self, key: str, default: str = "") -> str:
        """Retrieves a specific profile attribute value."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM user_profile WHERE key = ?", (key,))
                row = cursor.fetchone()
                if row:
                    return row["value"]
        except Exception as e:
            logger.error(f"Failed to get profile key '{key}': {e}")
        return DEFAULT_PROFILE.get(key, default)

    def set_profile_attribute(self, key: str, value: str) -> bool:
        """Sets or updates a profile attribute value."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO user_profile (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=CURRENT_TIMESTAMP",
                    (key, str(value))
                )
            logger.info(f"Updated profile attribute: {key} = {value}")
            return True
        except Exception as e:
            logger.error(f"Failed to set profile key '{key}': {e}")
            return False

    def get_full_profile(self) -> Dict[str, str]:
        """Returns all user profile key-value attributes."""
        profile = DEFAULT_PROFILE.copy()
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT key, value FROM user_profile")
                rows = cursor.fetchall()
                for r in rows:
                    profile[r["key"]] = r["value"]
        except Exception as e:
            logger.error(f"Failed to fetch full profile: {e}")
        return profile

    def update_profile_bulk(self, data: Dict[str, str]) -> bool:
        """Updates multiple profile fields at once."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                for k, v in data.items():
                    cursor.execute(
                        "INSERT INTO user_profile (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=CURRENT_TIMESTAMP",
                        (k, str(v))
                    )
            logger.info("Bulk profile update successful.")
            return True
        except Exception as e:
            logger.error(f"Failed bulk profile update: {e}")
            return False

    # Goals Engine
    def add_goal(self, title: str, category: str = "current", priority: str = "medium") -> str:
        """Adds a goal or learning topic."""
        goal_id = str(uuid.uuid4())
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO user_goals (id, title, category, priority, status) VALUES (?, ?, ?, ?, 'active')",
                    (goal_id, title, category.lower(), priority.lower())
                )
            logger.info(f"Added goal [{goal_id}]: {title}")
            return goal_id
        except Exception as e:
            logger.error(f"Failed to add goal: {e}")
            return goal_id

    def list_goals(self, status: str = "active") -> List[Dict[str, Any]]:
        """Lists user goals."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, title, category, priority, status, created_at FROM user_goals WHERE status = ? ORDER BY created_at DESC", (status,))
                rows = cursor.fetchall()
                return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"Failed to list goals: {e}")
            return []

    def delete_goal(self, goal_id: str) -> bool:
        """Deletes a goal."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM user_goals WHERE id = ?", (goal_id,))
            return True
        except Exception as e:
            logger.error(f"Failed to delete goal [{goal_id}]: {e}")
            return False

    # Prompt Adaptive Personalization
    def get_personalized_prompt_context(self) -> str:
        """Generates adaptive system prompt context based on user profile and active goals."""
        if self.get_profile_attribute("personalization_enabled", "true") != "true":
            return ""

        profile = self.get_full_profile()
        goals = self.list_goals(status="active")

        goals_str = ""
        if goals:
            goals_str = "\nActive User Goals:\n" + "\n".join([f"- [{g['category'].upper()}] {g['title']} (Priority: {g['priority']})" for g in goals[:3]])

        context = f"""
--- Personalized User Context & Persona ---
- User Name: {profile.get('user_name', 'User')} ({profile.get('profession', 'Developer')})
- Experience Level: {profile.get('experience_level', 'Intermediate')}
- Preferred Coding Style: {profile.get('coding_style', 'Clean Modular')}
- Preferred Explanation Depth: {profile.get('explanation_depth', 'Balanced')}
- Writing Style: {profile.get('writing_style', 'Technical & Concise')}
{goals_str}
---------------------------------------------
Adapt explanations, code snippets, and tone to align with this user profile.
"""
        return context

    # Export & Import
    def export_profile_json(self) -> str:
        """Exports full profile and goals to JSON string."""
        data = {
            "profile": self.get_full_profile(),
            "goals": self.list_goals(status="active")
        }
        return json.dumps(data, indent=2)

    def reset_profile(self) -> bool:
        """Resets profile to defaults and clears goals."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM user_profile;")
                cursor.execute("DELETE FROM user_goals;")
            self._ensure_default_profile()
            logger.info("Reset user profile to default settings.")
            return True
        except Exception as e:
            logger.error(f"Failed to reset profile: {e}")
            return False
