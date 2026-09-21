"""
Native PySide6 Desktop GUI Window Launcher for AetherMind Cortex
Embeds Gradio Web UI inside a native desktop window container with system tray support.
"""

import sys
import threading
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon

def launch_gradio_background():
    from main import main
    main()

def main_desktop():
    # Start Gradio Web Server in background thread
    t = threading.Thread(target=launch_gradio_background, daemon=True)
    t.start()
    time.sleep(3)  # Wait for server startup

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("AetherMind Cortex - Native Desktop Experience")
    window.resize(1400, 900)

    browser = QWebEngineView()
    browser.setUrl(QUrl("http://127.0.0.1:7860"))
    window.setCentralWidget(browser)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main_desktop()
