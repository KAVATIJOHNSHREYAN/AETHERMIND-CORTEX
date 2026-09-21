"""
AetherMind Cortex - Streamlit Desktop Web Dashboard
Alternative modern Streamlit interface integrated with central AppController.
"""

import os
import sys
import streamlit as st

# Ensure root directory is on sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.controller import AppController

# Page Configuration
st.set_page_config(
    page_title="AetherMind Cortex - AI Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Controller
@st.cache_resource
def get_controller():
    return AppController()

controller = get_controller()
meta = controller.get_metadata()
status = controller.get_system_status()

# Inject Heartbeat Watermark & Brand CSS
logo_url = "app/static/logo.png" if os.path.exists("app/static/logo.png") else "assets/logo.png"
st.markdown(f"""
<style>
    /* Background Heartbeat Watermark */
    .stApp {{
        background-color: #0f172a;
        color: #f8fafc;
    }}
    .stAppViewContainer::before {{
        content: "";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 550px;
        height: 550px;
        background-image: url('file/{os.path.abspath("assets/logo.png").replace("\\", "/")}');
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
        opacity: 0.05;
        pointer-events: none;
        z-index: 0;
        animation: stCortexHeartbeat 2.8s ease-in-out infinite;
    }}
    @keyframes stCortexHeartbeat {{
        0% {{ transform: translate(-50%, -50%) scale(1); opacity: 0.05; filter: drop-shadow(0 0 0px rgba(56, 189, 248, 0)); }}
        35% {{ transform: translate(-50%, -50%) scale(1.03); opacity: 0.06; filter: drop-shadow(0 0 25px rgba(56, 189, 248, 0.4)); }}
        70% {{ transform: translate(-50%, -50%) scale(1.008); opacity: 0.052; filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.15)); }}
        100% {{ transform: translate(-50%, -50%) scale(1); opacity: 0.05; filter: drop-shadow(0 0 0px rgba(56, 189, 248, 0)); }}
    }}
    .brand-header {{
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 24px;
    }}
    .brand-logo {{
        width: 56px;
        height: 56px;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }}
</style>
""", unsafe_allow_html=True)

# Sidebar Branding & Navigation
with st.sidebar:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("assets/logo.png", width=48)
    with col2:
        st.title("AetherMind")
        st.caption("Human-Centered AI Engine")
    
    st.divider()
    st.subheader("🤖 Active Model")
    models = controller.get_available_models()
    selected_model = st.selectbox("Ollama Model", options=models if models else ["No models found"])
    
    st.divider()
    st.subheader("💬 Sessions")
    if st.button("➕ New Chat"):
        controller.create_new_session(selected_model)
        st.rerun()
        
    sessions = controller.session_manager.list_sessions()
    session_titles = [s["title"] for s in sessions] if sessions else ["Default Chat"]
    selected_session = st.selectbox("Select Session", options=session_titles)

    st.divider()
    st.markdown(f"**Version:** `{meta['version']}`")
    st.markdown(f"**DB Status:** {'🟢 Healthy' if status['db_healthy'] else '🔴 Error'}")
    st.markdown(f"**Ollama:** {'🟢 Online' if status['ollama_online'] else '🔴 Offline'}")

# Main View Area & Header
st.markdown("""
<div class="brand-header">
    <h1 style="margin: 0; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🧠 AetherMind Cortex
    </h1>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab_chat, tab_knowledge, tab_memory, tab_decision, tab_diagnostics, tab_about = st.tabs([
    "💬 Chat", "📚 Knowledge Engine", "💾 Memory", "📊 Decision Engine", "🩺 Diagnostics", "ℹ️ About"
])

with tab_chat:
    st.subheader("Interactive Cognitive Chat Workspace")
    messages = controller.get_active_messages()
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    prompt = st.chat_input("Ask Cortex anything...")
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        controller.add_user_message(prompt)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Setup Cognitive Reasoning & Expert Skills System Prompt
            skills_context = controller.skill_manager.get_active_skills_prompt_injection()
            reasoning_prompt = controller.reasoning_engine.generate_reasoning_pipeline_prompt(
                prompt=prompt,
                user_context=controller.profile_manager.get_personalized_prompt_context(),
                memory_context=controller.memory_manager.get_context_prompt_injection(prompt),
                rag_context=controller.knowledge_engine.get_rag_context_injection(prompt)[0]
            )
            if skills_context:
                reasoning_prompt += "\n" + skills_context

            # Construct message history format
            history_msgs = []
            for m in messages:
                history_msgs.append({"role": m["role"], "content": m["content"]})
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

with tab_knowledge:
    st.subheader("📚 Offline RAG Knowledge Engine")
    docs = controller.knowledge_engine.list_indexed_documents()
    st.metric("Indexed Documents", len(docs))
    st.write(docs)

with tab_memory:
    st.subheader("💾 Long-Term Episodic Memory")
    mems = controller.memory_manager.list_memories()
    st.write(mems)

with tab_decision:
    st.subheader("📊 Decision Intelligence Engine")
    st.info("MCDA multi-criteria evaluation engine ready.")

with tab_diagnostics:
    st.subheader("🩺 System Health & Self-Healing Maintenance")
    if st.button("Run Full System Diagnostics"):
        rep = controller.diagnostics_engine.run_full_diagnostics()
        st.json(rep)
    if st.button("Execute Self-Healing Repair"):
        res = controller.diagnostics_engine.execute_self_healing_repair()
        st.success(res["message"])

with tab_about:
    st.subheader("ℹ️ About AetherMind Cortex")
    st.markdown(f"**Version:** `{meta['version']}` ({meta['stage']})")
    st.markdown("100% Offline, Privacy-First Human-Centered AI Reasoning Platform.")
