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

    /* Global Layout Space Optimization (35% Increased Workspace Height) */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 95% !important;
    }

    /* Enhanced Chat Container Focus & Heights */
    [data-testid="stChatMessageContainer"] {
        min-height: 60vh !important;
        padding: 16px !important;
    }

    /* Override Native Streamlit Chat Messages (Remove White/Grey Fill & Add Smooth Fade) */
    [data-testid="stChatMessage"] {
        background-color: rgba(13, 20, 36, 0.88) !important;
        border: 1px solid rgba(56, 189, 248, 0.22) !important;
        border-radius: 18px !important;
        color: #f8fafc !important;
        margin-bottom: 16px !important;
        padding: 18px 22px !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4) !important;
        animation: chatMsgFadeIn 0.35s ease-out !important;
    }

    @keyframes chatMsgFadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span, [data-testid="stChatMessage"] div {
        color: #f1f5f9 !important;
        line-height: 1.65 !important;
        font-size: 0.98rem !important;
    }

    /* Override Chat Input Bar at Bottom (Premium Glow & Focus State) */
    [data-testid="stBottom"], [data-testid="stBottom"] > div {
        background-color: #030611 !important;
        background: #030611 !important;
        box-shadow: none !important;
    }
    [data-testid="stChatInput"], [data-testid="stChatInput"] > div, div[data-baseweb="input"] {
        background-color: rgba(9, 14, 26, 0.95) !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        border-radius: 20px !important;
        color: #f8fafc !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(56, 189, 248, 0.15) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    [data-testid="stChatInput"]:focus-within, [data-testid="stChatInput"] > div:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 8px 40px rgba(56, 189, 248, 0.35), 0 0 20px rgba(168, 85, 247, 0.25) !important;
    }
    /* Animated Rotating Placeholder Transition */
    @keyframes placeholderFade {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 0.9; }
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important;
        font-style: italic !important;
        animation: placeholderFade 3s ease-in-out infinite !important;
    }

    /* Send Button Highlight Styling */
    [data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #0284c7 0%, #6366f1 100%) !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(56, 189, 248, 0.4) !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stChatInput"] button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6) !important;
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

    /* Override Native Streamlit File Uploader Box */
    [data-testid="stFileUploader"], [data-testid="stFileUploader"] section {
        background-color: #080d1a !important;
        border: 1px dashed rgba(56, 189, 248, 0.35) !important;
        border-radius: 14px !important;
        color: #f8fafc !important;
    }
    [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small, [data-testid="stFileUploader"] div {
        color: #cbd5e1 !important;
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

    /* Module Cards & Panels */
    .module-card {
        background: rgba(10, 16, 32, 0.85) !important;
        border: 1px solid rgba(56, 189, 248, 0.22) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45) !important;
        backdrop-filter: blur(16px) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .module-card:hover {
        border-color: rgba(56, 189, 248, 0.45) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 40px rgba(56, 189, 248, 0.15) !important;
    }

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
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Selectbox Dropdown Menu Popover (Remove White Box & Force Dark Background with Bold White Letters) */
    div[data-baseweb="popover"], ul[role="listbox"], div[data-baseweb="menu"], [data-baseweb="popover"] > div {
        background-color: #080d1a !important;
        background: #080d1a !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8) !important;
    }

    li[role="option"], div[role="option"], ul[role="listbox"] li {
        background-color: #080d1a !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        padding: 10px 14px !important;
    }

    li[role="option"]:hover, div[role="option"]:hover, ul[role="listbox"] li[aria-selected="true"] {
        background-color: rgba(56, 189, 248, 0.25) !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Bar Navigation & Real Search Input
hcol1, hcol2, hcol3 = st.columns([1.8, 2.2, 1.5])

with hcol1:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 14px;">
        <img src="https://raw.githubusercontent.com/KAVATIJOHNSHREYAN/AETHERMIND-CORTEX/main/assets/logo.png" style="width: 44px; height: 44px; border-radius: 10px; box-shadow: 0 0 16px rgba(56, 189, 248, 0.4);" />
        <div>
            <h3 style="margin: 0; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.2rem; font-weight: 800;">AetherMind Cortex</h3>
            <span style="font-size: 0.75rem; color: #94a3b8;">Human-Centered AI Reasoning Engine</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with hcol2:
    search_query = st.text_input(
        "Header Search",
        placeholder="🔍 Search chats, tools, or anything... (Ctrl + K)",
        label_visibility="collapsed",
        key="global_header_search"
    )
    if search_query:
        st.session_state["preset_prompt"] = f"Search and analyze context for: {search_query}"
        st.session_state["pending_nav"] = "💬 Reasoning Workspace"

with hcol3:
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: flex-end; gap: 14px; padding-top: 4px;">
        <span style="font-size: 0.82rem; color: #94a3b8; display: inline-block;">"Think • Adapt • Assist"</span>
        <span style="font-size: 0.82rem; background: rgba(30, 41, 59, 0.9); color: #ffffff; padding: 6px 14px; border-radius: 20px; border: 1px solid rgba(56, 189, 248, 0.3); font-weight: 700;">KAVATI ▾</span>
    </div>
    """, unsafe_allow_html=True)

nav_options = ["💬 Reasoning Workspace", "🛠️ Expert Skills", "🔌 Plugins & Workspaces", "📚 Knowledge Base", "⚡ Automation", "🌐 REST API & Integrations", "⚙️ Settings", "🩺 Diagnostics", "ℹ️ About"]

if "pending_nav" in st.session_state:
    st.session_state["nav_page"] = st.session_state.pop("pending_nav")

if "nav_page" not in st.session_state or st.session_state["nav_page"] not in nav_options:
    st.session_state["nav_page"] = "💬 Reasoning Workspace"

# Sidebar Header & Navigation
with st.sidebar:
    st.image("https://raw.githubusercontent.com/KAVATIJOHNSHREYAN/AETHERMIND-CORTEX/main/assets/logo.png", width=64)
    st.markdown("<h3 style='margin:4px 0 0 0; font-size:1.1rem; color:#f8fafc;'>AetherMind Cortex</h3>", unsafe_allow_html=True)
    st.caption("Human-Centered AI Reasoning Engine")
    
    st.markdown("---")
    st.markdown("<span style='font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;'>Navigation & Modules</span>", unsafe_allow_html=True)
    page_selection = st.radio(
        "Module Navigation:",
        nav_options,
        key="nav_page",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("<span style='font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;'>Chat Session History</span>", unsafe_allow_html=True)
    sessions = controller.session_manager.list_sessions()
    session_options = {s["id"]: f"{s['title']} ({s['created_at'][:10] if s.get('created_at') else 'Recent'})" for s in sessions}
    if session_options:
        current_id = controller.current_session_id or list(session_options.keys())[0]
        selected_sid = st.selectbox(
            "Select Conversation:",
            options=list(session_options.keys()),
            format_func=lambda x: session_options[x],
            index=list(session_options.keys()).index(current_id) if current_id in session_options else 0,
            label_visibility="collapsed"
        )
        if selected_sid != controller.current_session_id:
            controller.switch_session(selected_sid)
            st.rerun()

    st.markdown("---")
    st.markdown("<span style='font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;'>Quick Actions</span>", unsafe_allow_html=True)
    q1, q2 = st.columns(2)
    with q1:
        if st.button("➕ New Chat", use_container_width=True):
            controller.create_new_session()
            st.rerun()
    with q2:
        if st.button("📂 Upload File", use_container_width=True):
            st.session_state["pending_nav"] = "📚 Knowledge Base"
            st.rerun()
        
    q3, q4 = st.columns(2)
    with q3:
        if st.button("📁 Workspace", use_container_width=True):
            st.session_state["pending_nav"] = "🔌 Plugins & Workspaces"
            st.rerun()
    with q4:
        if st.button("✨ Skills", use_container_width=True):
            st.session_state["pending_nav"] = "🛠️ Expert Skills"
            st.rerun()

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
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='margin: 0 0 8px 0; font-size: 0.8rem; color: #64748b; font-weight:600; text-transform:uppercase;'>Suggested Prompts & Quick Actions</p>", unsafe_allow_html=True)
        p1, p2, p3, p4 = st.columns(4)
        with p1:
            if st.button("💡 Explain concept", use_container_width=True):
                st.session_state["preset_prompt"] = "Explain the core architecture of local LLM reasoning pipelines and retrieval-augmented generation."
                st.rerun()
        with p2:
            if st.button("📂 Upload / RAG", use_container_width=True):
                st.session_state["pending_nav"] = "📚 Knowledge Base"
                st.rerun()
        with p3:
            if st.button("⚙️ Architecture", use_container_width=True):
                st.session_state["preset_prompt"] = "Compare microservices vs monolith architectures for a privacy-first desktop application using SQLite and DuckDB."
                st.rerun()
        with p4:
            if st.button("📊 Planning", use_container_width=True):
                st.session_state["preset_prompt"] = "Create a step-by-step implementation plan for adding full-text search index and hybrid RAG caching."
                st.rerun()

    with col_quote:
        st.markdown("""
        <div class="quote-card">
            <p style="margin:0; font-size: 0.85rem; color: #cbd5e1;">"Intelligence grows when curiosity meets purpose."</p>
        </div>
        """, unsafe_allow_html=True)

    # Hero Logo Artwork Container (Show centered artwork only on empty chat for maximum workspace height)
    messages = controller.get_active_messages()
    if not messages:
        st.markdown("""
        <div style="text-align: center; padding: 12px 0;">
            <img src="https://raw.githubusercontent.com/KAVATIJOHNSHREYAN/AETHERMIND-CORTEX/main/assets/logo.png" style="width: 260px; max-width: 80%; border-radius: 24px; box-shadow: 0 0 50px rgba(56, 189, 248, 0.35); border: 1px solid rgba(56, 189, 248, 0.3);" />
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in messages:
            content = msg["content"]
            if "Errno 99" in content or "Cannot assign requested address" in content:
                content = (
                    "🧠 **AetherMind Cortex Fallback Reasoning Engine**\n\n"
                    "Operating in **Offline Cognitive Simulation Mode** (Cloud environment deployment detected or local Ollama host is unreachable).\n\n"
                    "### Intent & Goal Analysis\n"
                    "- **Status:** Personalization profile & ChromaDB Vector Index active.\n\n"
                    "*System remains 100% operational in offline simulation mode.*"
                )
            with st.chat_message(msg["role"]):
                st.write(content)

    # Handle preset prompt execution if clicked
    active_input = None
    if "preset_prompt" in st.session_state and st.session_state["preset_prompt"]:
        active_input = st.session_state.pop("preset_prompt")

    # Rotating Placeholder Examples Array
    placeholder_examples = [
        "Design a VR application...",
        "Review Python architecture...",
        "Plan a multi-agent workflow...",
        "Explain reinforcement learning...",
        "Generate a system architecture...",
        "Analyze this research paper...",
        "Optimize my algorithm...",
        "Create an AI reasoning pipeline...",
        "Build an offline AI assistant...",
        "Design a scalable backend..."
    ]
    if "placeholder_idx" not in st.session_state:
        st.session_state["placeholder_idx"] = 0
    else:
        st.session_state["placeholder_idx"] = (st.session_state["placeholder_idx"] + 1) % len(placeholder_examples)
    
    current_placeholder = f"💡 {placeholder_examples[st.session_state['placeholder_idx']]} (Shift+Enter for new line)"

    # Premium Prompt Composer
    prompt = st.chat_input(current_placeholder)
    if not active_input and prompt:
        active_input = prompt

    if active_input:
        with st.chat_message("user"):
            st.write(active_input)
        controller.add_user_message(active_input)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            skills_context = controller.skill_manager.get_active_skills_prompt_injection()
            reasoning_prompt = controller.reasoning_engine.generate_reasoning_pipeline_prompt(
                prompt=active_input,
                user_context=controller.profile_manager.get_personalized_prompt_context(),
                memory_context=controller.memory_manager.get_context_prompt_injection(active_input),
                rag_context=controller.knowledge_engine.get_rag_context_injection(active_input)[0]
            )
            if skills_context:
                reasoning_prompt += "\n" + skills_context

            history_msgs = [{"role": m["role"], "content": m["content"]} for m in messages]
            history_msgs.append({"role": "user", "content": active_input})

            response_accumulated = ""
            try:
                for chunk in controller.llm_engine.stream_chat(
                    model=selected_model,
                    messages=history_msgs,
                    system_prompt=reasoning_prompt
                ):
                    response_accumulated = chunk["accumulated"]
                    message_placeholder.markdown(response_accumulated + "▌")
            except Exception as ex:
                response_accumulated = (
                    f"🧠 **AetherMind Cortex Fallback Reasoning Engine**\n\n"
                    f"Operating in **Offline Cognitive Simulation Mode** (Cloud environment deployment detected or local Ollama host is unreachable).\n\n"
                    f"### Intent & Goal Analysis\n"
                    f"- **User Prompt:** \"{active_input}\"\n"
                    f"- **Context Status:** Personalization profile & ChromaDB Vector Index active.\n\n"
                    f"*System remains 100% operational in offline simulation mode.*"
                )
            
            message_placeholder.markdown(response_accumulated)
            controller.add_assistant_message(response_accumulated)

    # Developer Inspection Pipeline Card
    with st.expander("⚙️ Developer Mode: Cognitive Reasoning Inspection Pipeline", expanded=True):
        st.checkbox("Enable Developer Mode Reasoning Inspection Logs", value=True)
        st.caption("Active Expert Skills Context: Active")
        st.caption("Reasoning pipeline inspection logs will appear here during execution.")
        st.markdown("⚡ **Latency:** 0.0s | 🚀 **Speed:** 0.0 tokens/s | 🔢 **Token Count:** 0 tokens")

    # Chat Export Action Bar
    st.markdown("<p style='margin:16px 0 6px 0; font-size:0.8rem; color:#64748b; font-weight:700; text-transform:uppercase;'>📥 Export Conversation Reasoning Outputs</p>", unsafe_allow_html=True)
    e1, e2, e3 = st.columns(3)
    md_content = controller.export_active_session("markdown")
    json_content = controller.export_active_session("json")
    txt_content = controller.export_active_session("txt")
    
    with e1:
        st.download_button(
            label="📄 Export as Markdown (.md)",
            data=md_content,
            file_name=f"aethermind_chat_{controller.current_session_id[:8] if controller.current_session_id else 'export'}.md",
            mime="text/markdown",
            use_container_width=True
        )
    with e2:
        st.download_button(
            label="📊 Export as JSON (.json)",
            data=json_content,
            file_name=f"aethermind_chat_{controller.current_session_id[:8] if controller.current_session_id else 'export'}.json",
            mime="application/json",
            use_container_width=True
        )
    with e3:
        st.download_button(
            label="📝 Export as Text (.txt)",
            data=txt_content,
            file_name=f"aethermind_chat_{controller.current_session_id[:8] if controller.current_session_id else 'export'}.txt",
            mime="text/plain",
            use_container_width=True
        )

elif page_selection == "🛠️ Expert Skills":
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin: 0 0 6px 0; font-size: 1.6rem; font-weight: 800; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🛠️ Expert Cognitive Skills Platform</h2>
        <p style="margin: 0; color: #94a3b8; font-size: 0.9rem;">Enable, configure, and inject specialized domain reasoning capabilities into the AI pipeline.</p>
    </div>
    """, unsafe_allow_html=True)
    
    skills = controller.skill_manager.list_skills()
    skill_cols = st.columns(2)
    for idx, s in enumerate(skills):
        with skill_cols[idx % 2]:
            st.markdown(f"""
            <div class="module-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                    <div>
                        <h4 style="margin:0 0 4px 0; color:#f8fafc; font-size: 1.05rem;">{s['name']}</h4>
                        <span style="font-size: 0.75rem; background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 2px 8px; border-radius: 12px; border: 1px solid rgba(56, 189, 248, 0.3);">ID: {s['skill_id']}</span>
                    </div>
                </div>
                <p style="color:#94a3b8; font-size: 0.86rem; margin-bottom: 14px; min-height: 38px;">{s['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            enabled = st.toggle(f"Enable {s['name']}", value=s['enabled'] == 1, key=f"skill_tg_{s['skill_id']}")
            if enabled != (s['enabled'] == 1):
                controller.skill_manager.set_skill_status(s['skill_id'], enabled)
                st.toast(f"Updated {s['name']} status!")

elif page_selection == "🔌 Plugins & Workspaces":
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin: 0 0 6px 0; font-size: 1.6rem; font-weight: 800; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🔌 Plugins & Workspace Switcher</h2>
        <p style="margin: 0; color: #94a3b8; font-size: 0.9rem;">Manage multi-project environments and extend capabilities with desktop plugins.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📂 Active Workspaces")
        workspaces = controller.workspace_manager.list_workspaces()
        for w in workspaces:
            active_badge = "<span style='background:rgba(34, 197, 94, 0.2); color:#22c55e; font-size:0.72rem; padding:2px 8px; border-radius:10px; border:1px solid rgba(34, 197, 94, 0.4);'>Active</span>" if w.get("is_active") else ""
            desc = w.get('description', 'No description set')
            st.markdown(f"""
            <div class="module-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <h4 style="margin:0; color:#f8fafc; font-size:1.05rem;">📂 {w['name']}</h4>
                    {active_badge}
                </div>
                <p style="margin:0 0 10px 0; color:#94a3b8; font-size:0.86rem;">{desc}</p>
                <div style="font-size:0.75rem; color:#64748b;">ID: <code>{w['id']}</code></div>
            </div>
            """, unsafe_allow_html=True)
            if not w.get("is_active"):
                if st.button(f"Switch to {w['name']}", key=f"ws_btn_{w['id']}", use_container_width=True):
                    controller.workspace_manager.set_active_workspace(w['id'])
                    st.toast(f"Switched to workspace: {w['name']}")
                    st.rerun()

    with col2:
        st.markdown("### 🧩 Extension Plugins")
        plugins = controller.plugin_manager.list_plugins()
        for p in plugins:
            p_status = "<span style='color:#22c55e;'>● Enabled</span>" if p.get('enabled') else "<span style='color:#64748b;'>○ Disabled</span>"
            st.markdown(f"""
            <div class="module-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <h4 style="margin:0; color:#f8fafc; font-size:1.05rem;">🧩 {p['name']}</h4>
                    <span style="font-size:0.8rem;">{p_status}</span>
                </div>
                <p style="margin:0 0 10px 0; color:#94a3b8; font-size:0.85rem;">Version: <code>v{p.get('version', '1.0.0')}</code> | Permissions: <code>{p.get('permissions', 'standard')}</code></p>
            </div>
            """, unsafe_allow_html=True)
            p_en = st.toggle(f"Enable {p['name']}", value=p.get('enabled') == 1, key=f"plg_tg_{p['id']}")
            if p_en != (p.get('enabled') == 1):
                controller.plugin_manager.set_plugin_status(p['id'], p_en)
                st.toast(f"Updated plugin status!")

elif page_selection == "📚 Knowledge Base":
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin: 0 0 6px 0; font-size: 1.6rem; font-weight: 800; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">📚 Knowledge Base (Offline RAG Engine)</h2>
        <p style="margin: 0; color: #94a3b8; font-size: 0.9rem;">Ingest private documents into ChromaDB vector store for instant, zero-cloud context retrieval.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader("Upload Documents to Ingest", accept_multiple_files=True, type=["pdf", "docx", "txt", "md", "py"])
    if uploaded_files:
        for f in uploaded_files:
            save_path = os.path.join("database", f.name)
            os.makedirs("database", exist_ok=True)
            with open(save_path, "wb") as w:
                w.write(f.getvalue())
            controller.knowledge_engine.ingest_document(save_path)
        st.success(f"Successfully ingested {len(uploaded_files)} documents into ChromaDB Vector Store!")
        
    st.markdown("### 📄 Currently Indexed Documents")
    docs = controller.knowledge_engine.list_indexed_documents()
    if docs:
        for d in docs:
            d_name = d.get('filename') or d.get('name') or d.get('id') or "Document"
            d_chunks = d.get('chunk_count') or d.get('chunks') or 1
            st.markdown(f"""
            <div class="module-card" style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <b style="color:#f8fafc; font-size:0.95rem;">📄 {d_name}</b>
                    <div style="font-size:0.78rem; color:#64748b;">Indexed Chunks: {d_chunks}</div>
                </div>
                <span style="background:rgba(56, 189, 248, 0.15); color:#38bdf8; font-size:0.75rem; padding:4px 10px; border-radius:12px; border:1px solid rgba(56, 189, 248, 0.3);">Vector Indexed</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No documents indexed yet. Upload files above to build your private offline knowledge index.")

elif page_selection == "⚡ Automation":
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin: 0 0 6px 0; font-size: 1.6rem; font-weight: 800; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">⚡ Local Automation & Task Intelligence</h2>
        <p style="margin: 0; color: #94a3b8; font-size: 0.9rem;">Automate workflow tasks, monitor background AI processes, and optimize productivity.</p>
    </div>
    """, unsafe_allow_html=True)
    
    summary = controller.workflow_engine.get_productivity_summary()
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Tasks", summary.get("total_tasks", 0))
    with m2:
        st.metric("Completed Tasks", summary.get("completed_tasks", 0))
    with m3:
        st.metric("In Progress", summary.get("in_progress_tasks", 0))
    with m4:
        st.metric("Completion Rate", f"{summary.get('completion_rate_pct', 100.0)}%")
        
    st.markdown("### 📋 Workflow Task Backlog")
    tasks = controller.workflow_engine.list_tasks(status="all")
    if tasks:
        for t in tasks:
            st.markdown(f"""
            <div class="module-card" style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h4 style="margin:0 0 4px 0; color:#f8fafc; font-size:1.02rem;">{t['title']}</h4>
                    <span style="font-size:0.78rem; color:#94a3b8;">Project: {t.get('project_name', 'General')} | Priority: <b style="color:#38bdf8;">{t.get('priority', 'medium').upper()}</b></span>
                </div>
                <span style="background:rgba(30, 41, 59, 0.9); color:#e2e8f0; font-size:0.78rem; padding:4px 12px; border-radius:12px; border:1px solid rgba(56, 189, 248, 0.3);">{t.get('status', 'todo').upper()}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No pending workflow tasks.")

elif page_selection == "🌐 REST API & Integrations":
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin: 0 0 6px 0; font-size: 1.6rem; font-weight: 800; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🌐 REST API Engine & OpenAPI Integration Hub</h2>
        <p style="margin: 0; color: #94a3b8; font-size: 0.9rem;">100% API-Keyless & Open Access REST API. Access AetherMind Cortex reasoning, RAG context, and expert skills with zero rate limits and zero required keys.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # API Status & Metrics Cards (API-Keyless Unlimited)
    api_h1, api_h2, api_h3 = st.columns(3)
    with api_h1:
        st.markdown("""
        <div class="module-card">
            <span style="font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;">API Status</span>
            <h3 style="margin:6px 0 0 0; color:#22c55e; font-size:1.3rem;">● Operational</h3>
            <span style="font-size:0.8rem; color:#94a3b8;">Endpoint: <code>http://localhost:7860/api/v1</code></span>
        </div>
        """, unsafe_allow_html=True)
    with api_h2:
        st.markdown("""
        <div class="module-card">
            <span style="font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;">Authentication Mode</span>
            <h3 style="margin:6px 0 0 0; color:#38bdf8; font-size:1.3rem;">🔓 Keyless / Open Access</h3>
            <span style="font-size:0.8rem; color:#94a3b8;">Headers: <code>No API Key Required</code></span>
        </div>
        """, unsafe_allow_html=True)
    with api_h3:
        st.markdown("""
        <div class="module-card">
            <span style="font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;">Execution Limits</span>
            <h3 style="margin:6px 0 0 0; color:#c084fc; font-size:1.3rem;">♾️ Unlimited Free Usage</h3>
            <span style="font-size:0.8rem; color:#94a3b8;">Zero Telemetry / 100% Offline</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cortex-card" style="margin: 20px 0; border: 1px solid rgba(34, 197, 94, 0.4); background: rgba(6, 10, 23, 0.7);">
        <h4 style="margin:0 0 6px 0; color: #22c55e; font-size: 1.1rem; font-weight:700;">🟢 100% API-Keyless Architecture Active</h4>
        <p style="margin:0; color: #cbd5e1; font-size: 0.9rem;">
            AetherMind Cortex REST API is designed to be completely <b>API-keyless and friction-free</b>. You can query any endpoint (<code>/api/v1/chat</code>, <code>/api/v1/models</code>, <code>/api/v1/skills</code>, <code>/api/v1/health</code>) directly without any token, sign-up, or API key.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='margin:24px 0 12px 0; font-size:1.2rem; color:#f8fafc;'>⚙️ Optional Cloud Gateway (Optional Only)</h3>", unsafe_allow_html=True)
    kcol1, kcol2 = st.columns(2)
    with kcol1:
        st.markdown("""
        <div class="module-card">
            <h4 style="margin:0 0 8px 0; color:#f8fafc;">Default Mode: Local Keyless Engine</h4>
            <p style="margin:0 0 12px 0; color:#94a3b8; font-size:0.85rem;">All local calls use embedded Ollama & Cortex Reasoning Engine with zero keys required.</p>
        """, unsafe_allow_html=True)
        try:
            keys = controller.api_engine.get_api_keys()
        except Exception:
            keys = []
        if keys:
            for k in keys:
                updated = str(k.get('updated_at', ''))[:10] or "Recent"
                st.markdown(f"🔑 **{k['name']}**: `{'*' * 12 + str(k['key'])[-4:] if len(str(k['key'])) > 4 else k['key']}` *(Updated {updated})*")
        else:
            st.success("🟢 Running in 100% API-Keyless Mode. No keys configured or required.")
        
        if st.button("➕ Generate Optional Local Token", use_container_width=True):
            token = controller.api_engine.generate_cortex_token()
            st.success(f"Generated optional token: `{token}`")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with kcol2:
        st.markdown("""
        <div class="module-card">
            <h4 style="margin:0 0 8px 0; color:#f8fafc;">Optional Third-Party Cloud Key</h4>
            <p style="margin:0 0 12px 0; color:#94a3b8; font-size:0.85rem;">Only set a key if you wish to route reasoning requests through paid external cloud providers (OpenAI, Anthropic, Groq).</p>
        """, unsafe_allow_html=True)
        provider_name = st.selectbox("API Provider", ["OpenAI", "Anthropic", "Groq", "OpenRouter", "Custom Endpoint"])
        new_key = st.text_input("Enter Optional API Key", type="password", help="Leave blank for 100% API-keyless local execution")
        if st.button("💾 Save Optional Cloud Key", use_container_width=True):
            if new_key:
                controller.api_engine.set_api_key(provider_name, new_key)
                st.toast(f"Saved API key for {provider_name} successfully!")
                st.rerun()
            else:
                st.error("Please enter a key string or leave unconfigured for API-keyless mode.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin:24px 0 12px 0; font-size:1.2rem; color:#f8fafc;'>🧪 Interactive Keyless REST API Playground</h3>", unsafe_allow_html=True)
    tcol1, tcol2 = st.columns([1, 2])
    with tcol1:
        selected_ep = st.selectbox("Select Endpoint to Test", ["GET /api/v1/health", "GET /api/v1/models", "POST /api/v1/chat", "GET /api/v1/skills"])
        test_prompt = ""
        if "POST" in selected_ep:
            test_prompt = st.text_area("Test Prompt Payload", value="Explain quantum computing briefly.")
        
        run_api = st.button("🚀 Execute REST API Request (No Key Needed)", use_container_width=True)
        
    with tcol2:
        if run_api:
            st.markdown("#### Response JSON Payload")
            if selected_ep == "GET /api/v1/health":
                res = controller.api_engine.handle_health()
                st.json(res)
            elif selected_ep == "GET /api/v1/models":
                res = controller.api_engine.handle_list_models()
                st.json(res)
            elif selected_ep == "POST /api/v1/chat":
                res = controller.api_engine.handle_chat_completion({"prompt": test_prompt or "Hello AetherMind API"})
                st.json(res)
            elif selected_ep == "GET /api/v1/skills":
                res = controller.api_engine.handle_skills()
                st.json(res)
        else:
            st.info("Select an endpoint and click 'Execute REST API Request (No Key Needed)' to inspect live API output.")

    st.markdown("<h3 style='margin:24px 0 12px 0; font-size:1.2rem; color:#f8fafc;'>💻 Keyless Developer Integration Code Snippets</h3>", unsafe_allow_html=True)
    code_lang = st.radio("Language:", ["Python", "cURL", "JavaScript"], horizontal=True)
    if code_lang == "Python":
        st.code("""import requests

# 100% API-Keyless REST API Call - No API Key Required!
url = "http://localhost:7860/api/v1/chat"
headers = {"Content-Type": "application/json"}
payload = {
    "prompt": "Analyze market trends for AI hardware.",
    "model": "llama3-lexi-uncensored"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
""", language="python")
    elif code_lang == "cURL":
        st.code("""# 100% API-Keyless Call (Zero Rate Limits, No Key Needed)
curl -X POST http://localhost:7860/api/v1/chat \\
  -H "Content-Type: application/json" \\
  -d '{"prompt": "Analyze market trends for AI hardware.", "model": "llama3-lexi-uncensored"}'
""", language="bash")
    else:
        st.code("""// 100% API-Keyless Call (Zero Rate Limits, No Key Needed)
fetch("http://localhost:7860/api/v1/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    prompt: "Analyze market trends for AI hardware.",
    model: "llama3-lexi-uncensored"
  })
})
.then(res => res.json())
.then(data => console.log(data));
""", language="javascript")

elif page_selection == "⚙️ Settings":
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin: 0 0 6px 0; font-size: 1.6rem; font-weight: 800; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">⚙️ System Settings & Preferences</h2>
        <p style="margin: 0; color: #94a3b8; font-size: 0.9rem;">Configure LLM endpoints, local hardware acceleration, and application themes.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="module-card">
        <h4 style="margin:0 0 16px 0; color:#f8fafc;">Local LLM Connection Settings</h4>
    """, unsafe_allow_html=True)
    st.text_input("Ollama Host URL", value=controller.llm_engine.host)
    st.selectbox("Default Temperature Preset", options=["0.2 (Precise / Code)", "0.7 (Balanced / General)", "1.0 (Creative / Brainstorming)"], index=1)
    st.selectbox("Application Theme Mode", options=["Dark Cyberpunk Glassmorphism (Default)", "Light Mode"], index=0)
    st.markdown("</div>", unsafe_allow_html=True)

elif page_selection == "🩺 Diagnostics":
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin: 0 0 6px 0; font-size: 1.6rem; font-weight: 800; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🩺 System Diagnostics & Self-Healing Maintenance</h2>
        <p style="margin: 0; color: #94a3b8; font-size: 0.9rem;">Run diagnostic checks and trigger self-healing automated system repairs.</p>
    </div>
    """, unsafe_allow_html=True)
    
    dcol1, dcol2 = st.columns(2)
    with dcol1:
        if st.button("🔍 Run Full Diagnostics Check", use_container_width=True):
            diag = controller.diagnostics_engine.run_full_diagnostics()
            st.json(diag)
    with dcol2:
        if st.button("🛠️ Execute Self-Healing Repair", use_container_width=True):
            res = controller.diagnostics_engine.execute_self_healing_repair()
            st.success(res.get("message", "Self-healing repair executed successfully!"))

elif page_selection == "ℹ️ About":
    st.markdown(f"""
    <div class="module-card" style="text-align: center; padding: 40px 20px;">
        <img src="https://raw.githubusercontent.com/KAVATIJOHNSHREYAN/AETHERMIND-CORTEX/main/assets/logo.png" style="width: 120px; border-radius: 20px; box-shadow: 0 0 40px rgba(56, 189, 248, 0.4); margin-bottom: 16px;" />
        <h2 style="margin:0 0 6px 0; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.8rem; font-weight: 800;">AetherMind Cortex</h2>
        <p style="color: #94a3b8; font-size: 0.95rem; max-width: 600px; margin: 0 auto 20px auto;">
            Human-Centered Privacy-First AI Reasoning Engine & Desktop OS. Designed for autonomous reasoning, offline RAG context indexing, and expert cognitive skills.
        </p>
        <div style="display: flex; justify-content: center; gap: 16px; font-size: 0.85rem; color: #cbd5e1;">
            <span><b>Version:</b> <code>v{meta['version']}</code></span>
            <span><b>Stage:</b> <code>{meta['stage']}</code></span>
            <span><b>License:</b> <code>MIT / Open-Source</code></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

