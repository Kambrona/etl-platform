from datetime import datetime

from PySide6.QtWidgets import QTextEdit


class LogsPanel(QTextEdit):
    """Read-only log panel for desktop events."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setReadOnly(True)

    def log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.append(f"[{timestamp}] {message}")