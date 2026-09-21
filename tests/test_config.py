"""
Unit tests for Configuration and Settings Managers
"""

import os
import pytest
from core.config_manager import ConfigManager, ConfigModel
from core.settings import SettingsManager
from database.connection import DBConnection
from database.init_db import initialize_database

@pytest.fixture
def temp_db(tmp_path):
    db_file = str(tmp_path / "test_aethermind.db")
    db_conn = DBConnection(db_path=db_file)
    initialize_database(db_conn)
    return db_conn

def test_config_manager_default():
    config_mgr = ConfigManager()
    assert config_mgr.config.app.name == "AetherMind Cortex"
    assert config_mgr.config.app.theme in ["dark", "light"]

def test_settings_manager_set_get(temp_db):
    settings = SettingsManager(db_conn=temp_db)
    assert settings.set_setting("app.theme", "light") is True
    assert settings.get_setting("app.theme") == "light"
