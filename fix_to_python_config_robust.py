from pathlib import Path

for path in [
    Path("app/desktop/transformations/builtin/extract_year.py"),
    Path("app/desktop/transformations/builtin/extract_month.py"),
]:
    text = path.read_text(encoding="utf-8")

    text = text.replace(
'''    def to_python(self, config: dict[str, Any], *args: Any, **kwargs: Any) -> str:
        column = config.get("column")
        new_column = config.get("new_column") or config.get("output_column") or f"{column}_''',
'''    def to_python(self, config: Any = None, *args: Any, **kwargs: Any) -> str:
        real_config = config if isinstance(config, dict) else None

        if real_config is None:
            for item in args:
                if isinstance(item, dict):
                    real_config = item
                    break

        if real_config is None:
            real_config = kwargs.get("config") if isinstance(kwargs.get("config"), dict) else {}

        config = real_config

        column = config.get("column")
        new_column = config.get("new_column") or config.get("output_column") or f"{column}_'''
    )

    path.write_text(text, encoding="utf-8")
    print(f"Patched: {path}")
