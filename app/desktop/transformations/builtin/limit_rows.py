from typing import Any

import polars as pl

from app.desktop.transformations.base_transformation import BaseTransformation


class LimitRowsTransformation(BaseTransformation):
    transformation_id = "limit_rows"
    display_name = "Limit Rows"
    category = "Filas"

    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        return dataframe.head(config.get("n", 100))

    def to_python(self, dataframe_name: str, config: dict[str, Any]) -> list[str]:
        return [
            f"{dataframe_name} = {dataframe_name}.head({config.get('n', 100)!r})"
        ]
