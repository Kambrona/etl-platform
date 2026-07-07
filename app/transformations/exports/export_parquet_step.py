from pathlib import Path

from app.engine.base_step import BaseStep
from app.engine.step_registry import StepRegistry


class ExportParquetStep(BaseStep):

    def execute(self, context, step):

        input_name = step.config["input"]
        path = Path(step.config["path"])

        path.parent.mkdir(parents=True, exist_ok=True)

        df = context.get_dataframe(input_name)
        df.write_parquet(path)

        context.set_dataframe(step.name, df)


StepRegistry.register("export_parquet", ExportParquetStep)