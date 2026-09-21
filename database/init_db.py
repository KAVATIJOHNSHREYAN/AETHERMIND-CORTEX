"""
AetherMind Cortex Database Schema (Phase 5 Expanded)
Includes app_settings, sessions, messages, memories, indexed_documents, user_profile, user_goals, and logs_audit.
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

-- Long-Term Memory Engine Table
CREATE TABLE IF NOT EXISTS memories (
    id TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    key TEXT NOT NULL,
    content TEXT NOT NULL,
    importance INTEGER DEFAULT 5,
    is_pinned INTEGER DEFAULT 0,
    is_archived INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexed Documents for Knowledge RAG Engine
CREATE TABLE IF NOT EXISTS indexed_documents (
    id TEXT PRIMARY KEY,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_hash TEXT NOT NULL,
    file_type TEXT NOT NULL,
    chunk_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Profile Engine Key-Value Table
CREATE TABLE IF NOT EXISTS user_profile (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Goals & Milestones Table
CREATE TABLE IF NOT EXISTS user_goals (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT DEFAULT 'current', -- 'current', 'long_term', 'learning'
    priority TEXT DEFAULT 'medium', -- 'high', 'medium', 'low'
    status TEXT DEFAULT 'active', -- 'active', 'completed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
            logger.info("Database schema initialized successfully (Phase 5 schema active).")
            return True
    except Exception as e:
        logger.error(f"Failed to initialize database schema: {e}")
        return False
