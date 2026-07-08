from typing import Any

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


STEP_INDEX_ROLE = 1001


class PipelineTree(QTreeWidget):
    """Tree widget that displays query transformation steps."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setHeaderLabel("Transformaciones")
        self.refresh([])

    def refresh(self, steps: list[dict[str, Any]]) -> None:
        self.clear()

        root = QTreeWidgetItem(["Consulta activa"])
        self.addTopLevelItem(root)

        for index, step in enumerate(steps):
            label_number = index + 1
            name = step.get("name") or step.get("type") or f"Step {label_number}"
            step_type = step.get("type", "unknown")

            item = QTreeWidgetItem([f"{label_number}. {name} [{step_type}]"])
            item.setData(0, STEP_INDEX_ROLE, index)
            root.addChild(item)

        self.expandAll()
