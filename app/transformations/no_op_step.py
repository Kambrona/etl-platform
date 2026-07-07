"""
Paso de prueba.

No realiza ninguna transformación.
"""

from app.engine.base_step import BaseStep
from app.engine.step_registry import StepRegistry


class NoOpStep(BaseStep):

    def execute(self, context, step):

        context.log(
            f"Ejecutando paso '{step.name}'"
        )


StepRegistry.register(
    "noop",
    NoOpStep,
)