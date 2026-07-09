import streamlit as st

from utils.ui import (
    load_css,
    render_sidebar,
    render_response_summary,
    format_response_label
)

from utils.diagnostics import (
    compute_diagnostic_metrics,
    create_residuals_vs_fitted_plot,
    create_histogram_residuals_plot,
    create_qq_plot,
    create_observed_vs_fitted_plot,
    interpret_diagnostics
)


# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Diagnóstico | RSM Primer Orden",
    page_icon="🔍",
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
        <div class="page-title">🔍 Diagnóstico del Modelo</div>
        <div class="page-subtitle">
            Evaluación gráfica y numérica de los residuos del modelo lineal de primer orden.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "El diagnóstico permite revisar si los residuos del modelo presentan un comportamiento razonable. "
    "En diseños experimentales pequeños, las pruebas estadísticas deben interpretarse con cautela."
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
    # RESUMEN
    # =====================================================

    st.markdown(
        '<div class="section-title">1. Resumen del diagnóstico</div>',
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

    metrics = compute_diagnostic_metrics(
        model_results=model_results,
        response_col=response_col
    )

    # =====================================================
    # MÉTRICAS DE RESIDUOS
    # =====================================================

    st.markdown(
        '<div class="section-title">2. Métricas de residuos</div>',
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("RMSE", f"{metrics['rmse']:.4f}")

    with m2:
        st.metric("MAE", f"{metrics['mae']:.4f}")

    with m3:
        st.metric("Residuo promedio", f"{metrics['mean_residual']:.4f}")

    with m4:
        st.metric("Máx. residuo absoluto", f"{metrics['max_abs_residual']:.4f}")

    m5, m6 = st.columns(2)

    with m5:
        if metrics["shapiro_p"] == metrics["shapiro_p"]:
            st.metric("Shapiro-Wilk p-valor", f"{metrics['shapiro_p']:.4f}")
        else:
            st.metric("Shapiro-Wilk p-valor", "No calculable")

    with m6:
        if metrics["durbin_watson"] == metrics["durbin_watson"]:
            st.metric("Durbin-Watson", f"{metrics['durbin_watson']:.4f}")
        else:
            st.metric("Durbin-Watson", "No calculable")

    st.markdown("### Interpretación automática")

    diagnostic_messages = interpret_diagnostics(metrics)

    for message in diagnostic_messages:
        st.write(f"- {message}")

    # =====================================================
    # GRÁFICOS
    # =====================================================

    st.markdown(
        '<div class="section-title">3. Gráficos de diagnóstico</div>',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "Residuos vs ajustados",
        "Normalidad",
        "Observados vs ajustados",
        "Tabla de residuos"
    ])

    with tab1:
        st.plotly_chart(
            create_residuals_vs_fitted_plot(model_results),
            use_container_width=True
        )

        st.markdown(
            """
            **Lectura:** los residuos deberían distribuirse aleatoriamente alrededor de cero.
            Si aparece una curva, embudo o patrón claro, puede existir falta de ajuste.
            """
        )

    with tab2:
        st.plotly_chart(
            create_histogram_residuals_plot(model_results),
            use_container_width=True
        )

        st.plotly_chart(
            create_qq_plot(model_results),
            use_container_width=True
        )

        st.markdown(
            """
            **Lectura:** en el gráfico QQ, los puntos deberían ubicarse aproximadamente
            sobre la línea de referencia. Desviaciones fuertes pueden indicar falta de normalidad.
            """
        )

    with tab3:
        st.plotly_chart(
            create_observed_vs_fitted_plot(
                model_results=model_results,
                response_col=response_col,
                response_label=response_label
            ),
            use_container_width=True
        )

        st.markdown(
            f"""
            **Lectura:** mientras más cerca estén los puntos de la línea diagonal,
            mejor es el ajuste entre los valores observados de **{response_label}**
            y los valores estimados por el modelo.
            """
        )

    with tab4:
        results_display = model_results["results_df"].copy()

        if "Respuesta" in results_display.columns:
            results_display = results_display.rename(
                columns={"Respuesta": response_label}
            )

        st.dataframe(
            results_display,
            use_container_width=True
        )

    # =====================================================
    # NAVEGACIÓN
    # =====================================================

    st.success(
        "Diagnóstico generado correctamente. El siguiente paso recomendado es construir el Pareto de efectos."
    )

    col_next, col_back = st.columns(2)

    with col_next:
        if st.button("Continuar a Pareto de efectos", use_container_width=True):
            st.switch_page("pages/7_pareto.py")

    with col_back:
        if st.button("Volver a ANOVA", use_container_width=True):
            st.switch_page("pages/5_anova.py")