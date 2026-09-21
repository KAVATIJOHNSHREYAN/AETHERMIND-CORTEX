"""
Chat Component for AetherMind Cortex UI (Phase 9 Expanded)
Includes Expert Skills Prompt Injections, Cognitive Reasoning Pipeline, Developer Inspector, Memory, RAG, and User Profile Context.
"""

import gradio as gr
from typing import List, Tuple
from app.controller import AppController

def render_chat_tab(controller: AppController, model_dropdown: gr.Dropdown):
    """Renders the real-time cognitive reasoning chat workspace with active Expert Skills integration."""
    with gr.Tab("💬 Reasoning Workspace"):
        gr.Markdown("### 🤖 Cognitive AI Reasoning Workspace & Modular Expert Platform")
        
        chatbot = gr.Chatbot(
            value=[],
            height=460,
            show_copy_button=True,
            render_markdown=True,
            avatar_images=None
        )

        with gr.Row():
            msg_input = gr.Textbox(
                placeholder="Type your technical prompt or complex query here...",
                show_label=False,
                scale=5,
                lines=2
            )
            send_btn = gr.Button("🚀 Execute Reasoning", variant="primary", scale=1)

        # Action bar: Stop, Regenerate, Clear, Export, Dev Mode Toggle
        with gr.Row():
            stop_btn = gr.Button("🛑 Stop Generation", variant="stop", size="sm")
            regen_btn = gr.Button("🔄 Regenerate Response", variant="secondary", size="sm")
            clear_btn = gr.Button("🗑️ Clear Workspace", variant="secondary", size="sm")
            export_md_btn = gr.Button("📥 Export MD", variant="secondary", size="sm")
            export_txt_btn = gr.Button("📄 Export TXT", variant="secondary", size="sm")

        export_file = gr.File(label="Download Chat Export", visible=False)

        # Developer Mode Reasoning Inspector Accordion
        with gr.Accordion("⚙️ Developer Mode: Cognitive Reasoning Inspection Pipeline", open=True):
            dev_mode_toggle = gr.Checkbox(label="Enable Developer Mode Reasoning Inspection Logs", value=True)
            active_skills_md = gr.Markdown("*Active Expert Skills Context Active*")
            reasoning_inspection_md = gr.Markdown("*Reasoning pipeline inspection logs will appear here during execution.*")
            rag_citations_md = gr.Markdown("*No RAG citations retrieved.*")
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
        def user_submit(user_message: str, history: List[Tuple[str, str]], model_name: str, dev_mode: bool):
            if not user_message.strip():
                yield history, "", "", "*No prompt entered.*", "*No citations.*", "⚡ **Latency:** 0.0s | 🚀 **Speed:** 0.0 tokens/s | 🔢 **Token Count:** 0 tokens"
                return

            controller.add_user_message(user_message)
            history.append((user_message, "... 🧠 Executing Cognitive Reasoning & Expert Skills ..."))

            # 1. Expert Skills Injection
            skills_context = controller.skill_manager.get_active_skills_prompt_injection()
            active_skills_list = [s["name"] for s in controller.skill_manager.list_skills() if s["enabled"] == 1]
            skills_display = f"🛠️ **Active Expert Skills:** {', '.join(active_skills_list)}" if active_skills_list else "*No Expert Skills Active*"

            # 2. Reasoning System Prompt Setup
            reasoning_system_prompt = controller.reasoning_engine.generate_reasoning_pipeline_prompt(
                prompt=user_message,
                user_context=controller.profile_manager.get_personalized_prompt_context(),
                memory_context=controller.memory_manager.get_context_prompt_injection(user_message),
                rag_context=controller.knowledge_engine.get_rag_context_injection(user_message)[0]
            )

            if skills_context:
                reasoning_system_prompt += "\n" + skills_context

            # RAG Citations Display
            _, citations = controller.knowledge_engine.get_rag_context_injection(user_message)
            cit_display = ""
            if citations:
                cit_display += "#### 📄 Retrived RAG Document Citations:\n"
                for idx, c in enumerate(citations, 1):
                    cit_display += f"**[{idx}] {c['source']}** (Chunk {c['chunk_index']}, Confidence: {c['confidence']}%): `{c['content_snippet']}`\n\n"
            else:
                cit_display = "*No document citations retrieved.*"

            inspection_display = "*Analyzing intent & pipeline steps...*"
            yield history, "", skills_display, inspection_display, cit_display, "⚡ **Executing cognitive reasoning pipeline...**"

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
                system_prompt=reasoning_system_prompt
            ):
                assistant_accumulated = chunk["accumulated"]
                history[-1] = (user_message, assistant_accumulated)
                
                m = chunk["metrics"]
                final_metrics = f"⚡ **Latency:** {m['elapsed_sec']}s | 🚀 **Speed:** {m['tokens_per_sec']} tokens/s | 🔢 **Token Count:** {m['token_count']} tokens"

                if dev_mode:
                    dev_log = controller.reasoning_engine.build_developer_inspection_log(user_message, m['elapsed_sec'], m['token_count'])
                    inspection_display = f"#### ⚙️ Developer Inspection Pipeline Log\n- **Detected Intent:** `{dev_log['intent']}`\n- **Confidence Rating:** `{dev_log['confidence_score']}`\n"
                    for step in dev_log["reasoning_steps"]:
                        inspection_display += f"  - **Step {step['step']}: {step['title']}**: {step['detail']}\n"
                else:
                    inspection_display = "*Developer Mode Disabled.*"

                yield history, "", skills_display, inspection_display, cit_display, final_metrics

            controller.add_assistant_message(assistant_accumulated)
            yield history, "", skills_display, inspection_display, cit_display, final_metrics

        def regenerate_submit(history: List[Tuple[str, str]], model_name: str, dev_mode: bool):
            if not history:
                yield history, "", "*No prompt.*", "*No citations.*", "⚡ No messages to regenerate."
                return

            last_user_msg = history[-1][0]
            if not last_user_msg:
                yield history, "", "*No user message.*", "*No citations.*", "⚡ Cannot regenerate without user message."
                return

            history[-1] = (last_user_msg, "... 🔄 Regenerating Pipeline ...")

            skills_context = controller.skill_manager.get_active_skills_prompt_injection()
            active_skills_list = [s["name"] for s in controller.skill_manager.list_skills() if s["enabled"] == 1]
            skills_display = f"🛠️ **Active Expert Skills:** {', '.join(active_skills_list)}" if active_skills_list else "*No Expert Skills Active*"

            reasoning_system_prompt = controller.reasoning_engine.generate_reasoning_pipeline_prompt(
                prompt=last_user_msg,
                user_context=controller.profile_manager.get_personalized_prompt_context(),
                memory_context=controller.memory_manager.get_context_prompt_injection(last_user_msg),
                rag_context=controller.knowledge_engine.get_rag_context_injection(last_user_msg)[0]
            )

            if skills_context:
                reasoning_system_prompt += "\n" + skills_context

            _, citations = controller.knowledge_engine.get_rag_context_injection(last_user_msg)
            cit_display = f"#### 📄 Retrived RAG Document Citations:\n" + "\n".join([f"**[{idx+1}] {c['source']}**: `{c['content_snippet']}`" for idx, c in enumerate(citations)]) if citations else "*No document citations retrieved.*"
            inspection_display = "*Regenerating reasoning steps...*"

            yield history, skills_display, inspection_display, cit_display, "⚡ **Regenerating cognitive reasoning pipeline...**"

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
                system_prompt=reasoning_system_prompt
            ):
                assistant_accumulated = chunk["accumulated"]
                history[-1] = (last_user_msg, assistant_accumulated)
                
                m = chunk["metrics"]
                final_metrics = f"⚡ **Latency:** {m['elapsed_sec']}s | 🚀 **Speed:** {m['tokens_per_sec']} tokens/s | 🔢 **Token Count:** {m['token_count']} tokens"

                if dev_mode:
                    dev_log = controller.reasoning_engine.build_developer_inspection_log(last_user_msg, m['elapsed_sec'], m['token_count'])
                    inspection_display = f"#### ⚙️ Developer Inspection Pipeline Log\n- **Detected Intent:** `{dev_log['intent']}`\n- **Confidence Rating:** `{dev_log['confidence_score']}`\n"
                    for step in dev_log["reasoning_steps"]:
                        inspection_display += f"  - **Step {step['step']}: {step['title']}**: {step['detail']}\n"
                else:
                    inspection_display = "*Developer Mode Disabled.*"

                yield history, skills_display, inspection_display, cit_display, final_metrics

            controller.add_assistant_message(assistant_accumulated)
            yield history, skills_display, inspection_display, cit_display, final_metrics

        # Event triggers
        send_event = send_btn.click(
            fn=user_submit,
            inputs=[msg_input, chatbot, model_dropdown, dev_mode_toggle],
            outputs=[chatbot, msg_input, active_skills_md, reasoning_inspection_md, rag_citations_md, metrics_md]
        )
        submit_event = msg_input.submit(
            fn=user_submit,
            inputs=[msg_input, chatbot, model_dropdown, dev_mode_toggle],
            outputs=[chatbot, msg_input, active_skills_md, reasoning_inspection_md, rag_citations_md, metrics_md]
        )

        stop_btn.click(fn=None, cancels=[send_event, submit_event])

        regen_btn.click(
            fn=regenerate_submit,
            inputs=[chatbot, model_dropdown, dev_mode_toggle],
            outputs=[chatbot, active_skills_md, reasoning_inspection_md, rag_citations_md, metrics_md]
        )

        def clear_chat():
            controller.clear_active_session()
            return [], "*Cleared skills context.*", "*Cleared inspection log.*", "*Cleared citations.*", "⚡ Chat workspace cleared."

        clear_btn.click(fn=clear_chat, outputs=[chatbot, active_skills_md, reasoning_inspection_md, rag_citations_md, metrics_md])

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
