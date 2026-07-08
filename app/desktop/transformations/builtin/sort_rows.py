from typing import Any

import polars as pl

from app.desktop.transformations.base_transformation import BaseTransformation


class SortRowsTransformation(BaseTransformation):
    transformation_id = "sort_rows"
    display_name = "Sort Rows"
    category = "Filas"

    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        column = config.get("column")
        return dataframe.sort(column, descending=config.get("descending", False)) if column else dataframe

    def to_python(self, dataframe_name: str, config: dict[str, Any]) -> list[str]:
        return [
            f"{dataframe_name} = {dataframe_name}.sort({config.get('column', '')!r}, descending={config.get('descending', False)!r})"
        ]
