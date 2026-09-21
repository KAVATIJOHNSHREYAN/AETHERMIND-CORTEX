"""
AetherMind Cortex Configuration Manager
Handles YAML-based configuration loading, validation via Pydantic, and runtime modifications.
"""

import os
import yaml
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from core.logger import get_logger

logger = get_logger("ConfigManager")

class AppConfigModel(BaseModel):
    name: str = Field(default="AetherMind Cortex")
    theme: str = Field(default="dark")
    language: str = Field(default="en")
    debug: bool = Field(default=False)

class DatabaseConfigModel(BaseModel):
    db_name: str = Field(default="aethermind.db")
    path: str = Field(default="database/aethermind.db")

class LoggingConfigModel(BaseModel):
    level: str = Field(default="INFO")
    file_name: str = Field(default="aethermind.log")

class UIConfigModel(BaseModel):
    title: str = Field(default="AetherMind Cortex")
    server_name: str = Field(default="127.0.0.1")
    server_port: int = Field(default=7860)
    show_api: bool = Field(default=False)

class ConfigModel(BaseModel):
    app: AppConfigModel = Field(default_factory=AppConfigModel)
    database: DatabaseConfigModel = Field(default_factory=DatabaseConfigModel)
    logging: LoggingConfigModel = Field(default_factory=LoggingConfigModel)
    ui: UIConfigModel = Field(default_factory=UIConfigModel)

class ConfigManager:
    """Singleton Configuration Manager class."""
    _instance: Optional["ConfigManager"] = None

    def __new__(cls, config_path: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_path: Optional[str] = None):
        if self._initialized:
            return

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = config_path or os.path.join(base_dir, "config", "settings.yaml")
        self.config: ConfigModel = self._load_config()
        self._initialized = True

    def _load_config(self) -> ConfigModel:
        """Loads configuration from YAML file or falls back to defaults."""
        if not os.path.exists(self.config_path):
            logger.warning(f"Config file not found at {self.config_path}. Creating default configuration.")
            default_config = ConfigModel()
            self.save_config(default_config)
            return default_config

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                raw_data = yaml.safe_load(f) or {}
            config = ConfigModel(**raw_data)
            logger.info(f"Loaded configuration from {self.config_path}")
            return config
        except Exception as e:
            logger.error(f"Failed to load config file {self.config_path}: {e}. Using defaults.")
            return ConfigModel()

    def save_config(self, config: Optional[ConfigModel] = None) -> bool:
        """Saves current or provided configuration back to YAML."""
        target_config = config or self.config
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(target_config.model_dump(), f, default_flow_style=False)
            self.config = target_config
            logger.info(f"Saved configuration to {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False

    def get_dict(self) -> Dict[str, Any]:
        """Returns config as dictionary."""
        return self.config.model_dump()
