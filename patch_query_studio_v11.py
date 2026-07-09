from pathlib import Path
import re

root = Path(".")

# ------------------------------------------------------------
# 1. Patch QueryController: dynamic columns from current pipeline
# ------------------------------------------------------------

qc_candidates = list(root.rglob("query_controller.py"))

if not qc_candidates:
    raise SystemExit("No se encontro query_controller.py")

qc_path = qc_candidates[0]
text = qc_path.read_text(encoding="utf-8")

# Replace direct preview_current_source column usage with current flow helper where possible.
text = text.replace(
    "self.source_controller.preview_current_source()",
    "self.preview_current_pipeline_result()"
)

text = text.replace(
    "source_controller.preview_current_source()",
    "self.preview_current_pipeline_result()"
)

if "def preview_current_pipeline_result" not in text:
    insert_after = re.search(r"class\s+QueryController\s*\([^)]*\):|class\s+QueryController\s*:", text)

    if insert_after:
        method = r'''

    def preview_current_pipeline_result(self):
        """
        Returns the dataframe at the current state of the active query.

        Important:
        This must be used by transformation dialogs to obtain dynamic columns.
        It intentionally does NOT read again from the raw source when steps exist.
        """
        if hasattr(self, "run_pipeline_preview_mode"):
            return self.run_pipeline_preview_mode()

        if hasattr(self, "pipeline_runner") and hasattr(self, "current_pipeline"):
            return self.pipeline_runner.run(self.current_pipeline)

        if hasattr(self, "runner") and hasattr(self, "current_pipeline"):
            return self.runner.run(self.current_pipeline)

        if hasattr(self, "source_controller"):
            return self.source_controller.preview_current_source()

        raise RuntimeError("No preview provider available for current pipeline.")
'''
        pos = text.find("\n", insert_after.end())
        text = text[:pos] + method + text[pos:]
    else:
        print("WARNING: No pude insertar preview_current_pipeline_result automaticamente.")

# If add_transformation explicitly builds columns from raw source, redirect common patterns.
text = re.sub(
    r"df\s*=\s*self\.source_controller\.preview_current_source\(\)",
    "df = self.preview_current_pipeline_result()",
    text
)

text = re.sub(
    r"preview_df\s*=\s*self\.source_controller\.preview_current_source\(\)",
    "preview_df = self.preview_current_pipeline_result()",
    text
)

text = re.sub(
    r"columns\s*=\s*self\.source_controller\.preview_current_source\(\)\.columns",
    "columns = self.preview_current_pipeline_result().columns",
    text
)

qc_path.write_text(text, encoding="utf-8")
print(f"Patched: {qc_path}")


# ------------------------------------------------------------
# 2. Patch extract_year / extract_month robust for Date, Datetime, String
# ------------------------------------------------------------

def patch_date_part(file_keyword: str, part: str):
    candidates = [
        p for p in root.rglob("*.py")
        if file_keyword in p.name.lower()
    ]

    if not candidates:
        print(f"WARNING: No encontre archivo para {file_keyword}")
        return

    path = candidates[0]
    original = path.read_text(encoding="utf-8")

    class_name = "ExtractYearTransformation" if part == "year" else "ExtractMonthTransformation"
    output_suffix = "year" if part == "year" else "month"
    dt_method = "year" if part == "year" else "month"

    replacement = f'''from __future__ import annotations

from typing import Any

import polars as pl

from app.desktop.transformations.base_transformation import BaseTransformation


class {class_name}(BaseTransformation):
    name = "extract_{output_suffix}"
    label = "Extract {output_suffix.capitalize()}"
    description = "Extracts {output_suffix} from Date, Datetime or text date columns."

    def apply(self, df: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        column = config.get("column")
        output_column = config.get("output_column") or f"{{column}}_{output_suffix}"
        date_format = config.get("format")

        if not column:
            raise ValueError("Missing required config: column")

        if column not in df.columns:
            raise ValueError(f'Column "{{column}}" does not exist. Available columns: {{df.columns}}')

        dtype = df.schema[column]

        if dtype == pl.Date or dtype == pl.Datetime or dtype == pl.Time:
            expr = pl.col(column).dt.{dt_method}()
        elif dtype == pl.Utf8 or dtype == pl.String:
            if date_format:
                expr = pl.col(column).str.to_date(format=date_format, strict=False).dt.{dt_method}()
            else:
                expr = pl.col(column).str.to_date(strict=False).dt.{dt_method}()
        else:
            expr = pl.col(column).cast(pl.Utf8).str.to_date(strict=False).dt.{dt_method}()

        return df.with_columns(expr.alias(output_column))
'''

    try:
        path.write_text(replacement, encoding="utf-8")
        print(f"Patched: {path}")
    except Exception as exc:
        path.write_text(original, encoding="utf-8")
        raise exc


patch_date_part("extract_year", "year")
patch_date_part("extract_month", "month")


# ------------------------------------------------------------
# 3. Add tests for robust date extraction where possible
# ------------------------------------------------------------

tests_dir = root / "tests"
tests_dir.mkdir(exist_ok=True)

test_path = tests_dir / "test_extract_date_parts.py"

test_path.write_text(r'''import polars as pl

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
''', encoding="utf-8")

print(f"Created: {test_path}")
