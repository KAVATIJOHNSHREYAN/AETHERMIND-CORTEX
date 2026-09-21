"""
About Page Component for AetherMind Cortex UI (Phase 6 Expanded)
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
            - **Storage Engine:** SQLite 3 & ChromaDB Local Vector Store
            - **Repository:** `https://github.com/KAVATIJOHNSHREYAN/AETHERMIND-CORTEX`
            """)
            
        gr.Markdown("""
        ### Phase 6 Cognitive Reasoning Engine Milestones
        - ✅ Multi-Step Cognitive Reasoning Pipeline (Intent → Goal → Analysis → Alternatives → Trade-offs → Solution)
        - ✅ Intent Detection Engine & Clarification Generator
        - ✅ Alternative Solution Evaluator (Optimal, Faster, Simpler, Scalable)
        - ✅ Trade-off Analysis & Risk Engine
        - ✅ Confidence Engine & Uncertainty Score Calculator
        - ✅ Developer Mode Reasoning Inspector Accordion in Chat Workspace
        - ✅ 100% Offline Architecture - Zero external cloud dependency
        """)
