import streamlit as st
import pandas as pd

from utils.ui import load_css, render_sidebar, render_response_summary
from utils.design_generator import generate_first_order_design, create_factor_summary
from utils.simulator import simulate_first_order_response
from utils.example_cases import EXAMPLE_CASES, get_example_options, build_example_case_data


st.set_page_config(
    page_title="Diseño Experimental",
    page_icon="📐",
    layout="wide"
)

load_css()
render_sidebar()


def clear_downstream_outputs():
    keys_to_clear = [
        "model_results",
        "anova_df",
        "effects_df",
        "steepest_direction_df",
        "steepest_path_df",
    ]

    for key in keys_to_clear:
        st.session_state.pop(key, None)


def save_experiment_state(
    coded_design,
    real_design,
    model_df,
    factor_summary,
    factors,
    factor_cols,
    response_name,
    response_units,
    optimization_goal,
):
    clear_downstream_outputs()

    st.session_state["coded_design"] = coded_design
    st.session_state["real_design"] = real_design
    st.session_state["model_data"] = model_df
    st.session_state["factor_summary"] = factor_summary
    st.session_state["factors"] = factors

    st.session_state["factor_cols"] = factor_cols
    st.session_state["response_col"] = "Respuesta"
    st.session_state["response_name"] = response_name
    st.session_state["response_units"] = response_units
    st.session_state["optimization_goal"] = optimization_goal


def render_info_panel(title, text):
    st.markdown(
        f"""
        <div class="info-panel">
            <div class="info-panel-title">ℹ️ {title}</div>
            <div class="info-panel-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_design_configuration_help():
    st.markdown(
        """
        <div class="info-grid">
            <div class="info-mini-card">
                <div class="info-mini-title">Puntos centrales</div>
                <div class="info-mini-text">
                    Son corridas realizadas en el valor medio de todos los factores. 
                    Sirven para tener una referencia del centro del experimento y mejorar la evaluación del error.
                </div>
            </div>
            <div class="info-mini-card">
                <div class="info-mini-title">Aleatorizar corridas</div>
                <div class="info-mini-text">
                    Cambia el orden de ejecución de los ensayos para evitar que el tiempo, temperatura ambiente
                    u otros factores externos sesguen los resultados.
                </div>
            </div>
            <div class="info-mini-card">
                <div class="info-mini-title">Semilla</div>
                <div class="info-mini-text">
                    Es un número que permite repetir la misma aleatorización. 
                    Si usa la misma semilla, obtendrá el mismo orden de corridas.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    """
    <div class="page-header">
        <div class="page-title">Diseño Experimental</div>
        <div class="page-subtitle">
            Cree un diseño propio o use un ejemplo completo incluido para familiarizarse con la app.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "En esta sección puede trabajar de dos formas: usar un ejemplo completo con datos simulados "
    "o construir su propio diseño factorial de primer orden."
)

tab_example, tab_custom = st.tabs(
    [
        "Usar ejemplo incluido",
        "Crear diseño propio"
    ]
)


with tab_example:
    st.markdown("## Ejemplos completos disponibles")

    render_info_panel(
        "¿Para qué sirven estos ejemplos?",
        (
            "Los ejemplos ya vienen con factores, niveles, puntos centrales, variable respuesta "
            "y datos simulados. Sirven para que el usuario recorra toda la app sin tener que "
            "crear datos desde cero."
        )
    )

    st.write(
        "Seleccione un caso, revise sus datos y presione **Usar este ejemplo y continuar**. "
        "La app cargará automáticamente la base experimental y podrá avanzar al modelo lineal."
    )

    example_keys = get_example_options()
    default_key = st.session_state.get("selected_example_case", example_keys[0])

    if default_key not in example_keys:
        default_key = example_keys[0]

    selected_example = st.selectbox(
        "Seleccione un ejemplo",
        options=example_keys,
        index=example_keys.index(default_key),
        format_func=lambda key: EXAMPLE_CASES[key]["title"],
        key="design_selected_example",
        help=(
            "Elija un caso completo incluido en la app. Cada ejemplo trae diseño, niveles, "
            "respuesta simulada y objetivo de optimización."
        )
    )

    example_data = build_example_case_data(selected_example)
    case = example_data["case"]

    st.markdown(f"### {case['title']}")
    st.write(case["description"])

    response_label = render_response_summary(
        response_name=case["response_name"],
        response_units=case["response_units"],
        optimization_goal=case["optimization_goal"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Factores", len(example_data["factor_cols"]))

    with col2:
        st.metric("Corridas", len(example_data["model_df"]))

    with col3:
        st.metric("Puntos centrales", case["center_points"])

    st.markdown("### Factores y niveles del ejemplo")

    render_info_panel(
        "¿Cómo leer esta tabla?",
        (
            "Cada factor tiene un nivel bajo (-1), un centro (0) y un nivel alto (+1). "
            "La app usa estos niveles para construir la matriz codificada del diseño experimental."
        )
    )

    st.dataframe(
        example_data["factor_summary"],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Datos del ejemplo en unidades reales")

    render_info_panel(
        "Datos reales vs datos codificados",
        (
            "Esta tabla muestra las condiciones experimentales en unidades reales, por ejemplo °C, minutos o porcentajes. "
            "Internamente, el modelo usa la versión codificada para estimar los efectos de los factores."
        )
    )

    display_real = example_data["real_design_with_response"].copy()

    if case["response_name"] in display_real.columns:
        display_real = display_real.rename(columns={case["response_name"]: response_label})

    st.dataframe(
        display_real,
        use_container_width=True,
        hide_index=True
    )

    with st.expander("Ver matriz codificada usada por el modelo"):
        display_coded = example_data["model_df"].copy()
        display_coded = display_coded.rename(columns={"Respuesta": response_label})
        st.dataframe(display_coded, use_container_width=True, hide_index=True)

    st.markdown("### ¿Qué pasará al usar este ejemplo?")

    st.markdown(
        """
        La app guardará este ejemplo como base experimental activa y podrá continuar automáticamente con:

        ```text
        Datos Experimentales → Modelo Lineal → ANOVA → Diagnóstico → Pareto → Ascenso → Reporte
        ```
        """
    )

    if st.button(
        "Usar este ejemplo y continuar",
        type="primary",
        use_container_width=True,
        key="use_selected_example",
        help="Carga el ejemplo seleccionado como base activa y avanza a la pestaña de datos experimentales."
    ):
        save_experiment_state(
            coded_design=example_data["coded_design"],
            real_design=example_data["real_design"],
            model_df=example_data["model_df"],
            factor_summary=example_data["factor_summary"],
            factors=example_data["factors"],
            factor_cols=example_data["factor_cols"],
            response_name=case["response_name"],
            response_units=case["response_units"],
            optimization_goal=case["optimization_goal"],
        )

        st.session_state["selected_example_case"] = selected_example

        st.success("Ejemplo cargado correctamente como base experimental activa.")
        st.switch_page("pages/3_datos_experimentales.py")


with tab_custom:
    st.markdown("## Crear diseño experimental propio")

    st.write(
        "Use esta opción si desea definir sus propios factores, niveles y variable respuesta."
    )

    st.markdown("### 1. Definición de factores")

    render_info_panel(
        "¿Qué es un factor?",
        (
            "Un factor es una variable experimental que usted puede controlar. "
            "Por ejemplo: temperatura, tiempo, humedad, presión, velocidad o concentración. "
            "Para cada factor debe ingresar un nivel bajo y un nivel alto."
        )
    )

    num_factors = st.number_input(
        "Número de factores",
        min_value=1,
        max_value=6,
        value=3,
        step=1,
        key="custom_num_factors",
        help=(
            "Cantidad de variables experimentales controlables. Ejemplo: si estudiará temperatura, "
            "tiempo y humedad, entonces son 3 factores."
        )
    )

    default_names = [
        "Temperatura_C",
        "Tiempo_min",
        "Humedad_inicial_pct",
        "Presion_bar",
        "Velocidad_rpm",
        "Concentracion_pct",
    ]

    default_lows = [120.0, 20.0, 6.0, 2.0, 300.0, 5.0]
    default_highs = [140.0, 40.0, 10.0, 5.0, 600.0, 15.0]

    factors = []

    for i in range(int(num_factors)):
        st.markdown(f"#### Factor {i + 1}")

        col_name, col_low, col_high = st.columns(3)

        with col_name:
            name = st.text_input(
                "Nombre",
                value=default_names[i],
                key=f"custom_factor_name_{i}",
                help=(
                    "Nombre del factor experimental. Ejemplo: Temperatura_C, Tiempo_min, "
                    "Presion_bar o Concentracion_pct."
                )
            )

        with col_low:
            low = st.number_input(
                "Nivel bajo (-1)",
                value=default_lows[i],
                key=f"custom_factor_low_{i}",
                help=(
                    "Valor mínimo que tomará este factor en el experimento. "
                    "En escala codificada representa -1."
                )
            )

        with col_high:
            high = st.number_input(
                "Nivel alto (+1)",
                value=default_highs[i],
                key=f"custom_factor_high_{i}",
                help=(
                    "Valor máximo que tomará este factor en el experimento. "
                    "En escala codificada representa +1."
                )
            )

        factors.append(
            {
                "name": name.strip(),
                "low": float(low),
                "high": float(high),
            }
        )

    st.markdown("### 2. Configuración del diseño")

    render_info_panel(
        "¿Qué se configura aquí?",
        (
            "En esta parte se define cómo se organizarán las corridas experimentales. "
            "Los puntos centrales ayudan a evaluar estabilidad del proceso, la aleatorización "
            "evita sesgos por el orden de ejecución y la semilla permite repetir exactamente "
            "el mismo diseño aleatorizado."
        )
    )

    render_design_configuration_help()

    col_center, col_random, col_seed = st.columns(3)

    with col_center:
        center_points = st.number_input(
            "Puntos centrales",
            min_value=0,
            max_value=20,
            value=3,
            step=1,
            key="custom_center_points",
            help=(
                "Número de corridas adicionales ubicadas en el centro del diseño. "
                "Por ejemplo, si Temperatura va de 120 a 140, el centro es 130. "
                "Se recomienda usar entre 3 y 5 puntos centrales cuando sea posible."
            )
        )

    with col_random:
        randomize = st.checkbox(
            "Aleatorizar corridas",
            value=True,
            key="custom_randomize",
            help=(
                "Si está activado, la app mezcla el orden de las corridas. "
                "Esto es recomendable porque reduce sesgos por el orden de ejecución experimental."
            )
        )

    with col_seed:
        seed = st.number_input(
            "Semilla",
            min_value=1,
            value=123,
            step=1,
            key="custom_seed",
            help=(
                "Número usado para controlar la aleatorización. "
                "No representa una variable experimental. Solo permite reproducir el mismo orden de corridas."
            )
        )

    st.markdown("### 3. Variable respuesta")

    render_info_panel(
        "¿Qué es la variable respuesta?",
        (
            "La variable respuesta es el resultado que se desea analizar u optimizar. "
            "Por ejemplo: puntaje sensorial, rendimiento, humedad final, aceptabilidad, productividad o defectos."
        )
    )

    col_resp1, col_resp2, col_resp3 = st.columns(3)

    with col_resp1:
        response_name = st.text_input(
            "Nombre de la variable respuesta",
            value="Puntaje sensorial",
            key="custom_response_name",
            help=(
                "Es el resultado que se medirá en cada corrida experimental. "
                "Ejemplo: rendimiento, humedad final, puntaje sensorial, calidad o productividad."
            )
        )

    with col_resp2:
        response_units = st.text_input(
            "Unidad",
            value="puntos",
            key="custom_response_units",
            help=(
                "Unidad en la que se mide la respuesta. Ejemplo: %, puntos, kg, gramos, °Brix o unidades."
            )
        )

    with col_resp3:
        optimization_goal = st.selectbox(
            "Objetivo",
            options=["Maximizar", "Minimizar"],
            index=0,
            key="custom_optimization_goal",
            help=(
                "Seleccione Maximizar si desea aumentar la respuesta. "
                "Seleccione Minimizar si desea reducirla, por ejemplo humedad final o defectos."
            )
        )

    response_label = render_response_summary(
        response_name=response_name,
        response_units=response_units,
        optimization_goal=optimization_goal
    )

    st.markdown("### 4. Vista previa del diseño")

    render_info_panel(
        "¿Qué muestran estas tablas?",
        (
            "La tabla de niveles resume el rango de cada factor. El diseño real muestra las condiciones "
            "en unidades originales. La matriz codificada muestra la escala -1, 0, +1 usada por el modelo."
        )
    )

    try:
        coded_df, real_df, template_df = generate_first_order_design(
            factors=factors,
            center_points=int(center_points),
            randomize=randomize,
            seed=int(seed)
        )

        factor_cols = [factor["name"] for factor in factors]
        factor_summary = create_factor_summary(factors)

        col_preview1, col_preview2 = st.columns(2)

        with col_preview1:
            st.markdown("#### Niveles de factores")
            st.dataframe(factor_summary, use_container_width=True, hide_index=True)

        with col_preview2:
            st.markdown("#### Diseño real")
            st.dataframe(real_df, use_container_width=True, hide_index=True)

        with st.expander("Ver matriz codificada"):
            st.dataframe(coded_df, use_container_width=True, hide_index=True)

        st.markdown("### 5. Respuesta experimental")

        render_info_panel(
            "¿Qué debe hacer aquí?",
            (
                "Luego de tener el diseño, se necesita una respuesta para cada corrida. "
                "Puede simular respuestas para practicar o registrar manualmente resultados obtenidos en laboratorio."
            )
        )

        response_mode = st.radio(
            "¿Cómo desea ingresar la respuesta?",
            options=[
                "Simular respuesta para probar la app",
                "Registrar respuesta manualmente"
            ],
            key="custom_response_mode",
            help=(
                "Use simulación si solo desea probar la app. Use registro manual si ya ejecutó el experimento "
                "y tiene la respuesta observada para cada corrida."
            )
        )

        if response_mode == "Simular respuesta para probar la app":
            st.markdown("#### Parámetros de simulación")

            render_info_panel(
                "¿Qué significan estos parámetros?",
                (
                    "El intercepto representa el valor promedio esperado de la respuesta. "
                    "Los efectos indican cuánto cambia la respuesta al mover cada factor de nivel bajo a alto. "
                    "El ruido representa variación experimental aleatoria."
                )
            )

            col_intercept, col_noise, col_sim_seed = st.columns(3)

            with col_intercept:
                intercept = st.number_input(
                    "Intercepto esperado",
                    value=80.0,
                    key="custom_sim_intercept",
                    help=(
                        "Valor base aproximado de la respuesta cuando los factores están en el centro del diseño."
                    )
                )

            with col_noise:
                noise_sd = st.number_input(
                    "Ruido experimental",
                    min_value=0.0,
                    value=1.0,
                    step=0.1,
                    key="custom_sim_noise",
                    help=(
                        "Variación aleatoria agregada a la respuesta simulada. Un valor mayor genera datos más dispersos."
                    )
                )

            with col_sim_seed:
                sim_seed = st.number_input(
                    "Semilla de simulación",
                    min_value=1,
                    value=123,
                    step=1,
                    key="custom_sim_seed",
                    help=(
                        "Número que permite obtener la misma simulación cada vez que se repite el ejemplo."
                    )
                )

            coefficients = {}

            st.write("Coeficientes simulados por factor:")

            coef_cols = st.columns(min(3, len(factor_cols)))

            for idx, factor in enumerate(factor_cols):
                with coef_cols[idx % len(coef_cols)]:
                    coefficients[factor] = st.number_input(
                        f"Efecto de {factor}",
                        value=1.0,
                        step=0.1,
                        key=f"custom_coef_{factor}",
                        help=(
                            "Valor usado para simular el efecto de este factor sobre la respuesta. "
                            "Si es positivo, al subir el factor aumenta la respuesta. Si es negativo, la reduce."
                        )
                    )

            simulated_response = simulate_first_order_response(
                coded_df=coded_df,
                factor_cols=factor_cols,
                intercept=float(intercept),
                coefficients=coefficients,
                noise_sd=float(noise_sd),
                seed=int(sim_seed)
            )

            preview_model_df = coded_df[["Corrida"] + factor_cols + ["Tipo"]].copy()
            preview_model_df["Respuesta"] = simulated_response
            preview_model_df = preview_model_df[["Corrida"] + factor_cols + ["Respuesta", "Tipo"]]

            display_preview = preview_model_df.rename(columns={"Respuesta": response_label})

            st.markdown("#### Vista previa de datos simulados")
            st.dataframe(display_preview, use_container_width=True, hide_index=True)

            if st.button(
                "Usar diseño simulado y continuar",
                type="primary",
                use_container_width=True,
                key="custom_use_simulated",
                help="Guarda el diseño con respuestas simuladas y continúa a Datos Experimentales."
            ):
                save_experiment_state(
                    coded_design=coded_df,
                    real_design=real_df,
                    model_df=preview_model_df,
                    factor_summary=factor_summary,
                    factors=factors,
                    factor_cols=factor_cols,
                    response_name=response_name,
                    response_units=response_units,
                    optimization_goal=optimization_goal,
                )

                st.success("Diseño simulado cargado correctamente.")
                st.switch_page("pages/3_datos_experimentales.py")

        else:
            st.markdown("#### Registro manual de respuesta")

            render_info_panel(
                "¿Cómo registrar la respuesta?",
                (
                    "Complete la columna de respuesta para cada corrida del diseño. "
                    "Debe ingresar valores numéricos y no dejar celdas vacías."
                )
            )

            manual_df = template_df.copy()
            manual_df = manual_df.rename(columns={"Respuesta": response_label})

            edited_df = st.data_editor(
                manual_df,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                key="custom_manual_response_editor"
            )

            if st.button(
                "Validar respuestas y continuar",
                type="primary",
                use_container_width=True,
                key="custom_use_manual",
                help="Valida que todas las respuestas sean numéricas y continúa a Datos Experimentales."
            ):
                response_values = pd.to_numeric(
                    edited_df[response_label],
                    errors="coerce"
                )

                if response_values.isna().sum() > 0:
                    st.error("Debe completar todas las respuestas con valores numéricos.")
                else:
                    model_df = coded_df[["Corrida"] + factor_cols + ["Tipo"]].copy()
                    model_df["Respuesta"] = response_values.values
                    model_df = model_df[["Corrida"] + factor_cols + ["Respuesta", "Tipo"]]

                    save_experiment_state(
                        coded_design=coded_df,
                        real_design=real_df,
                        model_df=model_df,
                        factor_summary=factor_summary,
                        factors=factors,
                        factor_cols=factor_cols,
                        response_name=response_name,
                        response_units=response_units,
                        optimization_goal=optimization_goal,
                    )

                    st.success("Diseño con respuestas manuales cargado correctamente.")
                    st.switch_page("pages/3_datos_experimentales.py")

    except Exception as e:
        st.error(f"No fue posible generar el diseño: {e}")