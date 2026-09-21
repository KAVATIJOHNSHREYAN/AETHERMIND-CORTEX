"""
Chat Component Placeholder for AetherMind Cortex UI
"""

import gradio as gr

def render_chat_tab():
    """Renders the Chat reasoning engine UI tab placeholder."""
    with gr.Tab("💬 Reasoning Chat"):
        gr.Markdown("### 🤖 Human-Centered Reasoning Workspace")
        
        chatbot = gr.Chatbot(
            value=[
                (None, "Welcome to **AetherMind Cortex**! Phase 1 foundation shell is active. AI reasoning models will be connected in Phase 2.")
            ],
            height=500,
            show_copy_button=True
        )
        
        with gr.Row():
            msg_input = gr.Textbox(
                placeholder="Type your reasoning query or prompt here...",
                show_label=False,
                scale=5
            )
            send_btn = gr.Button("Send Prompt", variant="primary", scale=1)

        with gr.Accordion("🔍 Reasoning Log & Chain-of-Thought Pipeline (Placeholder)", open=False):
            gr.Markdown("""
            ```json
            {
              "phase": "Phase 1 - Shell Active",
              "reasoning_steps": [],
              "status": "Ready for AI Model Connection"
            }
            ```
            """)

        def user_send(user_message, history):
            if not user_message.strip():
                return "", history
            history = history + [(user_message, "AetherMind Phase 1: Interactive shell active. Reasoning engine pipeline ready for model attachment.")]
            return "", history

        send_btn.click(fn=user_send, inputs=[msg_input, chatbot], outputs=[msg_input, chatbot])
        msg_input.submit(fn=user_send, inputs=[msg_input, chatbot], outputs=[msg_input, chatbot])
