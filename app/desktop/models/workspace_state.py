from dataclasses import dataclass, field
from pathlib import Path

from app.desktop.models.data_source import DataSource
from app.desktop.models.desktop_pipeline_state import DesktopPipelineState


@dataclass
class WorkspaceState:
    """Represents the full desktop project workspace."""

    project_name: str = "Proyecto ETL"
    project_path: Path | None = None
    data_sources: list[DataSource] = field(default_factory=list)
    active_query: DesktopPipelineState = field(default_factory=DesktopPipelineState)
    is_dirty: bool = False

    def add_source(self, source: DataSource) -> None:
        existing_names = {item.name for item in self.data_sources}

        if source.name in existing_names:
            counter = 2
            base_name = source.name

            while f"{base_name}_{counter}" in existing_names:
                counter += 1

            source.name = f"{base_name}_{counter}"

        self.data_sources.append(source)
        self.is_dirty = True

    def get_source_by_name(self, name: str) -> DataSource | None:
        for source in self.data_sources:
            if source.name == name:
                return source

        return None
