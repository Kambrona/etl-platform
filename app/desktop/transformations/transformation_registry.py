from app.desktop.transformations.base_transformation import BaseTransformation


class TransformationRegistry:
    """Registry for desktop transformations."""

    def __init__(self) -> None:
        self._items: dict[str, BaseTransformation] = {}

    def register(self, transformation: BaseTransformation) -> None:
        self._items[transformation.transformation_id] = transformation

    def get(self, transformation_id: str) -> BaseTransformation:
        if transformation_id not in self._items:
            raise ValueError(f"Transformation not registered: {transformation_id}")

        return self._items[transformation_id]

    def exists(self, transformation_id: str) -> bool:
        return transformation_id in self._items

    def all(self) -> list[BaseTransformation]:
        return list(self._items.values())
