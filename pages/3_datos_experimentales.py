import streamlit as st

from utils.ui import load_css, render_sidebar, render_response_summary, format_response_label


# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Datos Experimentales | RSM Primer Orden",
    page_icon="📂",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()
render_sidebar()


# =====================================================
# ENCABEZADO
# =====================================================

st.markdown(
    """
    <div class="page-header">
        <div class="page-title">📂 Datos Experimentales</div>
        <div class="page-subtitle">
            Validación de la base experimental registrada desde el diseño factorial.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# VALIDACIÓN DE DATOS
# =====================================================

if "model_data" not in st.session_state:

    st.warning(
        "No existen datos experimentales validados. "
        "Primero genere el diseño experimental y registre o simule la variable respuesta."
    )

    if st.button("Ir a Diseño Experimental", use_container_width=True):
        st.switch_page("pages/2_diseno_experimental.py")

else:

    model_df = st.session_state["model_data"]
    factor_cols = st.session_state["factor_cols"]
    response_col = st.session_state["response_col"]

    response_name = st.session_state.get("response_name", response_col)
    response_units = st.session_state.get("response_units", "")
    optimization_goal = st.session_state.get("optimization_goal", "Maximizar")

    response_label = format_response_label(response_name, response_units)

    st.success(
        "La base experimental fue recibida correctamente desde el módulo de Diseño Experimental. "
        "No es necesario cargar archivos externos."
    )

    # =====================================================
    # RESUMEN DE LA BASE
    # =====================================================

    st.markdown(
        '<div class="section-title">1. Resumen de datos experimentales</div>',
        unsafe_allow_html=True
    )

    m1, m2 = st.columns(2)

    with m1:
        st.metric("Observaciones", model_df.shape[0])

    with m2:
        st.metric("Factores", len(factor_cols))

    st.markdown("### Variable respuesta definida")

    response_label = render_response_summary(
        response_name=response_name,
        response_units=response_units,
        optimization_goal=optimization_goal
    )

    # =====================================================
    # BASE FINAL
    # =====================================================

    st.markdown(
        '<div class="section-title">2. Base final para modelamiento</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
            Esta base usa los factores codificados del diseño experimental y la variable respuesta registrada.
            Será utilizada para ajustar el modelo lineal de primer orden.
        </div>
        """,
        unsafe_allow_html=True
    )

    display_df = model_df.copy()

    if "Respuesta" in display_df.columns:
        display_df = display_df.rename(columns={"Respuesta": response_label})

    st.dataframe(
        display_df,
        use_container_width=True
    )

    # =====================================================
    # FACTORES IDENTIFICADOS
    # =====================================================

    st.markdown(
        '<div class="section-title">3. Factores identificados</div>',
        unsafe_allow_html=True
    )

    st.write(", ".join(factor_cols))

    with st.expander("Ver detalles técnicos de la base interna", expanded=False):
        st.markdown(
            """
            Internamente la aplicación conserva la columna de respuesta con el nombre `Respuesta`.
            Esto permite que los módulos de Modelo Lineal, ANOVA, Diagnóstico y Ascenso Más Pronunciado
            funcionen de forma consistente.
            """
        )
        st.dataframe(model_df, use_container_width=True)

    st.success(
        "Datos validados correctamente. El siguiente paso es ajustar el modelo lineal de primer orden."
    )

    if st.button("Continuar a Modelo Lineal", use_container_width=True):
        st.switch_page("pages/4_modelo_lineal.py")
