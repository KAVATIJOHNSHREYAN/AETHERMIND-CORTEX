"""
About Page Component for AetherMind Cortex UI (Phase 8 Expanded)
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
        ### Phase 8 Decision Intelligence Milestones
        - ✅ Multi-Criteria Decision Analysis (MCDA) Weighted Scoring Framework
        - ✅ Alternative Comparison & Option Ranking (Best, Fastest, Safest, Scalable)
        - ✅ Technical & Resource Risk Matrix Evaluation
        - ✅ Interactive Decision Intelligence Dashboard UI
        - ✅ Decision History Persistence & Continuous Feedback Loop
        - ✅ 100% Offline Architecture - Zero cloud dependency & privacy-first design
        """)
