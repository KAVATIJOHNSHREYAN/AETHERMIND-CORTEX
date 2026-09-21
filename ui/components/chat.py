"""
Chat Component for AetherMind Cortex UI (Phase 4 Expanded)
Includes long-term memory context injection and RAG document context with source citations.
"""

import gradio as gr
from typing import List, Tuple
from app.controller import AppController

def render_chat_tab(controller: AppController, model_dropdown: gr.Dropdown):
    """Renders the real-time streaming chat tab with RAG & memory context awareness."""
    with gr.Tab("💬 Reasoning Chat"):
        gr.Markdown("### 🤖 Local Ollama AI Reasoning Workspace")
        
        chatbot = gr.Chatbot(
            value=[],
            height=500,
            show_copy_button=True,
            render_markdown=True,
            avatar_images=None
        )

        with gr.Row():
            msg_input = gr.Textbox(
                placeholder="Type your query or prompt here for the local model...",
                show_label=False,
                scale=5,
                lines=2
            )
            send_btn = gr.Button("🚀 Send Prompt", variant="primary", scale=1)

        # Action bar: Stop, Regenerate, Clear, Export
        with gr.Row():
            stop_btn = gr.Button("🛑 Stop Generation", variant="stop", size="sm")
            regen_btn = gr.Button("🔄 Regenerate Response", variant="secondary", size="sm")
            clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary", size="sm")
            export_md_btn = gr.Button("📥 Export Markdown", variant="secondary", size="sm")
            export_txt_btn = gr.Button("📄 Export TXT", variant="secondary", size="sm")

        export_file = gr.File(label="Download Chat Export", visible=False)

        # RAG Source Citations & Performance Accordion
        with gr.Accordion("📚 RAG Source Citations & Memory Context", open=True):
            rag_citations_md = gr.Markdown("*No RAG citations or document context retrieved.*")
            metrics_md = gr.Markdown("⚡ **Latency:** 0.0s | 🚀 **Speed:** 0.0 tokens/s | 🔢 **Token Count:** 0 tokens")

        def load_active_history():
            messages = controller.get_active_messages()
            history = []
            user_temp = None
            for m in messages:
                if m["role"] == "user":
                    user_temp = m["content"]
                elif m["role"] == "assistant":
                    if user_temp is not None:
                        history.append((user_temp, m["content"]))
                        user_temp = None
                    else:
                        history.append((None, m["content"]))
            if user_temp is not None:
                history.append((user_temp, None))
            return history

        # Event stream generator for user interaction
        def user_submit(user_message: str, history: List[Tuple[str, str]], model_name: str):
            if not user_message.strip():
                yield history, "", "*No prompt entered.*", "⚡ **Latency:** 0.0s | 🚀 **Speed:** 0.0 tokens/s | 🔢 **Token Count:** 0 tokens"
                return

            controller.add_user_message(user_message)
            history.append((user_message, "... 🤔 Thinking, Recalling Memories & Searching Knowledge Base ..."))

            # 1. Memory Context
            memory_context = controller.memory_manager.get_context_prompt_injection(user_message)
            
            # 2. RAG Knowledge Context & Citations
            rag_context, citations = controller.knowledge_engine.get_rag_context_injection(user_message)

            cit_display = ""
            if citations:
                cit_display += "#### 📄 Retrived RAG Document Citations:\n"
                for idx, c in enumerate(citations, 1):
                    cit_display += f"**[{idx}] {c['source']}** (Chunk {c['chunk_index']}): `{c['content_snippet']}`\n\n"
            else:
                cit_display = "*No document citations retrieved for this prompt.*"

            combined_system_prompt = "You are AetherMind Cortex, a privacy-first AI engine."
            if memory_context:
                combined_system_prompt += "\n" + memory_context
            if rag_context:
                combined_system_prompt += "\n" + rag_context

            yield history, "", cit_display, "⚡ **Generating streaming response...**"

            formatted_messages = []
            for u, a in history[:-1]:
                if u:
                    formatted_messages.append({"role": "user", "content": u})
                if a:
                    formatted_messages.append({"role": "assistant", "content": a})
            formatted_messages.append({"role": "user", "content": user_message})

            assistant_accumulated = ""
            final_metrics = ""

            for chunk in controller.llm_engine.stream_chat(
                model=model_name,
                messages=formatted_messages,
                system_prompt=combined_system_prompt
            ):
                assistant_accumulated = chunk["accumulated"]
                history[-1] = (user_message, assistant_accumulated)
                
                m = chunk["metrics"]
                final_metrics = f"⚡ **Latency:** {m['elapsed_sec']}s | 🚀 **Speed:** {m['tokens_per_sec']} tokens/s | 🔢 **Token Count:** {m['token_count']} tokens"
                
                yield history, "", cit_display, final_metrics

            controller.add_assistant_message(assistant_accumulated)
            yield history, "", cit_display, final_metrics

        def regenerate_submit(history: List[Tuple[str, str]], model_name: str):
            if not history:
                yield history, "*No prompt.*", "⚡ No messages to regenerate."
                return

            last_user_msg = history[-1][0]
            if not last_user_msg:
                yield history, "*No user message.*", "⚡ Cannot regenerate without user message."
                return

            history[-1] = (last_user_msg, "... 🔄 Regenerating ...")
            memory_context = controller.memory_manager.get_context_prompt_injection(last_user_msg)
            rag_context, citations = controller.knowledge_engine.get_rag_context_injection(last_user_msg)

            cit_display = ""
            if citations:
                cit_display += "#### 📄 Retrived RAG Document Citations:\n"
                for idx, c in enumerate(citations, 1):
                    cit_display += f"**[{idx}] {c['source']}** (Chunk {c['chunk_index']}): `{c['content_snippet']}`\n\n"
            else:
                cit_display = "*No document citations retrieved for this prompt.*"

            combined_system_prompt = "You are AetherMind Cortex, a privacy-first AI engine."
            if memory_context:
                combined_system_prompt += "\n" + memory_context
            if rag_context:
                combined_system_prompt += "\n" + rag_context

            yield history, cit_display, "⚡ **Regenerating streaming response...**"

            formatted_messages = []
            for u, a in history[:-1]:
                if u:
                    formatted_messages.append({"role": "user", "content": u})
                if a:
                    formatted_messages.append({"role": "assistant", "content": a})
            formatted_messages.append({"role": "user", "content": last_user_msg})

            assistant_accumulated = ""
            final_metrics = ""

            for chunk in controller.llm_engine.stream_chat(
                model=model_name,
                messages=formatted_messages,
                system_prompt=combined_system_prompt
            ):
                assistant_accumulated = chunk["accumulated"]
                history[-1] = (last_user_msg, assistant_accumulated)
                
                m = chunk["metrics"]
                final_metrics = f"⚡ **Latency:** {m['elapsed_sec']}s | 🚀 **Speed:** {m['tokens_per_sec']} tokens/s | 🔢 **Token Count:** {m['token_count']} tokens"
                
                yield history, cit_display, final_metrics

            controller.add_assistant_message(assistant_accumulated)
            yield history, cit_display, final_metrics

        # Event triggers
        send_event = send_btn.click(
            fn=user_submit,
            inputs=[msg_input, chatbot, model_dropdown],
            outputs=[chatbot, msg_input, rag_citations_md, metrics_md]
        )
        submit_event = msg_input.submit(
            fn=user_submit,
            inputs=[msg_input, chatbot, model_dropdown],
            outputs=[chatbot, msg_input, rag_citations_md, metrics_md]
        )

        stop_btn.click(fn=None, cancels=[send_event, submit_event])

        regen_btn.click(
            fn=regenerate_submit,
            inputs=[chatbot, model_dropdown],
            outputs=[chatbot, rag_citations_md, metrics_md]
        )

        def clear_chat():
            controller.clear_active_session()
            return [], "*Cleared citations context.*", "⚡ Chat cleared."

        clear_btn.click(fn=clear_chat, outputs=[chatbot, rag_citations_md, metrics_md])

        # Export Handlers
        def export_chat(fmt: str):
            content = controller.export_active_session(fmt)
            filename = f"chat_export.{'md' if fmt == 'markdown' else 'txt'}"
            filepath = f"logs/{filename}"
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return gr.update(value=filepath, visible=True)

        export_md_btn.click(fn=lambda: export_chat("markdown"), outputs=[export_file])
        export_txt_btn.click(fn=lambda: export_chat("txt"), outputs=[export_file])

        return chatbot, load_active_history
