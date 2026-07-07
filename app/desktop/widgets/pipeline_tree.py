from typing import Any

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


class PipelineTree(QTreeWidget):
    """Tree widget that displays pipeline steps."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setHeaderLabel("Pipeline")
        self.refresh([])

    def refresh(self, steps: list[dict[str, Any]]) -> None:
        self.clear()

        root = QTreeWidgetItem(["Pipeline"])
        self.addTopLevelItem(root)

        for index, step in enumerate(steps, start=1):
            name = step.get("name") or step.get("type") or f"Step {index}"
            step_type = step.get("type", "unknown")
            item = QTreeWidgetItem([f"{index}. {name} [{step_type}]"])
            root.addChild(item)

        self.expandAll()