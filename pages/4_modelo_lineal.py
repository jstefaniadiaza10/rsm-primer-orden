import streamlit as st

from utils.ui import (
    load_css,
    render_sidebar,
    render_response_summary,
    format_response_label
)
from utils.modeling import fit_first_order_model


# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Modelo Lineal | RSM Primer Orden",
    page_icon="📈",
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
        <div class="page-title">📈 Modelo Lineal de Primer Orden</div>
        <div class="page-subtitle">
            Ajuste del modelo lineal usando variables codificadas del diseño experimental.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "Este módulo ajusta un modelo de primer orden. "
    "No se incluyen términos cuadráticos porque corresponden a modelos de segundo orden."
)


# =====================================================
# VALIDACIÓN DE DATOS PREVIOS
# =====================================================

if "model_data" not in st.session_state:

    st.warning(
        "No existen datos experimentales validados. "
        "Primero genere el diseño experimental, registre o simule la variable respuesta "
        "y valide la base."
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

    # =====================================================
    # DATOS USADOS
    # =====================================================

    st.markdown(
        '<div class="section-title">1. Datos usados para el ajuste</div>',
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

    st.info(
        f"El modelo se ajustará para explicar la variable respuesta **{response_label}**. "
        f"El objetivo declarado por el usuario es **{optimization_goal.lower()}** esta respuesta."
    )

    with st.expander("Ver base experimental", expanded=False):
        display_df = model_df.copy()

        if "Respuesta" in display_df.columns:
            display_df = display_df.rename(columns={"Respuesta": response_label})

        st.dataframe(display_df, use_container_width=True)

    # =====================================================
    # AJUSTE DEL MODELO
    # =====================================================

    st.markdown(
        '<div class="section-title">2. Ajuste del modelo</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="section-subtitle">
            El modelo estimado tiene la forma:
            <b>{response_name} = β₀ + β₁X₁ + β₂X₂ + ... + error</b>,
            usando factores codificados en niveles -1, 0 y +1.
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Ajustar modelo lineal", use_container_width=True):

        try:
            with st.spinner("Ajustando modelo lineal..."):
                model_results = fit_first_order_model(
                    model_df=model_df,
                    factor_cols=factor_cols,
                    response_col=response_col,
                    response_label=response_name
                )

            st.session_state["model_results"] = model_results

            st.success("Modelo lineal ajustado correctamente.")

        except Exception as e:
            st.error(f"No se pudo ajustar el modelo: {e}")

    # =====================================================
    # RESULTADOS
    # =====================================================

    if "model_results" in st.session_state:

        model_results = st.session_state["model_results"]

        st.markdown(
            '<div class="section-title">3. Resultados del modelo</div>',
            unsafe_allow_html=True
        )

        st.markdown("### Ecuación estimada")

        st.code(model_results["equation"], language="text")

        r1, r2, r3, r4 = st.columns(4)

        with r1:
            st.metric("R²", f"{model_results['r2']:.4f}")

        with r2:
            st.metric("R² ajustado", f"{model_results['r2_adj']:.4f}")

        with r3:
            st.metric("AIC", f"{model_results['aic']:.2f}")

        with r4:
            st.metric("BIC", f"{model_results['bic']:.2f}")

        st.markdown("### Coeficientes estimados")

        coef_df = model_results["coef_df"].copy()

        st.dataframe(
            coef_df,
            use_container_width=True
        )

        st.markdown("### Valores ajustados y residuos")

        results_display = model_results["results_df"].copy()

        if "Respuesta" in results_display.columns:
            results_display = results_display.rename(
                columns={"Respuesta": response_label}
            )

        st.dataframe(
            results_display,
            use_container_width=True
        )

        st.success(
            "Modelo ajustado correctamente. El siguiente paso es revisar el ANOVA "
            "y luego los diagnósticos del modelo."
        )

        col_anova, col_diag = st.columns(2)

        with col_anova:
            if st.button("Continuar a ANOVA", use_container_width=True):
                st.switch_page("pages/5_anova.py")

        with col_diag:
           if st.button("Continuar a Diagnóstico", use_container_width=True):
                st.switch_page("pages/6_diagnostico.py")