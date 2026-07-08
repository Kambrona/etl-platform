from typing import Any
import polars as pl
from app.desktop.transformations.base_transformation import BaseTransformation


class RoundNumberTransformation(BaseTransformation):
    transformation_id = "round_number"
    display_name = "Round Number"
    category = "Números"

    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        column = config.get("column")
        decimals = config.get("decimals", 2)

        if not column:
            return dataframe

        return dataframe.with_columns(pl.col(column).round(decimals).alias(column))

    def to_python(self, dataframe_name: str, config: dict[str, Any]) -> list[str]:
        column = config.get("column", "")
        decimals = config.get("decimals", 2)
        return [
            f"{dataframe_name} = {dataframe_name}.with_columns(pl.col({column!r}).round({decimals!r}).alias({column!r}))"
        ]
