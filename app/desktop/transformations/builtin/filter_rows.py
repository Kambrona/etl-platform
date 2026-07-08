from typing import Any

import polars as pl

from app.desktop.transformations.base_transformation import BaseTransformation


class FilterRowsTransformation(BaseTransformation):
    transformation_id = "filter_rows"
    display_name = "Filter Rows"
    category = "Filas"

    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        expression = config.get("expression")
        return dataframe.sql(f"SELECT * FROM self WHERE {expression}") if expression else dataframe

    def to_python(self, dataframe_name: str, config: dict[str, Any]) -> list[str]:
        expression = config.get("expression", "")
        return [
            f'{dataframe_name} = {dataframe_name}.sql("SELECT * FROM self WHERE {expression}")'
        ]
