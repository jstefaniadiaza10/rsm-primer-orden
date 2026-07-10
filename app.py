import streamlit as st

from utils.ui import load_css, render_sidebar


st.set_page_config(
    page_title="RSM Primer Orden",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()
render_sidebar()


# =========================================================
# PORTADA PRINCIPAL
# =========================================================

st.markdown(
    """
    <div class="hero-container">
        <div class="hero-badge">Aplicativo académico de Diseño Experimental</div>
        <div class="hero-title">RSM Primer Orden</div>
        <div class="hero-subtitle">
            Plataforma interactiva para construir diseños experimentales, cargar datos propios,
            ajustar modelos lineales de primer orden, evaluar ANOVA, diagnosticar residuos,
            identificar factores relevantes y proponer una ruta de mejora experimental.
        </div>
        <div class="hero-footer">
            <div class="hero-chip">Diseños factoriales 2ᵏ</div>
            <div class="hero-chip">Modelo lineal</div>
            <div class="hero-chip">ANOVA</div>
            <div class="hero-chip">Pareto de efectos</div>
            <div class="hero-chip">Ascenso más pronunciado</div>
            <div class="hero-chip">Reporte PDF</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# ACCIONES PRINCIPALES
# =========================================================

st.markdown("## ¿Cómo desea comenzar?")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown(
        """
        <div class="landing-card">
            <div class="landing-card-title">📐 Crear un diseño experimental nuevo</div>
            <div class="landing-card-text">
                Use esta opción si todavía no tiene una tabla experimental.
                La app generará automáticamente el diseño factorial, puntos centrales
                y plantilla para registrar la respuesta.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Comenzar con diseño experimental",
        type="primary",
        use_container_width=True,
        key="home_start_design"
    ):
        st.switch_page("pages/2_diseno_experimental.py")


with col_b:
    st.markdown(
        """
        <div class="landing-card">
            <div class="landing-card-title">📂 Cargar datos existentes</div>
            <div class="landing-card-text">
                Use esta opción si ya tiene una tabla en Excel o CSV con una variable
                respuesta Y y factores experimentales X1, X2, X3. La app puede trabajar
                con datos en unidades reales y codificarlos internamente.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Cargar tabla de datos",
        use_container_width=True,
        key="home_upload_data"
    ):
        st.switch_page("pages/3_datos_experimentales.py")


st.divider()


# =========================================================
# GUÍA PASO A PASO
# =========================================================

st.markdown("## Guía rápida para usar la app")

st.markdown(
    """
    Esta aplicación tiene dos rutas de uso. Elija la que corresponda según su situación.
    """
)

guide_col1, guide_col2 = st.columns(2)

with guide_col1:
    st.markdown("### Ruta A: todavía no tengo datos")

    st.markdown(
        """
        <div class="step-box">
            <div class="step-title">Paso 1. Definir el diseño</div>
            <div class="step-text">
                Ingrese factores, niveles bajo y alto, puntos centrales y variable respuesta.
            </div>
        </div>

        <div class="step-box">
            <div class="step-title">Paso 2. Registrar o simular respuestas</div>
            <div class="step-text">
                Complete la respuesta observada o use simulación para probar el flujo.
            </div>
        </div>

        <div class="step-box">
            <div class="step-title">Paso 3. Ajustar el modelo</div>
            <div class="step-text">
                La app estima el modelo lineal de primer orden con factores codificados.
            </div>
        </div>

        <div class="step-box">
            <div class="step-title">Paso 4. Analizar y reportar</div>
            <div class="step-text">
                Revise ANOVA, diagnóstico, Pareto, ascenso más pronunciado y descargue el reporte.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with guide_col2:
    st.markdown("### Ruta B: ya tengo una tabla de datos")

    st.markdown(
        """
        <div class="step-box">
            <div class="step-title">Paso 1. Subir Excel o CSV</div>
            <div class="step-text">
                Cargue su tabla con columnas como Y, X1, X2, X3.
            </div>
        </div>

        <div class="step-box">
            <div class="step-title">Paso 2. Seleccionar variables</div>
            <div class="step-text">
                Indique cuál columna es la respuesta y cuáles son los factores.
            </div>
        </div>

        <div class="step-box">
            <div class="step-title">Paso 3. Codificar factores</div>
            <div class="step-text">
                Si sus factores están en unidades reales, la app calcula la escala -1, 0, +1.
            </div>
        </div>

        <div class="step-box">
            <div class="step-title">Paso 4. Continuar el análisis</div>
            <div class="step-text">
                Pase al modelo lineal, ANOVA, diagnóstico, Pareto, ascenso y reporte.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# =========================================================
# ESTADO ACTUAL DEL ANÁLISIS
# =========================================================

st.markdown("## Estado actual del análisis")

has_data = "model_data" in st.session_state
has_model = "model_results" in st.session_state
has_anova = "anova_df" in st.session_state
has_effects = "effects_df" in st.session_state
has_steepest = "steepest_path_df" in st.session_state

status_cols = st.columns(5)

with status_cols[0]:
    st.metric("Datos", "Listo" if has_data else "Pendiente")

with status_cols[1]:
    st.metric("Modelo", "Listo" if has_model else "Pendiente")

with status_cols[2]:
    st.metric("ANOVA", "Listo" if has_anova else "Pendiente")

with status_cols[3]:
    st.metric("Pareto", "Listo" if has_effects else "Pendiente")

with status_cols[4]:
    st.metric("Ascenso", "Listo" if has_steepest else "Pendiente")


if has_data:
    st.success("Ya existe una base experimental activa. Puede continuar con el análisis.")
    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
        if st.button(
            "Ir a Modelo Lineal",
            use_container_width=True,
            key="home_continue_model"
        ):
            st.switch_page("pages/4_modelo_lineal.py")

    with col_m2:
        if st.button(
            "Ir a Reporte",
            use_container_width=True,
            key="home_continue_report"
        ):
            st.switch_page("pages/9_reporte.py")

    with col_m3:
        if st.button(
            "Revisar datos",
            use_container_width=True,
            key="home_continue_data"
        ):
            st.switch_page("pages/3_datos_experimentales.py")
else:
    st.info(
        "Aún no existe una base experimental activa. Para iniciar, cree un diseño experimental "
        "o cargue una tabla de datos existente."
    )


st.divider()


# =========================================================
# FORMATO DE DATOS
# =========================================================

st.markdown("## ¿Cómo debe ingresar sus datos el usuario?")

st.markdown(
    """
    El usuario puede ingresar una tabla en **Excel** o **CSV**.  
    La estructura esperada es una columna para la respuesta `Y` y varias columnas para los factores `X`.
    """
)

st.dataframe(
    {
        "Puntaje_Sensorial_Y": [82.4, 85.1, 78.9, 88.3, 80.2, 86.7],
        "Temperatura_C_X1": [120, 130, 120, 130, 120, 130],
        "Tiempo_min_X2": [25, 25, 35, 35, 25, 35],
        "Humedad_pct_X3": [8, 8, 8, 8, 10, 10],
    },
    use_container_width=True
)

st.info(
    "No es obligatorio que el usuario cargue los factores ya codificados. "
    "Puede cargar unidades reales como °C, minutos, porcentaje, presión o concentración. "
    "La app los transforma internamente usando: x = (X - centro) / semirango."
)


# =========================================================
# EJEMPLOS
# =========================================================

st.divider()

st.markdown("## Ejemplos de aplicación")

ex1, ex2, ex3 = st.columns(3)

with ex1:
    st.markdown(
        """
        <div class="landing-card">
            <div class="landing-card-title">🍫 Tostado de cacao</div>
            <div class="landing-card-text">
                <b>Factores:</b> temperatura, tiempo, humedad inicial.<br>
                <b>Respuesta:</b> puntaje sensorial.<br>
                <b>Objetivo:</b> maximizar calidad.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with ex2:
    st.markdown(
        """
        <div class="landing-card">
            <div class="landing-card-title">🌾 Secado de granos</div>
            <div class="landing-card-text">
                <b>Factores:</b> temperatura, tiempo, velocidad de aire.<br>
                <b>Respuesta:</b> humedad final.<br>
                <b>Objetivo:</b> minimizar humedad.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with ex3:
    st.markdown(
        """
        <div class="landing-card">
            <div class="landing-card-title">⚙️ Proceso industrial</div>
            <div class="landing-card-text">
                <b>Factores:</b> presión, temperatura, velocidad.<br>
                <b>Respuesta:</b> rendimiento.<br>
                <b>Objetivo:</b> maximizar producción.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("")

with st.expander("Ver más ejemplos"):
    st.markdown(
        """
        <span class="example-pill">Fermentación</span>
        <span class="example-pill">Extracción de aceite</span>
        <span class="example-pill">Formulación de alimentos</span>
        <span class="example-pill">Tratamiento térmico</span>
        <span class="example-pill">Optimización de mezcla simple</span>
        <span class="example-pill">Control de calidad</span>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# TRANSPARENCIA
# =========================================================

st.divider()

st.markdown("## Transparencia académica")

st.write(
    "El proyecto incluye una declaración explícita sobre el uso de inteligencia artificial "
    "como apoyo técnico y académico."
)

st.page_link(
    "pages/10_declaracion_ia.py",
    label="🤖 Ver declaración de uso de Inteligencia Artificial"
)