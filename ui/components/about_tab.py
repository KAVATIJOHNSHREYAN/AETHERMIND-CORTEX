"""
About Page Component for AetherMind Cortex UI (Phase 4 Expanded)
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
        ### Phase 4 Offline Knowledge RAG Milestones
        - ✅ PDF, DOCX, TXT, Markdown, and Code Document Ingestion & Text Chunking
        - ✅ ChromaDB Knowledge Vector Database (`database/knowledge_vector/`)
        - ✅ Hybrid Semantic Retrieval & RAG Context Prompt Injection
        - ✅ Source Document Citations with Chunk Snippets in Chat UI
        - ✅ Interactive Knowledge Dashboard UI (Upload, Index, Query)
        - ✅ 100% Offline Architecture - Zero external API/cloud dependency
        """)
