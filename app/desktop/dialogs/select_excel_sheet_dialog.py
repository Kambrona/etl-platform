from PySide6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout


class SelectExcelSheetDialog(QDialog):
    """Dialog to select an Excel sheet."""

    def __init__(self, sheets: list[str], parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Seleccionar hoja de Excel")
        self.resize(420, 120)

        self.sheet_combo = QComboBox()
        self.sheet_combo.addItems(sheets)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        layout = QFormLayout(self)
        layout.addRow("Hoja:", self.sheet_combo)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def selected_sheet(self) -> str:
        return self.sheet_combo.currentText()
