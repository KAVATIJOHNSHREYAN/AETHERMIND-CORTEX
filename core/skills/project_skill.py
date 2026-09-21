"""
Project Planner Skill for AetherMind Cortex
Provides milestone roadmaps, sprint planning, and task generation.
"""

from core.skills.base_skill import BaseSkill

class ProjectSkill(BaseSkill):
    """Specialized AI Expert for Agile Project Planning & Roadmap Execution."""

    @property
    def skill_id(self) -> str:
        return "project_planner"

    @property
    def name(self) -> str:
        return "Agile Project & Sprint Planner"

    @property
    def category(self) -> str:
        return "Management"

    @property
    def description(self) -> str:
        return "Deconstructs project visions into milestones, sprint roadmaps, deliverable tasks, and dependency schedules."

    def get_system_prompt_snippet(self) -> str:
        return """
--- EXPERT SKILL: Agile Project & Sprint Planner ---
- Structure roadmaps into Phase milestones, Sprints, and actionable User Stories.
- Include effort estimates, dependencies, and risk mitigation strategies.
----------------------------------------------------
"""
