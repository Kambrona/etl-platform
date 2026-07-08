from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


TRANSFORMATION_TYPE_ROLE = 1000


class TransformationCatalog(QTreeWidget):
    """Collapsible catalog of available transformations."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setHeaderLabel("Transformaciones")
        self.setMinimumWidth(240)

        self._build_catalog()
        self.expandAll()

    def _build_catalog(self) -> None:
        self.clear()

        prep = self.add_category("Preparación")
        self.add_transformation(prep, "Promote First Row as Headers", "promote_headers", "Usa la primera fila como nombres de columna.")
        self.add_transformation(prep, "Change Type", "change_type", "Cambia el tipo de dato de una columna.")

        columns = self.add_category("Columnas")
        self.add_transformation(columns, "Rename Columns", "rename_columns", "Cambia el nombre de una columna.")
        self.add_transformation(columns, "Select Columns", "select_columns", "Conserva solo las columnas seleccionadas.")
        self.add_transformation(columns, "Drop Columns", "drop_columns", "Elimina las columnas seleccionadas.")

        rows = self.add_category("Filas")
        self.add_transformation(rows, "Filter Rows", "filter_rows", "Filtra filas usando columna, operador y valor.")
        self.add_transformation(rows, "Sort Rows", "sort_rows", "Ordena la tabla por una columna.")
        self.add_transformation(rows, "Remove Duplicates", "remove_duplicates", "Elimina filas duplicadas.")
        self.add_transformation(rows, "Limit Rows", "limit_rows", "Conserva solo las primeras N filas.")

        text = self.add_category("Texto")
        self.add_transformation(text, "Uppercase", "uppercase", "Convierte texto a mayúsculas.")
        self.add_transformation(text, "Lowercase", "lowercase", "Convierte texto a minúsculas.")
        self.add_transformation(text, "Trim", "trim", "Elimina espacios al inicio y final.")
        self.add_transformation(text, "Replace Value", "replace_value", "Reemplaza un valor dentro de una columna.")
        self.add_transformation(text, "Fill Null", "fill_null", "Rellena valores nulos.")

        numbers = self.add_category("Números")
        self.add_transformation(numbers, "Round Number", "round_number", "Redondea una columna numérica.")

        dates = self.add_category("Fechas")
        self.add_transformation(dates, "Extract Year", "extract_year", "Extrae el año de una fecha.")
        self.add_transformation(dates, "Extract Month", "extract_month", "Extrae el mes de una fecha.")

    def add_category(self, name: str) -> QTreeWidgetItem:
        item = QTreeWidgetItem([name])
        item.setToolTip(0, f"Grupo de transformaciones: {name}")
        self.addTopLevelItem(item)
        return item

    def add_transformation(self, parent: QTreeWidgetItem, label: str, step_type: str, tooltip: str) -> None:
        item = QTreeWidgetItem([label])
        item.setData(0, TRANSFORMATION_TYPE_ROLE, step_type)
        item.setToolTip(0, tooltip)
        parent.addChild(item)
