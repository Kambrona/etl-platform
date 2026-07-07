import sys

from PySide6.QtWidgets import QApplication

from app.desktop.main_window import MainWindow


def run_desktop_app() -> None:
    """Start the desktop ETL application."""
    app = QApplication(sys.argv)

    app.setApplicationName("ETL Platform Desktop")
    app.setOrganizationName("ETL Platform")

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())