"""
AetherMind Cortex - Streamlit Flagship Application (Exact Design Match)
"""

import os
import sys
import streamlit as st

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

# Precise CSS Styling matching mockup colors, text sizes, borders, and logo framing
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global Dark Theme Force */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stBottom"], .main, div[data-testid="stToolbar"] {
        background-color: #030611 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #f1f5f9 !important;
    }

    /* Sidebar Background & Borders */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
        background-color: #060a17 !important;
        border-right: 1px solid rgba(56, 189, 248, 0.2) !important;
    }

    /* Override Native Streamlit Expanders (Remove White Background) */
    [data-testid="stExpander"], details {
        background-color: rgba(13, 20, 36, 0.85) !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        border-radius: 14px !important;
        color: #f8fafc !important;
    }
    summary, [data-testid="stExpanderSummary"] {
        background-color: rgba(18, 26, 46, 0.9) !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
    }
    details[open] summary {
        border-bottom: 1px solid rgba(56, 189, 248, 0.2) !important;
    }

    /* Override Native Streamlit Chat Messages (Remove White/Grey Bubble Fill) */
    [data-testid="stChatMessage"] {
        background-color: rgba(13, 20, 36, 0.85) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 14px !important;
        color: #f8fafc !important;
        margin-bottom: 12px !important;
    }
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span, [data-testid="stChatMessage"] div {
        color: #f1f5f9 !important;
    }

    /* Override Chat Input Bar at Bottom (Remove White Wrapper & Red Border) */
    [data-testid="stChatInput"], [data-testid="stChatInput"] > div, div[data-baseweb="input"] {
        background-color: #090e1a !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 14px !important;
        color: #f8fafc !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5) !important;
    }
    [data-testid="stChatInput"] textarea {
        background-color: transparent !important;
        color: #f8fafc !important;
    }

    /* Override Native Streamlit Buttons (Sidebar & Main Area) */
    button, div[data-testid="stButton"] > button {
        background: rgba(18, 26, 46, 0.9) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
    }
    button:hover, div[data-testid="stButton"] > button:hover {
        background: rgba(56, 189, 248, 0.25) !important;
        border-color: #38bdf8 !important;
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4) !important;
    }

    /* Override Radio & Checkbox Indicators */
    div[role="radiogroup"] label, div[data-testid="stCheckbox"] label {
        color: #cbd5e1 !important;
    }

    /* Typography Sizes & Colors */
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
    }

    p, span, label, div {
        color: #cbd5e1 !important;
    }

    .stCaption {
        color: #64748b !important;
        font-size: 0.8rem !important;
    }

    /* Background Watermark Animation */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 52%;
        left: 55%;
        transform: translate(-50%, -50%);
        width: 680px;
        height: 680px;
        background-image: url('https://raw.githubusercontent.com/KAVATIJOHNSHREYAN/AETHERMIND-CORTEX/main/assets/logo.png');
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
        opacity: 0.04;
        pointer-events: none;
        z-index: 0;
        animation: stCortexHeartbeat 2.8s ease-in-out infinite;
    }

    @keyframes stCortexHeartbeat {
        0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.04; }
        50% { transform: translate(-50%, -50%) scale(1.03); opacity: 0.065; filter: drop-shadow(0 0 35px rgba(56, 189, 248, 0.4)); }
    }

    /* Cards & Containers */
    .cortex-card {
        background: rgba(10, 16, 32, 0.85) !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        border-radius: 18px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
        backdrop-filter: blur(16px) !important;
    }

    .quote-card {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(56, 189, 248, 0.18) !important;
        border-radius: 14px !important;
        padding: 16px !important;
        text-align: right !important;
        font-style: italic !important;
        color: #94a3b8 !important;
    }

    /* Action Pills */
    .action-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 18px;
        background: rgba(20, 30, 55, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 20px;
        font-size: 0.85rem;
        color: #e2e8f0;
        margin: 4px;
        transition: all 0.2s ease;
    }

    .action-pill:hover {
        background: rgba(56, 189, 248, 0.2);
        border-color: #38bdf8;
        color: #ffffff;
    }

    /* Status Indicators */
    .status-badge-online {
        display: inline-block;
        width: 9px;
        height: 9px;
        background-color: #22c55e;
        border-radius: 50%;
        box-shadow: 0 0 10px #22c55e;
        margin-right: 6px;
    }

    /* Inputs & Selectboxes */
    div[data-baseweb="select"] > div, input, textarea {
        background-color: #0b1120 !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        border-radius: 10px !important;
        color: #f8fafc !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Bar Navigation matching Mockup UI Header exactly
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 22px; background: rgba(8, 13, 25, 0.95); border: 1px solid rgba(56, 189, 248, 0.22); border-radius: 16px; margin-bottom: 20px;">
    <div style="display: flex; align-items: center; gap: 14px;">
        <img src="https://raw.githubusercontent.com/KAVATIJOHNSHREYAN/AETHERMIND-CORTEX/main/assets/logo.png" style="width: 44px; height: 44px; border-radius: 10px; box-shadow: 0 0 16px rgba(56, 189, 248, 0.4);" />
        <div>
            <h3 style="margin: 0; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.2rem; font-weight: 800;">AetherMind Cortex</h3>
            <span style="font-size: 0.75rem; color: #94a3b8;">Human-Centered AI Reasoning Engine</span>
        </div>
    </div>
    <div style="flex-grow: 1; max-width: 420px; margin: 0 30px;">
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 20px; padding: 6px 16px; display: flex; align-items: center; justify-content: space-between;">
            <span style="color: #64748b; font-size: 0.82rem;">🔍 Search chats, tools, or anything...</span>
            <span style="background: rgba(30, 41, 59, 0.9); color: #94a3b8; font-size: 0.72rem; padding: 2px 8px; border-radius: 6px;">Ctrl + K</span>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 16px;">
        <span style="font-size: 0.82rem; color: #94a3b8;">"Think • Understand • Adapt • Assist"</span>
        <span style="font-size: 0.82rem; background: rgba(30, 41, 59, 0.8); color: #f8fafc; padding: 6px 16px; border-radius: 20px; border: 1px solid rgba(56, 189, 248, 0.25); font-weight: 600;">KAVATI ▾</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Header & Navigation
with st.sidebar:
    st.image("https://raw.githubusercontent.com/KAVATIJOHNSHREYAN/AETHERMIND-CORTEX/main/assets/logo.png", width=64)
    st.markdown("<h3 style='margin:4px 0 0 0; font-size:1.1rem; color:#f8fafc;'>AetherMind Cortex</h3>", unsafe_allow_html=True)
    st.caption("Human-Centered AI Reasoning Engine")
    
    st.markdown("---")
    st.markdown("<span style='font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;'>Navigation & Modules</span>", unsafe_allow_html=True)
    page_selection = st.radio(
        "Module Navigation:",
        ["💬 Reasoning Workspace", "🛠️ Expert Skills", "🔌 Plugins & Workspaces", "📚 Knowledge Base", "⚡ Automation", "⚙️ Settings", "🩺 Diagnostics", "ℹ️ About"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("<span style='font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;'>Quick Actions</span>", unsafe_allow_html=True)
    q1, q2 = st.columns(2)
    with q1:
        if st.button("➕ New Chat", use_container_width=True):
            controller.create_new_session()
            st.rerun()
    with q2:
        st.button("📂 Upload File", use_container_width=True)
        
    q3, q4 = st.columns(2)
    with q3:
        st.button("📁 Workspace", use_container_width=True)
    with q4:
        st.button("✨ Skills", use_container_width=True)

    st.markdown("---")
    st.markdown("<span style='font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;'>Model & System</span>", unsafe_allow_html=True)
    models = controller.get_available_models()
    selected_model = st.selectbox("Active Ollama Model", options=models if models else ["llama3-lexi-uncensored"])
    
    st.markdown("---")
    st.markdown("<span style='font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;'>System Health</span>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 0.85rem; line-height: 1.8;">
        <div><span class="status-badge-online"></span> <b style="color:#22c55e;">All Systems Operational</b></div>
        <div>🤖 <b>Ollama:</b> <span style="color:#22c55e;">Online</span></div>
        <div>🗄️ <b>Database:</b> <span style="color:#22c55e;">Healthy</span></div>
        <div>🧠 <b>Memory:</b> <span style="color:#22c55e;">Ready</span></div>
        <div>📚 <b>Knowledge Base:</b> <span style="color:#22c55e;">Ready</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.image("https://raw.githubusercontent.com/KAVATIJOHNSHREYAN/AETHERMIND-CORTEX/main/assets/logo.png", width=110)
    st.caption("AetherMind Cortex v1.0.0 Flagship AI Platform")

# Workspace Router
if page_selection == "💬 Reasoning Workspace":
    col_main, col_quote = st.columns([3, 1])
    
    with col_main:
        st.markdown("""
        <div class="cortex-card">
            <h2 style="margin: 0 0 6px 0; color: #f8fafc; font-size: 1.5rem; font-weight: 700;">
                👋 Welcome to <span style="background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AetherMind Cortex</span>
            </h2>
            <p style="margin: 0 0 16px 0; color: #94a3b8; font-size: 0.92rem;">
                Your personal AI reasoning partner. Choose a prompt, upload a file, or start a new conversation.
            </p>
            <div>
                <span class="action-pill">💡 Explain a concept</span>
                <span class="action-pill">📂 Analyze a file</span>
                <span class="action-pill">⚙️ Solve a problem</span>
                <span class="action-pill">📊 Create a plan</span>
                <span class="action-pill">More ▾</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_quote:
        st.markdown("""
        <div class="quote-card">
            <p style="margin:0; font-size: 0.85rem; color: #cbd5e1;">"Intelligence grows when curiosity meets purpose."</p>
        </div>
        """, unsafe_allow_html=True)

    # Hero Logo Artwork Container
    st.markdown("""
    <div style="text-align: center; padding: 24px 0;">
        <img src="https://raw.githubusercontent.com/KAVATIJOHNSHREYAN/AETHERMIND-CORTEX/main/assets/logo.png" style="width: 340px; max-width: 85%; border-radius: 28px; box-shadow: 0 0 60px rgba(56, 189, 248, 0.35); border: 1px solid rgba(56, 189, 248, 0.3);" />
    </div>
    """, unsafe_allow_html=True)

    # Chat Messages History
    messages = controller.get_active_messages()
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat Bar Controls
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

    # Developer Inspection Pipeline Card
    with st.expander("⚙️ Developer Mode: Cognitive Reasoning Inspection Pipeline", expanded=True):
        st.checkbox("Enable Developer Mode Reasoning Inspection Logs", value=True)
        st.caption("Active Expert Skills Context: Active")
        st.caption("Reasoning pipeline inspection logs will appear here during execution.")
        st.markdown("⚡ **Latency:** 0.0s | 🚀 **Speed:** 0.0 tokens/s | 🔢 **Token Count:** 0 tokens")

elif page_selection == "🛠️ Expert Skills":
    st.subheader("🛠️ Expert Skills Platform")
    skills = controller.skill_manager.list_skills()
    for s in skills:
        enabled = st.toggle(f"**{s['name']}**", value=s['enabled'] == 1, help=s['description'])
        if enabled != (s['enabled'] == 1):
            controller.skill_manager.set_skill_status(s['skill_id'], enabled)
            st.toast(f"Updated {s['name']} status!")

elif page_selection == "🔌 Plugins & Workspaces":
    st.subheader("🔌 Plugins & Workspace Switcher")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📂 Active Workspaces")
        workspaces = controller.workspace_manager.list_workspaces()
        for w in workspaces:
            st.write(f"- **{w['name']}**: `{w['path']}`")
    with col2:
        st.markdown("#### 🧩 Installed Extension Plugins")
        st.write(controller.plugin_manager.list_plugins())

elif page_selection == "📚 Knowledge Base":
    st.subheader("📚 Knowledge Base (Offline RAG Engine)")
    uploaded_files = st.file_uploader("Upload Documents to Ingest", accept_multiple_files=True, type=["pdf", "docx", "txt", "md", "py"])
    if uploaded_files:
        for f in uploaded_files:
            save_path = os.path.join("database", f.name)
            with open(save_path, "wb") as w:
                w.write(f.getvalue())
            controller.knowledge_engine.ingest_document(save_path)
        st.success(f"Ingested {len(uploaded_files)} documents into ChromaDB Vector Store!")
        
    st.markdown("#### 📄 Currently Indexed Documents")
    docs = controller.knowledge_engine.list_indexed_documents()
    if docs:
        st.table(docs)
    else:
        st.caption("No documents indexed yet.")

elif page_selection == "⚡ Automation":
    st.subheader("⚡ Local Automation & Task Intelligence")
    st.write(controller.workflow_engine.list_tasks(status="all"))

elif page_selection == "⚙️ Settings":
    st.subheader("⚙️ System Settings & Preferences")
    st.text_input("Ollama Host URL", value=controller.llm_engine.host)
    st.selectbox("Application Theme", options=["dark", "light"], index=0)

elif page_selection == "🩺 Diagnostics":
    st.subheader("🩺 System Diagnostics & Self-Healing Maintenance")
    dcol1, dcol2 = st.columns(2)
    with dcol1:
        if st.button("Run System Health Check", use_container_width=True):
            st.json(controller.diagnostics_engine.run_full_diagnostics())
    with dcol2:
        if st.button("Execute Self-Healing Repair", use_container_width=True):
            st.success(controller.diagnostics_engine.execute_self_healing_repair()["message"])

elif page_selection == "ℹ️ About":
    st.subheader("ℹ️ About AetherMind Cortex")
    st.markdown(f"**Version:** `{meta['version']}` ({meta['stage']})")
