import streamlit as st

from utils.ui import load_css, render_sidebar
from utils.ai_disclosure import get_ai_disclosure_markdown, get_ai_tools_df


st.set_page_config(
    page_title="Declaración de uso de IA",
    page_icon="🤖",
    layout="wide"
)

load_css()
render_sidebar()

st.markdown(
    """
    <div class="page-header">
        <div class="page-title">Declaración de uso de Inteligencia Artificial</div>
        <div class="page-subtitle">
            Transparencia académica sobre el uso de herramientas de IA en el desarrollo del aplicativo.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(get_ai_disclosure_markdown())

st.markdown("### Herramientas utilizadas")

ai_tools_df = get_ai_tools_df()

st.dataframe(
    ai_tools_df,
    use_container_width=True,
    hide_index=True
)

st.info(
    "Esta declaración forma parte de la transparencia metodológica del proyecto y puede ser "
    "incluida también en el informe final o presentación académica."
)