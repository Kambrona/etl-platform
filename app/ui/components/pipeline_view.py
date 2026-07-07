import streamlit as st


def render_pipeline(pipeline):
    st.subheader("Pipeline")

    for index, step in enumerate(pipeline.steps, start=1):
        st.markdown(f"**{index}. {step.name}**")
        st.caption(f"Tipo: `{step.type}`")

        if index < len(pipeline.steps):
            st.markdown("↓")