from typing import Any
import polars as pl
from app.desktop.transformations.base_transformation import BaseTransformation


class ExtractMonthTransformation(BaseTransformation):
    transformation_id = "extract_month"
    display_name = "Extract Month"
    category = "Fecha"

    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        column = config.get("column")
        new_column = config.get("new_column") or f"{column}_month"

        if not column:
            return dataframe

        return dataframe.with_columns(pl.col(column).str.to_date(strict=False).dt.month().alias(new_column))

    def to_python(self, dataframe_name: str, config: dict[str, Any]) -> list[str]:
        column = config.get("column", "")
        new_column = config.get("new_column") or f"{column}_month"
        return [
            f"{dataframe_name} = {dataframe_name}.with_columns(pl.col({column!r}).str.to_date(strict=False).dt.month().alias({new_column!r}))"
        ]
