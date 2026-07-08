from typing import Any

import polars as pl

from app.desktop.transformations.base_transformation import BaseTransformation


class LowercaseTransformation(BaseTransformation):
    transformation_id = "lowercase"
    display_name = "Lowercase"
    category = "Texto"

    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        column = config.get("column")
        return dataframe.with_columns(pl.col(column).cast(pl.Utf8).str.to_lowercase().alias(column)) if column else dataframe

    def to_python(self, dataframe_name: str, config: dict[str, Any]) -> list[str]:
        column = config.get("column", "")
        return [
            f"{dataframe_name} = {dataframe_name}.with_columns(pl.col({column!r}).cast(pl.Utf8).str.to_lowercase().alias({column!r}))"
        ]
