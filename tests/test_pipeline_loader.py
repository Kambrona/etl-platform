from app.engine.pipeline_loader import PipelineLoader


def test_loader():

    pipeline = PipelineLoader.load("pipelines/demo.yaml")

    assert pipeline.name == "Demo Pipeline"
    assert pipeline.total_steps == 1

    assert pipeline.steps[0].name == "clientes"
    assert pipeline.steps[0].type == "read_csv"