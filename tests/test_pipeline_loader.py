from app.engine.pipeline_loader import PipelineLoader


def test_loader():

    pipeline = PipelineLoader.load("pipelines/demo.yaml")

    assert pipeline.name == "Demo Pipeline"
    assert pipeline.total_steps == 4

    assert pipeline.steps[0].type == "read_csv"
    assert pipeline.steps[1].type == "rename_columns"
    assert pipeline.steps[2].type == "filter_rows"
    assert pipeline.steps[3].type == "export_parquet"