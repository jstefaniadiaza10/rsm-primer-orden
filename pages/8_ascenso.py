import streamlit as st

from utils.ui import (
    load_css,
    render_sidebar,
    render_response_summary,
    format_response_label
)

from utils.steepest_tools import (
    compute_steepest_path,
    create_steepest_response_plot,
    create_direction_plot,
    interpret_steepest_path
)


# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Ascenso Más Pronunciado | RSM Primer Orden",
    page_icon="🚀",
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
        <div class="page-title">🚀 Ascenso Más Pronunciado</div>
        <div class="page-subtitle">
            Propuesta de nuevas corridas experimentales en la dirección de mayor mejora.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "En RSM de primer orden, el ascenso más pronunciado usa los coeficientes del modelo lineal "
    "para proponer una ruta experimental hacia mejores condiciones del proceso."
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

elif "factors" not in st.session_state:

    st.warning(
        "No se encontró la información de niveles reales de los factores. "
        "Regrese al módulo de Diseño Experimental y genere nuevamente el diseño."
    )

    if st.button("Ir a Diseño Experimental", use_container_width=True):
        st.switch_page("pages/2_diseno_experimental.py")

else:

    model_results = st.session_state["model_results"]
    factor_cols = st.session_state["factor_cols"]
    factors = st.session_state["factors"]

    response_col = st.session_state.get("response_col", "Respuesta")
    response_name = st.session_state.get("response_name", response_col)
    response_units = st.session_state.get("response_units", "")
    optimization_goal = st.session_state.get("optimization_goal", "Maximizar")

    response_label = format_response_label(response_name, response_units)

    # =====================================================
    # RESUMEN
    # =====================================================

    st.markdown(
        '<div class="section-title">1. Resumen del análisis</div>',
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

    # =====================================================
    # PARÁMETROS DE LA RUTA
    # =====================================================

    st.markdown(
        '<div class="section-title">2. Configuración de la ruta</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
            Configure cuántas corridas desea proponer y qué tamaño de paso usar
            sobre la escala codificada del diseño.
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.container(border=True):

        p1, p2, p3 = st.columns(3)

        with p1:
            start_point = st.selectbox(
                "Punto inicial",
                options=[
                    "Centro del diseño",
                    "Mejor corrida observada"
                ],
                index=0,
                help="El método clásico parte del centro del diseño. También puede partir desde la mejor corrida observada."
            )

        with p2:
            n_steps = st.number_input(
                "Número de pasos propuestos",
                min_value=3,
                max_value=15,
                value=6,
                step=1
            )

        with p3:
            coded_step = st.number_input(
                "Tamaño de paso codificado",
                min_value=0.05,
                max_value=2.00,
                value=0.25,
                step=0.05,
                help="El factor de mayor influencia cambiará este valor por cada paso."
            )

    try:
        path_df, direction_df = compute_steepest_path(
            model_results=model_results,
            factor_cols=factor_cols,
            factors=factors,
            optimization_goal=optimization_goal,
            n_steps=int(n_steps),
            coded_step=float(coded_step),
            start_point=start_point,
            response_col=response_col
        )

        st.session_state["steepest_path_df"] = path_df
        st.session_state["steepest_direction_df"] = direction_df

        # =====================================================
        # DIRECCIÓN
        # =====================================================

        st.markdown(
            '<div class="section-title">3. Dirección de mejora</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            direction_df.style.format({
                "Coeficiente": "{:.4f}",
                "Dirección normalizada": "{:.4f}",
                "Cambio codificado por paso": "{:.4f}"
            }),
            use_container_width=True
        )

        st.plotly_chart(
            create_direction_plot(direction_df),
            use_container_width=True
        )

        # =====================================================
        # RUTA PROPUESTA
        # =====================================================

        st.markdown(
            '<div class="section-title">4. Corridas experimentales propuestas</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            path_df.style.format("{:.4f}"),
            use_container_width=True
        )

        st.plotly_chart(
            create_steepest_response_plot(
                path_df=path_df,
                response_label=response_label
            ),
            use_container_width=True
        )

        st.warning(
            "Algunos pasos pueden quedar fuera de la región experimental original. "
            "Esto es normal en el ascenso más pronunciado, pero las nuevas corridas deben validarse "
            "según seguridad, costo y factibilidad del proceso."
        )

        # =====================================================
        # INTERPRETACIÓN
        # =====================================================

        st.markdown(
            '<div class="section-title">5. Interpretación automática</div>',
            unsafe_allow_html=True
        )

        messages = interpret_steepest_path(
            direction_df=direction_df,
            response_label=response_label,
            optimization_goal=optimization_goal
        )

        for message in messages:
            st.write(f"- {message}")

        # =====================================================
        # SIGUIENTE PASO METODOLÓGICO
        # =====================================================

        st.markdown(
            '<div class="section-title">6. Siguiente decisión experimental</div>',
            unsafe_allow_html=True
        )

        st.success(
            "La ruta de mejora fue generada correctamente. En un estudio real, el investigador "
            "debe ejecutar las corridas propuestas, registrar la nueva respuesta observada y decidir "
            "si continúa avanzando o si necesita construir un nuevo diseño alrededor de la mejor zona encontrada."
        )

        st.info(
            "Si la respuesta deja de mejorar en los pasos propuestos, eso indica que el modelo de primer orden "
            "ya no es suficiente y podría requerirse un diseño de segundo orden. En esta aplicación se deja como "
            "recomendación metodológica, sin implementar modelos cuadráticos."
        )

        col_report, col_back, col_home = st.columns(3)

        with col_report:
            if st.button(
                "Continuar a Reporte",
                use_container_width=True,
                key="btn_ascenso_to_reporte"
            ):
                st.switch_page("pages/9_reporte.py")

        with col_back:
            if st.button(
                "Volver a Pareto",
                use_container_width=True,
                key="btn_ascenso_to_pareto"
            ):
                st.switch_page("pages/7_pareto.py")

    except Exception as e:
        st.error(f"No se pudo generar la ruta de ascenso más pronunciado: {e}")