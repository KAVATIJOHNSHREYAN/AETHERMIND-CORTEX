"""
Human Profile Dashboard UI Component for AetherMind Cortex (Phase 5)
Allows viewing, editing, exporting, importing, and managing user identity, goals, and privacy settings.
"""

import gradio as gr
from app.controller import AppController

def render_profile_tab(controller: AppController):
    """Renders the privacy-first Human Profile Engine Dashboard."""
    with gr.Tab("👤 Human Profile"):
        gr.Markdown("### 👤 Human Profile & Adaptive Personalization Dashboard")
        gr.Markdown("*Configure your user persona, goals, coding/explanation preferences, and privacy controls stored 100% locally.*")

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### 🆔 User Identity & Preferences")
            with gr.Row():
                name_in = gr.Textbox(value=controller.profile_manager.get_profile_attribute("user_name", "User"), label="Full Name / Handle")
                prof_in = gr.Textbox(value=controller.profile_manager.get_profile_attribute("profession", "Developer"), label="Profession / Role")
                exp_in = gr.Dropdown(choices=["Beginner", "Intermediate", "Expert"], value=controller.profile_manager.get_profile_attribute("experience_level", "Intermediate"), label="Experience Level")
            
            with gr.Row():
                code_style_in = gr.Dropdown(choices=["Clean Modular Architecture", "Functional Programming", "Concise Scripting"], value=controller.profile_manager.get_profile_attribute("coding_style", "Clean Modular Architecture"), label="Preferred Coding Style")
                depth_in = gr.Dropdown(choices=["Brief", "Balanced", "Deep-Dive"], value=controller.profile_manager.get_profile_attribute("explanation_depth", "Balanced"), label="Explanation Depth")
                write_style_in = gr.Dropdown(choices=["Technical & Concise", "Conversational & Detailed", "Academic"], value=controller.profile_manager.get_profile_attribute("writing_style", "Technical & Concise"), label="Writing Style")

            save_profile_btn = gr.Button("💾 Save Identity & Preferences", variant="primary")
            profile_status = gr.Markdown()

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### 🎯 Active User Goals & Milestones Engine")
            with gr.Row():
                goal_title = gr.Textbox(placeholder="e.g. Master Rust, Build AI Cortex Engine", label="New Goal Title", scale=3)
                goal_cat = gr.Dropdown(choices=["current", "long_term", "learning"], value="current", label="Category", scale=1)
                goal_prio = gr.Dropdown(choices=["high", "medium", "low"], value="high", label="Priority", scale=1)
                add_goal_btn = gr.Button("➕ Add Goal", variant="secondary", scale=1)
            
            goals_table = gr.Dataframe(
                headers=["ID", "Goal Title", "Category", "Priority", "Status", "Created Date"],
                datatype=["str", "str", "str", "str", "str", "str"],
                col_count=(6, "fixed"),
                wrap=True
            )

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### 🔒 Privacy & Profile Management Controls")
            with gr.Row():
                pers_toggle = gr.Checkbox(label="Enable Adaptive Response Personalization", value=(controller.profile_manager.get_profile_attribute("personalization_enabled", "true") == "true"))
                export_json_btn = gr.Button("📥 Export Profile JSON", variant="secondary")
                reset_prof_btn = gr.Button("🚨 Reset Profile to Defaults", variant="stop")
            
            export_file = gr.File(label="Download Profile JSON", visible=False)
            privacy_status = gr.Markdown()

        def fetch_goals():
            goals = controller.profile_manager.list_goals()
            data = []
            for g in goals:
                data.append([
                    g["id"][:8],
                    g["title"],
                    g["category"].upper(),
                    g["priority"].upper(),
                    g["status"].upper(),
                    g["created_at"]
                ])
            return data

        def on_save_profile(name, prof, exp, code, depth, write, pers):
            data = {
                "user_name": name,
                "profession": prof,
                "experience_level": exp,
                "coding_style": code,
                "explanation_depth": depth,
                "writing_style": write,
                "personalization_enabled": "true" if pers else "false"
            }
            controller.profile_manager.update_profile_bulk(data)
            return f"✅ Profile updated for **{name}** ({prof})."

        def on_add_goal(title, cat, prio):
            if not title.strip():
                return fetch_goals(), "❌ Goal title cannot be empty."
            controller.profile_manager.add_goal(title.strip(), cat, prio)
            return fetch_goals(), f"✅ Goal added: **{title}**"

        def on_export_profile():
            content = controller.profile_manager.export_profile_json()
            filepath = "logs/profile_export.json"
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return gr.update(value=filepath, visible=True)

        def on_reset_profile():
            controller.profile_manager.reset_profile()
            return fetch_goals(), "✅ Profile reset to defaults."

        # Initial data
        goals_table.value = fetch_goals()

        # Event triggers
        save_profile_btn.click(
            fn=on_save_profile,
            inputs=[name_in, prof_in, exp_in, code_style_in, depth_in, write_style_in, pers_toggle],
            outputs=[profile_status]
        )
        add_goal_btn.click(
            fn=on_add_goal,
            inputs=[goal_title, goal_cat, goal_prio],
            outputs=[goals_table, profile_status]
        )
        export_json_btn.click(
            fn=on_export_profile,
            outputs=[export_file]
        )
        reset_prof_btn.click(
            fn=on_reset_profile,
            outputs=[goals_table, privacy_status]
        )
