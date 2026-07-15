from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.desktop.models.query_state import QueryState


@dataclass
class DesktopPipelineState:
    """Represents the current desktop pipeline editing state.
    
    Now supports multiple independent data sources with their own
    transformation chains, allowing for joins while preserving
    individual source transformations.
    """

    pipeline_path: Path | None = None
    pipeline_name: str = "Untitled Pipeline"
    
    # Multi-source support
    queries: dict[str, QueryState] = field(default_factory=dict)  # {query_id: QueryState}
    active_query_id: str | None = None  # Currently selected query
    
    # Final pipeline steps (joins, final transformations, etc.)
    final_steps: list[dict[str, Any]] = field(default_factory=list)
    
    # Export configuration
    output_path: Path | None = None
    export_config: dict[str, Any] = field(default_factory=dict)  # Format, path, credentials, etc.
    last_result_path: Path | None = None
    
    is_dirty: bool = False

    @property
    def active_query(self) -> QueryState | None:
        """Get the currently active query."""
        if self.active_query_id and self.active_query_id in self.queries:
            return self.queries[self.active_query_id]
        return None

    def get_source_path(self) -> Path | None:
        """Get the source path of the active query."""
        if active := self.active_query:
            return active.source_path
        return None

    def get_steps(self) -> list[dict[str, Any]]:
        """Get steps from active query."""
        if active := self.active_query:
            return active.steps
        return []

    def set_steps(self, steps: list[dict[str, Any]]) -> None:
        """Set steps for active query."""
        if active := self.active_query:
            active.steps = steps
            active.is_dirty = True
            self.is_dirty = True

    # Backwards compatibility properties
    @property
    def source_path(self) -> Path | None:
        return self.get_source_path()

    @source_path.setter
    def source_path(self, value: Path | None) -> None:
        # This is set when activating a source, handled elsewhere
        pass

    @property
    def steps(self) -> list[dict[str, Any]]:
        return self.get_steps()

    @steps.setter
    def steps(self, value: list[dict[str, Any]]) -> None:
        self.set_steps(value)
