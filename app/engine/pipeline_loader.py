"""
Pipeline Loader

Responsabilidad:
----------------
Leer archivos YAML o JSON y convertirlos en un diccionario Python.

Autor:
ETL Platform

Versión:
0.1
"""

from pathlib import Path
from typing import Dict, Any

import json
import yaml


class PipelineLoader:
    """
    Carga pipelines desde archivos YAML o JSON.
    """

    SUPPORTED_EXTENSIONS = [".yaml", ".yml", ".json"]

    @staticmethod
    def load(path: str | Path) -> Dict[str, Any]:
        """
        Carga un pipeline.

        Parameters
        ----------
        path : str | Path

        Returns
        -------
        dict
        """

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"No existe el archivo: {path}")

        suffix = path.suffix.lower()

        if suffix not in PipelineLoader.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Formato no soportado: {suffix}"
            )

        if suffix in [".yaml", ".yml"]:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)