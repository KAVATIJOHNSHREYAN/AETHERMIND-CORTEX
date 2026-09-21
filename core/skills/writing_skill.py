"""
Writing Expert Skill for AetherMind Cortex
Provides technical documentation, blog posts, reports, and grammar enhancement.
"""

from core.skills.base_skill import BaseSkill

class WritingSkill(BaseSkill):
    """Specialized AI Expert for Technical Writing and Content Refinement."""

    @property
    def skill_id(self) -> str:
        return "writing_expert"

    @property
    def name(self) -> str:
        return "Technical Writing & Editing Expert"

    @property
    def category(self) -> str:
        return "Content"

    @property
    def description(self) -> str:
        return "Crafts technical documentation, engineering reports, blogs, and refines grammar for publication."

    def get_system_prompt_snippet(self) -> str:
        return """
--- EXPERT SKILL: Technical Writing & Editing Expert ---
- Ensure clear, engaging, and precise prose tailored to the target audience.
- Use active voice, crisp headings, and logical paragraph flow.
--------------------------------------------------------
"""
