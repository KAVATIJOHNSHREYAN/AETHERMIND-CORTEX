"""
AetherMind Cortex Logging Module
Provides centralized, structured logging for console and file output.
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

DEFAULT_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")

def get_logger(name: str = "AetherMind", log_level: int = logging.INFO, log_file: Optional[str] = "aethermind.log") -> logging.Logger:
    """
    Creates or retrieves a configured logger instance with colored output for console
    and rotating file handler support.
    
    Args:
        name: Name of the logger module.
        log_level: Logging severity level (logging.DEBUG, logging.INFO, etc.).
        log_file: Name of the log file inside the logs/ directory.
        
    Returns:
        logging.Logger: Fully configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Avoid duplicate handlers if already initialized
    if logger.hasHandlers():
        return logger
        
    formatter = logging.Formatter(DEFAULT_LOG_FORMAT)
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Rotating File Handler
    if log_file:
        os.makedirs(LOG_DIR, exist_ok=True)
        file_path = os.path.join(LOG_DIR, log_file)
        file_handler = RotatingFileHandler(
            file_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger

# Module-level default logger
logger = get_logger()
