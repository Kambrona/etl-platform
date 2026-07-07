from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class DesktopPipelineState:
    """Represents the current desktop pipeline editing state."""

    pipeline_path: Path | None = None
    source_path: Path | None = None
    output_path: Path | None = None
    pipeline_name: str = "Untitled Pipeline"
    steps: list[dict[str, Any]] = field(default_factory=list)
    last_result_path: Path | None = None
    is_dirty: bool = False