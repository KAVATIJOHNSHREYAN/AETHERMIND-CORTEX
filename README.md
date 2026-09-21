# AetherMind Cortex

**Human-Centered AI Reasoning Engine**

AetherMind Cortex is a Python-first, scalable AI reasoning engine platform designed with clean modular architecture and SOLID principles.

## Features (Phase 1)
- 🐍 **100% Python Architecture**: Built without React/Next.js/Node.js dependencies.
- 🎨 **Gradio Modern Interface**: Glassmorphism themed sidebar, chat workspace, system settings, and status monitoring.
- 🗄️ **SQLite Persistence**: Thread-safe database initialization for settings, sessions, and logs.
- ⚙️ **Config & Settings Manager**: YAML configuration parsing with Pydantic runtime validation.
- 📜 **Centralized Logging System**: Rotating file logging with colored console outputs.
- 🧪 **Unit Test Suite**: Fully automated test coverage using `pytest`.

## Project Structure
```
AetherMind-Cortex/
├── app/          # Central Application Controller
├── core/         # Config, Logger, Settings, Version Managers
├── config/       # System YAML configuration
├── database/     # SQLite connection & Schema initializers
├── ui/           # Gradio layout & modular UI components
├── assets/       # Visual resources & themes
├── utils/        # Error handlers and utility logic
├── logs/         # System logs
├── tests/        # Pytest unit tests
├── docs/         # System & Architecture documentation
├── requirements.txt
├── README.md
└── main.py       # Application Launcher
```

## Getting Started

### Prerequisites
- Python 3.12+ (or 3.13)

### Installation
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
python main.py
```
Open your browser at `http://127.0.0.1:7860`.

### Running Tests
```bash
pytest
```
