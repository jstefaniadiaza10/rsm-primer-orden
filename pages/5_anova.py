import streamlit as st

from utils.ui import (
    load_css,
    render_sidebar,
    render_response_summary,
    format_response_label
)
from utils.anova_tools import compute_regression_anova, interpret_anova


# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="ANOVA | RSM Primer Orden",
    page_icon="📊",
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
        <div class="page-title">📊 ANOVA del Modelo Lineal</div>
        <div class="page-subtitle">
            Evaluación de la significancia global del modelo de primer orden.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "El ANOVA permite evaluar si el modelo lineal explica una proporción significativa "
    "de la variabilidad observada en la variable respuesta."
)


# =====================================================
# VALIDACIÓN
# =====================================================

if "model_results" not in st.session_state:

    st.warning(
        "No existe un modelo ajustado. Primero debe completar el módulo Modelo Lineal."
    )

    if st.button("Ir a Modelo Lineal", use_container_width=True):
        st.switch_page("pages/4_modelo_lineal.py")

else:

    model_results = st.session_state["model_results"]
    response_col = st.session_state.get("response_col", "Respuesta")

    response_name = st.session_state.get("response_name", response_col)
    response_units = st.session_state.get("response_units", "")
    optimization_goal = st.session_state.get("optimization_goal", "Maximizar")

    response_label = format_response_label(response_name, response_units)

    # =====================================================
    # RESUMEN DEL MODELO
    # =====================================================

    st.markdown(
        '<div class="section-title">1. Resumen del modelo</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.metric("R²", f"{model_results['r2']:.4f}")

    with c2:
        st.metric("R² ajustado", f"{model_results['r2_adj']:.4f}")

    st.markdown("### Variable respuesta definida")

    response_label = render_response_summary(
        response_name=response_name,
        response_units=response_units,
        optimization_goal=optimization_goal
    )

    st.info(
        f"El ANOVA evalúa si los factores experimentales explican significativamente "
        f"la variabilidad de **{response_label}**."
    )

    with st.expander("Ver ecuación estimada", expanded=False):
        st.code(model_results["equation"], language="text")

    # =====================================================
    # ANOVA
    # =====================================================

    st.markdown(
        '<div class="section-title">2. Tabla ANOVA</div>',
        unsafe_allow_html=True
    )

    alpha = st.selectbox(
        "Nivel de significancia",
        options=[0.01, 0.05, 0.10],
        index=1
    )

    anova_df = compute_regression_anova(
        model_results=model_results,
        response_col=response_col
    )

    st.session_state["anova_df"] = anova_df

    st.dataframe(
        anova_df.style.format({
            "SC": "{:.4f}",
            "CM": "{:.4f}",
            "F": "{:.4f}",
            "p-valor": "{:.4f}"
        }),
        use_container_width=True
    )

    interpretation = interpret_anova(
        anova_df,
        alpha=alpha,
        response_label=response_name
    )

    if interpretation["decision"] == "Modelo significativo":
        st.success(interpretation["message"])
    elif interpretation["decision"] == "Modelo no significativo":
        st.warning(interpretation["message"])
    else:
        st.error(interpretation["message"])

    # =====================================================
    # LECTURA ESTADÍSTICA
    # =====================================================

    st.markdown(
        '<div class="section-title">3. Lectura estadística</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        La tabla ANOVA descompone la variabilidad total de **{response_label}** en:

        - **Variabilidad explicada por el modelo**: parte atribuible a los factores experimentales.
        - **Variabilidad residual o error**: parte no explicada por el modelo.
        - **Variabilidad total**: variabilidad observada en la variable respuesta.

        Un p-valor pequeño indica que el modelo de primer orden tiene capacidad explicativa
        sobre **{response_label}**.
        """
    )

    with st.expander("Interpretación técnica de las columnas", expanded=False):
        st.markdown(
            """
            - **SC**: suma de cuadrados.
            - **GL**: grados de libertad.
            - **CM**: cuadrado medio.
            - **F**: estadístico de prueba.
            - **p-valor**: probabilidad asociada al estadístico F bajo la hipótesis nula.

            La hipótesis nula global del ANOVA es que todos los coeficientes de los factores
            son iguales a cero. Si el p-valor es menor que el nivel de significancia seleccionado,
            se concluye que el modelo tiene efecto global significativo.
            """
        )

    col_next, col_back = st.columns(2)

    with col_next:
        if st.button("Continuar a Diagnóstico", use_container_width=True):
            st.switch_page("pages/6_diagnostico.py")

    with col_back:
        if st.button("Volver a Modelo Lineal", use_container_width=True):
            st.switch_page("pages/4_modelo_lineal.py")