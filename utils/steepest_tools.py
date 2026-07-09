import numpy as np
import pandas as pd
import plotly.express as px


def get_model_coefficients(model_results, factor_cols):
    """
    Extrae los coeficientes del modelo para los factores.
    """

    coef_df = model_results["coef_df"].copy()

    coef_map = dict(zip(coef_df["Parámetro"], coef_df["Coeficiente"]))

    coefficients = {
        factor: float(coef_map.get(factor, 0.0))
        for factor in factor_cols
    }

    intercept = float(coef_map.get("const", 0.0))

    return intercept, coefficients


def build_factor_scaling(factors):
    """
    Construye información de centro y semirango para pasar de escala codificada a escala real.
    """

    rows = {}

    for factor in factors:
        name = factor["name"]
        low = float(factor["low"])
        high = float(factor["high"])

        center = (low + high) / 2
        half_range = (high - low) / 2

        rows[name] = {
            "low": low,
            "high": high,
            "center": center,
            "half_range": half_range
        }

    return rows


def coded_to_real_value(coded_value, factor_name, scaling):
    """
    Convierte un valor codificado a escala real.
    """

    center = scaling[factor_name]["center"]
    half_range = scaling[factor_name]["half_range"]

    return center + coded_value * half_range


def compute_steepest_path(
    model_results,
    factor_cols,
    factors,
    optimization_goal="Maximizar",
    n_steps=6,
    coded_step=0.25,
    start_point="Centro del diseño",
    response_col="Respuesta"
):
    """
    Calcula la ruta de ascenso o descenso más pronunciado.

    Para maximizar:
        dirección = gradiente = beta

    Para minimizar:
        dirección = -gradiente = -beta
    """

    intercept, coefficients = get_model_coefficients(
        model_results=model_results,
        factor_cols=factor_cols
    )

    beta = np.array([coefficients[factor] for factor in factor_cols], dtype=float)

    if optimization_goal == "Minimizar":
        direction = -beta
    else:
        direction = beta

    if np.all(np.isclose(direction, 0)):
        raise ValueError(
            "Todos los coeficientes de los factores son cercanos a cero. "
            "No se puede definir una dirección de mejora."
        )

    # Normalización: el factor más influyente avanza coded_step por paso.
    max_abs = np.max(np.abs(direction))
    normalized_direction = direction / max_abs

    if start_point == "Mejor corrida observada":
        results_df = model_results["results_df"].copy()

        if optimization_goal == "Minimizar":
            best_row = results_df.loc[results_df[response_col].idxmin()]
        else:
            best_row = results_df.loc[results_df[response_col].idxmax()]

        base_coded = np.array([best_row[factor] for factor in factor_cols], dtype=float)

    else:
        base_coded = np.zeros(len(factor_cols))

    scaling = build_factor_scaling(factors)

    rows = []

    for step in range(n_steps + 1):

        coded_values = base_coded + step * coded_step * normalized_direction

        predicted = intercept + np.dot(beta, coded_values)

        row = {
            "Paso": step,
            "Respuesta predicha": predicted
        }

        for i, factor in enumerate(factor_cols):
            row[f"{factor} codificado"] = coded_values[i]
            row[f"{factor} real"] = coded_to_real_value(
                coded_value=coded_values[i],
                factor_name=factor,
                scaling=scaling
            )

        rows.append(row)

    path_df = pd.DataFrame(rows)

    direction_df = pd.DataFrame({
        "Factor": factor_cols,
        "Coeficiente": beta,
        "Dirección normalizada": normalized_direction,
        "Cambio codificado por paso": coded_step * normalized_direction
    })

    direction_df["Sentido recomendado"] = np.where(
        direction_df["Cambio codificado por paso"] > 0,
        "Aumentar",
        np.where(
            direction_df["Cambio codificado por paso"] < 0,
            "Disminuir",
            "Mantener"
        )
    )

    return path_df, direction_df


def create_steepest_response_plot(path_df, response_label="Respuesta"):
    """
    Gráfico de la respuesta predicha a lo largo de los pasos.
    """

    fig = px.line(
        path_df,
        x="Paso",
        y="Respuesta predicha",
        markers=True,
        title=f"Trayectoria propuesta para {response_label}",
        labels={
            "Paso": "Paso experimental",
            "Respuesta predicha": f"{response_label} predicha"
        }
    )

    fig.update_layout(
        height=420,
        title_x=0.02
    )

    return fig


def create_direction_plot(direction_df):
    """
    Gráfico de dirección normalizada por factor.
    """

    fig = px.bar(
        direction_df,
        x="Factor",
        y="Cambio codificado por paso",
        title="Dirección de mejora por factor",
        text=direction_df["Cambio codificado por paso"].round(4)
    )

    fig.add_hline(
        y=0,
        line_dash="dash"
    )

    fig.update_layout(
        height=420,
        title_x=0.02,
        xaxis_title="Factor",
        yaxis_title="Cambio codificado por paso"
    )

    return fig


def interpret_steepest_path(direction_df, response_label="Respuesta", optimization_goal="Maximizar"):
    """
    Genera interpretación automática de la ruta.
    """

    messages = []

    objective_text = "aumentar" if optimization_goal == "Maximizar" else "reducir"

    messages.append(
        f"La ruta propuesta busca **{objective_text} {response_label}** siguiendo "
        "la dirección del gradiente estimado por el modelo lineal."
    )

    main_factor = direction_df.loc[
        direction_df["Cambio codificado por paso"].abs().idxmax()
    ]

    messages.append(
        f"El factor que marca la mayor variación por paso es **{main_factor['Factor']}**. "
        f"El sentido recomendado para este factor es: **{main_factor['Sentido recomendado']}**."
    )

    for _, row in direction_df.iterrows():
        messages.append(
            f"Para **{row['Factor']}**, el cambio codificado sugerido por paso es "
            f"{row['Cambio codificado por paso']:.4f}; recomendación: "
            f"**{row['Sentido recomendado']}**."
        )

    messages.append(
        "Estas corridas son propuestas de exploración. Después de ejecutarlas, "
        "se debe registrar la nueva respuesta observada y verificar si el proceso continúa mejorando."
    )

    return messages