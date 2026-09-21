"""
Knowledge Dashboard UI Component for AetherMind Cortex (Phase 4.2 Expanded)
Allows document uploading, folder scanning, local indexing, collection stats, index rebuilding, and semantic RAG search with confidence scores.
"""

import gradio as gr
from app.controller import AppController

def render_knowledge_tab(controller: AppController):
    """Renders the offline Knowledge Engine & Document Indexing Dashboard."""
    with gr.Tab("📚 Knowledge Engine"):
        gr.Markdown("### 📚 Production Offline Document RAG & Knowledge Engine")
        gr.Markdown("*Index local PDF, DOCX, TXT, Markdown, or Code files/folders into ChromaDB vector storage with local semantic retrieval & confidence scoring.*")

        # Collection Statistics Header Cards
        with gr.Row():
            stats_md = gr.Markdown("📊 **Collection Stats:** Loading statistics...")
            refresh_stats_btn = gr.Button("🔄 Refresh Stats", variant="secondary", size="sm")

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### 📥 Ingest Local Documents / Folders")
            with gr.Row():
                file_upload = gr.File(label="Upload Local File (PDF, DOCX, TXT, MD, Code)", file_count="single")
                folder_path_input = gr.Textbox(placeholder="Or enter absolute path to local folder / file...", label="Local Directory / File Path", scale=2)
            
            with gr.Row():
                index_btn = gr.Button("⚡ Ingest & Index Path/File", variant="primary")
                rebuild_btn = gr.Button("🔨 Rebuild Vector Index", variant="stop")
            index_status = gr.Markdown()

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### 🔍 Semantic Vector Search & Relevance Confidence Testing")
            with gr.Row():
                search_input = gr.Textbox(placeholder="Type query to test semantic document RAG retrieval...", label="Semantic Document Query", scale=5)
                search_btn = gr.Button("🔍 Query Vector DB", variant="secondary", scale=1)
            search_results_table = gr.Dataframe(
                headers=["Snippet", "File Name", "Chunk Index", "Confidence Score (%)"],
                datatype=["str", "str", "number", "str"],
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

        def fetch_stats():
            stats = controller.knowledge_engine.get_collection_stats()
            types_str = ", ".join([f"{k}: {v}" for k, v in stats["file_types"].items()]) or "None"
            return f"📁 **Indexed Files:** {stats['total_documents']} | 🧩 **Total Vector Chunks:** {stats['total_chunks']} | 📂 **Formats:** {types_str} | 🟢 **Status:** {stats['status']}"

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
                return fetch_docs(), fetch_stats(), "❌ Error: Please provide a file or folder path."

            path_clean = target_path.strip()
            import os
            if os.path.isdir(path_clean):
                res = controller.knowledge_engine.batch_ingest_directory(path_clean)
                msg = f"✅ {res['message']}"
            else:
                res = controller.knowledge_engine.ingest_file(path_clean)
                if res["success"]:
                    msg = f"✅ {res['message']}" if not res.get("duplicate") else f"⚠️ {res['message']}"
                else:
                    msg = f"❌ {res['message']}"
                    
            return fetch_docs(), fetch_stats(), msg

        def on_rebuild():
            success = controller.knowledge_engine.rebuild_index()
            status_msg = "✅ Vector index successfully rebuilt!" if success else "❌ Failed to rebuild vector index."
            return fetch_docs(), fetch_stats(), status_msg

        def on_search_docs(query: str):
            chunks = controller.knowledge_engine.search_rag_chunks(query, limit=5)
            data = []
            for c in chunks:
                meta = c["metadata"]
                data.append([
                    c["content"][:150] + "...",
                    meta.get("file_name", "Unknown"),
                    meta.get("chunk_index", 0),
                    f"{c.get('confidence_score', 85.0)}%"
                ])
            return data

        # Initial values
        stats_md.value = fetch_stats()

        # Event triggers
        refresh_stats_btn.click(fn=fetch_stats, outputs=[stats_md])
        index_btn.click(
            fn=on_index_doc,
            inputs=[file_upload, folder_path_input],
            outputs=[docs_table, stats_md, index_status]
        )
        rebuild_btn.click(
            fn=on_rebuild,
            outputs=[docs_table, stats_md, index_status]
        )
        search_btn.click(
            fn=on_search_docs,
            inputs=[search_input],
            outputs=[search_results_table]
        )
