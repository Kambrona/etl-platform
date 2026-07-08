from abc import ABC, abstractmethod
from typing import Any

import polars as pl


class BaseTransformation(ABC):
    """Base class for desktop transformations."""

    transformation_id: str
    display_name: str
    category: str

    @abstractmethod
    def apply(self, dataframe: pl.DataFrame, config: dict[str, Any]) -> pl.DataFrame:
        """Apply the transformation to a dataframe."""

    @abstractmethod
    def to_python(self, dataframe_name: str, config: dict[str, Any]) -> list[str]:
        """Generate Python code for this transformation."""
