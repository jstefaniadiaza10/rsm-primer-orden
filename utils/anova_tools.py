import pandas as pd
import numpy as np
from scipy import stats


def compute_regression_anova(model_results, response_col="Respuesta"):
    """
    Calcula la tabla ANOVA global para un modelo lineal de primer orden.

    Fuentes:
    - Modelo
    - Error
    - Total
    """

    results_df = model_results["results_df"].copy()

    y = results_df[response_col].astype(float)
    y_hat = results_df["Ajustado"].astype(float)
    residuals = results_df["Residuo"].astype(float)

    n = len(y)

    # Número de predictores, sin contar intercepto
    coef_df = model_results["coef_df"]
    p = coef_df[coef_df["Parámetro"] != "const"].shape[0]

    ss_total = np.sum((y - y.mean()) ** 2)
    ss_model = np.sum((y_hat - y.mean()) ** 2)
    ss_error = np.sum(residuals ** 2)

    df_model = p
    df_error = n - p - 1
    df_total = n - 1

    ms_model = ss_model / df_model if df_model > 0 else np.nan
    ms_error = ss_error / df_error if df_error > 0 else np.nan

    f_value = ms_model / ms_error if ms_error > 0 else np.nan
    p_value = stats.f.sf(f_value, df_model, df_error) if df_error > 0 else np.nan

    anova_df = pd.DataFrame({
        "Fuente": ["Modelo", "Error", "Total"],
        "SC": [ss_model, ss_error, ss_total],
        "GL": [df_model, df_error, df_total],
        "CM": [ms_model, ms_error, np.nan],
        "F": [f_value, np.nan, np.nan],
        "p-valor": [p_value, np.nan, np.nan]
    })

    return anova_df


def interpret_anova(anova_df, alpha=0.05, response_label="la respuesta"):
    """
    Genera una interpretación breve del ANOVA.
    """

    model_row = anova_df[anova_df["Fuente"] == "Modelo"].iloc[0]

    p_value = model_row["p-valor"]
    f_value = model_row["F"]

    if pd.isna(p_value):
        return {
            "decision": "No evaluable",
            "message": (
                "No es posible evaluar la significancia global del modelo. "
                "Revise que existan suficientes grados de libertad residuales."
            )
        }

    if p_value < alpha:
        return {
            "decision": "Modelo significativo",
            "message": (
                f"Con α = {alpha}, el modelo lineal es estadísticamente significativo "
                f"(F = {f_value:.4f}, p = {p_value:.4f}). "
                f"Existe evidencia de que al menos un factor influye en la variable respuesta {response_label}."
            )
        }

    return {
        "decision": "Modelo no significativo",
        "message": (
            f"Con α = {alpha}, el modelo lineal no es estadísticamente significativo "
            f"(F = {f_value:.4f}, p = {p_value:.4f}). "
            f"No existe evidencia suficiente de efecto global de los factores sobre la variable respuesta {response_label}."
        )
    }