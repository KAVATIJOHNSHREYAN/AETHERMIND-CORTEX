"""
Unit tests for Plugin Manager, Workspace Manager, and Backup Manager
"""

import os
import pytest
from core.plugin_manager import PluginManager
from core.workspace_manager import WorkspaceManager
from core.backup_manager import BackupManager
from database.connection import DBConnection
from database.init_db import initialize_database

@pytest.fixture
def temp_db(tmp_path):
    db_file = str(tmp_path / "test_desktop_phase11.db")
    db_conn = DBConnection(db_path=db_file)
    initialize_database(db_conn)
    return db_conn

def test_plugin_manager(temp_db):
    pm = PluginManager(db_conn=temp_db)
    plugins = pm.list_plugins()
    assert len(plugins) >= 1
    
    pid = plugins[0]["id"]
    assert pm.set_plugin_status(pid, False) is True

def test_workspace_manager(temp_db):
    wm = WorkspaceManager(db_conn=temp_db)
    workspaces = wm.list_workspaces()
    assert len(workspaces) >= 1
    
    new_wid = wm.create_workspace("Custom Test Workspace", "Test Description")
    assert new_wid is not None
    assert wm.set_active_workspace(new_wid) is True

def test_backup_manager():
    bm = BackupManager()
    res = bm.create_system_backup()
    assert res["success"] is True
    assert os.path.exists(res["backup_path"])
