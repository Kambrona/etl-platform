from typing import Any

import polars as pl

from app.desktop.transformations.base_transformation import BaseTransformation


class SelectColumnsTransformation(BaseTransformation):
    transformation_id = "select_columns"
    display_name = "Select Columns"
    category = "Columnas"

    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        columns = config.get("columns", [])
        return dataframe.select(columns) if columns else dataframe

    def to_python(self, dataframe_name: str, config: dict[str, Any]) -> list[str]:
        return [
            f"{dataframe_name} = {dataframe_name}.select({config.get('columns', [])!r})"
        ]
