from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QListWidget,
    QListWidgetItem,
)


class AddDataSourceDialog(QDialog):
    """Dialog to select the data source type."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Agregar fuente de datos")
        self.resize(420, 260)

        self.source_types = QListWidget()

        for label, value in [
            ("CSV", "csv"),
            ("Excel", "excel"),
            ("Parquet", "parquet"),
            ("Base de datos - próximamente", "database"),
            ("API REST - próximamente", "api"),
        ]:
            item = QListWidgetItem(label)
            item.setData(1000, value)

            if value in {"database", "api"}:
                item.setFlags(item.flags() & ~item.flags().ItemIsEnabled)

            self.source_types.addItem(item)

        self.source_types.setCurrentRow(0)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        layout = QFormLayout(self)
        layout.addRow("Tipo:", self.source_types)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def selected_source_type(self) -> str:
        item = self.source_types.currentItem()

        if item is None:
            return "csv"

        return item.data(1000)
