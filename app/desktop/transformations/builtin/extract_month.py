from __future__ import annotations

from typing import Any

import polars as pl

from app.desktop.transformations.base_transformation import BaseTransformation


class ExtractMonthTransformation(BaseTransformation):
    transformation_id = "extract_month"
    label = "Extract Month"
    description = "Extracts month from Date, Datetime or text date columns."

    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        column = config.get("column")
        new_column = config.get("new_column") or config.get("output_column") or f"{column}_month"
        date_format = config.get("format")

        if not column:
            raise ValueError("Missing required config: column")

        if column not in dataframe.columns:
            raise ValueError(f"Column '{column}' does not exist. Available columns: {dataframe.columns}")

        dtype = dataframe.schema[column]

        if dtype == pl.Date or isinstance(dtype, pl.Datetime):
            expr = pl.col(column).dt.month()
        elif dtype == pl.String or dtype == pl.Utf8:
            if date_format:
                expr = pl.col(column).str.to_date(format=date_format, strict=False).dt.month()
            else:
                expr = pl.col(column).str.to_date(strict=False).dt.month()
        else:
            expr = pl.col(column).cast(pl.String).str.to_date(strict=False).dt.month()

        return dataframe.with_columns(expr.alias(new_column))

    def to_python(self, config: Any = None, *args: Any, **kwargs: Any) -> str:
        real_config = config if isinstance(config, dict) else None

        if real_config is None:
            for item in args:
                if isinstance(item, dict):
                    real_config = item
                    break

        if real_config is None:
            real_config = kwargs.get("config") if isinstance(kwargs.get("config"), dict) else {}

        config = real_config

        column = config.get("column")
        new_column = config.get("new_column") or config.get("output_column") or f"{column}_month"
        date_format = config.get("format")

        if date_format:
            return (
                "df = df.with_columns(\n"
                f"    pl.col({column!r}).cast(pl.String).str.to_date(format={date_format!r}, strict=False).dt.month().alias({new_column!r})\n"
                ")"
            )

        return (
            "df = df.with_columns(\n"
            f"    pl.col({column!r}).cast(pl.String).str.to_date(strict=False).dt.month().alias({new_column!r})\n"
            ")"
        )
