import app.transformations.readers.read_csv_step

from app.engine.pipeline_loader import PipelineLoader
from app.engine.pipeline_runner import PipelineRunner


def test_runner():

    pipeline = PipelineLoader.load(
        "pipelines/demo.yaml"
    )

    runner = PipelineRunner()

    context = runner.run(pipeline)

    df = context.get_dataframe("clientes")

    assert df is not None

    assert df.shape == (5, 4)