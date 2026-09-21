"""
Plugins & Workspace Dashboard UI Component for AetherMind Cortex (Phase 11)
Allows plugin management, multi-workspace switching, and full system backup archives.
"""

import gradio as gr
from app.controller import AppController

def render_plugins_tab(controller: AppController):
    """Renders the Plugins, Workspace, and System Backup Dashboard."""
    with gr.Tab("🔌 Plugins & Workspaces"):
        gr.Markdown("### 🔌 Plugin Ecosystem, Workspace & Backup Management")
        gr.Markdown("*Manage desktop workspaces, installed ecosystem plugins, permissions, and create full system zip backups completely offline.*")

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### 🌐 Workspace Management")
            with gr.Row():
                ws_select = gr.Dropdown(
                    choices=[w["name"] for w in controller.workspace_manager.list_workspaces()],
                    value=[w["name"] for w in controller.workspace_manager.list_workspaces() if w["is_active"] == 1][0] if controller.workspace_manager.list_workspaces() else "Default Workspace",
                    label="Active Workspace"
                )
                switch_ws_btn = gr.Button("⚡ Switch Active Workspace", variant="primary")
            
            with gr.Row():
                new_ws_name = gr.Textbox(placeholder="e.g. AI Research Lab", label="New Workspace Name")
                new_ws_desc = gr.Textbox(placeholder="Brief description...", label="Workspace Description")
                add_ws_btn = gr.Button("➕ Create Workspace", variant="secondary")
            
            ws_status_md = gr.Markdown()

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### 🔌 Ecosystem Plugins & Permissions")
            plugins_table = gr.Dataframe(
                headers=["ID", "Plugin Name", "Version", "Permissions", "Status", "Installed Date"],
                datatype=["str", "str", "str", "str", "str", "str"],
                col_count=(6, "fixed"),
                wrap=True
            )
            with gr.Row():
                plugin_select = gr.Dropdown(
                    choices=[p["id"] for p in controller.plugin_manager.list_plugins()],
                    value=controller.plugin_manager.list_plugins()[0]["id"] if controller.plugin_manager.list_plugins() else None,
                    label="Select Plugin"
                )
                enable_plugin_btn = gr.Button("🟢 Enable Plugin", variant="primary")
                disable_plugin_btn = gr.Button("🔴 Disable Plugin", variant="secondary")
            plugin_status_md = gr.Markdown()

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### 💾 System Backup & Archive Restore")
            backup_btn = gr.Button("📦 Create Full System Backup Zip", variant="primary")
            backup_file = gr.File(label="Download System Backup Archive", visible=False)
            backup_status_md = gr.Markdown()

        def fetch_plugins_table():
            plugins = controller.plugin_manager.list_plugins()
            data = []
            for p in plugins:
                data.append([
                    p["id"],
                    p["name"],
                    p["version"],
                    p["permissions"],
                    "🟢 Enabled" if p["enabled"] == 1 else "🔴 Disabled",
                    p["created_at"]
                ])
            return data

        def on_switch_ws(ws_name: str):
            all_ws = controller.workspace_manager.list_workspaces()
            target = [w for w in all_ws if w["name"] == ws_name]
            if target:
                controller.workspace_manager.set_active_workspace(target[0]["id"])
                return f"✅ Switched active workspace to **{ws_name}**"
            return "❌ Workspace not found."

        def on_create_ws(name: str, desc: str):
            if not name.strip():
                return "❌ Workspace name cannot be empty."
            controller.workspace_manager.create_workspace(name.strip(), desc.strip())
            all_ws = controller.workspace_manager.list_workspaces()
            choices = [w["name"] for w in all_ws]
            return gr.update(choices=choices, value=name.strip()), f"✅ Workspace **{name}** created!"

        def on_toggle_plugin(plugin_id: str, enable: bool):
            if not plugin_id:
                return fetch_plugins_table(), "❌ Please select a plugin."
            controller.plugin_manager.set_plugin_status(plugin_id, enable)
            status_str = "enabled" if enable else "disabled"
            return fetch_plugins_table(), f"✅ Plugin `{plugin_id}` {status_str}."

        def on_create_backup():
            res = controller.backup_manager.create_system_backup()
            if res["success"]:
                return gr.update(value=res["backup_path"], visible=True), f"✅ {res['message']}"
            return gr.update(visible=False), f"❌ {res['message']}"

        # Initial data
        plugins_table.value = fetch_plugins_table()

        # Event triggers
        switch_ws_btn.click(
            fn=on_switch_ws,
            inputs=[ws_select],
            outputs=[ws_status_md]
        )
        add_ws_btn.click(
            fn=on_create_ws,
            inputs=[new_ws_name, new_ws_desc],
            outputs=[ws_select, ws_status_md]
        )
        enable_plugin_btn.click(
            fn=lambda pid: on_toggle_skill(pid, True),
            inputs=[plugin_select],
            outputs=[plugins_table, plugin_status_md]
        )
        disable_plugin_btn.click(
            fn=lambda pid: on_toggle_skill(pid, False),
            inputs=[plugin_select],
            outputs=[plugins_table, plugin_status_md]
        )
        backup_btn.click(
            fn=on_create_backup,
            outputs=[backup_file, backup_status_md]
        )
