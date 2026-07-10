import streamlit as st
import pandas as pd

from utils.ui import (
    load_css,
    render_sidebar,
    render_response_summary,
    format_response_label
)

from utils.data_loader import (
    read_uploaded_table,
    build_example_template_excel,
    prepare_uploaded_first_order_data
)


st.set_page_config(
    page_title="Datos Experimentales",
    page_icon="📂",
    layout="wide"
)

load_css()
render_sidebar()

st.markdown(
    """
    <div class="page-header">
        <div class="page-title">Datos Experimentales</div>
        <div class="page-subtitle">
            Valide datos generados por la app o cargue una tabla experimental existente.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

tab_active, tab_upload, tab_help = st.tabs(
    [
        "Base activa",
        "Cargar datos existentes",
        "Guía de formato"
    ]
)

with tab_active:
    st.markdown("## Base experimental activa")

    if "model_data" not in st.session_state:
        st.warning(
            "Todavía no existe una base experimental activa. "
            "Puede crear un diseño experimental o cargar una tabla existente."
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "Crear diseño experimental",
                use_container_width=True,
                key="data_go_design"
            ):
                st.switch_page("pages/2_diseno_experimental.py")

        with col2:
            st.info("También puede usar la pestaña 'Cargar datos existentes'.")

    else:
        model_df = st.session_state["model_data"]
        factor_cols = st.session_state["factor_cols"]
        response_col = st.session_state.get("response_col", "Respuesta")
        response_name = st.session_state.get("response_name", "Respuesta")
        response_units = st.session_state.get("response_units", "")
        optimization_goal = st.session_state.get("optimization_goal", "Maximizar")

        response_label = render_response_summary(
            response_name=response_name,
            response_units=response_units,
            optimization_goal=optimization_goal
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Observaciones", len(model_df))

        with col2:
            st.metric("Factores", len(factor_cols))

        with col3:
            st.metric("Variable interna", response_col)

        st.markdown("### Vista de la base usada para el modelo")

        display_df = model_df.copy()

        if "Respuesta" in display_df.columns:
            display_df = display_df.rename(columns={"Respuesta": response_label})

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        with st.expander("Ver columnas internas del modelo"):
            st.write("Factores usados por el modelo:")
            st.write(factor_cols)
            st.write("Columna interna de respuesta:")
            st.code(response_col)

        if st.button(
            "Continuar a Modelo Lineal",
            type="primary",
            use_container_width=True,
            key="data_to_model_from_active"
        ):
            st.switch_page("pages/4_modelo_lineal.py")


with tab_upload:
    st.markdown("## Cargar tabla experimental existente")

    st.write(
        "Use esta opción si ya tiene una tabla con su variable respuesta y sus factores. "
        "La tabla puede estar en unidades reales o ya codificada en escala -1, 0, +1."
    )

    template_bytes = build_example_template_excel()

    st.download_button(
        label="Descargar plantilla de ejemplo Excel",
        data=template_bytes,
        file_name="plantilla_datos_rsm_primer_orden.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        key="download_template_rsm"
    )

    uploaded_file = st.file_uploader(
        "Suba un archivo CSV o Excel",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:
        try:
            raw_df = read_uploaded_table(uploaded_file)

            st.success("Archivo cargado correctamente.")

            st.markdown("### Vista previa de los datos cargados")
            st.dataframe(raw_df.head(20), use_container_width=True, hide_index=True)

            columns = list(raw_df.columns)

            st.markdown("### Selección de variables")

            response_col_uploaded = st.selectbox(
                "Seleccione la variable respuesta Y",
                options=columns,
                key="uploaded_response_col"
            )

            available_factors = [
                col for col in columns if col != response_col_uploaded
            ]

            factor_cols_uploaded = st.multiselect(
                "Seleccione los factores experimentales X",
                options=available_factors,
                default=available_factors[:min(3, len(available_factors))],
                key="uploaded_factor_cols"
            )

            response_name = st.text_input(
                "Nombre que se mostrará para la variable respuesta",
                value=response_col_uploaded,
                key="uploaded_response_name"
            )

            response_units = st.text_input(
                "Unidad de la variable respuesta",
                value="",
                placeholder="Ejemplo: puntos, %, kg, °Brix",
                key="uploaded_response_units"
            )

            optimization_goal = st.selectbox(
                "Objetivo del análisis",
                options=["Maximizar", "Minimizar"],
                index=0,
                key="uploaded_optimization_goal"
            )

            st.markdown("### Tipo de datos de los factores")

            coding_option = st.radio(
                "¿Cómo están expresados sus factores X?",
                options=[
                    "Están en unidades reales y deseo codificarlos",
                    "Ya están codificados en escala -1, 0, +1"
                ],
                key="uploaded_coding_option"
            )

            coding_mode = "raw" if coding_option.startswith("Están en unidades reales") else "coded"

            factor_levels = {}

            if coding_mode == "raw" and factor_cols_uploaded:
                st.markdown("### Niveles para codificación")

                st.info(
                    "Para codificar cada factor, indique el nivel bajo y el nivel alto "
                    "usados en el diseño experimental. La app calculará el centro y el semirango."
                )

                for factor in factor_cols_uploaded:
                    numeric_factor = pd.to_numeric(raw_df[factor], errors="coerce")
                    min_value = float(numeric_factor.min())
                    max_value = float(numeric_factor.max())

                    col_low, col_high = st.columns(2)

                    with col_low:
                        low = st.number_input(
                            f"Nivel bajo (-1) para {factor}",
                            value=min_value,
                            key=f"low_{factor}"
                        )

                    with col_high:
                        high = st.number_input(
                            f"Nivel alto (+1) para {factor}",
                            value=max_value,
                            key=f"high_{factor}"
                        )

                    factor_levels[factor] = {
                        "low": low,
                        "high": high
                    }

            st.divider()

            if st.button(
                "Validar y usar esta base",
                type="primary",
                use_container_width=True,
                key="validate_uploaded_data"
            ):
                prepared = prepare_uploaded_first_order_data(
                    raw_df=raw_df,
                    factor_cols=factor_cols_uploaded,
                    response_col=response_col_uploaded,
                    coding_mode=coding_mode,
                    factor_levels=factor_levels if coding_mode == "raw" else None
                )

                st.session_state["model_data"] = prepared["model_df"]
                st.session_state["coded_design"] = prepared["coded_design"]
                st.session_state["real_design"] = prepared["real_design"]
                st.session_state["factor_summary"] = prepared["factor_summary"]
                st.session_state["factors"] = prepared["factors"]

                st.session_state["factor_cols"] = factor_cols_uploaded
                st.session_state["response_col"] = "Respuesta"
                st.session_state["response_name"] = response_name
                st.session_state["response_units"] = response_units
                st.session_state["optimization_goal"] = optimization_goal

                st.session_state.pop("model_results", None)
                st.session_state.pop("anova_df", None)
                st.session_state.pop("effects_df", None)
                st.session_state.pop("steepest_direction_df", None)
                st.session_state.pop("steepest_path_df", None)

                st.success("Base cargada y validada correctamente.")
                st.switch_page("pages/4_modelo_lineal.py")

        except Exception as e:
            st.error(f"No fue posible procesar el archivo: {e}")


with tab_help:
    st.markdown("## Guía de formato de datos")

    st.markdown(
        """
        La tabla debe tener una columna para la variable respuesta `Y` y una o más columnas
        para los factores experimentales `X`.

        Ejemplo:

        | Puntaje_Sensorial | Temperatura_C | Tiempo_min | Humedad_inicial_pct |
        |---:|---:|---:|---:|
        | 82.4 | 120 | 25 | 8 |
        | 85.1 | 130 | 25 | 8 |
        | 78.9 | 120 | 35 | 8 |
        | 88.3 | 130 | 35 | 8 |

        ### Caso A: factores en unidades reales

        Si sus factores están en unidades reales, por ejemplo temperatura en °C o tiempo en minutos,
        la app solicita el nivel bajo y alto para cada factor y aplica:

        ```text
        x = (X - centro) / semirango
        ```

        donde:

        ```text
        centro = (nivel alto + nivel bajo) / 2
        semirango = (nivel alto - nivel bajo) / 2
        ```

        ### Caso B: factores ya codificados

        Si su tabla ya tiene columnas en escala `-1, 0, +1`, puede seleccionar la opción
        de datos ya codificados.

        ### Importante

        El modelo se ajusta con factores codificados, pero la app conserva la información
        necesaria para interpretar los resultados en el contexto del experimento.
        """
    )