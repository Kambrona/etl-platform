import polars as pl

from app.desktop.transformations.builtin.extract_year import ExtractYearTransformation
from app.desktop.transformations.builtin.extract_month import ExtractMonthTransformation


def test_extract_year_from_date():
    df = pl.DataFrame({"date": ["2024-05-10"]}).with_columns(
        pl.col("date").str.to_date()
    )

    result = ExtractYearTransformation().apply(
        df,
        {"column": "date", "output_column": "year"},
    )

    assert result["year"].to_list() == [2024]


def test_extract_month_from_date():
    df = pl.DataFrame({"date": ["2024-05-10"]}).with_columns(
        pl.col("date").str.to_date()
    )

    result = ExtractMonthTransformation().apply(
        df,
        {"column": "date", "output_column": "month"},
    )

    assert result["month"].to_list() == [5]


def test_extract_year_from_text():
    df = pl.DataFrame({"date": ["2024-05-10"]})

    result = ExtractYearTransformation().apply(
        df,
        {"column": "date", "output_column": "year"},
    )

    assert result["year"].to_list() == [2024]


def test_extract_month_from_text():
    df = pl.DataFrame({"date": ["2024-05-10"]})

    result = ExtractMonthTransformation().apply(
        df,
        {"column": "date", "output_column": "month"},
    )

    assert result["month"].to_list() == [5]
