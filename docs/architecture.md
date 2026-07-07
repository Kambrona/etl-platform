# ETL Platform Architecture

## Objetivo

Construir una plataforma ETL/ELT visual, modular y de alto rendimiento, inspirada en Power Query, pero diseñada para ser más rápida, escalable y automatizable.

## Principios

- Modularidad.
- Separación de responsabilidades.
- Ejecución por pasos.
- Caché incremental.
- Soporte futuro para DAG.
- Transformaciones extensibles mediante registro de pasos.
- Backend primero; UI desacoplada.
- Cada módulo debe tener pruebas.

## Arquitectura general

```mermaid
graph TD
    A[Pipeline YAML/JSON] --> B[PipelineLoader]
    B --> C[Pipeline Domain Model]
    C --> D[PipelineRunner]
    D --> E[ExecutionContext]
    D --> F[StepRegistry]
    F --> G[BaseStep]
    G --> H[Readers]
    G --> I[Transformations]
    G --> J[Exports]
    D --> K[CacheManager]
    D --> L[LogManager]
    J --> M[Files / SQL / DuckDB]