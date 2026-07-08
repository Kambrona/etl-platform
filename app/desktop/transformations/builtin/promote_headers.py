from typing import Any
import polars as pl
from app.desktop.transformations.base_transformation import BaseTransformation


class PromoteHeadersTransformation(BaseTransformation):
    transformation_id = "promote_headers"
    display_name = "Promote First Row as Headers"
    category = "Preparación"

    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        if dataframe.height == 0:
            return dataframe

        first_row = dataframe.row(0)
        old_columns = dataframe.columns
        new_columns = []
        used = set()

        for index, value in enumerate(first_row):
            name = str(value).strip() if value is not None else f"Column_{index + 1}"
            if not name:
                name = f"Column_{index + 1}"

            base = name
            counter = 2
            while name in used:
                name = f"{base}_{counter}"
                counter += 1

            used.add(name)
            new_columns.append(name)

        return dataframe.slice(1).rename(dict(zip(old_columns, new_columns)))

    def to_python(self, dataframe_name: str, config: dict[str, Any]) -> list[str]:
        return [
            "first_row = df.row(0)",
            "new_columns = [str(value).strip() if value is not None else f'Column_{index + 1}' for index, value in enumerate(first_row)]",
            f"{dataframe_name} = {dataframe_name}.slice(1).rename(dict(zip({dataframe_name}.columns, new_columns)))",
        ]
