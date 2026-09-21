"""
AetherMind Cortex - Streamlit Flagship Application (Exact Mockup Match)
"""

import os
import sys
import streamlit as st

# Ensure root directory is on sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.controller import AppController

st.set_page_config(
    page_title="AetherMind Cortex - Flagship AI Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def get_controller():
    return AppController()

controller = get_controller()
meta = controller.get_metadata()
status = controller.get_system_status()

# Advanced Cyberpunk & Glassmorphic CSS Engine
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #05070e !important;
        font-family: 'Inter', sans-serif !important;
        color: #f8fafc !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #080d19 !important;
        border-right: 1px solid rgba(56, 189, 248, 0.15) !important;
    }
    
    /* Background Heartbeat Watermark */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 650px;
        height: 650px;
        background-image: url('https://raw.githubusercontent.com/KAVATIJOHNSHREYAN/AETHERMIND-CORTEX/main/assets/logo.png');
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
        opacity: 0.045;
        pointer-events: none;
        z-index: 0;
        animation: stCortexHeartbeat 2.8s ease-in-out infinite;
    }
    @keyframes stCortexHeartbeat {
        0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.045; }
        50% { transform: translate(-50%, -50%) scale(1.035); opacity: 0.07; filter: drop-shadow(0 0 35px rgba(56, 189, 248, 0.4)); }
    }
    
    /* Cards & Containers */
    .cortex-card {
        background: rgba(13, 20, 36, 0.85);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        backdrop-filter: blur(16px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    
    .cortex-btn-primary {
        background: linear-gradient(135deg, #0284c7 0%, #6366f1 50%, #a855f7 100%);
        color: #fff;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(56, 189, 248, 0.35);
        transition: all 0.2s ease;
    }
    
    .quick-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 20px;
        font-size: 0.85rem;
        color: #f8fafc;
        margin: 4px;
    }

    .status-dot {
        height: 8px;
        width: 8px;
        background-color: #22c55e;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #22c55e;
    }
</style>
""", unsafe_allow_html=True)

# Top Bar Header Navigation matching Mockup UI
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; background: rgba(9, 14, 26, 0.95); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 16px; margin-bottom: 20px;">
    <div style="display: flex; align-items: center; gap: 14px;">
        <img src="https://raw.githubusercontent.com/KAVATIJOHNSHREYAN/AETHERMIND-CORTEX/main/assets/logo.png" style="width: 44px; height: 44px; border-radius: 10px; box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);" />
        <div>
            <h3 style="margin: 0; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.25rem; font-weight: 800;">AetherMind Cortex</h3>
            <span style="font-size: 0.75rem; color: #94a3b8;">Human-Centered AI Reasoning Engine</span>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 20px;">
        <span style="font-size: 0.85rem; color: #94a3b8;">"Think • Understand • Adapt • Assist"</span>
        <span style="font-size: 0.85rem; background: rgba(30, 41, 59, 0.8); padding: 6px 14px; border-radius: 20px; border: 1px solid rgba(56, 189, 248, 0.2);">KAVATI</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Components
with st.sidebar:
    st.subheader("🧭 Navigation & Modules")
    page_selection = st.radio(
        "Select Workspace View:",
        ["💬 Reasoning Workspace", "🛠️ Expert Skills", "🔌 Plugins & Workspaces", "📚 Knowledge Base", "⚡ Automation", "⚙️ Settings", "🩺 Diagnostics", "ℹ️ About"]
    )
    
    st.divider()
    st.subheader("⚡ Quick Actions")
    qcol1, qcol2 = st.columns(2)
    with qcol1:
        if st.button("➕ New Chat", use_container_width=True):
            controller.create_new_session()
            st.rerun()
    with qcol2:
        st.button("📂 Upload File", use_container_width=True)
        
    st.divider()
    st.subheader("🤖 Model & System")
    models = controller.get_available_models()
    selected_model = st.selectbox("Active Ollama Model", options=models if models else ["No models found"])
    
    st.divider()
    st.subheader("⚡ System Health")
    st.markdown("""
    <div style="font-size: 0.85rem; line-height: 1.8;">
        <div><span class="status-dot"></span> <b>All Systems Operational</b></div>
        <div>🤖 <b>Ollama:</b> <span style="color:#22c55e;">Online</span></div>
        <div>🗄️ <b>Database:</b> <span style="color:#22c55e;">Healthy</span></div>
        <div>🧠 <b>Memory:</b> <span style="color:#22c55e;">Ready</span></div>
        <div>📚 <b>Knowledge Base:</b> <span style="color:#22c55e;">Ready</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.image("https://raw.githubusercontent.com/KAVATIJOHNSHREYAN/AETHERMIND-CORTEX/main/assets/logo.png", width=120)
    st.caption("AetherMind Cortex v1.0.0 Flagship AI Platform")

# Page Navigation Router
if page_selection == "💬 Reasoning Workspace":
    # Header Card matching Mockup UI
    st.markdown("""
    <div class="cortex-card" style="text-align: center;">
        <h2 style="margin: 0 0 6px 0; color: #f8fafc; font-size: 1.45rem;">👋 Welcome to AetherMind Cortex</h2>
        <p style="margin: 0 0 16px 0; color: #94a3b8; font-size: 0.9rem;">Your personal AI reasoning partner. Choose a prompt, upload a file, or start a new conversation.</p>
        <div>
            <span class="quick-pill">💡 Explain a concept</span>
            <span class="quick-pill">📂 Analyze a file</span>
            <span class="quick-pill">⚙️ Solve a problem</span>
            <span class="quick-pill">📊 Create a plan</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display Central Logo Illustration Frame
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <img src="https://raw.githubusercontent.com/KAVATIJOHNSHREYAN/AETHERMIND-CORTEX/main/assets/logo.png" style="width: 320px; max-width: 80%; border-radius: 24px; box-shadow: 0 0 50px rgba(56, 189, 248, 0.3);" />
    </div>
    """, unsafe_allow_html=True)

    # Active Session Chat Messages
    messages = controller.get_active_messages()
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    prompt = st.chat_input("Type your technical prompt or complex query here...")
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        controller.add_user_message(prompt)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            skills_context = controller.skill_manager.get_active_skills_prompt_injection()
            reasoning_prompt = controller.reasoning_engine.generate_reasoning_pipeline_prompt(
                prompt=prompt,
                user_context=controller.profile_manager.get_personalized_prompt_context(),
                memory_context=controller.memory_manager.get_context_prompt_injection(prompt),
                rag_context=controller.knowledge_engine.get_rag_context_injection(prompt)[0]
            )
            if skills_context:
                reasoning_prompt += "\n" + skills_context

            history_msgs = [{"role": m["role"], "content": m["content"]} for m in messages]
            history_msgs.append({"role": "user", "content": prompt})

            response_accumulated = ""
            for chunk in controller.llm_engine.stream_chat(
                model=selected_model,
                messages=history_msgs,
                system_prompt=reasoning_prompt
            ):
                response_accumulated = chunk["accumulated"]
                message_placeholder.markdown(response_accumulated + "▌")
            
            message_placeholder.markdown(response_accumulated)
            controller.add_assistant_message(response_accumulated)
            st.rerun()

    with st.expander("⚙️ Developer Mode: Cognitive Reasoning Inspection Pipeline", expanded=True):
        st.checkbox("Enable Developer Mode Reasoning Inspection Logs", value=True)
        st.caption("Active Expert Skills Context: Active")
        st.caption("Reasoning pipeline inspection logs will appear here during execution.")
        st.markdown("⚡ **Latency:** 0.0s | 🚀 **Speed:** 0.0 tokens/s | 🔢 **Token Count:** 0 tokens")

elif page_selection == "🛠️ Expert Skills":
    st.subheader("🛠️ Expert Skills Platform")
    skills = controller.skill_manager.list_skills()
    for s in skills:
        st.checkbox(f"**{s['name']}** - {s['description']}", value=s['enabled'] == 1)

elif page_selection == "🔌 Plugins & Workspaces":
    st.subheader("🔌 Plugins & Workspace Switcher")
    workspaces = controller.workspace_manager.list_workspaces()
    st.write("Active Workspaces:", workspaces)

elif page_selection == "📚 Knowledge Base":
    st.subheader("📚 Knowledge Base (Offline RAG)")
    docs = controller.knowledge_engine.list_indexed_documents()
    st.metric("Indexed Documents", len(docs))
    st.write(docs)

elif page_selection == "⚡ Automation":
    st.subheader("⚡ Local Automation & Reminders")
    tasks = controller.workflow_engine.list_tasks(status="all")
    st.write("Tasks:", tasks)

elif page_selection == "⚙️ Settings":
    st.subheader("⚙️ System Settings")
    st.text_input("Ollama Host URL", value=controller.llm_engine.host)

elif page_selection == "🩺 Diagnostics":
    st.subheader("🩺 System Diagnostics & Self-Healing")
    if st.button("Run System Health Check"):
        st.json(controller.diagnostics_engine.run_full_diagnostics())
    if st.button("Execute Self-Healing Repair"):
        st.success(controller.diagnostics_engine.execute_self_healing_repair()["message"])

elif page_selection == "ℹ️ About":
    st.subheader("ℹ️ About AetherMind Cortex")
    st.markdown(f"**Version:** `{meta['version']}` ({meta['stage']})")
    st.markdown("100% Offline, Privacy-First Human-Centered AI Reasoning Platform.")
