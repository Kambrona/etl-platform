"""
Modelos de dominio del Pipeline.

Estos modelos representan la estructura interna del sistema.
El objetivo es que el resto de la aplicación nunca trabaje
directamente con diccionarios provenientes del YAML.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Step:
    """
    Representa un paso del pipeline.
    """

    name: str
    type: str
    config: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Pipeline:
    """
    Representa un pipeline completo.
    """

    name: str
    description: str = ""
    version: str = "1.0"
    steps: list[Step] = field(default_factory=list)

    def add_step(self, step: Step) -> None:
        """
        Agrega un paso al pipeline.
        """
        self.steps.append(step)

    def get_step(self, name: str) -> Step | None:
        """
        Devuelve un paso por nombre.
        """
        for step in self.steps:
            if step.name == name:
                return step

        return None

    @property
    def total_steps(self) -> int:
        return len(self.steps)