"""
Clase base para todos los pasos del motor ETL.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.execution import ExecutionContext
from app.models.pipeline import Step


class BaseStep(ABC):
    """
    Clase base para todas las transformaciones.

    Cada transformación debe implementar execute().
    """

    @abstractmethod
    def execute(
        self,
        context: ExecutionContext,
        step: Step,
    ) -> None:
        """
        Ejecuta el paso.

        Parameters
        ----------
        context
            Estado completo de la ejecución.

        step
            Definición del paso.
        """
        raise NotImplementedError