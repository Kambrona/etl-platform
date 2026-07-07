from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar


class AppMenuBar(QMenuBar):
    """Main application menu bar."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.new_pipeline_action = QAction("Nuevo Pipeline", self)
        self.open_csv_action = QAction("Abrir CSV", self)
        self.open_excel_action = QAction("Abrir Excel", self)
        self.open_pipeline_action = QAction("Abrir Pipeline", self)
        self.save_pipeline_action = QAction("Guardar Pipeline", self)
        self.export_action = QAction("Exportar", self)
        self.exit_action = QAction("Salir", self)

        self.run_action = QAction("Ejecutar Pipeline", self)
        self.add_transformation_action = QAction("Agregar Transformación", self)

        self._build_menu()

    def _build_menu(self) -> None:
        file_menu = self.addMenu("Archivo")
        file_menu.addAction(self.new_pipeline_action)
        file_menu.addSeparator()
        file_menu.addAction(self.open_csv_action)
        file_menu.addAction(self.open_excel_action)
        file_menu.addAction(self.open_pipeline_action)
        file_menu.addSeparator()
        file_menu.addAction(self.save_pipeline_action)
        file_menu.addAction(self.export_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        pipeline_menu = self.addMenu("Pipeline")
        pipeline_menu.addAction(self.add_transformation_action)
        pipeline_menu.addAction(self.run_action)

        self.addMenu("Herramientas")
        self.addMenu("Ayuda")