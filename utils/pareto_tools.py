import pandas as pd
import numpy as np
import plotly.graph_objects as go


def compute_effects_table(model_results):
    """
    Construye la tabla de efectos para un modelo lineal de primer orden.

    En variables codificadas (-1, +1), el efecto principal de un factor
    se calcula como:

        Efecto = 2 * coeficiente
    """

    coef_df = model_results["coef_df"].copy()

    effects_df = coef_df[coef_df["Parámetro"] != "const"].copy()

    effects_df["Efecto estimado"] = 2 * effects_df["Coeficiente"]
    effects_df["Efecto absoluto"] = effects_df["Efecto estimado"].abs()
    effects_df["Importancia relativa (%)"] = (
        effects_df["Efecto absoluto"] / effects_df["Efecto absoluto"].sum()
    ) * 100

    effects_df["Dirección"] = np.where(
        effects_df["Efecto estimado"] >= 0,
        "Aumenta la respuesta",
        "Disminuye la respuesta"
    )

    effects_df = effects_df.sort_values(
        by="Efecto absoluto",
        ascending=False
    ).reset_index(drop=True)

    effects_df.insert(0, "Ranking", range(1, len(effects_df) + 1))

    return effects_df


def create_pareto_plot(effects_df, response_label="Respuesta"):
    """
    Crea el gráfico Pareto de efectos absolutos.
    """

    plot_df = effects_df.sort_values(
        by="Efecto absoluto",
        ascending=True
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=plot_df["Efecto absoluto"],
            y=plot_df["Parámetro"],
            orientation="h",
            text=plot_df["Efecto absoluto"].round(4),
            textposition="auto",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Efecto absoluto: %{x:.4f}<br>"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title=f"Pareto de efectos sobre {response_label}",
        xaxis_title="Efecto absoluto",
        yaxis_title="Factor",
        height=420,
        title_x=0.02
    )

    return fig


def create_signed_effects_plot(effects_df, response_label="Respuesta"):
    """
    Crea gráfico de efectos con signo.
    """

    plot_df = effects_df.sort_values(
        by="Efecto estimado",
        ascending=True
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=plot_df["Efecto estimado"],
            y=plot_df["Parámetro"],
            orientation="h",
            text=plot_df["Efecto estimado"].round(4),
            textposition="auto",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Efecto estimado: %{x:.4f}<br>"
                "<extra></extra>"
            )
        )
    )

    fig.add_vline(
        x=0,
        line_dash="dash"
    )

    fig.update_layout(
        title=f"Efectos con signo sobre {response_label}",
        xaxis_title="Efecto estimado",
        yaxis_title="Factor",
        height=420,
        title_x=0.02
    )

    return fig


def interpret_effects(effects_df, response_label="Respuesta", optimization_goal="Maximizar"):
    """
    Genera interpretación automática de los efectos principales.
    """

    if effects_df.empty:
        return [
            "No existen factores disponibles para construir el Pareto de efectos."
        ]

    main_factor = effects_df.iloc[0]

    factor_name = main_factor["Parámetro"]
    effect_value = main_factor["Efecto estimado"]
    relative_importance = main_factor["Importancia relativa (%)"]

    messages = []

    messages.append(
        f"El factor con mayor efecto absoluto sobre {response_label} es "
        f"**{factor_name}**, con un efecto estimado de {effect_value:.4f}."
    )

    messages.append(
        f"Este factor concentra aproximadamente el {relative_importance:.2f}% "
        "de la importancia relativa entre los efectos principales evaluados."
    )

    if effect_value > 0:
        messages.append(
            f"Al pasar {factor_name} del nivel bajo (-1) al nivel alto (+1), "
            f"{response_label} tiende a aumentar."
        )
    elif effect_value < 0:
        messages.append(
            f"Al pasar {factor_name} del nivel bajo (-1) al nivel alto (+1), "
            f"{response_label} tiende a disminuir."
        )
    else:
        messages.append(
            f"El efecto estimado de {factor_name} es cercano a cero."
        )

    if optimization_goal == "Maximizar":
        messages.append(
            "Como el objetivo declarado es maximizar, los efectos positivos son favorables "
            "y los efectos negativos deben revisarse con cuidado."
        )
    else:
        messages.append(
            "Como el objetivo declarado es minimizar, los efectos negativos son favorables "
            "y los efectos positivos deben revisarse con cuidado."
        )

    return messages