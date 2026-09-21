"""
AetherMind Cortex Entrypoint Launcher
Initializes controller, logs startup parameters, and starts Gradio Web Server.
"""

import sys
import os
import argparse

# Add root directory to sys.path to enable clean package imports
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.controller import AppController
from core.logger import get_logger
from ui.layout import build_ui

logger = get_logger("Main")

def parse_args():
    parser = argparse.ArgumentParser(description="AetherMind Cortex - Human-Centered AI Reasoning Engine")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host IP to bind web server")
    parser.add_argument("--port", type=int, default=7860, help="Port to run web server")
    parser.add_argument("--share", action="store_true", help="Create public Gradio link")
    return parser.parse_args()

def main():
    args = parse_args()
    logger.info("Starting AetherMind Cortex Phase 1...")
    
    # Initialize Central App Controller
    controller = AppController()
    status = controller.get_system_status()
    logger.info(f"System initialized: {status['app_name']} v{status['version']} [State: {status['status']}]")
    
    # Build Gradio UI
    app = build_ui(controller)
    
    host = args.host or controller.config_manager.config.ui.server_name
    port = args.port or controller.config_manager.config.ui.server_port
    
    logger.info(f"Launching Gradio interface at http://{host}:{port}")
    app.launch(
        server_name=host,
        server_port=port,
        share=args.share
    )

if __name__ == "__main__":
    main()
