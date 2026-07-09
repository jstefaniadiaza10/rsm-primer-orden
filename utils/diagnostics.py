import numpy as np
import pandas as pd
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go


def compute_diagnostic_metrics(model_results, response_col="Respuesta"):
    """
    Calcula métricas básicas de diagnóstico del modelo.
    """

    results_df = model_results["results_df"].copy()

    y = results_df[response_col].astype(float)
    fitted = results_df["Ajustado"].astype(float)
    residuals = results_df["Residuo"].astype(float)

    n = len(residuals)

    rmse = np.sqrt(np.mean(residuals ** 2))
    mae = np.mean(np.abs(residuals))
    mean_residual = np.mean(residuals)
    max_abs_residual = np.max(np.abs(residuals))

    if np.sum(residuals ** 2) > 0 and n > 1:
        durbin_watson = np.sum(np.diff(residuals) ** 2) / np.sum(residuals ** 2)
    else:
        durbin_watson = np.nan

    if 3 <= n <= 5000:
        shapiro_stat, shapiro_p = stats.shapiro(residuals)
    else:
        shapiro_stat, shapiro_p = np.nan, np.nan

    return {
        "n": n,
        "rmse": rmse,
        "mae": mae,
        "mean_residual": mean_residual,
        "max_abs_residual": max_abs_residual,
        "durbin_watson": durbin_watson,
        "shapiro_stat": shapiro_stat,
        "shapiro_p": shapiro_p
    }


def create_residuals_vs_fitted_plot(model_results):
    """
    Gráfico de residuos vs valores ajustados.
    """

    df = model_results["results_df"].copy()

    fig = px.scatter(
        df,
        x="Ajustado",
        y="Residuo",
        hover_data=df.columns,
        title="Residuos vs valores ajustados",
        labels={
            "Ajustado": "Valor ajustado",
            "Residuo": "Residuo"
        }
    )

    fig.add_hline(
        y=0,
        line_dash="dash"
    )

    fig.update_layout(
        height=420,
        title_x=0.02
    )

    return fig


def create_histogram_residuals_plot(model_results):
    """
    Histograma de residuos.
    """

    df = model_results["results_df"].copy()

    fig = px.histogram(
        df,
        x="Residuo",
        nbins=10,
        title="Distribución de residuos",
        labels={
            "Residuo": "Residuo"
        }
    )

    fig.update_layout(
        height=420,
        title_x=0.02
    )

    return fig


def create_qq_plot(model_results):
    """
    Gráfico QQ para evaluar normalidad de residuos.
    """

    residuals = model_results["results_df"]["Residuo"].astype(float)

    theoretical_q, ordered_residuals = stats.probplot(
        residuals,
        dist="norm",
        fit=False
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=theoretical_q,
            y=ordered_residuals,
            mode="markers",
            name="Residuos"
        )
    )

    min_x = min(theoretical_q)
    max_x = max(theoretical_q)
    min_y = min(ordered_residuals)
    max_y = max(ordered_residuals)

    fig.add_trace(
        go.Scatter(
            x=[min_x, max_x],
            y=[min_y, max_y],
            mode="lines",
            name="Referencia",
            line=dict(dash="dash")
        )
    )

    fig.update_layout(
        title="Gráfico QQ de residuos",
        xaxis_title="Cuantiles teóricos normales",
        yaxis_title="Cuantiles observados de residuos",
        height=420,
        title_x=0.02
    )

    return fig


def create_observed_vs_fitted_plot(model_results, response_col="Respuesta", response_label="Respuesta"):
    """
    Gráfico de valores observados vs ajustados.
    """

    df = model_results["results_df"].copy()

    fig = px.scatter(
        df,
        x=response_col,
        y="Ajustado",
        hover_data=df.columns,
        title="Valores observados vs valores ajustados",
        labels={
            response_col: response_label,
            "Ajustado": "Valor ajustado"
        }
    )

    min_value = min(df[response_col].min(), df["Ajustado"].min())
    max_value = max(df[response_col].max(), df["Ajustado"].max())

    fig.add_trace(
        go.Scatter(
            x=[min_value, max_value],
            y=[min_value, max_value],
            mode="lines",
            name="Ajuste perfecto",
            line=dict(dash="dash")
        )
    )

    fig.update_layout(
        height=420,
        title_x=0.02
    )

    return fig


def interpret_diagnostics(metrics, alpha=0.05):
    """
    Interpretación breve de diagnóstico.
    """

    messages = []

    if abs(metrics["mean_residual"]) < 0.10 * metrics["rmse"]:
        messages.append(
            "El promedio de los residuos es cercano a cero, lo cual es deseable en un modelo lineal."
        )
    else:
        messages.append(
            "El promedio de los residuos no es tan cercano a cero. Conviene revisar el ajuste del modelo."
        )

    if not np.isnan(metrics["shapiro_p"]):
        if metrics["shapiro_p"] >= alpha:
            messages.append(
                f"La prueba de Shapiro-Wilk no evidencia una desviación fuerte de normalidad "
                f"(p = {metrics['shapiro_p']:.4f})."
            )
        else:
            messages.append(
                f"La prueba de Shapiro-Wilk sugiere posible falta de normalidad en los residuos "
                f"(p = {metrics['shapiro_p']:.4f})."
            )
    else:
        messages.append(
            "No se pudo calcular la prueba de Shapiro-Wilk por el tamaño de muestra."
        )

    if not np.isnan(metrics["durbin_watson"]):
        if 1.5 <= metrics["durbin_watson"] <= 2.5:
            messages.append(
                f"El estadístico Durbin-Watson es {metrics['durbin_watson']:.4f}, "
                "sin señales fuertes de autocorrelación residual."
            )
        else:
            messages.append(
                f"El estadístico Durbin-Watson es {metrics['durbin_watson']:.4f}. "
                "Conviene revisar el orden de las corridas y la independencia de los residuos."
            )

    return messages