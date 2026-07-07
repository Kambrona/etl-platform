"""
Ejecutor de un paso del pipeline.
"""

from __future__ import annotations

import time

from app.engine.step_factory import StepFactory
from app.models.execution import ExecutionContext, StepResult
from app.models.pipeline import Step


class StepExecutor:
    """
    Ejecuta un paso y registra su resultado.
    """

    def execute(
        self,
        context: ExecutionContext,
        step: Step,
    ) -> StepResult:

        started = time.perf_counter()

        instance = StepFactory.create(step.type)

        instance.execute(context, step)

        elapsed = time.perf_counter() - started

        result = StepResult(
            step_name=step.name,
            success=True,
            duration=elapsed,
        )

        context.result.add_step(result)

        return result