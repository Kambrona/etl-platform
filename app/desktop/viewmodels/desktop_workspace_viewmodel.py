from dataclasses import dataclass, field
from pathlib import Path

from app.desktop.models.data_source import DataSource
from app.desktop.models.desktop_pipeline_state import DesktopPipelineState


@dataclass
class DesktopWorkspaceViewModel:
    """View model for the desktop workspace."""

    project_name: str = "Proyecto ETL"
    project_path: Path | None = None
    data_sources: list[DataSource] = field(default_factory=list)
    active_query: DesktopPipelineState = field(default_factory=DesktopPipelineState)
    is_dirty: bool = False
