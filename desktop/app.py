"""
ProgTrain Desktop — PySide6 application shell with embedded web UI.

Launches a native desktop window containing a QWebEngineView that loads
the Flask-served web frontend.  The Flask API server runs in a background
thread inside the same process.

Usage:
    python3 -m desktop.app          # default
    python3 -m desktop.app --port 8080
"""
from __future__ import annotations

import argparse
import os
import sys
import time

# Ensure repo root is on the path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def main() -> None:
    parser = argparse.ArgumentParser(description="ProgTrain Desktop")
    parser.add_argument("--port", type=int, default=44556)
    args = parser.parse_args()

    # Import Qt AFTER path setup
    from PySide6.QtCore import QUrl, Qt
    from PySide6.QtGui import QIcon
    from PySide6.QtWidgets import QApplication, QMainWindow
    from PySide6.QtWebEngineWidgets import QWebEngineView

    # Start the API server in a background thread
    from desktop.server import start_server
    base_url = start_server(port=args.port)

    # Give the server a moment to start
    time.sleep(0.5)

    # Create Qt application
    qt_app = QApplication(sys.argv)
    qt_app.setApplicationName("ProgTrain")
    qt_app.setApplicationDisplayName("ProgTrain — Programátorské Tréninkové Centrum")
    qt_app.setOrganizationName("ProgTrain")

    # Main window
    window = QMainWindow()
    window.setWindowTitle("ProgTrain — Programátorské Tréninkové Centrum")
    window.setMinimumSize(1200, 800)
    window.resize(1400, 900)

    # Web view
    web_view = QWebEngineView()
    web_view.setUrl(QUrl(base_url))
    window.setCentralWidget(web_view)

    window.show()
    sys.exit(qt_app.exec())


if __name__ == "__main__":
    main()
