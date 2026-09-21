"""
Workflow Intelligence Dashboard UI Component for AetherMind Cortex (Phase 7)
Allows task intelligence tracking, productivity analytics monitoring, and smart automation suggestion triggers.
"""

import gradio as gr
from app.controller import AppController

def render_workflow_tab(controller: AppController):
    """Renders the privacy-first Workflow Intelligence Dashboard."""
    with gr.Tab("⚡ Workflow Intelligence"):
        gr.Markdown("### ⚡ Workflow Intelligence & Productivity Partner Dashboard")
        gr.Markdown("*Track active tasks, monitor productivity trends, and discover smart automation opportunities completely offline.*")

        # Productivity Summary Cards
        with gr.Row():
            metrics_summary_md = gr.Markdown("📊 **Productivity Metrics:** Loading analytics...")
            refresh_summary_btn = gr.Button("🔄 Refresh Summary", variant="secondary", size="sm")

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### 📋 Task Intelligence & Dependency Board")
            with gr.Row():
                task_title = gr.Textbox(placeholder="e.g. Implement Async Document Pipeline", label="Task Title", scale=3)
                task_project = gr.Textbox(value="AetherMind Cortex", label="Project Name", scale=2)
                task_prio = gr.Dropdown(choices=["high", "medium", "low"], value="high", label="Priority", scale=1)
                task_hours = gr.Number(value=2.0, label="Est. Hours", scale=1)
                add_task_btn = gr.Button("➕ Add Task", variant="primary", scale=1)

            tasks_table = gr.Dataframe(
                headers=["ID", "Task Title", "Project", "Priority", "Est. Hours", "Status", "Created Date"],
                datatype=["str", "str", "str", "str", "number", "str", "str"],
                col_count=(7, "fixed"),
                wrap=True
            )

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### 🤖 Smart Workflow & Automation Suggestions")
            insights_table = gr.Dataframe(
                headers=["ID", "Category", "Smart Workflow Suggestion", "Impact Level", "Discovered Date"],
                datatype=["str", "str", "str", "str", "str"],
                col_count=(5, "fixed"),
                wrap=True
            )

        def fetch_metrics():
            summary = controller.workflow_engine.get_productivity_summary()
            return f"📋 **Total Tasks:** {summary['total_tasks']} | ✅ **Completed:** {summary['completed_tasks']} | ⏳ **In Progress:** {summary['in_progress_tasks']} | 📈 **Completion Rate:** {summary['completion_rate_pct']}% | 🤖 **Automation Status:** {summary['automation_score']}"

        def fetch_tasks():
            tasks = controller.workflow_engine.list_tasks(status="all")
            data = []
            for t in tasks:
                data.append([
                    t["id"][:8],
                    t["title"],
                    t["project_name"],
                    t["priority"].upper(),
                    t["estimated_hours"],
                    t["status"].upper(),
                    t["created_at"]
                ])
            return data

        def fetch_insights():
            insights = controller.workflow_engine.list_insights()
            data = []
            for i in insights:
                data.append([
                    i["id"][:8],
                    i["category"].upper(),
                    i["suggestion"],
                    i["impact"].upper(),
                    i["created_at"]
                ])
            return data

        def on_add_task(title, project, prio, hours):
            if not title.strip():
                return fetch_tasks(), fetch_metrics(), "❌ Error: Task title cannot be empty."
            controller.workflow_engine.add_task(title.strip(), project.strip(), prio, hours)
            return fetch_tasks(), fetch_metrics(), f"✅ Added task: **{title}**"

        # Initial values
        metrics_summary_md.value = fetch_metrics()
        tasks_table.value = fetch_tasks()
        insights_table.value = fetch_insights()

        # Event triggers
        refresh_summary_btn.click(
            fn=lambda: (fetch_metrics(), fetch_tasks(), fetch_insights()),
            outputs=[metrics_summary_md, tasks_table, insights_table]
        )
        add_task_btn.click(
            fn=on_add_task,
            inputs=[task_title, task_project, task_prio, task_hours],
            outputs=[tasks_table, metrics_summary_md, metrics_summary_md]
        )
