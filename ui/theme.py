"""
AetherMind Cortex UI Theme & Custom CSS Definitions
Applies modern glassmorphism styling and dark/light mode themes for Gradio.
"""

import gradio as gr

CUSTOM_CSS = """
/* AetherMind Cortex Cyberpunk Glassmorphism Theme (Match Exact Mockup UI) */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');

:root {
    --bg-dark: #05070e;
    --bg-sidebar: #090e1a;
    --bg-card: rgba(13, 20, 36, 0.85);
    --bg-card-hover: rgba(22, 33, 58, 0.95);
    --border-glow: rgba(56, 189, 248, 0.25);
    --border-accent: rgba(129, 140, 248, 0.4);
    --gradient-btn: linear-gradient(135deg, #0284c7 0%, #6366f1 50%, #a855f7 100%);
    --gradient-glow: linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%);
}

body, html, .gradio-container {
    background-color: var(--bg-dark) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #f8fafc !important;
}

.gradio-container {
    max-width: 1560px !important;
    margin: 0 auto !important;
    padding: 0.75rem !important;
}

/* Background Heartbeat Watermark */
.aether-watermark {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 650px;
    height: 650px;
    max-width: 85vw;
    max-height: 85vh;
    background-image: url('/file=assets/logo.png');
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    opacity: 0.045;
    pointer-events: none;
    z-index: 0;
    will-change: transform, opacity;
    animation: cortexHeartbeat 2.8s ease-in-out infinite;
}

@keyframes cortexHeartbeat {
    0%, 100% {
        transform: translate(-50%, -50%) scale(1);
        opacity: 0.045;
    }
    50% {
        transform: translate(-50%, -50%) scale(1.035);
        opacity: 0.07;
        filter: drop-shadow(0 0 35px rgba(56, 189, 248, 0.4));
    }
}

/* Sidebar Container */
.sidebar-panel {
    background: var(--bg-sidebar) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 18px !important;
    padding: 1.25rem !important;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.6) !important;
}

/* Workspace Panels & Blocks */
.card-panel, div[data-testid="block"] {
    background: var(--bg-card) !important;
    backdrop-filter: blur(14px) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 16px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
}

/* Top App Header Bar */
.aether-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 24px;
    background: linear-gradient(135deg, #090e1a 0%, #111827 100%);
    border: 1px solid var(--border-glow);
    border-radius: 18px;
    margin-bottom: 1rem;
    box-shadow: 0 0 25px rgba(56, 189, 248, 0.15);
}

.aether-header-logo {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
}

/* Primary Action Buttons */
button.primary, button.lg.primary {
    background: var(--gradient-btn) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(56, 189, 248, 0.35) !important;
}

button.primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(168, 85, 247, 0.5) !important;
}

/* Secondary Buttons */
button.secondary {
    background: rgba(17, 24, 39, 0.9) !important;
    color: #f8fafc !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

button.secondary:hover {
    background: rgba(30, 41, 59, 0.95) !important;
    border-color: rgba(56, 189, 248, 0.5) !important;
}

/* Text Inputs & Textarea */
textarea, input[type="text"], select, .gr-dropdown {
    background: rgba(9, 14, 26, 0.95) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(56, 189, 248, 0.2) !important;
    border-radius: 12px !important;
}

textarea:focus, input[type="text"]:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.3) !important;
}

/* Tab Navigation */
.tabs button {
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s ease !important;
}

.tabs button.selected {
    background: var(--gradient-glow) !important;
    color: #38bdf8 !important;
    border: 1px solid var(--border-accent) !important;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.2) !important;
}

/* Chat Component Hero Banner Card */
.chat-hero-banner {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%);
    border: 1px solid var(--border-glow);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    text-align: center;
}

/* Custom Quick Action Pill Buttons */
.quick-action-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 20px;
    font-size: 0.85rem;
    color: #f8fafc;
    cursor: pointer;
    transition: all 0.2s ease;
}

.quick-action-pill:hover {
    background: rgba(56, 189, 248, 0.15);
    border-color: #38bdf8;
    transform: translateY(-1px);
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
