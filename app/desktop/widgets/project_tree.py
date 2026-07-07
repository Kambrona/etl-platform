from pathlib import Path

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


class ProjectTree(QTreeWidget):
    """Tree widget that displays project-level resources."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setHeaderLabel("Proyecto")
        self.refresh(None)

    def refresh(self, source_path: Path | None) -> None:
        self.clear()

        root = QTreeWidgetItem(["Proyecto ETL"])
        self.addTopLevelItem(root)

        sources = QTreeWidgetItem(["Fuentes"])
        pipelines = QTreeWidgetItem(["Pipelines"])
        outputs = QTreeWidgetItem(["Outputs"])

        root.addChild(sources)
        root.addChild(pipelines)
        root.addChild(outputs)

        if source_path:
            sources.addChild(QTreeWidgetItem([source_path.name]))

        self.expandAll()