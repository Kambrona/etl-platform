import app.transformations.readers.read_csv_step
import app.transformations.columns.rename_columns_step
import app.transformations.filters.filter_rows_step
import app.transformations.exports.export_parquet_step

from app.engine.pipeline_loader import PipelineLoader
from app.engine.pipeline_runner import PipelineRunner


class PipelineService:

    @staticmethod
    def run_pipeline(path: str):
        pipeline = PipelineLoader.load(path)
        runner = PipelineRunner()
        context = runner.run(pipeline)
        return pipeline, context