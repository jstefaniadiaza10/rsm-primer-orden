import streamlit as st

from utils.ui import load_css, render_sidebar

# ==========================================================
# Configuración general
# ==========================================================

st.set_page_config(
    page_title="RSM Primer Orden",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()
render_sidebar()


# ==========================================================
# Hero principal
# ==========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">Sistema de análisis experimental</div>
        <div class="hero-title">RSM Primer Orden</div>
        <div class="hero-subtitle">
            Aplicación para diseñar, analizar y optimizar experimentos de primer orden
            mediante Metodología de Superficie de Respuesta. Orientada a procesos
            agroindustriales y alimentarios.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# Métricas principales
# ==========================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-value">2ᵏ</div>
            <div class="metric-label">Diseños factoriales</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-value">1°</div>
            <div class="metric-label">Modelo de primer orden</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-value">ANOVA</div>
            <div class="metric-label">Validación estadística</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m4:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-value">RSM</div>
            <div class="metric-label">Ascenso más pronunciado</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# Accesos principales
# ==========================================================

st.markdown('<div class="section-title">Panel de trabajo</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Seleccione el módulo que desea utilizar dentro del flujo de análisis.</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">📐</div>
            <div class="card-title">Diseño experimental</div>
            <div class="card-text">
                Defina factores, niveles bajo y alto, número de puntos centrales
                y genere la matriz experimental codificada y real.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Abrir diseño experimental", use_container_width=True):
        st.switch_page("pages/2_diseno_experimental.py")

with c2:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">📂</div>
            <div class="card-title">Carga de datos</div>
            <div class="card-text">
                Importe archivos CSV o Excel, valide columnas, detecte datos faltantes
                y prepare la base experimental para el modelamiento.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Cargar datos", use_container_width=True):
        st.warning("Este módulo se implementará después del diseño experimental.")

with c3:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">📈</div>
            <div class="card-title">Modelo y ANOVA</div>
            <div class="card-text">
                Ajuste el modelo lineal, estime coeficientes, evalúe significancia,
                R², R² ajustado y tabla ANOVA.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Ajustar modelo", use_container_width=True):
        st.warning("Primero debe generarse o cargarse un diseño experimental.")


c4, c5, c6 = st.columns(3)

with c4:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">🔍</div>
            <div class="card-title">Diagnóstico</div>
            <div class="card-text">
                Analice residuos, normalidad, valores ajustados y consistencia
                del modelo antes de tomar decisiones.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.button("Ver diagnóstico")

with c5:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">📉</div>
            <div class="card-title">Pareto de efectos</div>
            <div class="card-text">
                Visualice la magnitud de efectos principales e interacciones
                para identificar los factores más influyentes.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.button("Ver Pareto")

with c6:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">🚀</div>
            <div class="card-title">Ascenso más pronunciado</div>
            <div class="card-text">
                Calcule la dirección de mejora y genere nuevos puntos experimentales
                recomendados dentro del proceso.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.button("Calcular ascenso")


# ==========================================================
# Flujo metodológico
# ==========================================================

st.markdown('<div class="section-title">Flujo metodológico</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">La aplicación sigue la secuencia formal de un análisis RSM de primer orden.</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.2, 1])

with left:
    st.markdown(
        """
        <div class="step-box">
            <div class="step-title">1. Definición del experimento</div>
            <div class="step-text">Selección de factores, niveles experimentales y puntos centrales.</div>
        </div>

        <div class="step-box">
            <div class="step-title">2. Generación del diseño factorial</div>
            <div class="step-text">Construcción automática de la matriz codificada y real.</div>
        </div>

        <div class="step-box">
            <div class="step-title">3. Ajuste del modelo de primer orden</div>
            <div class="step-text">Estimación de coeficientes mediante regresión lineal.</div>
        </div>

        <div class="step-box">
            <div class="step-title">4. Diagnóstico y validación</div>
            <div class="step-text">ANOVA, residuos, R², R² ajustado y significancia estadística.</div>
        </div>

        <div class="step-box">
            <div class="step-title">5. Recomendación operativa</div>
            <div class="step-text">Cálculo de la trayectoria de ascenso más pronunciado.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    st.markdown(
        """
        <div class="card" style="min-height: 360px;">
            <div class="card-icon">🧪</div>
            <div class="card-title">Caso aplicado sugerido</div>
            <div class="card-text">
                <b>Optimización del tostado de cacao Nacional ecuatoriano</b><br><br>
                Factores posibles:<br>
                • Temperatura de tostado<br>
                • Tiempo de tostado<br>
                • Humedad inicial<br><br>
                Respuesta posible:<br>
                • Puntaje sensorial<br>
                • Intensidad aromática<br>
                • Rendimiento del proceso<br><br>
                El sistema permitirá generar recomendaciones experimentales
                basadas en el modelo de primer orden.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# Estado final
# ==========================================================

st.markdown("---")

st.success("Interfaz profesional cargada correctamente. Siguiente módulo: generador de diseño experimental.")