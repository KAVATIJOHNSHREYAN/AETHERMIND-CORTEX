"""
Knowledge Dashboard UI Component for AetherMind Cortex (Phase 4)
Allows document uploading, local indexing, RAG vector database management, and semantic document search.
"""

import gradio as gr
from app.controller import AppController

def render_knowledge_tab(controller: AppController):
    """Renders the offline Knowledge Engine & Document Indexing Dashboard."""
    with gr.Tab("📚 Knowledge Engine"):
        gr.Markdown("### 📚 Offline Document Ingestion & RAG Engine")
        gr.Markdown("*Index local PDF, DOCX, TXT, Markdown, or Code files into local ChromaDB vector storage for Retrieval-Augmented Generation.*")

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### 📥 Index New Documents")
            file_upload = gr.File(label="Upload Local File (PDF, DOCX, TXT, MD, Code)", file_count="single")
            file_path_input = gr.Textbox(placeholder="Or enter absolute path to local file...", label="Local File System Path")
            index_btn = gr.Button("⚡ Ingest & Index Document", variant="primary")
            index_status = gr.Markdown()

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### 🔍 Test Knowledge Vector Query")
            with gr.Row():
                search_input = gr.Textbox(placeholder="Type query to test semantic document RAG retrieval...", label="Semantic Document Query", scale=5)
                search_btn = gr.Button("🔍 Query Vector DB", variant="secondary", scale=1)
            search_results_table = gr.Dataframe(
                headers=["Snippet", "File Name", "Chunk Index", "Relevance Distance"],
                datatype=["str", "str", "number", "number"],
                col_count=(4, "fixed"),
                wrap=True
            )

        gr.Markdown("#### 📑 Indexed Document Library")
        docs_table = gr.Dataframe(
            headers=["ID", "File Name", "File Path", "File Type", "Chunks", "Indexed Date"],
            datatype=["str", "str", "str", "str", "number", "str"],
            col_count=(6, "fixed"),
            wrap=True
        )

        def fetch_docs():
            docs = controller.knowledge_engine.list_indexed_documents()
            data = []
            for d in docs:
                data.append([
                    d["id"][:8],
                    d["file_name"],
                    d["file_path"],
                    d["file_type"].upper(),
                    d["chunk_count"],
                    d["created_at"]
                ])
            return data

        def on_index_doc(upload_file, path_input):
            target_path = upload_file.name if upload_file else path_input
            if not target_path or not target_path.strip():
                return fetch_docs(), "❌ Error: Please provide a file or file path."

            res = controller.knowledge_engine.ingest_file(target_path.strip())
            if res["success"]:
                msg = f"✅ {res['message']}" if not res.get("duplicate") else f"⚠️ {res['message']}"
            else:
                msg = f"❌ {res['message']}"
            return fetch_docs(), msg

        def on_search_docs(query: str):
            chunks = controller.knowledge_engine.search_rag_chunks(query, limit=5)
            data = []
            for c in chunks:
                meta = c["metadata"]
                data.append([
                    c["content"][:150] + "...",
                    meta.get("file_name", "Unknown"),
                    meta.get("chunk_index", 0),
                    round(c.get("distance", 0.0), 3)
                ])
            return data

        # Event triggers
        index_btn.click(
            fn=on_index_doc,
            inputs=[file_upload, file_path_input],
            outputs=[docs_table, index_status]
        )
        search_btn.click(
            fn=on_search_docs,
            inputs=[search_input],
            outputs=[search_results_table]
        )
