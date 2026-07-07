import streamlit as st


def render_preview(context, dataframe_name: str):
    st.subheader("Vista previa")

    df = context.get_dataframe(dataframe_name)

    if df is None:
        st.warning("No hay datos para mostrar.")
        return

    st.write(f"Filas: {df.height} | Columnas: {df.width}")
    st.dataframe(df.to_pandas(), use_container_width=True)