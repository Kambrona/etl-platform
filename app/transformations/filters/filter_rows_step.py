import polars as pl

from app.engine.base_step import BaseStep
from app.engine.step_registry import StepRegistry


class FilterRowsStep(BaseStep):

    def execute(self, context, step):

        input_name = step.config["input"]
        column = step.config["column"]
        operator = step.config["operator"]
        value = step.config["value"]

        df = context.get_dataframe(input_name)

        if operator == ">":
            result = df.filter(pl.col(column) > value)
        elif operator == ">=":
            result = df.filter(pl.col(column) >= value)
        elif operator == "<":
            result = df.filter(pl.col(column) < value)
        elif operator == "<=":
            result = df.filter(pl.col(column) <= value)
        elif operator == "==":
            result = df.filter(pl.col(column) == value)
        elif operator == "!=":
            result = df.filter(pl.col(column) != value)
        else:
            raise ValueError(f"Operador no soportado: {operator}")

        context.set_dataframe(step.name, result)


StepRegistry.register("filter_rows", FilterRowsStep)