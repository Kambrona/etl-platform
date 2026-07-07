from pathlib import Path

import polars as pl

from app.desktop.services.pipeline_desktop_service import PipelineDesktopService


def test_create_pipeline_resets_state() -> None:
    service = PipelineDesktopService()

    state = service.create_pipeline("Demo Pipeline")

    assert state.pipeline_name == "Demo Pipeline"
    assert state.steps == []
    assert state.is_dirty is False


def test_open_csv_creates_read_step(tmp_path: Path) -> None:
    csv_path = tmp_path / "customers.csv"

    dataframe = pl.DataFrame(
        {
            "id": [1, 2],
            "name": ["A", "B"],
        }
    )
    dataframe.write_csv(csv_path)

    service = PipelineDesktopService()
    preview = service.open_csv(csv_path)

    assert preview.shape == (2, 2)
    assert service.state.source_path == csv_path
    assert service.state.pipeline_name == "customers"
    assert service.state.steps[0]["type"] == "read_csv"
    assert service.state.is_dirty is True


def test_save_pipeline_creates_yaml_file(tmp_path: Path) -> None:
    csv_path = tmp_path / "input.csv"
    pipeline_path = tmp_path / "pipeline.yaml"

    pl.DataFrame({"id": [1]}).write_csv(csv_path)

    service = PipelineDesktopService()
    service.open_csv(csv_path)
    service.save_pipeline(pipeline_path)

    assert pipeline_path.exists()
    assert service.state.pipeline_path == pipeline_path
    assert service.state.is_dirty is False

    content = pipeline_path.read_text(encoding="utf-8")

    assert "name: input" in content
    assert "type: read_csv" in content


def test_add_export_step_replaces_existing_export_step(tmp_path: Path) -> None:
    service = PipelineDesktopService()

    first_output = tmp_path / "first.parquet"
    second_output = tmp_path / "second.parquet"

    service.add_export_step(first_output)
    service.add_export_step(second_output)

    export_steps = [
        step for step in service.state.steps if step["type"] == "export_parquet"
    ]

    assert len(export_steps) == 1
    assert export_steps[0]["config"]["path"] == str(second_output)