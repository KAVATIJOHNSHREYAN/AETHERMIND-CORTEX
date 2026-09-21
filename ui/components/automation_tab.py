"""
Automation Dashboard UI Component for AetherMind Cortex (Phase 10)
Provides project template generation, Python script execution, reminder scheduling, and automation logs tracking.
"""

import gradio as gr
from app.controller import AppController

def render_automation_tab(controller: AppController):
    """Renders the safe local Automation Engine Dashboard."""
    with gr.Tab("🤖 Local Automation"):
        gr.Markdown("### 🤖 Safe Local Automation & Script Execution Dashboard")
        gr.Markdown("*Execute safe local Python automation scripts, initialize clean architecture project templates, and manage scheduled reminders completely offline.*")

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### 📁 Initialize Project Template")
            with gr.Row():
                proj_name_in = gr.Textbox(placeholder="e.g. MyNewProject", label="Project Name", scale=2)
                target_dir_in = gr.Textbox(value="C:\\Users\\johns\\Documents", label="Target Parent Directory", scale=3)
                create_template_btn = gr.Button("⚡ Create Project Structure", variant="primary", scale=1)
            template_status_md = gr.Markdown()

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### 🐍 Python Script Executor & Runner")
            script_code_in = gr.Code(
                value='# Python Automation Script Example\nimport sys\nprint(f"Executing Python Automation via Cortex Engine: {sys.version}")\n',
                language="python",
                label="Python Script Code"
            )
            exec_script_btn = gr.Button("▶️ Run Python Script Safely", variant="primary")
            script_output_out = gr.Code(label="Execution Output Logs", language="shell")

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### ⏰ Local Reminders & Scheduled Triggers")
            with gr.Row():
                reminder_msg_in = gr.Textbox(placeholder="e.g. Review RAG index stats at 5 PM", label="Reminder Text", scale=4)
                add_reminder_btn = gr.Button("⏰ Set Reminder", variant="secondary", scale=1)
            reminders_table = gr.Dataframe(
                headers=["ID", "Reminder Message", "Scheduled Time", "Status", "Created Date"],
                datatype=["str", "str", "str", "str", "str"],
                col_count=(5, "fixed"),
                wrap=True
            )

        gr.Markdown("#### 📜 Automation Jobs History & Execution Logs")
        jobs_table = gr.Dataframe(
            headers=["ID", "Job Name", "Type", "Status", "Logs / Output Snippet", "Execution Date"],
            datatype=["str", "str", "str", "str", "str", "str"],
            col_count=(6, "fixed"),
            wrap=True
        )

        def fetch_reminders():
            rems = controller.automation_engine.list_reminders()
            data = []
            for r in rems:
                data.append([
                    r["id"][:8],
                    r["message"],
                    r["scheduled_time"],
                    r["status"].upper(),
                    r["created_at"]
                ])
            return data

        def fetch_jobs():
            jobs = controller.automation_engine.list_automation_jobs()
            data = []
            for j in jobs:
                data.append([
                    j["id"][:8],
                    j["name"],
                    j["type"].upper(),
                    j["status"].upper(),
                    (j["logs"][:120] + "...") if j["logs"] else "None",
                    j["created_at"]
                ])
            return data

        def on_create_template(p_name: str, t_dir: str):
            if not p_name.strip() or not t_dir.strip():
                return fetch_jobs(), "❌ Error: Project Name and Target Directory cannot be empty."
            res = controller.automation_engine.create_project_template(p_name.strip(), t_dir.strip())
            msg = f"✅ {res['message']}" if res["success"] else f"❌ {res['message']}"
            return fetch_jobs(), msg

        def on_exec_script(code: str):
            if not code.strip():
                return fetch_jobs(), "❌ Error: Script code is empty."
            res = controller.automation_engine.execute_python_script(code)
            return fetch_jobs(), res["output"]

        def on_add_reminder(msg: str):
            if not msg.strip():
                return fetch_reminders(), fetch_jobs(), "❌ Error: Reminder text cannot be empty."
            controller.automation_engine.add_reminder(msg.strip())
            return fetch_reminders(), fetch_jobs(), f"✅ Reminder set: **{msg}**"

        # Initial data load
        reminders_table.value = fetch_reminders()
        jobs_table.value = fetch_jobs()

        # Event triggers
        create_template_btn.click(
            fn=on_create_template,
            inputs=[proj_name_in, target_dir_in],
            outputs=[jobs_table, template_status_md]
        )
        exec_script_btn.click(
            fn=on_exec_script,
            inputs=[script_code_in],
            outputs=[jobs_table, script_output_out]
        )
        add_reminder_btn.click(
            fn=on_add_reminder,
            inputs=[reminder_msg_in],
            outputs=[reminders_table, jobs_table, template_status_md]
        )
