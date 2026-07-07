"""
Modelos de ejecución del motor ETL.

Estos objetos contienen el estado de una ejecución completa
de un pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class StepResult:
    """
    Resultado de la ejecución de un paso.
    """

    step_name: str
    success: bool
    duration: float = 0.0
    rows: int = 0
    message: str = ""


@dataclass(slots=True)
class PipelineResult:
    """
    Resultado general del pipeline.
    """

    success: bool = True

    started_at: datetime = field(default_factory=datetime.now)

    finished_at: datetime | None = None

    steps: list[StepResult] = field(default_factory=list)

    def add_step(self, result: StepResult):

        self.steps.append(result)

    @property
    def total_steps(self):

        return len(self.steps)


@dataclass(slots=True)
class ExecutionContext:
    """
    Estado de ejecución.
    """

    pipeline_name: str

    dataframes: dict[str, Any] = field(default_factory=dict)

    variables: dict[str, Any] = field(default_factory=dict)

    cache: dict[str, Any] = field(default_factory=dict)

    metrics: dict[str, Any] = field(default_factory=dict)

    logs: list[str] = field(default_factory=list)

    result: PipelineResult = field(default_factory=PipelineResult)

    def log(self, message: str):

        self.logs.append(message)

    def set_dataframe(self, name: str, dataframe: Any):

        self.dataframes[name] = dataframe

    def get_dataframe(self, name: str):

        return self.dataframes.get(name)

    def set_variable(self, name: str, value: Any):

        self.variables[name] = value

    def get_variable(self, name: str):

        return self.variables.get(name)