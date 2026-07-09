from __future__ import annotations

from typing import Any

import polars as pl

from app.desktop.transformations.base_transformation import BaseTransformation


class ExtractYearTransformation(BaseTransformation):
    name = "extract_year"
    label = "Extract Year"
    description = "Extracts year from Date, Datetime or text date columns."

    def apply(self, df: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        column = config.get("column")
        output_column = config.get("output_column") or f"{column}_year"
        date_format = config.get("format")

        if not column:
            raise ValueError("Missing required config: column")

        if column not in df.columns:
            raise ValueError(f'Column "{column}" does not exist. Available columns: {df.columns}')

        dtype = df.schema[column]

        if dtype == pl.Date or dtype == pl.Datetime or dtype == pl.Time:
            expr = pl.col(column).dt.year()
        elif dtype == pl.Utf8 or dtype == pl.String:
            if date_format:
                expr = pl.col(column).str.to_date(format=date_format, strict=False).dt.year()
            else:
                expr = pl.col(column).str.to_date(strict=False).dt.year()
        else:
            expr = pl.col(column).cast(pl.Utf8).str.to_date(strict=False).dt.year()

        return df.with_columns(expr.alias(output_column))
