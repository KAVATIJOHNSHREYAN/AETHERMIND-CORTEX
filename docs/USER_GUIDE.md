# AetherMind Cortex – User Guide (v1.0 Flagship Release)

Welcome to **AetherMind Cortex**, a human-centered, privacy-first AI reasoning platform designed to run 100% offline on your local machine.

---

## 🚀 Quick Start Guide

### 1. Launching AetherMind Cortex
You can run AetherMind Cortex using either the CLI Python launcher or the native desktop container:
- **PySide6 Native Desktop App:**
  ```bash
  python pyside_app.py
  ```
- **Web Interface (Gradio):**
  ```bash
  python app/main.py
  ```

---

## 🛠 Subsystem Overview & Usage

### 🧠 1. Chat & Multi-Step Reasoning Engine
- **Model Selection:** Choose from locally installed Ollama models (e.g., `llama3`, `mistral`, `gemma`).
- **Reasoning Mode:** Select between *Fast*, *Detailed*, or *Multi-Perspective* reasoning to view step-by-step evaluation, intent detection, trade-offs, and confidence scores.

### 📚 2. Offline Knowledge Engine (RAG)
- Navigate to the **Knowledge Base** tab.
- Ingest documents (`.pdf`, `.docx`, `.txt`, `.md`, `.py`) via file upload or folder indexing.
- Run hybrid semantic search and ask context-aware questions with direct source citations.

### 👤 3. Human Profile & Adaptive Personalization
- Manage stored preferences, coding style, goal trackers, and working style insights.
- Privacy First: Edit or erase profile attributes at any time.

### 📊 4. Decision Intelligence & Risk Assessment
- Open the **Decision Engine** tab.
- Compare multiple choices across technical, financial, and time risks with transparent weighted scores.

### ⚡ 5. Local Automation & Python Script Execution
- Schedule automated folder cleanup, python script execution, document summaries, and local reminders.
- Includes safety check confirmation before executing file mutations.

### 🧩 6. Ecosystem Plugin Manager & Workspaces
- Manage workspaces and toggle modular extension plugins safely with explicit permission controls.

### 🩺 7. System Diagnostics & Self-Healing
- Open the **Diagnostics** tab to perform automated 12-subsystem health checks.
- Click **Run Self-Healing Repair** to optimize SQLite database indexes and clear temporary caches.

---

## 🔒 Privacy & Local Security
- 100% Offline execution — zero external API telemetry.
- All vector databases, memory traces, and local user settings reside on your device in `database/`.
