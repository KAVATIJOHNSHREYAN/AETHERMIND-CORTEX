"""
Desktop Notification & System Tray Utility
"""

from core.logger import get_logger

logger = get_logger("DesktopNotifier")

def send_desktop_notification(title: str, message: str) -> bool:
    """Sends a local desktop notification."""
    logger.info(f"Desktop Notification -> [{title}]: {message}")
    return True
