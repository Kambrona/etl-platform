from app.desktop.transformations.builtin.change_type import ChangeTypeTransformation
from app.desktop.transformations.builtin.drop_columns import DropColumnsTransformation
from app.desktop.transformations.builtin.extract_month import ExtractMonthTransformation
from app.desktop.transformations.builtin.extract_year import ExtractYearTransformation
from app.desktop.transformations.builtin.fill_null import FillNullTransformation
from app.desktop.transformations.builtin.filter_rows import FilterRowsTransformation
from app.desktop.transformations.builtin.limit_rows import LimitRowsTransformation
from app.desktop.transformations.builtin.lowercase import LowercaseTransformation
from app.desktop.transformations.builtin.promote_headers import PromoteHeadersTransformation
from app.desktop.transformations.builtin.remove_duplicates import RemoveDuplicatesTransformation
from app.desktop.transformations.builtin.rename_columns import RenameColumnsTransformation
from app.desktop.transformations.builtin.replace_value import ReplaceValueTransformation
from app.desktop.transformations.builtin.round_number import RoundNumberTransformation
from app.desktop.transformations.builtin.select_columns import SelectColumnsTransformation
from app.desktop.transformations.builtin.sort_rows import SortRowsTransformation
from app.desktop.transformations.builtin.trim import TrimTransformation
from app.desktop.transformations.builtin.uppercase import UppercaseTransformation
from app.desktop.transformations.transformation_registry import TransformationRegistry


def build_default_transformation_registry() -> TransformationRegistry:
    """Build the default desktop transformation registry."""
    registry = TransformationRegistry()

    registry.register(PromoteHeadersTransformation())
    registry.register(ChangeTypeTransformation())
    registry.register(RenameColumnsTransformation())
    registry.register(SelectColumnsTransformation())
    registry.register(DropColumnsTransformation())

    registry.register(FilterRowsTransformation())
    registry.register(SortRowsTransformation())
    registry.register(RemoveDuplicatesTransformation())
    registry.register(LimitRowsTransformation())

    registry.register(UppercaseTransformation())
    registry.register(LowercaseTransformation())
    registry.register(TrimTransformation())
    registry.register(ReplaceValueTransformation())
    registry.register(FillNullTransformation())

    registry.register(RoundNumberTransformation())

    registry.register(ExtractYearTransformation())
    registry.register(ExtractMonthTransformation())

    return registry
