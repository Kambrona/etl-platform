from __future__ import annotations

from typing import Any

import polars as pl

from app.desktop.transformations.base_transformation import BaseTransformation


class ExtractMonthTransformation(BaseTransformation):
    name = "extract_month"
    label = "Extract Month"
    description = "Extracts month from Date, Datetime or text date columns."

    def apply(self, df: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        column = config.get("column")
        output_column = config.get("output_column") or f"{column}_month"
        date_format = config.get("format")

        if not column:
            raise ValueError("Missing required config: column")

        if column not in df.columns:
            raise ValueError(f'Column "{column}" does not exist. Available columns: {df.columns}')

        dtype = df.schema[column]

        if dtype == pl.Date or dtype == pl.Datetime or dtype == pl.Time:
            expr = pl.col(column).dt.month()
        elif dtype == pl.Utf8 or dtype == pl.String:
            if date_format:
                expr = pl.col(column).str.to_date(format=date_format, strict=False).dt.month()
            else:
                expr = pl.col(column).str.to_date(strict=False).dt.month()
        else:
            expr = pl.col(column).cast(pl.Utf8).str.to_date(strict=False).dt.month()

        return df.with_columns(expr.alias(output_column))
