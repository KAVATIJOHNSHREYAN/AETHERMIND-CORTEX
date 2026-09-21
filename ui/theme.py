"""
AetherMind Cortex UI Theme & Custom CSS Definitions
Applies modern glassmorphism styling and dark/light mode themes for Gradio.
"""

import gradio as gr

CUSTOM_CSS = """
/* AetherMind Cortex Glassmorphism & Cyberpunk Theme */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');

:root {
    --bg-primary: #0b0f19;
    --bg-card: rgba(18, 24, 38, 0.75);
    --border-color: rgba(56, 189, 248, 0.15);
    --accent-cyan: #38bdf8;
    --accent-indigo: #818cf8;
    --accent-purple: #c084fc;
    --text-primary: #f8fafc;
    --text-muted: #94a3b8;
}

body, html, .gradio-container {
    background-color: #0b0f19 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-primary) !important;
}

.gradio-container {
    max-width: 1440px !important;
    margin: 0 auto !important;
    padding: 1rem !important;
}

/* Background Heartbeat Watermark */
.aether-watermark {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 600px;
    height: 600px;
    max-width: 80vw;
    max-height: 80vh;
    background-image: url('/file=assets/logo.png');
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    opacity: 0.04;
    pointer-events: none;
    z-index: 0;
    will-change: transform, opacity;
    animation: cortexHeartbeat 3s ease-in-out infinite;
}

@keyframes cortexHeartbeat {
    0%, 100% {
        transform: translate(-50%, -50%) scale(1);
        opacity: 0.04;
    }
    50% {
        transform: translate(-50%, -50%) scale(1.03);
        opacity: 0.065;
        filter: drop-shadow(0 0 30px rgba(56, 189, 248, 0.3));
    }
}

/* Sidebar Styling */
.sidebar-panel {
    background: var(--bg-card) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 16px !important;
    padding: 1.25rem !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
}

/* Card Containers */
.card-panel, div[data-testid="block"] {
    background: var(--bg-card) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
}

/* Header Component */
.aether-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px 18px;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.7) 100%);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    margin-bottom: 1.2rem;
}

.aether-header-logo {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
}

.aether-header h1 {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    font-size: 1.6rem;
    margin: 0;
}

/* Buttons */
button.primary, button.lg.primary {
    background: linear-gradient(135deg, #0284c7 0%, #6366f1 100%) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(2, 132, 199, 0.3) !important;
}

button.primary:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(2, 132, 199, 0.5) !important;
}

button.secondary {
    background: rgba(30, 41, 59, 0.8) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

button.secondary:hover {
    background: rgba(51, 65, 85, 0.9) !important;
    border-color: rgba(56, 189, 248, 0.4) !important;
}

/* Text Inputs & Dropdowns */
textarea, input[type="text"], select, .gr-dropdown {
    background: rgba(15, 23, 42, 0.8) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
}

textarea:focus, input[type="text"]:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.2) !important;
}

/* Tab Navigation */
.tabs button.selected {
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.2) 0%, rgba(129, 140, 248, 0.2) 100%) !important;
    color: var(--accent-cyan) !important;
    border-bottom: 2px solid var(--accent-cyan) !important;
    font-weight: 600 !important;
}

/* Status Bar */
.status-bar-box {
    background: rgba(11, 15, 25, 0.95) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.2rem !important;
    margin-top: 1rem !important;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.6);
}
::-webkit-scrollbar-thumb {
    background: rgba(56, 189, 248, 0.3);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(56, 189, 248, 0.6);
}
"""

def get_theme(theme_name: str = "dark") -> gr.Theme:
    """Returns configured Gradio theme instance."""
    if theme_name == "light":
        return gr.themes.Soft(
            primary_hue="indigo",
            secondary_hue="blue",
            neutral_hue="slate"
        )
    return gr.themes.Default(
        primary_hue="cyan",
        secondary_hue="indigo",
        neutral_hue="slate"
    )
