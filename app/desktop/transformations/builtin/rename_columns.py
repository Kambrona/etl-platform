from typing import Any

import polars as pl

from app.desktop.transformations.base_transformation import BaseTransformation


class RenameColumnsTransformation(BaseTransformation):
    transformation_id = "rename_columns"
    display_name = "Rename Columns"
    category = "Columnas"

    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        return dataframe.rename(config.get("columns", {}))

    def to_python(self, dataframe_name: str, config: dict[str, Any]) -> list[str]:
        return [
            f"{dataframe_name} = {dataframe_name}.rename({config.get('columns', {})!r})"
        ]
