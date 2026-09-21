"""
AetherMind Cortex Error Handling Module
Provides custom exception classes and global error handling utils.
"""

import sys
import traceback
from typing import Callable, Any
from core.logger import get_logger

logger = get_logger("ErrorHandler")

class AetherMindException(Exception):
    """Base exception class for AetherMind Cortex."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        super().__init__(message)
        self.message = message
        self.code = code

class ConfigurationError(AetherMindException):
    """Raised when configuration fails or is invalid."""
    def __init__(self, message: str):
        super().__init__(message, code="CONFIG_ERROR")

class DatabaseError(AetherMindException):
    """Raised when database interactions fail."""
    def __init__(self, message: str):
        super().__init__(message, code="DB_ERROR")

def safe_execute(func: Callable, *args: Any, **kwargs: Any) -> Any:
    """
    Safely executes a function, logging any unhandled exceptions and preventing application crash.
    """
    try:
        return func(*args, **kwargs)
    except AetherMindException as e:
        logger.error(f"Handled Exception [{e.code}]: {e.message}")
        return None
    except Exception as e:
        exc_type, exc_val, exc_tb = sys.exc_info()
        tb_str = "".join(traceback.format_exception(exc_type, exc_val, exc_tb))
        logger.critical(f"Unhandled Exception in {func.__name__}: {e}\n{tb_str}")
        return None
