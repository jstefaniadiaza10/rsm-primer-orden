import streamlit as st

from utils.ui import (
    load_css,
    render_sidebar,
    render_response_summary,
    format_response_label
)

from utils.report_tools import (
    build_executive_summary,
    create_excel_report
)
from utils.pdf_report import create_management_pdf_report

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Reporte | RSM Primer Orden",
    page_icon="📄",
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
        <div class="page-title">📄 Reporte Ejecutivo</div>
        <div class="page-subtitle">
            Consolidación final de resultados del análisis experimental de primer orden.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "Este módulo consolida las principales salidas del aplicativo en un reporte ejecutivo "
    "y permite descargar un respaldo en Excel."
)


# =====================================================
# VALIDACIÓN GENERAL
# =====================================================

if "model_results" not in st.session_state:

    st.warning(
        "Todavía no existe un modelo ajustado. Primero complete el flujo mínimo: "
        "Diseño Experimental → Datos Experimentales → Modelo Lineal."
    )

    if st.button("Ir a Diseño Experimental", use_container_width=True, key="btn_report_to_design"):
        st.switch_page("pages/2_diseno_experimental.py")

else:

    response_col = st.session_state.get("response_col", "Respuesta")
    response_name = st.session_state.get("response_name", response_col)
    response_units = st.session_state.get("response_units", "")
    optimization_goal = st.session_state.get("optimization_goal", "Maximizar")

    response_label = format_response_label(response_name, response_units)

    factor_summary = st.session_state.get("factor_summary")
    coded_design = st.session_state.get("coded_design")
    real_design = st.session_state.get("real_design")
    model_data = st.session_state.get("model_data")
    model_results = st.session_state.get("model_results")
    anova_df = st.session_state.get("anova_df")
    effects_df = st.session_state.get("effects_df")
    steepest_direction_df = st.session_state.get("steepest_direction_df")
    steepest_path_df = st.session_state.get("steepest_path_df")

    # =====================================================
    # RESUMEN
    # =====================================================

    st.markdown(
        '<div class="section-title">1. Resumen del estudio</div>',
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
    # ESTADO DE MÓDULOS
    # =====================================================

    st.markdown(
        '<div class="section-title">2. Estado de módulos completados</div>',
        unsafe_allow_html=True
    )

    status_rows = [
        {"Módulo": "Diseño experimental", "Estado": "Completado" if coded_design is not None else "Pendiente"},
        {"Módulo": "Datos experimentales", "Estado": "Completado" if model_data is not None else "Pendiente"},
        {"Módulo": "Modelo lineal", "Estado": "Completado" if model_results is not None else "Pendiente"},
        {"Módulo": "ANOVA", "Estado": "Completado" if anova_df is not None else "Pendiente"},
        {"Módulo": "Pareto de efectos", "Estado": "Completado" if effects_df is not None else "Pendiente"},
        {"Módulo": "Ascenso más pronunciado", "Estado": "Completado" if steepest_path_df is not None else "Pendiente"},
    ]

    st.dataframe(
        status_rows,
        use_container_width=True
    )

    # =====================================================
    # RESUMEN EJECUTIVO
    # =====================================================

    st.markdown(
        '<div class="section-title">3. Resumen ejecutivo generado</div>',
        unsafe_allow_html=True
    )

    executive_summary = build_executive_summary(
        response_label=response_label,
        optimization_goal=optimization_goal,
        model_results=model_results,
        anova_df=anova_df,
        effects_df=effects_df,
        steepest_path_df=steepest_path_df
    )

    st.markdown(executive_summary)

    # =====================================================
    # DESCARGAS
    # =====================================================

    st.markdown(
        '<div class="section-title">4. Descargas</div>',
        unsafe_allow_html=True
    )

    excel_output = create_excel_report(
        factor_summary=factor_summary,
        coded_design=coded_design,
        real_design=real_design,
        model_data=model_data,
        model_results=model_results,
        anova_df=anova_df,
        effects_df=effects_df,
        steepest_direction_df=steepest_direction_df,
        steepest_path_df=steepest_path_df,
        executive_summary=executive_summary
    )

    pdf_output = create_management_pdf_report(
        response_label=response_label,
        optimization_goal=optimization_goal,
        factor_summary=factor_summary,
        coded_design=coded_design,
        real_design=real_design,
        model_data=model_data,
        model_results=model_results,
        anova_df=anova_df,
        effects_df=effects_df,
        steepest_direction_df=steepest_direction_df,
        steepest_path_df=steepest_path_df
    )

    col_pdf, col_excel, col_md = st.columns(3)

    with col_pdf:
        st.download_button(
            label="Descargar PDF gerencial",
            data=pdf_output,
            file_name="reporte_gerencial_rsm_primer_orden.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="download_pdf_management_report"
        )

    with col_excel:
        st.download_button(
            label="Descargar respaldo Excel",
            data=excel_output,
            file_name="reporte_rsm_primer_orden.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="download_excel_report"
        )

    with col_md:
        st.download_button(
            label="Descargar resumen TXT",
            data=executive_summary.encode("utf-8"),
            file_name="resumen_ejecutivo_rsm.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_txt_report"
        )

    # =====================================================
    # CIERRE METODOLÓGICO
    # =====================================================

    st.markdown(
        '<div class="section-title">5. Cierre metodológico</div>',
        unsafe_allow_html=True
    )

    st.success(
        "El análisis de primer orden está completo. La app permite diseñar el experimento, "
        "registrar o simular la respuesta, ajustar el modelo, evaluar ANOVA, revisar diagnóstico, "
        "priorizar efectos y proponer una ruta de mejora."
    )

    st.warning(
        "Si la ruta de ascenso más pronunciado deja de mejorar la respuesta, metodológicamente "
        "se recomienda construir un nuevo diseño alrededor de la mejor región encontrada. "
        "Los modelos cuadráticos no se implementan porque están fuera del alcance de primer orden."
    )

    col_back, col_home = st.columns(2)

    with col_back:
        if st.button("Volver a Ascenso Más Pronunciado", use_container_width=True, key="btn_report_to_ascenso"):
            st.switch_page("pages/8_ascenso.py")

    with col_home:
        if st.button("Volver al inicio", use_container_width=True, key="btn_report_to_home"):
            st.switch_page("app.py")