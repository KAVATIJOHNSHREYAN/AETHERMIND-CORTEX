"""
AetherMind Cortex UI Layout Assembly (Phase 10 Expanded)
Assembles sidebar, streaming chat workspace, local automation dashboard, expert skills, decision intelligence, workflow dashboard, human profile, memory, knowledge engine, settings, about, and status bar.
"""

import gradio as gr
from app.controller import AppController
from ui.theme import get_theme, CUSTOM_CSS
from ui.components.sidebar import render_sidebar
from ui.components.chat import render_chat_tab
from ui.components.automation_tab import render_automation_tab
from ui.components.skills_tab import render_skills_tab
from ui.components.decision_tab import render_decision_tab
from ui.components.workflow_tab import render_workflow_tab
from ui.components.profile_tab import render_profile_tab
from ui.components.memory_tab import render_memory_tab
from ui.components.knowledge_tab import render_knowledge_tab
from ui.components.settings_tab import render_settings_tab
from ui.components.about_tab import render_about_tab
from ui.components.status_bar import render_status_bar

def build_ui(controller: AppController) -> gr.Blocks:
    """Assembles and returns the Gradio UI Blocks interface for Phase 10."""
    current_theme_name = controller.settings_manager.get_setting("app.theme", "dark")
    theme = get_theme(current_theme_name)
    
    with gr.Blocks(
        theme=theme,
        css=CUSTOM_CSS,
        title="AetherMind Cortex - Human-Centered AI Reasoning Platform"
    ) as demo:
        with gr.Row(elem_classes=["aether-header"]):
            gr.Markdown("# 🧠 AetherMind Cortex (Human-Centered AI Platform)")
            
        with gr.Row():
            # Left Sidebar Navigation & Controls
            model_dropdown, session_dropdown, new_chat_btn = render_sidebar(controller)
            
            # Main View Area with Tabs
            with gr.Column(scale=4):
                with gr.Tabs():
                    chatbot, load_active_history = render_chat_tab(controller, model_dropdown)
                    render_automation_tab(controller)
                    render_skills_tab(controller)
                    render_decision_tab(controller)
                    render_workflow_tab(controller)
                    render_profile_tab(controller)
                    render_memory_tab(controller)
                    render_knowledge_tab(controller)
                    render_settings_tab(controller)
                    render_about_tab(controller)
                    
        # Bottom Persistent Status Bar
        render_status_bar(controller)

        # Connect Sidebar Session Controls
        def on_new_chat():
            new_id = controller.create_new_session(model_dropdown.value)
            sessions = controller.session_manager.list_sessions()
            choices = [s["title"] for s in sessions]
            return gr.update(choices=choices, value=choices[0]), []

        new_chat_btn.click(fn=on_new_chat, outputs=[session_dropdown, chatbot])

        # Connect Session Switch
        def on_session_change(selected_title: str):
            sessions = controller.session_manager.list_sessions()
            matched = [s for s in sessions if s["title"] == selected_title]
            if matched:
                controller.switch_session(matched[0]["id"])
                return load_active_history()
            return []

        session_dropdown.change(fn=on_session_change, inputs=[session_dropdown], outputs=[chatbot])

        # Initial Load Event
        demo.load(fn=load_active_history, outputs=[chatbot])
        
    return demo
