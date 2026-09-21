"""
AetherMind Cortex Skill Manager
Manages discovery, registration, enabling/disabling, priority, and prompt injection for Modular Expert Skills.
"""

from typing import Dict, List, Any, Optional
from database.connection import DBConnection
from core.logger import get_logger
from core.skills.base_skill import BaseSkill
from core.skills.coding_skill import CodingSkill
from core.skills.research_skill import ResearchSkill
from core.skills.writing_skill import WritingSkill
from core.skills.data_skill import DataSkill
from core.skills.learning_skill import LearningSkill
from core.skills.project_skill import ProjectSkill

logger = get_logger("SkillManager")

class SkillManager:
    """Registry and orchestrator for AetherMind Modular Expert Skills."""

    def __init__(self, db_conn: Optional[DBConnection] = None):
        self.db_conn = db_conn or DBConnection()
        self.skills: Dict[str, BaseSkill] = {}
        
        # Register core skills
        self._register_default_skills()
        self._sync_skills_db()

    def _register_default_skills(self):
        """Instantiates default expert skill implementations."""
        defaults = [
            CodingSkill(),
            ResearchSkill(),
            WritingSkill(),
            DataSkill(),
            LearningSkill(),
            ProjectSkill()
        ]
        for skill in defaults:
            self.skills[skill.skill_id] = skill

    def _sync_skills_db(self):
        """Syncs registered skills into SQLite database."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                for skill in self.skills.values():
                    cursor.execute(
                        """
                        INSERT INTO registered_skills (skill_id, name, category, description, enabled, priority)
                        VALUES (?, ?, ?, ?, 1, 5)
                        ON CONFLICT(skill_id) DO UPDATE SET name=excluded.name, description=excluded.description
                        """,
                        (skill.skill_id, skill.name, skill.category, skill.description)
                    )
        except Exception as e:
            logger.error(f"Error syncing skills DB: {e}")

    def list_skills(self) -> List[Dict[str, Any]]:
        """Lists registered skills and their enable state."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT skill_id, name, category, description, enabled, priority FROM registered_skills ORDER BY priority DESC")
                rows = cursor.fetchall()
                return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"Failed to list skills: {e}")
            return []

    def set_skill_status(self, skill_id: str, enabled: bool) -> bool:
        """Enables or disables a specific expert skill."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE registered_skills SET enabled = ? WHERE skill_id = ?", (1 if enabled else 0, skill_id))
            logger.info(f"Updated skill [{skill_id}] enabled = {enabled}")
            return True
        except Exception as e:
            logger.error(f"Failed to update skill status: {e}")
            return False

    def get_active_skills_prompt_injection(self) -> str:
        """Builds system prompt context snippet combining all currently enabled skills."""
        active_ids = []
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT skill_id FROM registered_skills WHERE enabled = 1")
                active_ids = [r["skill_id"] for r in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to fetch active skills: {e}")
            active_ids = list(self.skills.keys())

        if not active_ids:
            return ""

        snippets = []
        for sid in active_ids:
            if sid in self.skills:
                snippets.append(self.skills[sid].get_system_prompt_snippet())

        return "\n".join(snippets)
