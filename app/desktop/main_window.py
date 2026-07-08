from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QWidget,
    QVBoxLayout,
)

from app.desktop.controllers.query_controller import QueryController
from app.desktop.controllers.source_controller import SourceController
from app.desktop.services.pipeline_desktop_service import PipelineDesktopService
from app.desktop.widgets.data_preview import DataPreviewTable
from app.desktop.widgets.logs_panel import LogsPanel
from app.desktop.widgets.menu_bar import AppMenuBar
from app.desktop.widgets.pipeline_tree import PipelineTree
from app.desktop.widgets.project_tree import ProjectTree
from app.desktop.widgets.properties_panel import PropertiesPanel
from app.desktop.widgets.toolbar import MainToolBar
from app.desktop.widgets.transformation_catalog import TransformationCatalog


class MainWindow(QMainWindow):
    """Main desktop window for the ETL platform."""

    def __init__(self) -> None:
        super().__init__()

        self.service = PipelineDesktopService()
        self.source_controller = SourceController(self)
        self.query_controller = QueryController(self)

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
        self.project_tree.itemDoubleClicked.connect(
            self.source_controller.activate_source_from_tree
        )

        self.transformation_catalog = TransformationCatalog(self)
        self.transformation_catalog.itemDoubleClicked.connect(
            self.query_controller.add_transformation_from_catalog
        )

        self.pipeline_tree = PipelineTree(self)
        self.pipeline_tree.itemDoubleClicked.connect(
            self.query_controller.preview_until_step
        )
        self.pipeline_tree.preview_step_requested.connect(
            self.query_controller.preview_until_step_index
        )
        self.pipeline_tree.insert_after_step_requested.connect(
            self.query_controller.insert_after_step
        )
        self.pipeline_tree.delete_step_requested.connect(
            self.query_controller.delete_step
        )

        self.properties_panel = PropertiesPanel(self)
        self.data_preview = DataPreviewTable(self)
        self.logs_panel = LogsPanel(self)

        self._build_layout()
        self._connect_actions()
        self.refresh_ui()

        self.logs_panel.log("Aplicación iniciada correctamente.")
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
        main_splitter.setSizes([320, 920, 360])

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(main_splitter)

        self.setCentralWidget(container)

    def _connect_actions(self) -> None:
        self.menu.new_pipeline_action.triggered.connect(self.create_query)
        self.menu.open_csv_action.triggered.connect(self.source_controller.add_source)
        self.menu.open_excel_action.triggered.connect(self.source_controller.add_source)
        self.menu.open_pipeline_action.triggered.connect(self.open_query)
        self.menu.save_pipeline_action.triggered.connect(self.save_query)
        self.menu.run_action.triggered.connect(self.query_controller.run_query)
        self.menu.add_transformation_action.triggered.connect(
            self.query_controller.add_transformation
        )
        self.menu.export_action.triggered.connect(self.export_query)
        self.menu.export_python_action.triggered.connect(self.export_python)
        self.menu.exit_action.triggered.connect(self.close)

    def create_query(self) -> None:
        self.service.create_pipeline()
        self.data_preview.clear()
        self.logs_panel.log("Nueva consulta creada.")
        self.status.showMessage("Nueva consulta creada")
        self.refresh_ui()

    def open_query(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir Consulta",
            "",
            "YAML Files (*.yaml *.yml)",
        )

        if not file_path:
            return

        try:
            self.service.load_pipeline(Path(file_path))
            self.logs_panel.log(f"Consulta abierta: {file_path}")
            self.status.showMessage("Consulta abierta correctamente")
            self.refresh_ui()
        except Exception as exc:
            self.show_error("Error abriendo consulta", exc)

    def save_query(self) -> None:
        current_path = self.service.state.pipeline_path

        if current_path:
            file_path = str(current_path)
        else:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar Consulta",
                "",
                "YAML Files (*.yaml *.yml)",
            )

        if not file_path:
            return

        try:
            self.service.save_pipeline(Path(file_path))
            self.logs_panel.log(f"Consulta guardada: {file_path}")
            self.status.showMessage("Consulta guardada correctamente")
            self.refresh_ui()
        except Exception as exc:
            self.show_error("Error guardando consulta", exc)

    def export_query(self) -> None:
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
            self.status.showMessage("Exportación completada")
            self.refresh_ui()
        except Exception as exc:
            self.show_error("Error exportando resultado", exc)


    def export_python(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Python",
            "",
            "Python Files (*.py)",
        )

        if not file_path:
            return

        try:
            output_path = Path(file_path)
            script = self.service.generate_python_script()

            output_path.write_text(script, encoding="utf-8")

            self.logs_panel.log(f"Script Python exportado: {output_path}")
            self.status.showMessage("Python exportado correctamente")

        except Exception as exc:
            self.show_error("Error exportando Python", exc)
    def refresh_ui(self) -> None:
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

    def show_error(self, title: str, exc: Exception) -> None:
        self.logs_panel.log(f"{title}: {exc}")
        self.status.showMessage("Error")
        QMessageBox.critical(self, title, str(exc))

