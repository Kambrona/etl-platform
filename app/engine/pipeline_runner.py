"""
Motor principal de ejecución de pipelines.
"""

from __future__ import annotations

from datetime import datetime

from app.engine.step_executor import StepExecutor
from app.models.execution import ExecutionContext, PipelineResult
from app.models.pipeline import Pipeline


class PipelineRunner:
    """
    Orquestador principal del pipeline.
    """

    def __init__(self):

        self.executor = StepExecutor()

    def run(
        self,
        pipeline: Pipeline,
    ) -> PipelineResult:

        context = ExecutionContext(
            pipeline_name=pipeline.name,
        )

        for step in pipeline.steps:

            self.executor.execute(
                context=context,
                step=step,
            )

        context.result.finished_at = datetime.now()

        return context.result