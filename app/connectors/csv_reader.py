"""
Conector para lectura de archivos CSV.
"""

from pathlib import Path

import polars as pl


class CsvReader:

    @staticmethod
    def read(path: str, **kwargs) -> pl.DataFrame:

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        return pl.read_csv(path, **kwargs)