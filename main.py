import app.transformations.readers.read_csv_step
import app.transformations.columns.rename_columns_step
import app.transformations.filters.filter_rows_step
import app.transformations.exports.export_parquet_step

from app.engine.pipeline_loader import PipelineLoader
from app.engine.pipeline_runner import PipelineRunner


def main():
    pipeline = PipelineLoader.load("pipelines/demo.yaml")

    runner = PipelineRunner()
    context = runner.run(pipeline)

    df = context.get_dataframe("clientes_filtrados")

    print("\n=== ETL PLATFORM MVP ===")
    print(f"Pipeline: {pipeline.name}")
    print(f"Filas finales: {df.height}")
    print(f"Columnas finales: {df.width}")
    print("\nResultado:")
    print(df)
    print("\nArchivo generado:")
    print("output/clientes_filtrados.parquet")


if __name__ == "__main__":
    main()