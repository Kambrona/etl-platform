from pathlib import Path

files = {
    Path("app/desktop/transformations/builtin/extract_year.py"): ("ExtractYearTransformation", "year", "year"),
    Path("app/desktop/transformations/builtin/extract_month.py"): ("ExtractMonthTransformation", "month", "month"),
}

template = '''from __future__ import annotations

from typing import Any

import polars as pl

from app.desktop.transformations.base_transformation import BaseTransformation


class {class_name}(BaseTransformation):
    name = "extract_{suffix}"
    label = "Extract {label}"
    description = "Extracts {suffix} from Date, Datetime or text date columns."

    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        column = config.get("column")
        new_column = config.get("new_column") or config.get("output_column") or f"{{column}}_{suffix}"
        date_format = config.get("format")

        if not column:
            raise ValueError("Missing required config: column")

        if column not in dataframe.columns:
            raise ValueError(f"Column '{{column}}' does not exist. Available columns: {{dataframe.columns}}")

        dtype = dataframe.schema[column]

        if dtype == pl.Date or isinstance(dtype, pl.Datetime):
            expr = pl.col(column).dt.{method}()
        elif dtype == pl.String or dtype == pl.Utf8:
            if date_format:
                expr = pl.col(column).str.to_date(format=date_format, strict=False).dt.{method}()
            else:
                expr = pl.col(column).str.to_date(strict=False).dt.{method}()
        else:
            expr = pl.col(column).cast(pl.String).str.to_date(strict=False).dt.{method}()

        return dataframe.with_columns(expr.alias(new_column))
'''

for path, (class_name, suffix, method) in files.items():
    if not path.exists():
        raise SystemExit(f"No existe: {path}")

    path.write_text(
        template.format(
            class_name=class_name,
            suffix=suffix,
            label=suffix.capitalize(),
            method=method,
        ),
        encoding="utf-8",
    )
    print(f"Patched real file: {path}")
