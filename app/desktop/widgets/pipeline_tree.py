from typing import Any

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QMenu, QTreeWidget, QTreeWidgetItem


STEP_INDEX_ROLE = 1001


class PipelineTree(QTreeWidget):
    """Tree widget that displays query transformation steps."""

    preview_step_requested = Signal(int)
    insert_after_step_requested = Signal(int)
    delete_step_requested = Signal(int)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setHeaderLabel("Transformaciones")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._open_context_menu)
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

    def _open_context_menu(self, position) -> None:
        item = self.itemAt(position)

        if item is None:
            return

        step_index = item.data(0, STEP_INDEX_ROLE)

        if step_index is None:
            return

        menu = QMenu(self)

        preview_action = menu.addAction("Ver datos hasta aquí")
        insert_action = menu.addAction("Insertar transformación después")
        delete_action = menu.addAction("Eliminar paso")

        if step_index == 0:
            delete_action.setEnabled(False)

        selected_action = menu.exec(self.viewport().mapToGlobal(position))

        if selected_action == preview_action:
            self.preview_step_requested.emit(step_index)

        elif selected_action == insert_action:
            self.insert_after_step_requested.emit(step_index)

        elif selected_action == delete_action:
            self.delete_step_requested.emit(step_index)
