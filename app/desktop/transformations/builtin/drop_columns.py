from typing import Any

import polars as pl

from app.desktop.transformations.base_transformation import BaseTransformation


class DropColumnsTransformation(BaseTransformation):
    transformation_id = "drop_columns"
    display_name = "Drop Columns"
    category = "Columnas"

    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        columns = config.get("columns", [])
        return dataframe.drop(columns) if columns else dataframe

    def to_python(self, dataframe_name: str, config: dict[str, Any]) -> list[str]:
        return [
            f"{dataframe_name} = {dataframe_name}.drop({config.get('columns', [])!r})"
        ]
