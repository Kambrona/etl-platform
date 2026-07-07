import pytest

from app.engine.step_registry import StepRegistry
from app.exceptions import StepNotRegisteredException


def test_step_not_registered():

    with pytest.raises(StepNotRegisteredException):
        StepRegistry.get("paso_inexistente")