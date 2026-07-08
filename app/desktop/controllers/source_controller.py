from pathlib import Path

import polars as pl
from PySide6.QtWidgets import QFileDialog, QMessageBox, QDialog

from app.desktop.dialogs.add_data_source_dialog import AddDataSourceDialog
from app.desktop.dialogs.select_excel_sheet_dialog import SelectExcelSheetDialog


class SourceController:
    """Controller responsible for adding and activating data sources."""

    def __init__(self, window) -> None:
        self.window = window

    def add_source(self) -> None:
        dialog = AddDataSourceDialog(self.window)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        source_type = dialog.selected_source_type()

        if source_type == "csv":
            self._add_csv()
        elif source_type == "excel":
            self._add_excel()
        elif source_type == "parquet":
            self._add_parquet()
        else:
            QMessageBox.information(
                self.window,
                "Próximamente",
                "Este tipo de fuente estará disponible en un siguiente hito.",
            )

    def _add_csv(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Agregar CSV",
            "",
            "CSV Files (*.csv)",
        )

        if not file_path:
            return

        try:
            source = self.window.service.add_data_source(Path(file_path))
            dataframe = self.window.service.activate_source_as_query(source.name)
            self.window.data_preview.load_dataframe(dataframe)
            self.window.logs_panel.log(f"Fuente CSV agregada: {file_path}")
            self.window.status.showMessage("Fuente CSV agregada")
            self.window.refresh_ui()
        except Exception as exc:
            self.window.show_error("Error agregando CSV", exc)

    def _add_excel(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Agregar Excel",
            "",
            "Excel Files (*.xlsx)",
        )

        if not file_path:
            return

        try:
            path = Path(file_path)
            sheets = self.window.service.get_excel_sheet_names(path)

            sheet_dialog = SelectExcelSheetDialog(sheets, self.window)

            if sheet_dialog.exec() != QDialog.DialogCode.Accepted:
                return

            sheet_name = sheet_dialog.selected_sheet()

            source = self.window.service.add_data_source(path, sheet_name)
            dataframe = self.window.service.activate_source_as_query(source.name)

            self.window.data_preview.load_dataframe(dataframe)
            self.window.logs_panel.log(f"Fuente Excel agregada: {file_path} / {sheet_name}")
            self.window.status.showMessage("Fuente Excel agregada")
            self.window.refresh_ui()
        except Exception as exc:
            self.window.show_error("Error agregando Excel", exc)

    def _add_parquet(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Agregar Parquet",
            "",
            "Parquet Files (*.parquet)",
        )

        if not file_path:
            return

        try:
            source = self.window.service.add_data_source(Path(file_path))
            dataframe = self.window.service.activate_source_as_query(source.name)
            self.window.data_preview.load_dataframe(dataframe)
            self.window.logs_panel.log(f"Fuente Parquet agregada: {file_path}")
            self.window.status.showMessage("Fuente Parquet agregada")
            self.window.refresh_ui()
        except Exception as exc:
            self.window.show_error("Error agregando Parquet", exc)

    def activate_source_from_tree(self, item) -> None:
        from app.desktop.widgets.project_tree import SOURCE_NAME_ROLE

        source_name = item.data(0, SOURCE_NAME_ROLE)

        if not source_name:
            return

        try:
            dataframe = self.window.service.activate_source_as_query(source_name)
            self.window.data_preview.load_dataframe(dataframe)
            self.window.logs_panel.log(f"Fuente activada como consulta: {source_name}")
            self.window.status.showMessage(f"Consulta activa: {source_name}")
            self.window.refresh_ui()
        except Exception as exc:
            self.window.show_error("Error activando fuente", exc)
