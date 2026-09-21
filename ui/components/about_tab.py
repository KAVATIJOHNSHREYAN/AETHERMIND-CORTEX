"""
About Page Component for AetherMind Cortex UI (Phase 11 Expanded)
"""

import gradio as gr
from app.controller import AppController

def render_about_tab(controller: AppController):
    """Renders the About system information page."""
    meta = controller.get_metadata()
    with gr.Tab("ℹ️ About AetherMind"):
        gr.Markdown(f"# {meta['app_name']}")
        gr.Markdown(f"### {meta['description']}")
        
        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown(f"""
            - **Version:** `{meta['version']}` ({meta['stage']})
            - **Python Target:** `{meta['python_target']}`
            - **Architecture:** Clean Modular Python Architecture & PySide6 Desktop Container
            - **UI Framework:** Gradio & PySide6 (Qt)
            - **Storage Engine:** SQLite 3 & ChromaDB Local Vector Store
            - **Repository:** `https://github.com/KAVATIJOHNSHREYAN/AETHERMIND-CORTEX`
            """)
            
        gr.Markdown("""
        ### Phase 12 Production Release v1.0 Milestones
        - ✅ **System Diagnostics & Self-Healing:** Automated health verification & SQLite VACUUM optimization
        - ✅ **Local Encryption & Security:** Base64 local obfuscation & SHA-256 password security hashing
        - ✅ **PyInstaller Desktop Builder:** `aethermind.spec` multi-platform standalone executable configuration
        - ✅ **Native PySide6 Desktop GUI Window Container:** Standalone launcher (`pyside_app.py`)
        - ✅ **Ecosystem Plugin Manager & Permissions:** Modularity & safety controls
        - ✅ **Multi-Workspace Switcher & Session State Restoration:** Workspaces & profile management
        - ✅ **100% Offline Privacy-First Architecture:** Zero cloud telemetry & 100% local model integration
        """)

