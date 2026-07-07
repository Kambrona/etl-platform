import streamlit as st


def render_logs(context):
    st.subheader("Ejecución")

    for step in context.result.steps:
        status = "✅" if step.success else "❌"
        st.write(f"{status} {step.step_name} — {step.duration:.4f} s")