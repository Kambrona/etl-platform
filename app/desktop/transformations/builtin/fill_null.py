from typing import Any
import polars as pl
from app.desktop.transformations.base_transformation import BaseTransformation


class FillNullTransformation(BaseTransformation):
    transformation_id = "fill_null"
    display_name = "Fill Null"
    category = "Limpieza"

    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        column = config.get("column")
        value = config.get("value")

        if not column:
            return dataframe

        return dataframe.with_columns(pl.col(column).fill_null(value).alias(column))

    def to_python(self, dataframe_name: str, config: dict[str, Any]) -> list[str]:
        column = config.get("column", "")
        value = config.get("value", "")
        return [
            f"{dataframe_name} = {dataframe_name}.with_columns(pl.col({column!r}).fill_null({value!r}).alias({column!r}))"
        ]
