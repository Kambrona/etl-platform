import streamlit as st

from app.ui.components.logs import render_logs
from app.ui.components.pipeline_view import render_pipeline
from app.ui.components.preview import render_preview
from app.ui.services.pipeline_service import PipelineService


st.set_page_config(
    page_title="ETL Platform",
    page_icon="⚙️",
    layout="wide",
)

st.title("⚙️ ETL Platform")
st.caption("MVP visual inspirado en Power Query")

pipeline_path = st.sidebar.text_input(
    "Pipeline YAML",
    value="pipelines/demo.yaml",
)

output_dataframe = st.sidebar.text_input(
    "Resultado a mostrar",
    value="clientes_filtrados",
)

run_button = st.sidebar.button("Ejecutar pipeline")

if run_button:
    pipeline, context = PipelineService.run_pipeline(pipeline_path)

    left, right = st.columns([1, 2])

    with left:
        render_pipeline(pipeline)
        render_logs(context)

    with right:
        render_preview(context, output_dataframe)

else:
    st.info("Selecciona un pipeline y presiona Ejecutar.")