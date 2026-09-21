"""
Expert Skills Dashboard UI Component for AetherMind Cortex (Phase 9)
Allows enabling, disabling, viewing, and launching modular domain skills.
"""

import gradio as gr
from app.controller import AppController

def render_skills_tab(controller: AppController):
    """Renders the modular Expert Skills Dashboard."""
    with gr.Tab("🛠️ Expert Skills"):
        gr.Markdown("### 🛠️ Modular Expert Skills & Domain Plugins Catalog")
        gr.Markdown("*Activate domain-specific AI expert skills that inject specialized reasoning capabilities over core memory & knowledge engines.*")

        gr.Markdown("#### 📦 Registered Domain Experts")
        skills_table = gr.Dataframe(
            headers=["ID", "Expert Name", "Category", "Description", "Status", "Priority"],
            datatype=["str", "str", "str", "str", "str", "number"],
            col_count=(6, "fixed"),
            wrap=True
        )

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### ⚙️ Manage Skill Enablement")
            with gr.Row():
                skill_select = gr.Dropdown(
                    choices=[s["skill_id"] for s in controller.skill_manager.list_skills()],
                    value=controller.skill_manager.list_skills()[0]["skill_id"] if controller.skill_manager.list_skills() else None,
                    label="Select Skill to Toggle"
                )
                enable_btn = gr.Button("🟢 Enable Skill", variant="primary")
                disable_btn = gr.Button("🔴 Disable Skill", variant="secondary")
            skill_status_md = gr.Markdown()

        def fetch_skills_table():
            skills = controller.skill_manager.list_skills()
            data = []
            for s in skills:
                data.append([
                    s["skill_id"],
                    s["name"],
                    s["category"].upper(),
                    s["description"],
                    "🟢 Enabled" if s["enabled"] == 1 else "🔴 Disabled",
                    s["priority"]
                ])
            return data

        def on_toggle_skill(skill_id: str, enable: bool):
            if not skill_id:
                return fetch_skills_table(), "❌ Please select a skill."
            controller.skill_manager.set_skill_status(skill_id, enable)
            status_text = "enabled" if enable else "disabled"
            return fetch_skills_table(), f"✅ Expert skill `{skill_id}` {status_text} successfully."

        # Initial data load
        skills_table.value = fetch_skills_table()

        # Event triggers
        enable_btn.click(
            fn=lambda sid: on_toggle_skill(sid, True),
            inputs=[skill_select],
            outputs=[skills_table, skill_status_md]
        )
        disable_btn.click(
            fn=lambda sid: on_toggle_skill(sid, False),
            inputs=[skill_select],
            outputs=[skills_table, skill_status_md]
        )
