import app.transformations.no_op_step

from app.engine.pipeline_loader import PipelineLoader
from app.engine.pipeline_runner import PipelineRunner


def test_runner():

    pipeline = PipelineLoader.load(
        "pipelines/demo.yaml"
    )

    runner = PipelineRunner()

    result = runner.run(pipeline)

    assert result.success

    assert result.total_steps == 2