"""
Chat Component for AetherMind Cortex UI (Phase 3 Expanded)
Includes long-term memory context injection into Ollama prompts.
"""

import gradio as gr
from typing import List, Tuple
from app.controller import AppController

def render_chat_tab(controller: AppController, model_dropdown: gr.Dropdown):
    """Renders the real-time streaming chat tab with memory context awareness."""
    with gr.Tab("💬 Reasoning Chat"):
        gr.Markdown("### 🤖 Local Ollama AI Reasoning Workspace")
        
        chatbot = gr.Chatbot(
            value=[],
            height=520,
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

        # Performance & Memory Context Accordion
        with gr.Accordion("🧠 Active Long-Term Memory Context & Metrics", open=True):
            memory_context_md = gr.Markdown("*No memory context retrieved yet.*")
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

            # Append user message to controller DB
            controller.add_user_message(user_message)
            history.append((user_message, "... 🤔 Thinking & Recalling Memories ..."))

            # Retrieve Memory Context
            memory_context = controller.memory_manager.get_context_prompt_injection(user_message)
            mem_display = memory_context if memory_context else "*No relevant memories retrieved.*"

            yield history, "", mem_display, "⚡ **Generating streaming response...**"

            # Prepare message payload for Ollama
            formatted_messages = []
            for u, a in history[:-1]:
                if u:
                    formatted_messages.append({"role": "user", "content": u})
                if a:
                    formatted_messages.append({"role": "assistant", "content": a})
            formatted_messages.append({"role": "user", "content": user_message})

            # Stream from Ollama Engine with injected system prompt memory context
            assistant_accumulated = ""
            final_metrics = ""

            for chunk in controller.llm_engine.stream_chat(
                model=model_name,
                messages=formatted_messages,
                system_prompt=f"You are AetherMind Cortex, a human-centered AI engine. {memory_context}" if memory_context else None
            ):
                assistant_accumulated = chunk["accumulated"]
                history[-1] = (user_message, assistant_accumulated)
                
                m = chunk["metrics"]
                final_metrics = f"⚡ **Latency:** {m['elapsed_sec']}s | 🚀 **Speed:** {m['tokens_per_sec']} tokens/s | 🔢 **Token Count:** {m['token_count']} tokens"
                
                yield history, "", mem_display, final_metrics

            # Save completed assistant response to DB
            controller.add_assistant_message(assistant_accumulated)
            yield history, "", mem_display, final_metrics

        # Event stream generator for regenerate action
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
            mem_display = memory_context if memory_context else "*No relevant memories retrieved.*"

            yield history, mem_display, "⚡ **Regenerating streaming response...**"

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
                system_prompt=f"You are AetherMind Cortex, a human-centered AI engine. {memory_context}" if memory_context else None
            ):
                assistant_accumulated = chunk["accumulated"]
                history[-1] = (last_user_msg, assistant_accumulated)
                
                m = chunk["metrics"]
                final_metrics = f"⚡ **Latency:** {m['elapsed_sec']}s | 🚀 **Speed:** {m['tokens_per_sec']} tokens/s | 🔢 **Token Count:** {m['token_count']} tokens"
                
                yield history, mem_display, final_metrics

            controller.add_assistant_message(assistant_accumulated)
            yield history, mem_display, final_metrics

        # Event triggers
        send_event = send_btn.click(
            fn=user_submit,
            inputs=[msg_input, chatbot, model_dropdown],
            outputs=[chatbot, msg_input, memory_context_md, metrics_md]
        )
        submit_event = msg_input.submit(
            fn=user_submit,
            inputs=[msg_input, chatbot, model_dropdown],
            outputs=[chatbot, msg_input, memory_context_md, metrics_md]
        )

        stop_btn.click(fn=None, cancels=[send_event, submit_event])

        regen_btn.click(
            fn=regenerate_submit,
            inputs=[chatbot, model_dropdown],
            outputs=[chatbot, memory_context_md, metrics_md]
        )

        def clear_chat():
            controller.clear_active_session()
            return [], "*Cleared memory context.*", "⚡ Chat cleared."

        clear_btn.click(fn=clear_chat, outputs=[chatbot, memory_context_md, metrics_md])

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
