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
}

.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
}

.sidebar-panel {
    background: rgba(30, 41, 59, 0.7) !important;
    backdrop-filter: blur(12px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    padding: 1.5rem !important;
    border-radius: 12px !important;
}

.card-panel {
    background: rgba(30, 41, 59, 0.5) !important;
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

.aether-header h1 {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    letter-spacing: -0.02em;
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
