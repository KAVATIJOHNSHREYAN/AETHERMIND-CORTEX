"""
Memory Dashboard UI Component for AetherMind Cortex (Phase 3)
Allows viewing, searching, adding, pinning, archiving, and deleting long-term memories.
"""

import gradio as gr
from app.controller import AppController

def render_memory_tab(controller: AppController):
    """Renders the privacy-first Long-Term Memory Dashboard."""
    with gr.Tab("🧠 Long-Term Memory"):
        gr.Markdown("### 🧠 Privacy-First Long-Term Memory Engine")
        gr.Markdown("*All memories are stored 100% locally in SQLite & ChromaDB vector store.*")

        with gr.Row():
            category_filter = gr.Dropdown(
                choices=["All", "User", "Project", "Conversation"],
                value="All",
                label="Filter by Category",
                scale=2
            )
            search_input = gr.Textbox(
                placeholder="Type keywords or query for semantic memory search...",
                label="Semantic Vector Search",
                scale=4
            )
            search_btn = gr.Button("🔍 Search Memory", variant="secondary", scale=1)

        memory_table = gr.Dataframe(
            headers=["ID", "Category", "Key", "Content", "Importance (1-10)", "Pinned", "Archived"],
            datatype=["str", "str", "str", "str", "number", "number", "number"],
            col_count=(7, "fixed"),
            wrap=True
        )

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### ➕ Add New Memory Record")
            with gr.Row():
                mem_cat = gr.Dropdown(choices=["user", "project", "conversation"], value="user", label="Category")
                mem_key = gr.Textbox(placeholder="e.g. Favorite Language / Project Milestone", label="Memory Key")
                mem_imp = gr.Slider(minimum=1, maximum=10, value=7, step=1, label="Importance Score")
            mem_content = gr.Textbox(placeholder="Memory details to remember across sessions...", label="Memory Content", lines=2)
            mem_pinned = gr.Checkbox(label="Pin as Important Memory", value=False)
            add_mem_btn = gr.Button("💾 Store Memory Record", variant="primary")
            add_status = gr.Markdown()

        def fetch_memories(category: str, query: str):
            if query.strip():
                records = controller.memory_manager.search_semantic_memories(query, limit=10)
            else:
                records = controller.memory_manager.list_memories(category=category, include_archived=True)
            
            data = []
            for r in records:
                data.append([
                    r["id"][:8],
                    r["category"].upper(),
                    r["key"],
                    r["content"],
                    r["importance"],
                    "📌 Yes" if r.get("is_pinned") else "No",
                    "📦 Archived" if r.get("is_archived") else "Active"
                ])
            return data

        def on_add_memory(cat: str, key: str, content: str, imp: int, pinned: bool, cur_cat: str):
            if not key.strip() or not content.strip():
                return fetch_memories(cur_cat, ""), "❌ Error: Key and Content cannot be empty."
            
            controller.memory_manager.add_memory(
                category=cat,
                key=key,
                content=content,
                importance=imp,
                is_pinned=pinned
            )
            return fetch_memories(cur_cat, ""), f"✅ Saved memory record: **{key}**"

        # Event triggers
        search_btn.click(
            fn=fetch_memories,
            inputs=[category_filter, search_input],
            outputs=[memory_table]
        )
        category_filter.change(
            fn=fetch_memories,
            inputs=[category_filter, search_input],
            outputs=[memory_table]
        )
        add_mem_btn.click(
            fn=on_add_memory,
            inputs=[mem_cat, mem_key, mem_content, mem_imp, mem_pinned, category_filter],
            outputs=[memory_table, add_status]
        )
