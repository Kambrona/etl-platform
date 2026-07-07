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
from app.models.pipeline import Pipeline, Step


class PipelineLoader:
    """
    Carga pipelines desde archivos YAML o JSON.
    """

    SUPPORTED_EXTENSIONS = [".yaml", ".yml", ".json"]

    @staticmethod
    def load(path: str | Path) -> Pipeline:

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        suffix = path.suffix.lower()

        if suffix in [".yaml", ".yml"]:

            with open(path, "r", encoding="utf8") as f:
                data = yaml.safe_load(f)

        elif suffix == ".json":

            with open(path, "r", encoding="utf8") as f:
                data = json.load(f)

        else:
            raise ValueError(f"Formato no soportado: {suffix}")

        pipeline = Pipeline(
            name=data["name"],
            description=data.get("description", ""),
            version=data.get("version", "1.0"),
        )

        for step_data in data.get("steps", []):

            config = {
                k: v
                for k, v in step_data.items()
                if k not in ("name", "type")
            }

            pipeline.add_step(
                Step(
                    name=step_data["name"],
                    type=step_data["type"],
                    config=config,
                )
            )

        return pipeline