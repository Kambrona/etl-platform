from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QSpinBox,
)


class AddTransformationDialog(QDialog):
    """Dialog used to add a transformation step to the query."""

    def __init__(
        self,
        columns: list[str],
        parent=None,
        forced_step_type: str | None = None,
    ) -> None:
        super().__init__(parent)

        self.columns = columns

        self.setWindowTitle("Agregar Transformacion")
        self.resize(580, 420)

        self.transformation_type = QComboBox()
        self.transformation_type.addItems(
            [
                "rename_columns",
                "filter_rows",
                "select_columns",
                "drop_columns",
                "sort_rows",
                "remove_duplicates",
                "limit_rows",
                "uppercase",
                "lowercase",
                "trim",
            ]
        )

        self.column_label = QLabel("Columna:")
        self.source_column = QComboBox()
        self.source_column.addItems(columns)

        self.operator_label = QLabel("Operador:")
        self.operator = QComboBox()
        self.operator.addItems(["=", "!=", ">", ">=", "<", "<=", "contains"])

        self.value_label = QLabel("Valor:")
        self.target_value = QLineEdit()

        self.sort_descending = QCheckBox("Orden descendente")

        self.limit_label = QLabel("Cantidad:")
        self.limit_rows = QSpinBox()
        self.limit_rows.setMinimum(1)
        self.limit_rows.setMaximum(10000000)
        self.limit_rows.setValue(100)

        self.columns_label = QLabel("Columnas:")
        self.columns_list = QListWidget()
        self.columns_list.setSelectionMode(QListWidget.MultiSelection)

        for column in columns:
            self.columns_list.addItem(QListWidgetItem(column))

        self.help_label = QLabel("")
        self.help_label.setWordWrap(True)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.layout = QFormLayout(self)
        self.layout.addRow("Transformacion:", self.transformation_type)
        self.layout.addRow(self.column_label, self.source_column)
        self.layout.addRow(self.operator_label, self.operator)
        self.layout.addRow(self.value_label, self.target_value)
        self.layout.addRow("", self.sort_descending)
        self.layout.addRow(self.limit_label, self.limit_rows)
        self.layout.addRow(self.columns_label, self.columns_list)
        self.layout.addRow("Ayuda:", self.help_label)
        self.layout.addWidget(self.buttons)

        if forced_step_type:
            index = self.transformation_type.findText(forced_step_type)
            if index >= 0:
                self.transformation_type.setCurrentIndex(index)
                self.transformation_type.setEnabled(False)

        self.transformation_type.currentTextChanged.connect(self._refresh_form)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self._refresh_form()

    def _refresh_form(self) -> None:
        step_type = self.transformation_type.currentText()

        self.column_label.setVisible(False)
        self.source_column.setVisible(False)
        self.operator_label.setVisible(False)
        self.operator.setVisible(False)
        self.value_label.setVisible(False)
        self.target_value.setVisible(False)
        self.sort_descending.setVisible(False)
        self.limit_label.setVisible(False)
        self.limit_rows.setVisible(False)
        self.columns_label.setVisible(False)
        self.columns_list.setVisible(False)

        if step_type == "rename_columns":
            self.column_label.setVisible(True)
            self.source_column.setVisible(True)
            self.value_label.setVisible(True)
            self.target_value.setVisible(True)
            self.value_label.setText("Nuevo nombre:")
            self.target_value.setPlaceholderText("Ejemplo: TotalVentas")
            self.help_label.setText("Selecciona una columna y escribe el nuevo nombre.")

        elif step_type == "filter_rows":
            self.column_label.setVisible(True)
            self.source_column.setVisible(True)
            self.operator_label.setVisible(True)
            self.operator.setVisible(True)
            self.value_label.setVisible(True)
            self.target_value.setVisible(True)
            self.value_label.setText("Valor:")
            self.target_value.setPlaceholderText("Ejemplo: 2024 o Enero")
            self.help_label.setText("Construye un filtro sin escribir la columna manualmente.")

        elif step_type in {"select_columns", "drop_columns", "remove_duplicates"}:
            self.columns_label.setVisible(True)
            self.columns_list.setVisible(True)

            if step_type == "select_columns":
                self.help_label.setText("Selecciona las columnas que quieres conservar.")
            elif step_type == "drop_columns":
                self.help_label.setText("Selecciona las columnas que quieres eliminar.")
            else:
                self.help_label.setText("Selecciona columnas para detectar duplicados. Si no seleccionas ninguna, se usa toda la fila.")

        elif step_type == "sort_rows":
            self.column_label.setVisible(True)
            self.source_column.setVisible(True)
            self.sort_descending.setVisible(True)
            self.help_label.setText("Ordena la consulta por la columna seleccionada.")

        elif step_type == "limit_rows":
            self.limit_label.setVisible(True)
            self.limit_rows.setVisible(True)
            self.help_label.setText("Conserva solo las primeras N filas.")

        elif step_type in {"uppercase", "lowercase", "trim"}:
            self.column_label.setVisible(True)
            self.source_column.setVisible(True)

            if step_type == "uppercase":
                self.help_label.setText("Convierte la columna seleccionada a mayusculas.")
            elif step_type == "lowercase":
                self.help_label.setText("Convierte la columna seleccionada a minusculas.")
            else:
                self.help_label.setText("Elimina espacios al inicio y final de la columna seleccionada.")

    def _selected_columns(self) -> list[str]:
        return [item.text() for item in self.columns_list.selectedItems()]

    def _build_filter_expression(self) -> str:
        column = self.source_column.currentText()
        operator = self.operator.currentText()
        value = self.target_value.text().strip()

        if not value:
            raise ValueError("Debes escribir un valor para el filtro.")

        if value.replace(".", "", 1).isdigit():
            formatted_value = value
        else:
            formatted_value = f"'{value}'"

        if operator == "contains":
            return f'CAST("{column}" AS TEXT) LIKE ''%{value}%'''

        return f'"{column}" {operator} {formatted_value}'

    def get_step(self) -> dict:
        step_type = self.transformation_type.currentText()
        column = self.source_column.currentText()
        value = self.target_value.text().strip()

        if step_type == "rename_columns":
            return {
                "type": "rename_columns",
                "name": "Rename Columns",
                "config": {"columns": {column: value}},
            }

        if step_type == "filter_rows":
            return {
                "type": "filter_rows",
                "name": "Filter Rows",
                "config": {"expression": self._build_filter_expression()},
            }

        if step_type == "select_columns":
            return {
                "type": "select_columns",
                "name": "Select Columns",
                "config": {"columns": self._selected_columns()},
            }

        if step_type == "drop_columns":
            return {
                "type": "drop_columns",
                "name": "Drop Columns",
                "config": {"columns": self._selected_columns()},
            }

        if step_type == "sort_rows":
            return {
                "type": "sort_rows",
                "name": "Sort Rows",
                "config": {
                    "column": column,
                    "descending": self.sort_descending.isChecked(),
                },
            }

        if step_type == "remove_duplicates":
            return {
                "type": "remove_duplicates",
                "name": "Remove Duplicates",
                "config": {"columns": self._selected_columns()},
            }

        if step_type == "limit_rows":
            return {
                "type": "limit_rows",
                "name": "Limit Rows",
                "config": {"n": self.limit_rows.value()},
            }

        if step_type in {"uppercase", "lowercase", "trim"}:
            return {
                "type": step_type,
                "name": step_type.replace("_", " ").title(),
                "config": {"column": column},
            }

        raise ValueError(f"Unsupported transformation type: {step_type}")
