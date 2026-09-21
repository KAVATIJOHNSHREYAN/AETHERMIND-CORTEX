"""
Sidebar Component for AetherMind Cortex UI (Phase 4 Expanded)
Provides Ollama Model Selector, Session History, and System Controls.
"""

import gradio as gr
from app.controller import AppController

def render_sidebar(controller: AppController):
    """Renders left navigation sidebar with Model selector & Chat sessions list."""
    meta = controller.get_metadata()
    available_models = controller.get_available_models()
    default_model = available_models[0] if available_models else "None Found"
    
    with gr.Column(scale=1, elem_classes=["sidebar-panel"]):
        gr.Markdown(f"## 🧠 {meta['app_name']}")
        gr.Markdown(f"*{meta['description']}*")
        gr.Markdown(f"**Version:** `{meta['version']}`")
        gr.Markdown("---")
        
        # Local AI Engine Controls
        gr.Markdown("### 🤖 Local Model Selection")
        model_dropdown = gr.Dropdown(
            choices=available_models if available_models else ["No models found"],
            value=default_model,
            label="Active Ollama Model",
            interactive=True if available_models else False
        )
        refresh_models_btn = gr.Button("🔄 Refresh Models", variant="secondary", size="sm")
        
        gr.Markdown("---")
        # Chat Session History List
        gr.Markdown("### 💬 Chat Sessions")
        new_chat_btn = gr.Button("➕ New Chat Session", variant="primary", size="sm")
        
        sessions = controller.session_manager.list_sessions()
        session_choices = [(s["title"], s["id"]) for s in sessions] if sessions else [("New Chat", controller.current_session_id or "default")]
        
        session_dropdown = gr.Dropdown(
            choices=[title for title, _ in session_choices],
            value=session_choices[0][0] if session_choices else "New Chat",
            label="Session History",
            interactive=True
        )

        gr.Markdown("---")
        gr.Markdown("### ⚡ System Health")
        status_md = gr.Markdown()

        def refresh_status():
            status = controller.get_system_status()
            db_icon = "🟢" if status["db_healthy"] else "🔴"
            ollama_icon = "🟢" if status["ollama_online"] else "🔴"
            return (
                f"{db_icon} **DB:** {'Healthy' if status['db_healthy'] else 'Error'}\n\n"
                f"{ollama_icon} **Ollama:** {'Online' if status['ollama_online'] else 'Offline'} ({status['ollama_models']} models)\n\n"
                f"🧠 **Memories:** {status['memory_count']} | 📚 **Docs:** {status['doc_count']}"
            )

        status_md.value = refresh_status()

        # Dynamic refresh handler for models
        def on_refresh_models():
            models = controller.get_available_models()
            val = models[0] if models else "No models found"
            return gr.update(choices=models if models else ["No models found"], value=val), refresh_status()

        refresh_models_btn.click(fn=on_refresh_models, outputs=[model_dropdown, status_md])

        return model_dropdown, session_dropdown, new_chat_btn
