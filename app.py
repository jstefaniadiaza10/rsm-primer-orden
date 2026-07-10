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

st.markdown(
    """
    <div class="page-header">
        <div class="page-title">RSM Primer Orden</div>
        <div class="page-subtitle">
            Aplicativo interactivo para diseñar, analizar y documentar experimentos de primer orden.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    ### ¿Qué hace esta aplicación?

    Esta app permite aplicar una metodología completa de **Superficie de Respuesta de Primer Orden**:

    - Crear un diseño experimental factorial.
    - Registrar o cargar datos experimentales.
    - Ajustar un modelo lineal.
    - Evaluar ANOVA.
    - Diagnosticar residuos.
    - Identificar factores importantes.
    - Proponer una ruta de ascenso o descenso más pronunciado.
    - Generar un reporte ejecutivo.
    """
)

st.divider()

st.markdown("## Comenzar")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Diseñar un experimento nuevo")
    st.write(
        "Usa esta opción si todavía no tienes una tabla de datos y quieres que la app "
        "genere el diseño experimental."
    )
    if st.button(
        "Comenzar con diseño experimental",
        type="primary",
        use_container_width=True,
        key="home_start_design"
    ):
        st.switch_page("pages/2_diseno_experimental.py")

with col2:
    st.markdown("### Cargar datos existentes")
    st.write(
        "Usa esta opción si ya tienes una tabla en Excel o CSV con tu variable respuesta "
        "y tus factores experimentales."
    )
    if st.button(
        "Cargar tabla de datos",
        use_container_width=True,
        key="home_upload_data"
    ):
        st.switch_page("pages/3_datos_experimentales.py")

st.divider()

st.markdown("## Guía rápida de uso")

with st.expander("Ver recorrido paso a paso", expanded=True):
    st.markdown(
        """
        ### Ruta 1: cuando aún no tienes datos

        **Paso 1. Diseño Experimental**  
        Define tus factores, niveles bajos, niveles altos, puntos centrales y variable respuesta.

        **Paso 2. Datos Experimentales**  
        Registra manualmente la respuesta observada o simula datos para probar la app.

        **Paso 3. Modelo Lineal**  
        La app ajusta el modelo de primer orden.

        **Paso 4. ANOVA y Diagnóstico**  
        Evalúa si el modelo es significativo y revisa los residuos.

        **Paso 5. Pareto y Ascenso Más Pronunciado**  
        Identifica los factores más importantes y propone nuevas condiciones experimentales.

        **Paso 6. Reporte**  
        Descarga el PDF gerencial, Excel de respaldo y resumen TXT.

        ---

        ### Ruta 2: cuando ya tienes una tabla de datos

        **Paso 1. Datos Experimentales**  
        Carga un archivo Excel o CSV.

        **Paso 2. Selecciona columnas**  
        Indica cuál columna es la respuesta `Y` y cuáles son los factores `X1, X2, X3...`.

        **Paso 3. Codificación**  
        Si tus factores están en unidades reales, la app los codifica internamente.

        **Paso 4. Continúa el análisis**  
        Pasa al modelo lineal, ANOVA, diagnóstico, Pareto, ascenso y reporte.
        """
    )

st.divider()

st.markdown("## ¿Cómo debe ser la tabla de datos?")

st.markdown(
    """
    El usuario puede ingresar datos en formato **Excel** o **CSV**.  
    La tabla puede estar en unidades reales, por ejemplo:
    """
)

st.dataframe(
    {
        "Puntaje_Sensorial": [82.4, 85.1, 78.9, 88.3],
        "Temperatura_C": [120, 130, 120, 130],
        "Tiempo_min": [25, 25, 35, 35],
        "Humedad_inicial_pct": [8, 10, 8, 10],
    },
    use_container_width=True
)

st.info(
    "La app no exige que el usuario escriba los datos ya codificados. "
    "Puede cargar factores en unidades reales y la aplicación los transforma a escala -1, 0, +1."
)

st.divider()

st.markdown("## Ejemplos de aplicación")

examples = [
    {
        "title": "Tostado de cacao",
        "factors": "Temperatura, tiempo de tostado, humedad inicial",
        "response": "Puntaje sensorial o intensidad aromática",
        "goal": "Maximizar calidad sensorial"
    },
    {
        "title": "Secado de granos",
        "factors": "Temperatura, velocidad de aire, tiempo",
        "response": "Humedad final",
        "goal": "Minimizar humedad final"
    },
    {
        "title": "Formulación de alimento",
        "factors": "Concentración de ingrediente A, ingrediente B, temperatura",
        "response": "Aceptabilidad o rendimiento",
        "goal": "Maximizar aceptabilidad"
    },
    {
        "title": "Proceso industrial",
        "factors": "Presión, temperatura, velocidad",
        "response": "Rendimiento del proceso",
        "goal": "Maximizar rendimiento"
    }
]

for ex in examples:
    with st.expander(ex["title"]):
        st.markdown(f"""
        **Factores:** {ex["factors"]}  
        **Variable respuesta:** {ex["response"]}  
        **Objetivo:** {ex["goal"]}
        """)

st.divider()

st.markdown("## Transparencia académica")

st.page_link(
    "pages/10_declaracion_ia.py",
    label="🤖 Ver declaración de uso de Inteligencia Artificial"
)