import app.transformations.readers.read_csv_step
import app.transformations.columns.rename_columns_step
import app.transformations.filters.filter_rows_step
import app.transformations.exports.export_parquet_step

from app.engine.pipeline_loader import PipelineLoader
from app.engine.pipeline_runner import PipelineRunner


def test_runner():

    pipeline = PipelineLoader.load("pipelines/demo.yaml")

    runner = PipelineRunner()
    context = runner.run(pipeline)

    df = context.get_dataframe("clientes_filtrados")

    assert df is not None
    assert df.shape == (3, 4)
    assert "cliente" in df.columns
    assert "ciudad_residencia" in df.columns