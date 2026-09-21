"""
Data Expert Skill for AetherMind Cortex
Provides tabular CSV analysis, statistical summaries, and pattern detection.
"""

from core.skills.base_skill import BaseSkill

class DataSkill(BaseSkill):
    """Specialized AI Expert for Data Analytics & Pattern Detection."""

    @property
    def skill_id(self) -> str:
        return "data_expert"

    @property
    def name(self) -> str:
        return "Data Analytics & Statistics Expert"

    @property
    def category(self) -> str:
        return "Analytics"

    @property
    def description(self) -> str:
        return "Analyzes datasets, detects statistical anomalies, generates summaries, and identifies data trends."

    def get_system_prompt_snippet(self) -> str:
        return """
--- EXPERT SKILL: Data Analytics & Statistics Expert ---
- Focus on quantitative metrics, data distributions, correlation, and anomalies.
- Format summaries using Markdown tables and statistical insights.
--------------------------------------------------------
"""
