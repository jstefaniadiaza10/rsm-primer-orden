import streamlit as st
import pandas as pd
from io import BytesIO

from utils.design_generator import generate_first_order_design, create_factor_summary
from utils.ui import load_css, render_sidebar, render_response_summary, format_response_label
from utils.simulator import simulate_first_order_response


# =====================================================
# CONFIGURACIÓN DE PÁGINA
# =====================================================

st.set_page_config(
    page_title="Diseño Experimental | RSM Primer Orden",
    page_icon="📐",
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
        <div class="page-title">📐 Diseño Experimental de Primer Orden</div>
        <div class="page-subtitle">
            Generación de diseños factoriales completos 2ᵏ con puntos centrales.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "Este módulo corresponde únicamente a diseños de primer orden. "
    "No se generan diseños CCD ni Box-Behnken porque pertenecen a modelos de segundo orden."
)


# =====================================================
# FORMULARIO
# =====================================================

st.markdown(
    '<div class="section-title">1. Definición del experimento</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">Configure los factores, niveles experimentales, puntos centrales y variable respuesta.</div>',
    unsafe_allow_html=True
)

with st.container(border=True):

    col_a, col_b, col_c = st.columns([1, 1, 1])

    with col_a:
        k = st.number_input(
            "Número de factores",
            min_value=2,
            max_value=5,
            value=2,
            step=1
        )

    with col_b:
        center_points = st.number_input(
            "Puntos centrales",
            min_value=0,
            max_value=10,
            value=3,
            step=1
        )

    with col_c:
        randomize = st.toggle(
            "Aleatorizar corridas",
            value=True
        )

    st.markdown("### Niveles experimentales")

    default_names = ["Temperatura", "Tiempo", "Humedad", "Velocidad", "Concentración"]
    default_lows = [160.0, 10.0, 40.0, 100.0, 5.0]
    default_highs = [180.0, 20.0, 60.0, 200.0, 15.0]

    factors = []

    for i in range(k):
        c1, c2, c3 = st.columns([2, 1, 1])

        with c1:
            name = st.text_input(
                f"Nombre del factor {i + 1}",
                value=default_names[i],
                key=f"name_{i}"
            )

        with c2:
            low = st.number_input(
                f"Nivel bajo (-1) - {i + 1}",
                value=default_lows[i],
                key=f"low_{i}"
            )

        with c3:
            high = st.number_input(
                f"Nivel alto (+1) - {i + 1}",
                value=default_highs[i],
                key=f"high_{i}"
            )

        factors.append({
            "name": name.strip(),
            "low": low,
            "high": high
        })

    st.markdown("### Variable respuesta")

    r1, r2, r3 = st.columns([2, 1, 1])

    with r1:
        response_name = st.text_input(
            "Nombre de la variable respuesta",
            value="Puntaje sensorial",
            help="Variable que se desea explicar u optimizar con el experimento."
        )

    with r2:
        response_units = st.text_input(
            "Unidad de medida",
            value="puntos",
            help="Ejemplo: %, puntos, kg, °Brix, minutos, g/L."
        )

    with r3:
        optimization_goal = st.selectbox(
            "Objetivo",
            options=["Maximizar", "Minimizar"],
            index=0,
            help="Indique si se busca aumentar o reducir la variable respuesta."
        )

    generate = st.button(
        "Generar diseño experimental",
        use_container_width=True
    )


# =====================================================
# GENERACIÓN DEL DISEÑO
# =====================================================

if generate:
    try:
        if response_name.strip() == "":
            raise ValueError("Debe ingresar el nombre de la variable respuesta.")

        coded_df, real_df, template_df = generate_first_order_design(
            factors=factors,
            center_points=center_points,
            randomize=randomize
        )

        factor_summary = create_factor_summary(factors)

        st.session_state["coded_design"] = coded_df
        st.session_state["real_design"] = real_df
        st.session_state["template_design"] = template_df
        st.session_state["factor_summary"] = factor_summary
        st.session_state["factors"] = factors

        st.session_state["response_name"] = response_name.strip()
        st.session_state["response_units"] = response_units.strip()
        st.session_state["optimization_goal"] = optimization_goal

        # Reiniciar estados posteriores cuando se genera un nuevo diseño
        st.session_state.pop("model_data", None)
        st.session_state.pop("factor_cols", None)
        st.session_state.pop("response_col", None)
        st.session_state.pop("model_results", None)
        st.session_state.pop("anova_df", None)

        st.session_state["editor_version"] = st.session_state.get("editor_version", 0) + 1

        st.success("Diseño experimental generado correctamente.")

    except Exception as e:
        st.error(f"Error al generar el diseño: {e}")


# =====================================================
# RESULTADOS
# =====================================================

if "coded_design" in st.session_state:

    coded_df = st.session_state["coded_design"]
    real_df = st.session_state["real_design"]
    template_df = st.session_state["template_design"]
    factor_summary = st.session_state["factor_summary"]

    response_name = st.session_state.get("response_name", "Respuesta")
    response_units = st.session_state.get("response_units", "")
    optimization_goal = st.session_state.get("optimization_goal", "Maximizar")

    st.markdown(
        '<div class="section-title">2. Resumen del diseño</div>',
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("Factores", len(st.session_state["factors"]))

    with m2:
        st.metric("Corridas totales", len(real_df))

    with m3:
        st.metric(
            "Puntos factoriales",
            len(real_df[real_df["Tipo"] == "Factorial"])
        )

    with m4:
        st.metric(
            "Puntos centrales",
            len(real_df[real_df["Tipo"] == "Centro"])
        )

    # =====================================================
    # VARIABLE RESPUESTA
    # =====================================================

    st.markdown("### Variable respuesta definida")

    response_label = render_response_summary(
        response_name=response_name,
        response_units=response_units,
        optimization_goal=optimization_goal
    )

    # =====================================================
    # FACTORES
    # =====================================================

    st.markdown("### Resumen de factores")
    st.dataframe(factor_summary, use_container_width=True)

    tab1, tab2, tab3 = st.tabs([
        "Matriz codificada",
        "Matriz real",
        "Registro de respuesta"
    ])

    with tab1:
        st.dataframe(coded_df, use_container_width=True)

    with tab2:
        st.dataframe(real_df, use_container_width=True)

    with tab3:
        st.markdown(
            """
            <div class="section-title">Registro o simulación de resultados</div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="section-subtitle">
                Cada fila representa una corrida experimental, es decir, una combinación
                de condiciones del proceso que debe evaluarse. En la columna
                <b>{response_name}</b> se registra el valor observado o simulado de la variable respuesta.
                Objetivo del análisis: <b>{optimization_goal}</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info(
            f"Puede ingresar manualmente la variable respuesta '{response_name}' "
            "o generar datos simulados para probar el funcionamiento completo de la aplicación."
        )

        st.warning(
            "Las respuestas simuladas son únicamente para demostración del aplicativo. "
            "En un estudio real deben reemplazarse por resultados medidos experimentalmente."
        )

        factor_cols_design = [
            col for col in coded_df.columns
            if col not in ["Corrida", "Tipo"]
        ]

        if "editor_version" not in st.session_state:
            st.session_state["editor_version"] = 0

        with st.expander("Simular respuesta experimental para caso de prueba", expanded=True):

            st.markdown(
                """
                La simulación usa un modelo de primer orden sobre variables codificadas:

                `Respuesta = promedio + efectos de factores + error aleatorio`
                """
            )

            col_s1, col_s2, col_s3 = st.columns(3)

            with col_s1:
                intercept = st.number_input(
                    "Valor promedio esperado",
                    value=80.0,
                    step=1.0,
                    help="Valor central aproximado de la respuesta."
                )

            with col_s2:
                noise_sd = st.number_input(
                    "Variabilidad experimental",
                    value=1.5,
                    min_value=0.0,
                    step=0.5,
                    help="Representa el error aleatorio del experimento."
                )

            with col_s3:
                seed = st.number_input(
                    "Semilla de simulación",
                    value=123,
                    step=1,
                    help="Permite reproducir los mismos datos simulados."
                )

            st.markdown("#### Efectos esperados de los factores")

            coefficients = {}

            for factor in factor_cols_design:
                default_effect = 1.0

                if "temperatura" in factor.lower():
                    default_effect = 3.0
                elif "tiempo" in factor.lower():
                    default_effect = 2.0
                elif "humedad" in factor.lower():
                    default_effect = -1.5
                elif "velocidad" in factor.lower():
                    default_effect = 1.0
                elif "concentración" in factor.lower() or "concentracion" in factor.lower():
                    default_effect = 1.5

                coefficients[factor] = st.number_input(
                    f"Efecto esperado de {factor}",
                    value=float(default_effect),
                    step=0.5,
                    help=(
                        "Efecto estimado del factor en la respuesta usando variables codificadas. "
                        "Valor positivo aumenta la respuesta; valor negativo la disminuye."
                    )
                )

            if st.button("Generar respuestas simuladas", use_container_width=True):

                simulated_y = simulate_first_order_response(
                    coded_df=coded_df,
                    factor_cols=factor_cols_design,
                    intercept=intercept,
                    coefficients=coefficients,
                    noise_sd=noise_sd,
                    seed=int(seed)
                )

                simulated_template = st.session_state["template_design"].copy()
                simulated_template["Respuesta"] = simulated_y.values

                st.session_state["template_design"] = simulated_template
                st.session_state["editor_version"] += 1

                st.success("Respuestas simuladas generadas correctamente.")
                st.rerun()

        st.markdown("#### Tabla editable de resultados")

        template_to_edit = st.session_state["template_design"].copy()

        template_to_edit["Respuesta"] = pd.to_numeric(
            template_to_edit["Respuesta"],
            errors="coerce"
        )

        disabled_columns = [
            col for col in template_to_edit.columns
            if col != "Respuesta"
        ]

        edited_template = st.data_editor(
            template_to_edit,
            use_container_width=True,
            num_rows="fixed",
            disabled=disabled_columns,
            column_config={
                "Respuesta": st.column_config.NumberColumn(
                    f"{response_name} ({response_units})" if response_units else response_name,
                    help=f"Ingrese o revise el valor observado o simulado de {response_name}.",
                    format="%.4f"
                )
            },
            key=f"editor_respuesta_experimental_{st.session_state['editor_version']}"
        )

        st.session_state["template_design"] = edited_template

    # =====================================================
    # CONTINUAR A DATOS EXPERIMENTALES
    # =====================================================

    st.markdown("---")

    st.success(
        "Siguiente paso: registre o simule la variable respuesta y presione el botón "
        "para validar la base experimental."
    )

    col_continue, col_export = st.columns([2, 1])

    with col_continue:
        if st.button(
            "Validar respuestas y continuar a Datos Experimentales",
            use_container_width=True
        ):
            try:
                current_template = st.session_state["template_design"].copy()
                current_coded = st.session_state["coded_design"].copy()

                if "Respuesta" not in current_template.columns:
                    raise ValueError("No existe la columna interna 'Respuesta'.")

                if current_template["Respuesta"].isna().sum() > 0:
                    raise ValueError(
                        "Existen respuestas experimentales vacías. "
                        "Complete o simule todos los valores antes de continuar."
                    )

                current_template["Respuesta"] = pd.to_numeric(
                    current_template["Respuesta"],
                    errors="raise"
                )

                response_df = current_template[["Corrida", "Respuesta"]].copy()

                model_df = current_coded.merge(
                    response_df,
                    on="Corrida",
                    how="left"
                )

                factor_cols = [
                    col for col in current_coded.columns
                    if col not in ["Corrida", "Tipo"]
                ]

                st.session_state["model_data"] = model_df
                st.session_state["factor_cols"] = factor_cols
                st.session_state["response_col"] = "Respuesta"

                st.session_state["response_name"] = response_name
                st.session_state["response_units"] = response_units
                st.session_state["optimization_goal"] = optimization_goal

                st.success("Base experimental validada correctamente.")
                st.switch_page("pages/3_datos_experimentales.py")

            except Exception as e:
                st.error(f"No se puede continuar: {e}")

    with col_export:
        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            factor_summary.to_excel(writer, index=False, sheet_name="Factores")
            coded_df.to_excel(writer, index=False, sheet_name="Matriz_Codificada")
            real_df.to_excel(writer, index=False, sheet_name="Matriz_Real")
            st.session_state["template_design"].to_excel(
                writer,
                index=False,
                sheet_name="Plantilla_Resultados"
            )

        output.seek(0)

        st.download_button(
            label="Exportar respaldo Excel",
            data=output,
            file_name="diseno_primer_orden.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )