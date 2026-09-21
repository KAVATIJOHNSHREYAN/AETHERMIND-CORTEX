# AetherMind Cortex – Developer & Architecture Guide (v1.0)

This guide provides technical specifications, architectural patterns, and extension points for developers contributing to or extending **AetherMind Cortex**.

---

## 🏗 Architecture Overview

AetherMind Cortex follows a **Clean Modular Architecture** orchestrated via a Singleton pattern:

```
                  ┌───────────────────────────────┐
                  │    PySide6 / Gradio UI        │
                  └──────────────┬────────────────┘
                                 │
                  ┌──────────────▼────────────────┐
                  │      AppController (Facade)    │
                  └──────────────┬────────────────┘
                                 │
     ┌───────────────────────────┼───────────────────────────┐
     │                           │                           │
┌────▼─────────────┐   ┌─────────▼───────────┐   ┌───────────▼─────────┐
│ ReasoningEngine  │   │ KnowledgeEngine     │   │ DecisionEngine      │
└──────────────────┘   └─────────────────────┘   └─────────────────────┘
```

---

## 📁 Repository Structure

- `app/controller.py`: Central facade coordinating all 12 subsystems.
- `app/main.py`: Gradio Web interface entry point.
- `pyside_app.py`: Qt PySide6 Desktop application window entry point.
- `core/`: Primary reasoning, diagnostics, and domain models (`reasoning.py`, `diagnostics.py`, `version.py`).
- `database/`: Database connection wrapper (`db.py`), SQLite schema, and ChromaDB vector persistence.
- `knowledge/`: RAG document processing, text chunking, and semantic vector indexing.
- `memory/`: Short-term session memory and long-term vector-backed episodic memory.
- `human_profile/`: User identity, preference engine, goal tracking, and workflow analysis.
- `decision/`: Decision framework, weighted MCDA scoring, and risk assessment engine.
- `skills/`: Expert skill modules (Coding, Research, Writing, Data, Learning, Project Planner).
- `automation/`: File automation, document batch processing, script runner, and scheduler.
- `plugins/`: Dynamic plugin registry, plugin loader, and security permissions manager.
- `workspace/`: Multi-workspace switcher and session state restoration manager.
- `utils/`: Cryptographic hashing, encryption helper, backup manager, and logging.
- `ui/`: Modern Gradio components and responsive CSS theme system.
- `tests/`: Unit and integration test suite using `pytest`.

---

## 🧪 Testing Guidelines

Run unit tests locally using `pytest`:
```bash
pytest tests/ -v
```

---

## 📦 Building Executable Bundle

AetherMind Cortex includes PyInstaller configuration file `aethermind.spec`. To build a standalone executable:
```bash
pyinstaller aethermind.spec --noconfirm
```
Output standalone executable will be located under `dist/AetherMindCortex/`.
