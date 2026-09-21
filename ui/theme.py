"""
AetherMind Cortex UI Theme & Custom CSS Definitions
Applies modern glassmorphism styling and dark/light mode themes for Gradio.
"""

import gradio as gr

CUSTOM_CSS = """
/* AetherMind Cortex Glassmorphism Theme CSS */
body {
    background-color: #0f172a;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    position: relative;
    overflow-x: hidden;
}

.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
    position: relative;
    z-index: 1;
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
    opacity: 0.05;
    pointer-events: none;
    z-index: 0;
    will-change: transform, opacity, filter;
    animation: cortexHeartbeat 2.8s ease-in-out infinite;
}

@keyframes cortexHeartbeat {
    0% {
        transform: translate(-50%, -50%) scale(1);
        opacity: 0.05;
        filter: drop-shadow(0 0 0px rgba(56, 189, 248, 0));
    }
    35% {
        transform: translate(-50%, -50%) scale(1.03);
        opacity: 0.06;
        filter: drop-shadow(0 0 25px rgba(56, 189, 248, 0.4));
    }
    70% {
        transform: translate(-50%, -50%) scale(1.008);
        opacity: 0.052;
        filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.15));
    }
    100% {
        transform: translate(-50%, -50%) scale(1);
        opacity: 0.05;
        filter: drop-shadow(0 0 0px rgba(56, 189, 248, 0));
    }
}

.sidebar-panel {
    background: rgba(30, 41, 59, 0.75) !important;
    backdrop-filter: blur(12px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    padding: 1.5rem !important;
    border-radius: 12px !important;
}

.card-panel {
    background: rgba(30, 41, 59, 0.55) !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
    margin-bottom: 1rem !important;
}

.status-bar-box {
    background: rgba(15, 23, 42, 0.9) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
    padding: 0.5rem 1rem !important;
    font-size: 0.85rem !important;
}

.aether-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 10px 0;
}

.aether-header-logo {
    width: 48px;
    height: 48px;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
    object-fit: cover;
}

.aether-header h1 {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0;
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
