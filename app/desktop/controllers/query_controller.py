from PySide6.QtWidgets import QDialog, QMessageBox

from app.desktop.dialogs.add_transformation_dialog import AddTransformationDialog
from app.desktop.widgets.pipeline_tree import STEP_INDEX_ROLE


class QueryController:
    """Controller responsible for query execution and transformations."""

    def __init__(self, window) -> None:
        self.window = window

    def run_query(self) -> None:
        try:
            dataframe = self.window.service.run_pipeline_preview_mode()
            self.window.data_preview.load_dataframe(dataframe)
            self.window.logs_panel.log("Consulta ejecutada en modo preview.")
            self.window.status.showMessage("Consulta ejecutada")
            self.window.refresh_ui()
        except Exception as exc:
            self.window.show_error("Error ejecutando consulta", exc)

    def add_transformation_from_catalog(self, item, column_index: int = 0) -> None:
        step_type = item.data(0, 1000)

        if not step_type:
            return

        self.add_transformation(step_type)

    def add_transformation(
        self,
        forced_step_type: str | None = None,
        insert_index: int | None = None,
        columns: list[str] | None = None,
    ) -> None:
        try:
            if columns is None:
                dataframe = self.window.service.preview_current_source()
                columns = dataframe.columns

                if dataframe.is_empty():
                    QMessageBox.warning(
                        self.window,
                        "Sin datos",
                        "Primero debes agregar una fuente de datos.",
                    )
                    return

            dialog = AddTransformationDialog(
                columns,
                self.window,
                forced_step_type=forced_step_type,
            )

            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            step = dialog.get_step()
            self.window.service.add_transformation_step(step, index=insert_index)

            result = self.window.service.run_pipeline_preview_mode()
            self.window.data_preview.load_dataframe(result)

            self.window.logs_panel.log(f"Transformación agregada: {step['type']}")
            self.window.status.showMessage("Transformación agregada")
            self.window.refresh_ui()

        except Exception as exc:
            self.window.show_error("Error agregando transformación", exc)

    def preview_until_step(self, item) -> None:
        step_index = item.data(0, STEP_INDEX_ROLE)

        if step_index is None:
            return

        self.preview_until_step_index(step_index)

    def preview_until_step_index(self, step_index: int) -> None:
        try:
            dataframe = self.window.service.run_pipeline_until_step(step_index)
            self.window.data_preview.load_dataframe(dataframe)
            self.window.logs_panel.log(f"Vista previa hasta el paso {step_index + 1}.")
            self.window.status.showMessage(f"Preview hasta paso {step_index + 1}")
        except Exception as exc:
            self.window.show_error("Error mostrando preview por paso", exc)

    def insert_after_step(self, step_index: int) -> None:
        try:
            dataframe = self.window.service.run_pipeline_until_step(step_index)
            self.add_transformation(
                insert_index=step_index + 1,
                columns=dataframe.columns,
            )
        except Exception as exc:
            self.window.show_error("Error insertando transformación", exc)

    def delete_step(self, step_index: int) -> None:
        try:
            self.window.service.delete_step(step_index)

            dataframe = self.window.service.run_pipeline_preview_mode()
            self.window.data_preview.load_dataframe(dataframe)

            self.window.logs_panel.log(f"Paso eliminado: {step_index + 1}")
            self.window.status.showMessage("Paso eliminado")
            self.window.refresh_ui()

        except Exception as exc:
            self.window.show_error("Error eliminando paso", exc)
