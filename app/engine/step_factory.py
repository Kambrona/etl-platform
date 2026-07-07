"""
Factory para crear instancias de pasos.
"""

from __future__ import annotations

from app.engine.step_registry import StepRegistry
from app.engine.base_step import BaseStep


class StepFactory:
    """
    Crea instancias de pasos registrados.
    """

    @staticmethod
    def create(step_type: str) -> BaseStep:
        step_class = StepRegistry.get(step_type)
        return step_class()
    