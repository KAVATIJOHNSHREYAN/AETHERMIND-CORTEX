"""
Decision Dashboard UI Component for AetherMind Cortex (Phase 8)
Provides MCDA weighted scoring, option ranking tables, risk analysis, and decision history.
"""

import gradio as gr
from app.controller import AppController

def render_decision_tab(controller: AppController):
    """Renders the privacy-first Decision Intelligence Dashboard."""
    with gr.Tab("⚖️ Decision Intelligence"):
        gr.Markdown("### ⚖️ Multi-Criteria Decision Analysis (MCDA) Dashboard")
        gr.Markdown("*Evaluate technical options, compare alternatives, assess risk matrices, and save recommendations completely offline.*")

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### 🎯 Evaluate New Decision Topic")
            decision_topic = gr.Textbox(placeholder="e.g. Select Local Database Engine for AetherMind Cortex", label="Decision Topic / Objective")
            options_input = gr.Textbox(placeholder="Enter candidate options separated by commas (e.g. SQLite, PostgreSQL, ChromaDB)", label="Candidate Options (Comma separated)")
            
            with gr.Row():
                w_speed = gr.Slider(minimum=0.0, maximum=1.0, value=0.2, step=0.05, label="Weight: Speed & Performance")
                w_maintain = gr.Slider(minimum=0.0, maximum=1.0, value=0.25, step=0.05, label="Weight: Maintainability")
                w_scale = gr.Slider(minimum=0.0, maximum=1.0, value=0.25, step=0.05, label="Weight: Scalability")
                w_risk = gr.Slider(minimum=0.0, maximum=1.0, value=0.1, step=0.05, label="Weight: Risk & Security")

            eval_btn = gr.Button("⚖️ Execute MCDA Decision Evaluation", variant="primary")
            eval_summary_md = gr.Markdown()

        with gr.Group(elem_classes=["card-panel"]):
            gr.Markdown("#### 📊 Ranked Options & Risk Analysis Matrix")
            ranking_table = gr.Dataframe(
                headers=["Rank", "Option Name", "MCDA Score (0-100)", "Risk Level", "Pros / Advantages", "Cons / Disadvantages"],
                datatype=["number", "str", "number", "str", "str", "str"],
                col_count=(6, "fixed"),
                wrap=True
            )

        gr.Markdown("#### 📜 Saved Decision History & Feedback")
        history_table = gr.Dataframe(
            headers=["ID", "Decision Topic", "Recommended Option", "Confidence Score", "Rating", "Evaluated Date"],
            datatype=["str", "str", "str", "number", "number", "str"],
            col_count=(6, "fixed"),
            wrap=True
        )

        def fetch_saved_decisions():
            history = controller.decision_engine.list_saved_decisions()
            data = []
            for d in history:
                data.append([
                    d["id"][:8],
                    d["topic"],
                    d["recommended_option"],
                    f"{d['confidence_score']}%",
                    f"⭐ {d['feedback_rating']}/5" if d['feedback_rating'] > 0 else "Unrated",
                    d["created_at"]
                ])
            return data

        def on_evaluate(topic: str, options_str: str, w_sp: float, w_ma: float, w_sc: float, w_ri: float):
            if not topic.strip() or not options_str.strip():
                return [], fetch_saved_decisions(), "❌ Error: Topic and Candidate Options cannot be empty."

            raw_opts = [o.strip() for o in options_str.split(",") if o.strip()]
            custom_weights = {
                "speed": w_sp,
                "cost": 0.2,
                "maintainability": w_ma,
                "scalability": w_sc,
                "risk": w_ri
            }

            res = controller.decision_engine.evaluate_decision(topic.strip(), raw_opts, custom_weights)
            
            table_data = []
            for idx, opt in enumerate(res["ranked_options"], 1):
                table_data.append([
                    idx,
                    opt["option_name"],
                    opt["score"],
                    opt["risk_level"].upper(),
                    opt["pros"],
                    opt["cons"]
                ])

            summary = f"🏆 **Top Recommendation:** `{res['recommended_option']}` (Score: {res['ranked_options'][0]['score']}/100, Confidence: {res['confidence_score']}%)"
            return table_data, fetch_saved_decisions(), summary

        # Initial values
        history_table.value = fetch_saved_decisions()

        # Event triggers
        eval_btn.click(
            fn=on_evaluate,
            inputs=[decision_topic, options_input, w_speed, w_maintain, w_scale, w_risk],
            outputs=[ranking_table, history_table, eval_summary_md]
        )
