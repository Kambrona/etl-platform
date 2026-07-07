from app.engine.pipeline_loader import PipelineLoader


def test_loader():

    pipeline = PipelineLoader.load("pipelines/demo.yaml")

    assert pipeline.name == "Demo Pipeline"

    assert pipeline.total_steps == 2

    assert pipeline.steps[0].name == "leer_csv"

    assert pipeline.steps[1].type == "export"