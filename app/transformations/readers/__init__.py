from app.connectors.csv_reader import CsvReader
from app.engine.base_step import BaseStep
from app.engine.step_registry import StepRegistry


class ReadCsvStep(BaseStep):

    def execute(self, context, step):

        df = CsvReader.read(
            step.config["path"]
        )

        context.set_dataframe(
            step.name,
            df
        )


StepRegistry.register(
    "read_csv",
    ReadCsvStep
)