from typing import Any

from PySide6.QtWidgets import QFormLayout, QLabel, QWidget


class PropertiesPanel(QWidget):
    """Panel that displays selected pipeline or project properties."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.layout = QFormLayout(self)

        self.pipeline_name = QLabel("-")
        self.source_path = QLabel("-")
        self.output_path = QLabel("-")
        self.steps_count = QLabel("0")

        self.layout.addRow("Pipeline:", self.pipeline_name)
        self.layout.addRow("Fuente:", self.source_path)
        self.layout.addRow("Salida:", self.output_path)
        self.layout.addRow("Pasos:", self.steps_count)

    def update_properties(self, data: dict[str, Any]) -> None:
        self.pipeline_name.setText(str(data.get("pipeline_name", "-")))
        self.source_path.setText(str(data.get("source_path", "-")))
        self.output_path.setText(str(data.get("output_path", "-")))
        self.steps_count.setText(str(data.get("steps_count", 0)))