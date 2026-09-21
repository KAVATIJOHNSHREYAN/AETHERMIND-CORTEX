"""
Settings Component for AetherMind Cortex UI
"""

import gradio as gr
from app.controller import AppController

def render_settings_tab(controller: AppController):
    """Renders application settings tab."""
    with gr.Tab("⚙️ System Settings"):
        gr.Markdown("### Application Configuration & Theme Controls")
        
        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### Appearance")
            theme_dropdown = gr.Dropdown(
                choices=["dark", "light"],
                value=controller.settings_manager.get_setting("app.theme", "dark"),
                label="Interface Theme"
            )
            theme_btn = gr.Button("Save Theme Setting", variant="secondary")
            theme_status = gr.Markdown()
            
            theme_btn.click(
                fn=lambda t: controller.update_theme(t),
                inputs=[theme_dropdown],
                outputs=[theme_status]
            )

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### Database Configuration")
            db_path_input = gr.Textbox(
                value=controller.config_manager.config.database.path,
                label="SQLite Database Path",
                interactive=False
            )
            db_health = gr.Button("Test Database Connection", variant="secondary")
            db_status = gr.Markdown()
            
            db_health.click(
                fn=lambda: f"Database Status: {'Healthy ✅' if controller.db_conn.check_health() else 'Unhealthy ❌'}",
                outputs=[db_status]
            )
