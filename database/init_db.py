"""
AetherMind Cortex Database Initialization & Migration
Sets up required relational tables for state, audit logs, key-value settings, sessions, and messages.
"""

from database.connection import DBConnection
from core.logger import get_logger

logger = get_logger("DBInitializer")

SCHEMA_SQL = """
-- Application Key-Value Settings Table
CREATE TABLE IF NOT EXISTS app_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sessions Table for Chat & Reasoning Context
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    model_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat Messages Table
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    prompt_tokens INTEGER DEFAULT 0,
    completion_tokens INTEGER DEFAULT 0,
    eval_duration_ms REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

-- Audit Log Table
CREATE TABLE IF NOT EXISTS logs_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level TEXT NOT NULL,
    module TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def initialize_database(db_connection: DBConnection = None) -> bool:
    """
    Executes schema initialization queries to create tables if they do not exist.
    """
    connection = db_connection or DBConnection()
    try:
        with connection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(SCHEMA_SQL)
            logger.info("Database schema initialized successfully (Phase 2 schema active).")
            return True
    except Exception as e:
        logger.error(f"Failed to initialize database schema: {e}")
        return False
