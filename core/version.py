"""
AetherMind Cortex Version Manager
Provides version information and project metadata.
"""

from typing import Dict, Any

VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 0
VERSION_STAGE = "alpha"

APP_NAME = "AetherMind Cortex"
APP_DESCRIPTION = "Human-Centered AI Reasoning Engine"
AUTHOR = "AetherMind Team"
AUTHOR = "KAVATI JOHN SHREYAN"

def get_version_string() -> str:
    """Returns the formatted semantic version string."""
    return f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}-{VERSION_STAGE}"

def get_app_metadata() -> Dict[str, Any]:
    """Returns application metadata summary."""
    return {
        "app_name": APP_NAME,
        "description": APP_DESCRIPTION,
        "version": get_version_string(),
        "author": AUTHOR,
        "stage": VERSION_STAGE,
        "python_target": ">=3.12"
    }
