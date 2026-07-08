from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataSource:
    """Represents a data source loaded in the desktop workspace."""

    name: str
    path: Path
    source_type: str
    sheet_name: str | None = None

    @property
    def display_name(self) -> str:
        if self.sheet_name:
            return f"{self.name} / {self.sheet_name} ({self.source_type})"

        return f"{self.name} ({self.source_type})"
