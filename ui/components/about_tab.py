"""
About Page Component for AetherMind Cortex UI
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
            - **Architecture:** Clean Modular Python Architecture (No JS Frameworks)
            - **UI Framework:** Gradio
            - **Storage Engine:** SQLite 3
            - **Repository:** `https://github.com/KAVATIJOHNSHREYAN/AETHERMIND-CORTEX`
            """)
            
        gr.Markdown("""
        ### Phase 1 Architectural Milestones
        - ✅ Modular Directory Structure (`app`, `core`, `config`, `database`, `ui`, `utils`, `logs`, `tests`, `docs`)
        - ✅ Persistent SQLite database configuration & schema management
        - ✅ Dual console & file logger with rotation
        - ✅ Modern Python-first Gradio web application layout
        - ✅ Dynamic runtime configuration manager
        """)
