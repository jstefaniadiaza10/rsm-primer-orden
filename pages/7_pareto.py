import streamlit as st

from utils.ui import (
    load_css,
    render_sidebar,
    render_response_summary,
    format_response_label
)

from utils.pareto_tools import (
    compute_effects_table,
    create_pareto_plot,
    create_signed_effects_plot,
    interpret_effects
)


# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Pareto de Efectos | RSM Primer Orden",
    page_icon="📉",
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
        <div class="page-title">📉 Pareto de Efectos</div>
        <div class="page-subtitle">
            Identificación de los factores con mayor influencia sobre la variable respuesta.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "El Pareto de efectos permite priorizar los factores más importantes del modelo lineal. "
    "En variables codificadas, el efecto principal se calcula como 2 veces el coeficiente estimado."
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
    # TABLA DE EFECTOS
    # =====================================================

    st.markdown(
        '<div class="section-title">2. Tabla de efectos principales</div>',
        unsafe_allow_html=True
    )

    effects_df = compute_effects_table(model_results)

    st.session_state["effects_df"] = effects_df

    st.dataframe(
        effects_df.style.format({
            "Coeficiente": "{:.4f}",
            "Error estándar": "{:.4f}",
            "t": "{:.4f}",
            "p-valor": "{:.4f}",
            "Efecto estimado": "{:.4f}",
            "Efecto absoluto": "{:.4f}",
            "Importancia relativa (%)": "{:.2f}"
        }),
        use_container_width=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
            El efecto estimado representa el cambio esperado al pasar un factor
            desde su nivel bajo (-1) hasta su nivel alto (+1), manteniendo los demás factores constantes.
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # GRÁFICOS
    # =====================================================

    st.markdown(
        '<div class="section-title">3. Visualización de efectos</div>',
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs([
        "Pareto de efectos absolutos",
        "Efectos con signo"
    ])

    with tab1:
        st.plotly_chart(
            create_pareto_plot(
                effects_df=effects_df,
                response_label=response_label
            ),
            use_container_width=True
        )

        st.markdown(
            """
            **Lectura:** mientras mayor sea la barra, mayor es la influencia del factor
            sobre la variable respuesta, sin considerar si el efecto aumenta o disminuye la respuesta.
            """
        )

    with tab2:
        st.plotly_chart(
            create_signed_effects_plot(
                effects_df=effects_df,
                response_label=response_label
            ),
            use_container_width=True
        )

        st.markdown(
            """
            **Lectura:** los efectos positivos indican que al aumentar el factor también aumenta
            la respuesta. Los efectos negativos indican que al aumentar el factor la respuesta disminuye.
            """
        )

    # =====================================================
    # INTERPRETACIÓN
    # =====================================================

    st.markdown(
        '<div class="section-title">4. Interpretación automática</div>',
        unsafe_allow_html=True
    )

    messages = interpret_effects(
        effects_df=effects_df,
        response_label=response_label,
        optimization_goal=optimization_goal
    )

    for message in messages:
        st.write(f"- {message}")

    # =====================================================
    # RECOMENDACIÓN OPERATIVA
    # =====================================================

    st.markdown(
        '<div class="section-title">5. Recomendación preliminar</div>',
        unsafe_allow_html=True
    )

    recommendation_df = effects_df[[
        "Ranking",
        "Parámetro",
        "Efecto estimado",
        "Dirección",
        "Importancia relativa (%)"
    ]].copy()

    if optimization_goal == "Maximizar":
        recommendation_df["Conveniencia"] = recommendation_df["Efecto estimado"].apply(
            lambda x: "Favorable" if x > 0 else "No favorable"
        )
    else:
        recommendation_df["Conveniencia"] = recommendation_df["Efecto estimado"].apply(
            lambda x: "Favorable" if x < 0 else "No favorable"
        )

    st.dataframe(
        recommendation_df.style.format({
            "Efecto estimado": "{:.4f}",
            "Importancia relativa (%)": "{:.2f}"
        }),
        use_container_width=True
    )

    st.warning(
        "Esta recomendación es preliminar. Para proponer una dirección de mejora del proceso, "
        "se debe continuar con el módulo de Ascenso Más Pronunciado."
    )

        # =====================================================
    # NAVEGACIÓN
    # =====================================================

    col_next, col_back = st.columns(2)

    with col_next:
        if st.button(
            "Continuar a Ascenso Más Pronunciado",
            use_container_width=True,
            key="btn_pareto_to_ascenso"
        ):
            st.switch_page("pages/8_ascenso.py")

    with col_back:
        if st.button(
            "Volver a Diagnóstico",
            use_container_width=True,
            key="btn_pareto_to_diagnostico"
        ):
            st.switch_page("pages/6_diagnostico.py")