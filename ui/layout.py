"""
AetherMind Cortex UI Layout Assembly
Combines sidebar, chat, settings, about, and status bar into a single Gradio Blocks layout.
"""

import gradio as gr
from app.controller import AppController
from ui.theme import get_theme, CUSTOM_CSS
from ui.components.sidebar import render_sidebar
from ui.components.chat import render_chat_tab
from ui.components.settings_tab import render_settings_tab
from ui.components.about_tab import render_about_tab
from ui.components.status_bar import render_status_bar

def build_ui(controller: AppController) -> gr.Blocks:
    """Assembles and returns the Gradio UI Blocks interface."""
    current_theme_name = controller.settings_manager.get_setting("app.theme", "dark")
    theme = get_theme(current_theme_name)
    
    with gr.Blocks(
        theme=theme,
        css=CUSTOM_CSS,
        title="AetherMind Cortex - Human-Centered AI Reasoning Engine"
    ) as demo:
        with gr.Row(elem_classes=["aether-header"]):
            gr.Markdown("# 🧠 AetherMind Cortex")
            
        with gr.Row():
            # Left Sidebar Navigation & Controls
            render_sidebar(controller)
            
            # Main View Area with Tabs
            with gr.Column(scale=4):
                with gr.Tabs():
                    render_chat_tab()
                    render_settings_tab(controller)
                    render_about_tab(controller)
                    
        # Bottom Persistent Status Bar
        render_status_bar(controller)
        
    return demo
