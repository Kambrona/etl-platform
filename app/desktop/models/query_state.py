from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class QueryState:
    """Represents a single query/transformation pipeline for a data source.
    
    This allows maintaining independent transformation chains for each source,
    which can be combined later via joins.
    """

    query_id: str  # Unique identifier for this query (e.g., "source_1", "source_2")
    source_name: str  # Name of the data source
    source_path: Path
    source_type: str  # CSV, Excel, Parquet
    sheet_name: str | None = None
    steps: list[dict[str, Any]] = field(default_factory=list)
    is_dirty: bool = False

    @property
    def display_name(self) -> str:
        """Display name for the query in UI."""
        if self.sheet_name:
            return f"{self.source_name} ({self.sheet_name})"
        return self.source_name
