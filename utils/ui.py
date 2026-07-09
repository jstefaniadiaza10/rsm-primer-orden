import streamlit as st
from pathlib import Path
from html import escape


def load_css(file_path: str = "assets/css/styles.css") -> None:
    css_path = Path(file_path)

    if css_path.exists():
        with open(css_path, encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            """
            <div style="padding: 18px 8px 8px 8px;">
                <div style="font-size: 30px; font-weight: 800;">RSM</div>
                <div style="font-size: 15px; opacity: 0.85;">Primer Orden</div>
                <hr style="border: 0.5px solid rgba(255,255,255,0.22);">
            </div>
            """,
            unsafe_allow_html=True
        )

        st.page_link("app.py", label="🏠 Inicio")
        st.page_link("pages/2_diseno_experimental.py", label="📐 Diseño Experimental")
        st.page_link("pages/3_datos_experimentales.py", label="📂 Datos Experimentales")
        st.page_link("pages/4_modelo_lineal.py", label="📈 Modelo Lineal")
        st.page_link("pages/5_anova.py", label="📊 ANOVA")
        st.page_link("pages/6_diagnostico.py", label="🔍 Diagnóstico")
        st.page_link("pages/7_pareto.py", label="📉 Pareto")
        st.page_link("pages/8_ascenso.py", label="🚀 Ascenso Más Pronunciado")
        st.page_link("pages/9_reporte.py", label="📄 Reporte")

        st.markdown(
            """

            <hr style="border: 0.5px solid rgba(255,255,255,0.22); margin-top: 25px;">

            <div style="font-size: 12px; opacity: 0.75; padding-left: 8px;">
                Versión 1.0<br>
                Ingeniería Estadística
            </div>
            """,
            unsafe_allow_html=True
        )

def format_response_label(response_name: str, response_units: str = "") -> str:
    """
    Construye el nombre visible de la variable respuesta.
    """

    response_name = response_name or "Respuesta"
    response_units = response_units or ""

    if response_units.strip():
        return f"{response_name} ({response_units})"

    return response_name


def render_response_summary(
    response_name: str,
    response_units: str = "",
    optimization_goal: str = "Maximizar"
) -> str:
    """
    Muestra la variable respuesta en tarjetas compactas.
    Evita usar st.metric porque agranda demasiado el texto.
    """

    response_label = format_response_label(response_name, response_units)

    st.markdown(
        f"""
        <div class="response-grid">
            <div class="response-card">
                <div class="response-card-title">Variable respuesta</div>
                <div class="response-card-value">{escape(response_name)}</div>
            </div>
            <div class="response-card">
                <div class="response-card-title">Unidad</div>
                <div class="response-card-value">{escape(response_units) if response_units else "No especificada"}</div>
            </div>
            <div class="response-card">
                <div class="response-card-title">Objetivo</div>
                <div class="response-card-value">{escape(optimization_goal)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    return response_label