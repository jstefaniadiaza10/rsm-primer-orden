from io import BytesIO

import numpy as np
import pandas as pd


def read_uploaded_table(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
        return pd.read_excel(uploaded_file)

    raise ValueError("Formato no soportado. Use archivos CSV o Excel.")


def build_example_template_excel():
    df = pd.DataFrame({
        "Puntaje_Sensorial": [82.4, 85.1, 78.9, 88.3, 80.2, 86.7, 83.5, 89.1],
        "Temperatura_C": [120, 130, 120, 130, 120, 130, 125, 125],
        "Tiempo_min": [25, 25, 35, 35, 25, 35, 30, 30],
        "Humedad_inicial_pct": [8, 8, 8, 8, 10, 10, 9, 9],
    })

    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Datos")

    buffer.seek(0)
    return buffer.getvalue()


def create_factor_summary_from_levels(factor_levels):
    rows = []

    for factor, levels in factor_levels.items():
        low = float(levels["low"])
        high = float(levels["high"])
        center = (low + high) / 2
        step = (high - low) / 2

        rows.append({
            "Factor": factor,
            "Nivel bajo (-1)": low,
            "Centro (0)": center,
            "Nivel alto (+1)": high,
            "Semirango": step
        })

    return pd.DataFrame(rows)


def prepare_uploaded_first_order_data(
    raw_df,
    factor_cols,
    response_col,
    coding_mode,
    factor_levels=None
):
    if raw_df is None or raw_df.empty:
        raise ValueError("La base cargada está vacía.")

    if not factor_cols:
        raise ValueError("Debe seleccionar al menos un factor experimental.")

    if response_col in factor_cols:
        raise ValueError("La variable respuesta no puede ser también un factor.")

    required_cols = factor_cols + [response_col]

    data = raw_df.copy()

    for col in required_cols:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    if data[required_cols].isna().sum().sum() > 0:
        raise ValueError(
            "Existen valores faltantes o no numéricos en la respuesta o en los factores seleccionados."
        )

    n = len(data)
    k = len(factor_cols)

    if n <= k + 1:
        raise ValueError(
            "No hay suficientes observaciones para ajustar el modelo. "
            "Se requiere más cantidad de corridas que parámetros del modelo."
        )

    model_df = pd.DataFrame()
    model_df["Corrida"] = range(1, n + 1)

    real_design = pd.DataFrame()
    real_design["Corrida"] = range(1, n + 1)

    final_factor_levels = {}

    if coding_mode == "raw":
        if factor_levels is None:
            raise ValueError("Debe definir niveles bajo y alto para codificar los factores.")

        for factor in factor_cols:
            low = float(factor_levels[factor]["low"])
            high = float(factor_levels[factor]["high"])

            if low >= high:
                raise ValueError(
                    f"En el factor {factor}, el nivel bajo debe ser menor que el nivel alto."
                )

            center = (low + high) / 2
            step = (high - low) / 2

            model_df[factor] = (data[factor] - center) / step
            real_design[factor] = data[factor]

            final_factor_levels[factor] = {
                "low": low,
                "high": high
            }

    else:
        for factor in factor_cols:
            model_df[factor] = data[factor]
            real_design[factor] = data[factor]

            final_factor_levels[factor] = {
                "low": -1,
                "high": 1
            }

        max_abs = model_df[factor_cols].abs().max().max()

        if max_abs > 1.5:
            raise ValueError(
                "Seleccionó que los datos ya están codificados, pero existen valores muy alejados "
                "de la escala -1, 0, +1. Revise si realmente debe usar la opción de codificar "
                "desde unidades reales."
            )

    model_df["Respuesta"] = data[response_col]
    model_df["Tipo"] = "Cargado"

    coded_design = model_df[["Corrida"] + factor_cols].copy()
    coded_design["Tipo"] = "Cargado"

    real_design["Tipo"] = "Cargado"

    factor_summary = create_factor_summary_from_levels(final_factor_levels)

    factors = []

    for factor in factor_cols:
        factors.append({
            "name": factor,
            "low": final_factor_levels[factor]["low"],
            "high": final_factor_levels[factor]["high"]
        })

    return {
        "model_df": model_df,
        "coded_design": coded_design,
        "real_design": real_design,
        "factor_summary": factor_summary,
        "factors": factors
    }