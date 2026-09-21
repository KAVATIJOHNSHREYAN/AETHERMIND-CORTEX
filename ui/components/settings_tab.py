"""
Settings Component for AetherMind Cortex UI (Phase 2)
"""

import gradio as gr
from app.controller import AppController

def render_settings_tab(controller: AppController):
    """Renders application settings tab."""
    with gr.Tab("⚙️ System Settings"):
        gr.Markdown("### Application Configuration & Model Parameters")
        
        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### Local LLM & Ollama Configuration")
            ollama_host_input = gr.Textbox(
                value=controller.llm_engine.host,
                label="Ollama Server Host URL"
            )
            temp_slider = gr.Slider(minimum=0.0, maximum=1.5, value=0.7, step=0.1, label="Temperature (Creativity)")
            top_p_slider = gr.Slider(minimum=0.0, maximum=1.0, value=0.9, step=0.05, label="Top P (Nucleus Sampling)")

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
