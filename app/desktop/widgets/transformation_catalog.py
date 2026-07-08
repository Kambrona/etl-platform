from PySide6.QtWidgets import QListWidget, QListWidgetItem


class TransformationCatalog(QListWidget):
    """Catalog of available transformations."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setMinimumWidth(220)
        self.add_category("Columnas")
        self.add_transformation("Rename Columns", "rename_columns")
        self.add_transformation("Select Columns", "select_columns")
        self.add_transformation("Drop Columns", "drop_columns")

        self.add_category("Filas")
        self.add_transformation("Filter Rows", "filter_rows")

    def add_category(self, name: str) -> None:
        item = QListWidgetItem(f"▼ {name}")
        item.setFlags(item.flags() & ~item.flags().ItemIsSelectable)
        self.addItem(item)

    def add_transformation(self, label: str, step_type: str) -> None:
        item = QListWidgetItem(f"   {label}")
        item.setData(1000, step_type)
        self.addItem(item)
        