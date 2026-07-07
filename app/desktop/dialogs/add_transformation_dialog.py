from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
)


class AddTransformationDialog(QDialog):
    """Dialog used to add a transformation step to the pipeline."""

    def __init__(self, columns: list[str], parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Agregar Transformación")
        self.resize(420, 180)

        self.transformation_type = QComboBox()
        self.transformation_type.addItems(
            [
                "rename_columns",
                "filter_rows",
                "select_columns",
                "drop_columns",
            ]
        )

        self.source_column = QComboBox()
        self.source_column.addItems(columns)

        self.target_value = QLineEdit()
        self.target_value.setPlaceholderText(
            "Nuevo nombre, expresión filtro o columnas separadas por coma"
        )

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        layout = QFormLayout(self)
        layout.addRow("Transformación:", self.transformation_type)
        layout.addRow("Columna:", self.source_column)
        layout.addRow("Valor:", self.target_value)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_step(self) -> dict:
        step_type = self.transformation_type.currentText()
        column = self.source_column.currentText()
        value = self.target_value.text().strip()

        if step_type == "rename_columns":
            return {
                "type": "rename_columns",
                "name": "Rename Columns",
                "config": {
                    "columns": {
                        column: value,
                    }
                },
            }

        if step_type == "filter_rows":
            return {
                "type": "filter_rows",
                "name": "Filter Rows",
                "config": {
                    "expression": value,
                },
            }

        if step_type == "select_columns":
            return {
                "type": "select_columns",
                "name": "Select Columns",
                "config": {
                    "columns": [item.strip() for item in value.split(",") if item.strip()],
                },
            }

        if step_type == "drop_columns":
            return {
                "type": "drop_columns",
                "name": "Drop Columns",
                "config": {
                    "columns": [item.strip() for item in value.split(",") if item.strip()],
                },
            }

        raise ValueError(f"Unsupported transformation type: {step_type}")