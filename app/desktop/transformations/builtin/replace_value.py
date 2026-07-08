from typing import Any
import polars as pl
from app.desktop.transformations.base_transformation import BaseTransformation


class ReplaceValueTransformation(BaseTransformation):
    transformation_id = "replace_value"
    display_name = "Replace Value"
    category = "Limpieza"

    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        column = config.get("column")
        old_value = config.get("old_value")
        new_value = config.get("new_value")

        if not column:
            return dataframe

        return dataframe.with_columns(
            pl.col(column).cast(pl.Utf8).str.replace_all(str(old_value), str(new_value)).alias(column)
        )

    def to_python(self, dataframe_name: str, config: dict[str, Any]) -> list[str]:
        column = config.get("column", "")
        old_value = config.get("old_value", "")
        new_value = config.get("new_value", "")
        return [
            f"{dataframe_name} = {dataframe_name}.with_columns(pl.col({column!r}).cast(pl.Utf8).str.replace_all({old_value!r}, {new_value!r}).alias({column!r}))"
        ]
