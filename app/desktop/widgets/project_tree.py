from app.desktop.models.workspace_state import WorkspaceState

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


SOURCE_NAME_ROLE = 1002


class ProjectTree(QTreeWidget):
    """Tree widget that displays workspace resources."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setHeaderLabel("Proyecto")
        self.refresh_workspace(None)

    def refresh_workspace(self, workspace: WorkspaceState | None) -> None:
        self.clear()

        project_name = workspace.project_name if workspace else "Proyecto ETL"

        root = QTreeWidgetItem([project_name])
        self.addTopLevelItem(root)

        sources = QTreeWidgetItem(["Fuentes de datos"])
        queries = QTreeWidgetItem(["Consultas"])
        outputs = QTreeWidgetItem(["Resultados"])

        root.addChild(sources)
        root.addChild(queries)
        root.addChild(outputs)

        if workspace:
            for source in workspace.data_sources:
                item = QTreeWidgetItem([source.display_name])
                item.setData(0, SOURCE_NAME_ROLE, source.name)
                sources.addChild(item)

            active_query = workspace.active_query

            if active_query.pipeline_name:
                queries.addChild(QTreeWidgetItem([active_query.pipeline_name]))

            if active_query.output_path:
                outputs.addChild(QTreeWidgetItem([active_query.output_path.name]))

        self.expandAll()
