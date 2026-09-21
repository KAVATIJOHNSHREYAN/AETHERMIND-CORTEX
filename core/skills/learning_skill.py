"""
Learning Expert Skill for AetherMind Cortex
Provides custom learning roadmaps, quizzes, flashcards, and concept mastery tracking.
"""

from core.skills.base_skill import BaseSkill

class LearningSkill(BaseSkill):
    """Specialized AI Expert for Pedagogy, Quizzes, and Learning Roadmaps."""

    @property
    def skill_id(self) -> str:
        return "learning_expert"

    @property
    def name(self) -> str:
        return "Learning & Pedagogy Expert"

    @property
    def category(self) -> str:
        return "Education"

    @property
    def description(self) -> str:
        return "Generates step-by-step learning roadmaps, interactive quizzes, flashcards, and concept breakdown."

    def get_system_prompt_snippet(self) -> str:
        return """
--- EXPERT SKILL: Learning & Pedagogy Expert ---
- Break complex subjects into digestible learning modules.
- Include practice questions, quiz checks, and conceptual flashcards.
------------------------------------------------
"""
