"""
Research Expert Skill for AetherMind Cortex
Provides document comparison, literature synthesis, and source summarization.
"""

from core.skills.base_skill import BaseSkill

class ResearchSkill(BaseSkill):
    """Specialized AI Expert for Research, Literature Review, and Source Synthesis."""

    @property
    def skill_id(self) -> str:
        return "research_expert"

    @property
    def name(self) -> str:
        return "Research & Literature Synthesis Expert"

    @property
    def category(self) -> str:
        return "Research"

    @property
    def description(self) -> str:
        return "Synthesizes literature, compares document sources, and generates structured academic/technical summaries."

    def get_system_prompt_snippet(self) -> str:
        return """
--- EXPERT SKILL: Research & Synthesis Expert ---
- Provide rigorous source citations and cross-document comparison.
- Highlight key findings, methodologies, constraints, and conflicting evidence.
- Structure responses with bulleted summaries and executive abstracts.
--------------------------------------------------
"""
