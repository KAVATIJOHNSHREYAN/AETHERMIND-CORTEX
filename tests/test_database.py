"""
Unit tests for Database Connection and Initialization
"""

import os
import pytest
from database.connection import DBConnection
from database.init_db import initialize_database

def test_database_connection(tmp_path):
    db_file = str(tmp_path / "test_db.db")
    db_conn = DBConnection(db_path=db_file)
    assert db_conn.check_health() is True

def test_database_initialization(tmp_path):
    db_file = str(tmp_path / "test_db.db")
    db_conn = DBConnection(db_path=db_file)
    assert initialize_database(db_conn) is True
    
    with db_conn.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row["name"] for row in cursor.fetchall()]
        assert "app_settings" in tables
        assert "sessions" in tables
        assert "logs_audit" in tables
