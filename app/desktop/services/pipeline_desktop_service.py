from pathlib import Path
from typing import Any

import polars as pl
import yaml

from app.desktop.models.desktop_pipeline_state import DesktopPipelineState


class PipelineDesktopService:
    """Application service used by the desktop UI to manage pipelines."""

    def __init__(self) -> None:
        self.state = DesktopPipelineState()

    def create_pipeline(self, name: str = "Untitled Pipeline") -> DesktopPipelineState:
        """Create a new empty pipeline."""
        self.state = DesktopPipelineState(pipeline_name=name)
        return self.state

    def open_csv(self, path: Path) -> pl.DataFrame:
        """Open a CSV file and load a preview dataframe."""
        self.state.source_path = path
        self.state.pipeline_name = path.stem
        self.state.steps = [
            {
                "type": "read_csv",
                "name": "Read CSV",
                "config": {
                    "path": str(path),
                },
            }
        ]
        self.state.is_dirty = True
        return pl.read_csv(path)

    def open_excel(self, path: Path) -> pl.DataFrame:
        """Open an Excel file and load a preview dataframe."""
        self.state.source_path = path
        self.state.pipeline_name = path.stem
        self.state.steps = [
            {
                "type": "read_excel",
                "name": "Read Excel",
                "config": {
                    "path": str(path),
                },
            }
        ]
        self.state.is_dirty = True

        return pl.read_excel(path)

    def add_export_step(self, output_path: Path) -> None:
        """Add or update an export parquet step."""
        self.state.output_path = output_path

        export_step = {
            "type": "export_parquet",
            "name": "Export Parquet",
            "config": {
                "path": str(output_path),
            },
        }

        self.state.steps = [
            step for step in self.state.steps if step.get("type") != "export_parquet"
        ]
        self.state.steps.append(export_step)
        self.state.is_dirty = True

    def build_pipeline_document(self) -> dict[str, Any]:
        """Build a YAML serializable pipeline document."""
        return {
            "name": self.state.pipeline_name,
            "steps": self.state.steps,
        }

    def save_pipeline(self, path: Path) -> None:
        """Save the current pipeline as YAML."""
        document = self.build_pipeline_document()

        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            yaml.safe_dump(document, file, sort_keys=False, allow_unicode=True)

        self.state.pipeline_path = path
        self.state.is_dirty = False

    def load_pipeline(self, path: Path) -> DesktopPipelineState:
        """Load a pipeline YAML file."""
        with path.open("r", encoding="utf-8") as file:
            document = yaml.safe_load(file) or {}

        self.state = DesktopPipelineState(
            pipeline_path=path,
            pipeline_name=document.get("name", path.stem),
            steps=document.get("steps", []),
            is_dirty=False,
        )

        return self.state

    def preview_current_source(self, limit: int = 500) -> pl.DataFrame:
        """Return a preview for the current source file."""
        if self.state.source_path is None:
            return pl.DataFrame()

        suffix = self.state.source_path.suffix.lower()

        if suffix == ".csv":
            return pl.read_csv(self.state.source_path).head(limit)

        if suffix in {".xlsx", ".xls"}:
            return pl.read_excel(self.state.source_path).head(limit)

        return pl.DataFrame()

    def run_pipeline_preview_mode(self) -> pl.DataFrame:
        """
        Execute the currently supported desktop preview flow.

        This method intentionally stays simple in UI v1.0.
        Full engine execution remains delegated to the existing PipelineRunner
        in the following hito.
        """
        return self.preview_current_source()
    def add_transformation_step(self, step: dict[str, Any]) -> None:
        """Add a transformation step to the current pipeline."""
        export_steps = [
            current_step
            for current_step in self.state.steps
            if current_step.get("type") == "export_parquet"
        ]

        self.state.steps = [
            current_step
            for current_step in self.state.steps
            if current_step.get("type") != "export_parquet"
        ]

        self.state.steps.append(step)
        self.state.steps.extend(export_steps)
        self.state.is_dirty = True

    def apply_preview_transformations(self, dataframe: pl.DataFrame) -> pl.DataFrame:
        """Apply supported desktop transformations to a dataframe."""
        result = dataframe

        for step in self.state.steps:
            step_type = step.get("type")
            config = step.get("config", {})

            if step_type == "rename_columns":
                result = result.rename(config.get("columns", {}))

            elif step_type == "filter_rows":
                expression = config.get("expression")
                if expression:
                    result = result.sql(f"SELECT * FROM self WHERE {expression}")

            elif step_type == "select_columns":
                columns = config.get("columns", [])
                if columns:
                    result = result.select(columns)

            elif step_type == "drop_columns":
                columns = config.get("columns", [])
                if columns:
                    result = result.drop(columns)

        return result

    def run_pipeline_preview_mode(self) -> pl.DataFrame:
        """Execute the currently supported desktop preview flow."""
        dataframe = self.preview_current_source()
        return self.apply_preview_transformations(dataframe)