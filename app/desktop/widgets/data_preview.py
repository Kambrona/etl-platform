import polars as pl

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem


class DataPreviewTable(QTableWidget):
    """Table widget used to preview dataframe data."""

    def load_dataframe(self, dataframe: pl.DataFrame, limit: int = 500) -> None:
        preview = dataframe.head(limit)

        self.clear()
        self.setRowCount(preview.height)
        self.setColumnCount(len(preview.columns))
        self.setHorizontalHeaderLabels(preview.columns)

        for row_index, row in enumerate(preview.iter_rows()):
            for col_index, value in enumerate(row):
                item = QTableWidgetItem("" if value is None else str(value))
                self.setItem(row_index, col_index, item)

        self.resizeColumnsToContents()