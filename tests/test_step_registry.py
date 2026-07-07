import app.transformations.no_op_step

from app.engine.step_registry import StepRegistry


def test_registry():

    step = StepRegistry.get("noop")

    assert step is not None

    assert "noop" in StepRegistry.available_steps()