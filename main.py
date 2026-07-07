import app.transformations.readers.read_csv_step

from app.engine.pipeline_loader import PipelineLoader
from app.engine.pipeline_runner import PipelineRunner


def main():
    pipeline = PipelineLoader.load("pipelines/demo.yaml")

    runner = PipelineRunner()
    context = runner.run(pipeline)

    df = context.get_dataframe("clientes")

    print("\n=== ETL PLATFORM MVP ===")
    print(f"Pipeline: {pipeline.name}")
    print(f"Filas: {df.height}")
    print(f"Columnas: {df.width}")
    print("\nVista previa:")
    print(df)


if __name__ == "__main__":
    main()