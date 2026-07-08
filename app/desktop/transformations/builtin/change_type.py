from typing import Any
import polars as pl
from app.desktop.transformations.base_transformation import BaseTransformation


class ChangeTypeTransformation(BaseTransformation):
    transformation_id = "change_type"
    display_name = "Change Type"
    category = "Preparación"

    TYPE_MAP = {
        "text": pl.Utf8,
        "integer": pl.Int64,
        "float": pl.Float64,
        "date": pl.Date,
        "datetime": pl.Datetime,
        "boolean": pl.Boolean,
    }

    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        column = config.get("column")
        dtype = config.get("dtype", "text")

        if not column:
            return dataframe

        return dataframe.with_columns(
            pl.col(column).cast(self.TYPE_MAP.get(dtype, pl.Utf8), strict=False).alias(column)
        )

    def to_python(self, dataframe_name: str, config: dict[str, Any]) -> list[str]:
        column = config.get("column", "")
        dtype = config.get("dtype", "text")
        polars_type = {
            "text": "pl.Utf8",
            "integer": "pl.Int64",
            "float": "pl.Float64",
            "date": "pl.Date",
            "datetime": "pl.Datetime",
            "boolean": "pl.Boolean",
        }.get(dtype, "pl.Utf8")

        return [
            f"{dataframe_name} = {dataframe_name}.with_columns(pl.col({column!r}).cast({polars_type}, strict=False).alias({column!r}))"
        ]
