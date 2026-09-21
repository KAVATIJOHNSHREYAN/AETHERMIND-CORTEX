# AetherMind Cortex - Architecture Documentation

## Overview
**AetherMind Cortex** is a human-centered AI reasoning engine designed with a Python-first, modular architecture. It uses **Gradio** for user interface rendering, **SQLite** for relational session and configuration persistence, and clean software architecture (SOLID principles).

## Directory Structure & Responsibilities

- **`main.py`**: Application launcher and entry point.
- **`app/`**:
  - `controller.py`: Central Application Controller orchestrating database state, runtime configurations, and UI interactions.
- **`core/`**:
  - `config_manager.py`: Pydantic & YAML-backed configuration loader and validator.
  - `logger.py`: Centralized dual console and rotating file logger.
  - `settings.py`: DB & YAML synchronized settings manager.
  - `version.py`: Version metadata manager.
- **`config/`**:
  - `settings.yaml`: Default system configuration settings.
- **`database/`**:
  - `connection.py`: Thread-safe SQLite connection context manager.
  - `init_db.py`: Schema setup and SQL table migrations.
- **`ui/`**:
  - `theme.py`: Custom CSS and Gradio theme provider.
  - `layout.py`: Master Gradio UI builder assembling modular components.
  - `components/`: Modular UI widgets (`sidebar.py`, `chat.py`, `settings_tab.py`, `about_tab.py`, `status_bar.py`).
- **`utils/`**:
  - `error_handler.py`: Global exception classes and safe execution wrappers.
- **`logs/`**: Log outputs (`aethermind.log`).
- **`tests/`**: Automated unit test suite using `pytest`.
