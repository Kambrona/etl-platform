from pathlib import Path
from app.desktop.dialogs.add_transformation_dialog import AddTransformationDialog
from app.desktop.dialogs.add_data_source_dialog import AddDataSourceDialog
from app.desktop.dialogs.select_excel_sheet_dialog import SelectExcelSheetDialog
from app.desktop.dialogs.add_data_source_dialog import AddDataSourceDialog
from app.desktop.dialogs.select_excel_sheet_dialog import SelectExcelSheetDialog
from app.desktop.widgets.pipeline_tree import PipelineTree, STEP_INDEX_ROLE

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QDialog,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QWidget,
    QVBoxLayout,
)

from app.desktop.services.pipeline_desktop_service import PipelineDesktopService
from app.desktop.widgets.data_preview import DataPreviewTable
from app.desktop.widgets.logs_panel import LogsPanel
from app.desktop.widgets.menu_bar import AppMenuBar
from app.desktop.widgets.pipeline_tree import PipelineTree
from app.desktop.widgets.project_tree import ProjectTree, SOURCE_NAME_ROLE, SOURCE_NAME_ROLE
from app.desktop.widgets.properties_panel import PropertiesPanel
from app.desktop.widgets.toolbar import MainToolBar
from app.desktop.widgets.transformation_catalog import TransformationCatalog


class MainWindow(QMainWindow):
    """Main desktop window for the ETL platform."""

    def __init__(self) -> None:
        super().__init__()

        self.service = PipelineDesktopService()

        self.setWindowTitle("ETL Platform Desktop")
        self.resize(1600, 900)

        self.menu = AppMenuBar(self)
        self.setMenuBar(self.menu)

        self.toolbar = MainToolBar(
            new_action=self.menu.new_pipeline_action,
            open_csv_action=self.menu.open_csv_action,
            open_excel_action=self.menu.open_excel_action,
            save_action=self.menu.save_pipeline_action,
            run_action=self.menu.run_action,
            export_action=self.menu.export_action,
            parent=self,
        )
        self.addToolBar(self.toolbar)

        self.status = QStatusBar(self)
        self.setStatusBar(self.status)

        self.project_tree = ProjectTree(self)
        self.project_tree.itemDoubleClicked.connect(self.activate_source_from_project_tree)
        self.project_tree.itemDoubleClicked.connect(self.activate_source_from_project_tree)
        self.pipeline_tree = PipelineTree(self)
        self.pipeline_tree.itemDoubleClicked.connect(self.preview_until_selected_step)
        self.transformation_catalog = TransformationCatalog(self)
        self.transformation_catalog.itemDoubleClicked.connect(
            self.add_transformation_from_catalog
        )
        self.properties_panel = PropertiesPanel(self)
        self.data_preview = DataPreviewTable(self)
        self.logs_panel = LogsPanel(self)

        self._build_layout()
        self._connect_actions()
        self._refresh_ui()

        self.logs_panel.log("AplicaciÃ³n iniciada correctamente.")
        self.status.showMessage("Listo")

    def _build_layout(self) -> None:
        left_splitter = QSplitter(Qt.Vertical)
        left_splitter.addWidget(self.project_tree)
        left_splitter.addWidget(self.transformation_catalog)
        left_splitter.addWidget(self.pipeline_tree)
        left_splitter.setSizes([250, 250, 350])   
                
        center_tabs = QTabWidget()
        center_tabs.addTab(self.data_preview, "Vista previa")

        bottom_tabs = QTabWidget()
        bottom_tabs.addTab(self.logs_panel, "Logs")

        center_splitter = QSplitter(Qt.Vertical)
        center_splitter.addWidget(center_tabs)
        center_splitter.addWidget(bottom_tabs)
        center_splitter.setSizes([650, 250])

        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(center_splitter)
        main_splitter.addWidget(self.properties_panel)
        main_splitter.setSizes([300, 950, 350])

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(main_splitter)

        self.setCentralWidget(container)

    def _connect_actions(self) -> None:
        self.menu.new_pipeline_action.triggered.connect(self.create_pipeline)
        self.menu.open_csv_action.triggered.connect(self.open_csv)
        self.menu.open_excel_action.triggered.connect(self.open_excel)
        self.menu.open_pipeline_action.triggered.connect(self.open_pipeline)
        self.menu.save_pipeline_action.triggered.connect(self.save_pipeline)
        self.menu.run_action.triggered.connect(self.run_pipeline)
        self.menu.add_transformation_action.triggered.connect(self.add_transformation)
        self.menu.export_action.triggered.connect(self.export_pipeline)
        self.menu.exit_action.triggered.connect(self.close)

    def create_pipeline(self) -> None:
        self.service.create_pipeline()
        self.data_preview.clear()
        self.logs_panel.log("Nuevo pipeline creado.")
        self.status.showMessage("Nuevo pipeline creado")
        self._refresh_ui()

    def open_csv(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir CSV",
            "",
            "CSV Files (*.csv)",
        )

        if not file_path:
            return

        try:
            dataframe = self.service.open_csv(Path(file_path))
            self.data_preview.load_dataframe(dataframe)
            self.logs_panel.log(f"CSV abierto: {file_path}")
            self.status.showMessage("CSV cargado correctamente")
            self._refresh_ui()
        except Exception as exc:
            self._show_error("Error abriendo CSV", exc)

    def open_excel(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir Excel",
            "",
            "Excel Files (*.xlsx *.xls)",
        )

        if not file_path:
            return

        try:
            dataframe = self.service.open_excel(Path(file_path))
            self.data_preview.load_dataframe(dataframe)
            self.logs_panel.log(f"Excel abierto: {file_path}")
            self.status.showMessage("Excel cargado correctamente")
            self._refresh_ui()
        except Exception as exc:
            self._show_error("Error abriendo Excel", exc)

    def open_pipeline(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir Pipeline",
            "",
            "YAML Files (*.yaml *.yml)",
        )

        if not file_path:
            return

        try:
            self.service.load_pipeline(Path(file_path))
            self.logs_panel.log(f"Pipeline abierto: {file_path}")
            self.status.showMessage("Pipeline abierto correctamente")
            self._refresh_ui()
        except Exception as exc:
            self._show_error("Error abriendo pipeline", exc)

    def save_pipeline(self) -> None:
        current_path = self.service.state.pipeline_path

        if current_path:
            file_path = str(current_path)
        else:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar Pipeline",
                "",
                "YAML Files (*.yaml *.yml)",
            )

        if not file_path:
            return

        try:
            self.service.save_pipeline(Path(file_path))
            self.logs_panel.log(f"Pipeline guardado: {file_path}")
            self.status.showMessage("Pipeline guardado correctamente")
            self._refresh_ui()
        except Exception as exc:
            self._show_error("Error guardando pipeline", exc)

    def run_pipeline(self) -> None:
        try:
            dataframe = self.service.run_pipeline_preview_mode()
            self.data_preview.load_dataframe(dataframe)
            self.logs_panel.log("Pipeline ejecutado en modo preview.")
            self.status.showMessage("Pipeline ejecutado")
            self._refresh_ui()
        except Exception as exc:
            self._show_error("Error ejecutando pipeline", exc)

    def export_pipeline(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Parquet",
            "",
            "Parquet Files (*.parquet)",
        )

        if not file_path:
            return

        try:
            output_path = Path(file_path)
            self.service.add_export_step(output_path)

            dataframe = self.service.run_pipeline_preview_mode()
            dataframe.write_parquet(output_path)

            self.service.state.last_result_path = output_path

            self.logs_panel.log(f"Resultado exportado: {output_path}")
            self.status.showMessage("ExportaciÃ³n completada")
            self._refresh_ui()
        except Exception as exc:
            self._show_error("Error exportando resultado", exc)

    def _refresh_ui(self) -> None:
        state = self.service.state

        self.project_tree.refresh_workspace(self.service.workspace)
        self.pipeline_tree.refresh(state.steps)

        self.properties_panel.update_properties(
            {
                "pipeline_name": state.pipeline_name,
                "source_path": state.source_path or "-",
                "output_path": state.output_path or "-",
                "steps_count": len(state.steps),
                "generated_script": self.service.generate_python_script(),
            }
        )
        dirty_mark = "*" if state.is_dirty else ""
        self.setWindowTitle(f"ETL Platform Desktop - {state.pipeline_name}{dirty_mark}")

    def add_transformation_from_catalog(self, item) -> None:
        step_type = item.data(1000)

        if not step_type:
            return

        self.add_transformation(step_type)

    def add_transformation(self, forced_step_type: str | None = None) -> None:
        try:
            dataframe = self.service.preview_current_source()

            if dataframe.is_empty():
                QMessageBox.warning(
                    self,
                    "Sin datos",
                    "Primero debes abrir un CSV o Excel.",
                )
                return

            dialog = AddTransformationDialog(
                dataframe.columns,
                self,
                forced_step_type=forced_step_type,
            )

            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            step = dialog.get_step()
            self.service.add_transformation_step(step)

            result = self.service.run_pipeline_preview_mode()
            self.data_preview.load_dataframe(result)

            self.logs_panel.log(f"TransformaciÃ³n agregada: {step['type']}")
            self.status.showMessage("TransformaciÃ³n agregada")
            self._refresh_ui()

        except Exception as exc:
            self._show_error("Error agregando transformaciÃ³n", exc)


    def activate_source_from_project_tree(self, item) -> None:
        source_name = item.data(0, SOURCE_NAME_ROLE)

        if not source_name:
            return

        try:
            dataframe = self.service.activate_source_as_query(source_name)
            self.data_preview.load_dataframe(dataframe)

            self.logs_panel.log(f"Fuente activada como consulta: {source_name}")
            self.status.showMessage(f"Consulta activa: {source_name}")
            self._refresh_ui()

        except Exception as exc:
            self._show_error("Error activando fuente", exc)
    def _show_error(self, title: str, exc: Exception) -> None:
        self.logs_panel.log(f"{title}: {exc}")
        self.status.showMessage("Error")
        QMessageBox.critical(self, title, str(exc))

    def preview_until_selected_step(self, item) -> None:
        step_index = item.data(0, STEP_INDEX_ROLE)

        if step_index is None:
            return

        try:
            dataframe = self.service.run_pipeline_until_step(step_index)
            self.data_preview.load_dataframe(dataframe)

            self.logs_panel.log(
                f"Vista previa hasta el paso {step_index + 1}."
            )
            self.status.showMessage(f"Preview hasta paso {step_index + 1}")

        except Exception as exc:
            self._show_error("Error mostrando preview por paso", exc)

