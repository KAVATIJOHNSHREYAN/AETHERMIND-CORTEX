"""
Status Bar Component for AetherMind Cortex UI
"""

import gradio as gr
from app.controller import AppController

def render_status_bar(controller: AppController):
    """Renders the persistent status bar at bottom of app."""
    status = controller.get_system_status()
    with gr.Row(elem_classes=["status-bar-box"]):
        gr.Markdown(
            f"**AetherMind Cortex v{status['version']}** | "
            f"System State: `{status['status']}` | "
            f"Database: `Connected` | "
            f"Python-first Architecture"
        )
