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

    def __init__(self, columns: list[str], parent=None, forced_step_type: str | None = None) -> None:
        super().__init__(parent)

        self.columns = columns
        self.setWindowTitle("Agregar Transformación")
        self.resize(620, 460)

        self.transformation_type = QComboBox()
        self.transformation_type.addItems([
            "promote_headers",
            "change_type",
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
            "replace_value",
            "fill_null",
            "round_number",
            "extract_year",
            "extract_month",
        ])

        self.column_label = QLabel("Columna:")
        self.source_column = QComboBox()
        self.source_column.addItems(columns)

        self.operator_label = QLabel("Operador:")
        self.operator = QComboBox()
        self.operator.addItems(["=", "!=", ">", ">=", "<", "<=", "contains"])

        self.value_label = QLabel("Valor:")
        self.target_value = QLineEdit()

        self.second_value_label = QLabel("Nuevo valor:")
        self.second_value = QLineEdit()

        self.dtype_label = QLabel("Tipo:")
        self.dtype_combo = QComboBox()
        self.dtype_combo.addItems(["text", "integer", "float", "date", "datetime", "boolean"])

        self.sort_descending = QCheckBox("Orden descendente")

        self.limit_label = QLabel("Cantidad:")
        self.limit_rows = QSpinBox()
        self.limit_rows.setMinimum(1)
        self.limit_rows.setMaximum(10000000)
        self.limit_rows.setValue(100)

        self.decimals_label = QLabel("Decimales:")
        self.decimals = QSpinBox()
        self.decimals.setMinimum(0)
        self.decimals.setMaximum(10)
        self.decimals.setValue(2)

        self.columns_label = QLabel("Columnas:")
        self.columns_list = QListWidget()
        self.columns_list.setSelectionMode(QListWidget.MultiSelection)

        for column in columns:
            self.columns_list.addItem(QListWidgetItem(column))

        self.help_label = QLabel("")
        self.help_label.setWordWrap(True)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QFormLayout(self)
        layout.addRow("Transformación:", self.transformation_type)
        layout.addRow(self.column_label, self.source_column)
        layout.addRow(self.operator_label, self.operator)
        layout.addRow(self.value_label, self.target_value)
        layout.addRow(self.second_value_label, self.second_value)
        layout.addRow(self.dtype_label, self.dtype_combo)
        layout.addRow("", self.sort_descending)
        layout.addRow(self.limit_label, self.limit_rows)
        layout.addRow(self.decimals_label, self.decimals)
        layout.addRow(self.columns_label, self.columns_list)
        layout.addRow("Ayuda:", self.help_label)
        layout.addWidget(self.buttons)

        if forced_step_type:
            index = self.transformation_type.findText(forced_step_type)
            if index >= 0:
                self.transformation_type.setCurrentIndex(index)
                self.transformation_type.setEnabled(False)

        self.transformation_type.currentTextChanged.connect(self._refresh_form)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self._refresh_form()

    def _hide_all(self) -> None:
        for widget in [
            self.column_label,
            self.source_column,
            self.operator_label,
            self.operator,
            self.value_label,
            self.target_value,
            self.second_value_label,
            self.second_value,
            self.dtype_label,
            self.dtype_combo,
            self.sort_descending,
            self.limit_label,
            self.limit_rows,
            self.decimals_label,
            self.decimals,
            self.columns_label,
            self.columns_list,
        ]:
            widget.setVisible(False)

    def _refresh_form(self) -> None:
        step_type = self.transformation_type.currentText()
        self._hide_all()

        if step_type == "promote_headers":
            self.help_label.setText("Usa la primera fila como nombres de columna.")

        elif step_type == "change_type":
            self.column_label.setVisible(True)
            self.source_column.setVisible(True)
            self.dtype_label.setVisible(True)
            self.dtype_combo.setVisible(True)
            self.help_label.setText("Cambia el tipo de dato de una columna.")

        elif step_type == "rename_columns":
            self.column_label.setVisible(True)
            self.source_column.setVisible(True)
            self.value_label.setVisible(True)
            self.target_value.setVisible(True)
            self.value_label.setText("Nuevo nombre:")
            self.help_label.setText("Renombra la columna seleccionada.")

        elif step_type == "filter_rows":
            self.column_label.setVisible(True)
            self.source_column.setVisible(True)
            self.operator_label.setVisible(True)
            self.operator.setVisible(True)
            self.value_label.setVisible(True)
            self.target_value.setVisible(True)
            self.value_label.setText("Valor:")
            self.help_label.setText("Filtra filas usando columna, operador y valor.")

        elif step_type in {"select_columns", "drop_columns", "remove_duplicates"}:
            self.columns_label.setVisible(True)
            self.columns_list.setVisible(True)
            self.help_label.setText("Selecciona columnas.")

        elif step_type == "sort_rows":
            self.column_label.setVisible(True)
            self.source_column.setVisible(True)
            self.sort_descending.setVisible(True)
            self.help_label.setText("Ordena la consulta por la columna seleccionada.")

        elif step_type == "limit_rows":
            self.limit_label.setVisible(True)
            self.limit_rows.setVisible(True)
            self.help_label.setText("Conserva solo las primeras N filas.")

        elif step_type in {"uppercase", "lowercase", "trim", "fill_null", "round_number", "extract_year", "extract_month"}:
            self.column_label.setVisible(True)
            self.source_column.setVisible(True)

            if step_type == "fill_null":
                self.value_label.setVisible(True)
                self.target_value.setVisible(True)
                self.value_label.setText("Valor para rellenar:")

            if step_type == "round_number":
                self.decimals_label.setVisible(True)
                self.decimals.setVisible(True)

            self.help_label.setText("Aplica la transformación sobre la columna seleccionada.")

        elif step_type == "replace_value":
            self.column_label.setVisible(True)
            self.source_column.setVisible(True)
            self.value_label.setVisible(True)
            self.target_value.setVisible(True)
            self.second_value_label.setVisible(True)
            self.second_value.setVisible(True)
            self.value_label.setText("Valor actual:")
            self.second_value_label.setText("Nuevo valor:")
            self.help_label.setText("Reemplaza un valor por otro.")

    def _selected_columns(self) -> list[str]:
        return [item.text() for item in self.columns_list.selectedItems()]

    def _build_filter_expression(self) -> str:
        column = self.source_column.currentText()
        operator = self.operator.currentText()
        value = self.target_value.text().strip()

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

        if step_type == "promote_headers":
            return {"type": "promote_headers", "name": "Promote First Row as Headers", "config": {}}

        if step_type == "change_type":
            return {"type": "change_type", "name": "Change Type", "config": {"column": column, "dtype": self.dtype_combo.currentText()}}

        if step_type == "rename_columns":
            return {"type": "rename_columns", "name": "Rename Columns", "config": {"columns": {column: self.target_value.text().strip()}}}

        if step_type == "filter_rows":
            return {"type": "filter_rows", "name": "Filter Rows", "config": {"expression": self._build_filter_expression()}}

        if step_type == "select_columns":
            return {"type": "select_columns", "name": "Select Columns", "config": {"columns": self._selected_columns()}}

        if step_type == "drop_columns":
            return {"type": "drop_columns", "name": "Drop Columns", "config": {"columns": self._selected_columns()}}

        if step_type == "sort_rows":
            return {"type": "sort_rows", "name": "Sort Rows", "config": {"column": column, "descending": self.sort_descending.isChecked()}}

        if step_type == "remove_duplicates":
            return {"type": "remove_duplicates", "name": "Remove Duplicates", "config": {"columns": self._selected_columns()}}

        if step_type == "limit_rows":
            return {"type": "limit_rows", "name": "Limit Rows", "config": {"n": self.limit_rows.value()}}

        if step_type in {"uppercase", "lowercase", "trim"}:
            return {"type": step_type, "name": step_type.replace("_", " ").title(), "config": {"column": column}}

        if step_type == "replace_value":
            return {"type": "replace_value", "name": "Replace Value", "config": {"column": column, "old_value": self.target_value.text(), "new_value": self.second_value.text()}}

        if step_type == "fill_null":
            return {"type": "fill_null", "name": "Fill Null", "config": {"column": column, "value": self.target_value.text()}}

        if step_type == "round_number":
            return {"type": "round_number", "name": "Round Number", "config": {"column": column, "decimals": self.decimals.value()}}

        if step_type == "extract_year":
            return {"type": "extract_year", "name": "Extract Year", "config": {"column": column, "new_column": f"{column}_year"}}

        if step_type == "extract_month":
            return {"type": "extract_month", "name": "Extract Month", "config": {"column": column, "new_column": f"{column}_month"}}

        raise ValueError(f"Unsupported transformation type: {step_type}")
