"""
Registro de transformaciones disponibles.
"""

from __future__ import annotations

from typing import Type

from app.engine.base_step import BaseStep


class StepRegistry:
    """
    Registro central de pasos.
    """

    _registry: dict[str, Type[BaseStep]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        step_class: Type[BaseStep],
    ) -> None:

        cls._registry[name] = step_class

    @classmethod
    def get(
        cls,
        name: str,
    ) -> Type[BaseStep]:

        if name not in cls._registry:
            raise ValueError(
                f"No existe el paso '{name}'."
            )

        return cls._registry[name]

    @classmethod
    def available_steps(cls):

        return sorted(cls._registry.keys())