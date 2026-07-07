from app.engine.pipeline_loader import PipelineLoader


def test_loader():

    pipeline = PipelineLoader.load("pipelines/demo.yaml")

    assert pipeline["name"] == "Demo Pipeline"

    assert len(pipeline["steps"]) == 2
    