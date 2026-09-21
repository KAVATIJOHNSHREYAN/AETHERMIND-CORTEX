"""
Sidebar Component for AetherMind Cortex UI
"""

import gradio as gr
from app.controller import AppController

def render_sidebar(controller: AppController):
    """Renders the left navigation sidebar."""
    meta = controller.get_metadata()
    with gr.Column(scale=1, elem_classes=["sidebar-panel"]):
        gr.Markdown(f"## 🧠 {meta['app_name']}")
        gr.Markdown(f"*{meta['description']}*")
        gr.Markdown(f"**Version:** `{meta['version']}`")
        gr.Markdown("---")
        gr.Markdown("### Navigation & Quick Status")
        
        status_md = gr.Markdown("🟢 DB Connection: Active\n⚡ Mode: Phase 1 Shell")
        refresh_btn = gr.Button("🔄 Refresh System Status", variant="secondary", size="sm")
        
        def refresh():
            status = controller.get_system_status()
            db_icon = "🟢" if status["db_healthy"] else "🔴"
            return f"{db_icon} DB Status: {status['status']}\n⚡ Theme: {status['theme'].capitalize()}\n📦 Ver: {status['version']}"

        refresh_btn.click(fn=refresh, outputs=[status_md])
