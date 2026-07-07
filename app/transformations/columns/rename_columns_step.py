from app.engine.base_step import BaseStep
from app.engine.step_registry import StepRegistry


class RenameColumnsStep(BaseStep):

    def execute(self, context, step):

        input_name = step.config["input"]
        columns = step.config["columns"]

        df = context.get_dataframe(input_name)
        result = df.rename(columns)

        context.set_dataframe(step.name, result)


StepRegistry.register("rename_columns", RenameColumnsStep)