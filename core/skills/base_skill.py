"""
Abstract Base Skill Interface for AetherMind Cortex Expert Skills System
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseSkill(ABC):
    """Abstract Base Class for all modular AetherMind Expert Skills."""

    @property
    @abstractmethod
    def skill_id(self) -> str:
        """Unique identifier string for the skill."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human readable name for the skill."""
        pass

    @property
    @abstractmethod
    def category(self) -> str:
        """Skill category classification."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Brief description of skill capabilities."""
        pass

    @abstractmethod
    def get_system_prompt_snippet(self) -> str:
        """Returns the system prompt context injection for this expert skill."""
        pass
