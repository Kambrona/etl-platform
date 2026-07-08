from typing import Any

import polars as pl

from app.desktop.transformations.base_transformation import BaseTransformation


class RemoveDuplicatesTransformation(BaseTransformation):
    transformation_id = "remove_duplicates"
    display_name = "Remove Duplicates"
    category = "Filas"

    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        columns = config.get("columns", [])
        return dataframe.unique(subset=columns, keep="first") if columns else dataframe.unique(keep="first")

    def to_python(self, dataframe_name: str, config: dict[str, Any]) -> list[str]:
        columns = config.get("columns", [])

        if columns:
            return [
                f"{dataframe_name} = {dataframe_name}.unique(subset={columns!r}, keep='first')"
            ]

        return [
            f"{dataframe_name} = {dataframe_name}.unique(keep='first')"
        ]
