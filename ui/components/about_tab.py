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
        ### Phase 11 Desktop Experience & Ecosystem Milestones
        - ✅ Native PySide6 Desktop GUI Window Container (`pyside_app.py`)
        - ✅ Ecosystem Plugin Manager & Permissions Control (`installed_plugins` table)
        - ✅ Multi-Workspace Switcher & Session State Restoration (`workspaces` table)
        - ✅ Full System Backup Zip Archive Generator & Restore Manager
        - ✅ 100% Offline Architecture - Zero cloud telemetry & privacy-first design
        """)
