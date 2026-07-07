import app.transformations.readers.read_csv_step
import app.transformations.columns.rename_columns_step
import app.transformations.filters.filter_rows_step
import app.transformations.exports.export_parquet_step

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit,
    QTableWidget, QTableWidgetItem, QListWidget
)

from app.engine.pipeline_loader import PipelineLoader
from app.engine.pipeline_runner import PipelineRunner


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ETL Platform - Desktop MVP")
        self.resize(1200, 700)

        self.pipeline_input = QLineEdit("pipelines/demo.yaml")
        self.output_input = QLineEdit("clientes_filtrados")

        self.run_button = QPushButton("Ejecutar Pipeline")
        self.run_button.clicked.connect(self.run_pipeline)

        self.steps_list = QListWidget()
        self.table = QTableWidget()
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)

        layout = QVBoxLayout()

        top = QHBoxLayout()
        top.addWidget(QLabel("Pipeline:"))
        top.addWidget(self.pipeline_input)
        top.addWidget(QLabel("Resultado:"))
        top.addWidget(self.output_input)
        top.addWidget(self.run_button)

        body = QHBoxLayout()

        left = QVBoxLayout()
        left.addWidget(QLabel("Pasos"))
        left.addWidget(self.steps_list)

        right = QVBoxLayout()
        right.addWidget(QLabel("Vista previa"))
        right.addWidget(self.table)
        right.addWidget(QLabel("Logs"))
        right.addWidget(self.logs)

        body.addLayout(left, 1)
        body.addLayout(right, 3)

        layout.addLayout(top)
        layout.addLayout(body)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def run_pipeline(self):
        self.steps_list.clear()
        self.logs.clear()
        self.table.clear()

        pipeline_path = self.pipeline_input.text()
        output_name = self.output_input.text()

        pipeline = PipelineLoader.load(pipeline_path)
        runner = PipelineRunner()
        context = runner.run(pipeline)

        for step in pipeline.steps:
            self.steps_list.addItem(f"{step.name} ({step.type})")

        for step_result in context.result.steps:
            self.logs.append(
                f"OK {step_result.step_name} - {step_result.duration:.4f} s"
            )

        df = context.get_dataframe(output_name)

        if df is None:
            self.logs.append(f"No existe el dataframe: {output_name}")
            return

        self.table.setRowCount(df.height)
        self.table.setColumnCount(df.width)
        self.table.setHorizontalHeaderLabels(df.columns)

        rows = df.rows()

        for row_index, row in enumerate(rows):
            for col_index, value in enumerate(row):
                self.table.setItem(
                    row_index,
                    col_index,
                    QTableWidgetItem(str(value))
                )

        self.logs.append("Pipeline ejecutado correctamente.")