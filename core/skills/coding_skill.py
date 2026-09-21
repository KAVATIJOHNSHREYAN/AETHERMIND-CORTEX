"""
Coding Expert Skill for AetherMind Cortex
Provides specialized code generation, refactoring, debugging, docstrings, and clean architecture guidance.
"""

from core.skills.base_skill import BaseSkill

class CodingSkill(BaseSkill):
    """Specialized AI Expert for Software Engineering & Code Generation."""

    @property
    def skill_id(self) -> str:
        return "coding_expert"

    @property
    def name(self) -> str:
        return "Software Engineering & Code Expert"

    @property
    def category(self) -> str:
        return "Development"

    @property
    def description(self) -> str:
        return "Generates clean modular code, executes debugging analysis, refactors functions, and writes docstrings."

    def get_system_prompt_snippet(self) -> str:
        return """
--- EXPERT SKILL: Software Engineering & Code Expert ---
- Enforce clean modular software architecture, type hints, and complete docstrings.
- Write robust error handling and avoid silent exception swallowing.
- Include unit test examples when generating code functions.
--------------------------------------------------------
"""
