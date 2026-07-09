from io import BytesIO
import pandas as pd


def build_executive_summary(
    response_label,
    optimization_goal,
    model_results=None,
    anova_df=None,
    effects_df=None,
    steepest_path_df=None
):
    """
    Construye un resumen ejecutivo en formato Markdown.
    """

    lines = []

    lines.append("# Reporte Ejecutivo - RSM de Primer Orden")
    lines.append("")
    lines.append(f"**Variable respuesta:** {response_label}")
    lines.append(f"**Objetivo declarado:** {optimization_goal}")
    lines.append("")

    lines.append("## 1. Alcance metodológico")
    lines.append(
        "El análisis corresponde a una metodología de superficie de respuesta de primer orden. "
        "Se emplea un diseño factorial completo 2^k con puntos centrales y un modelo lineal "
        "sin términos cuadráticos."
    )
    lines.append("")

    if model_results is not None:
        lines.append("## 2. Modelo lineal ajustado")
        lines.append(f"**Ecuación estimada:** `{model_results['equation']}`")
        lines.append(f"**R²:** {model_results['r2']:.4f}")
        lines.append(f"**R² ajustado:** {model_results['r2_adj']:.4f}")
        lines.append("")

    if anova_df is not None:
        try:
            model_row = anova_df[anova_df["Fuente"] == "Modelo"].iloc[0]
            lines.append("## 3. ANOVA")
            lines.append(f"**F:** {model_row['F']:.4f}")
            lines.append(f"**p-valor:** {model_row['p-valor']:.4f}")
            lines.append("")
        except Exception:
            pass

    if effects_df is not None and not effects_df.empty:
        top = effects_df.iloc[0]
        lines.append("## 4. Factor más influyente")
        lines.append(
            f"El factor con mayor efecto absoluto es **{top['Parámetro']}**, "
            f"con un efecto estimado de **{top['Efecto estimado']:.4f}**."
        )
        lines.append("")

    if steepest_path_df is not None and not steepest_path_df.empty:
        lines.append("## 5. Ascenso más pronunciado")
        lines.append(
            "Se generó una ruta experimental propuesta para explorar nuevas condiciones "
            "del proceso en la dirección de mejora estimada por el modelo lineal."
        )
        lines.append(
            f"Número de pasos propuestos: **{steepest_path_df['Paso'].max()}**."
        )
        lines.append("")

    lines.append("## 6. Recomendación final")
    lines.append(
        "Ejecutar las corridas propuestas por el módulo de ascenso más pronunciado, "
        "registrar la nueva respuesta observada y verificar si existe mejora real del proceso. "
        "Si la respuesta deja de mejorar, se recomienda construir un nuevo diseño alrededor "
        "de la mejor zona encontrada."
    )

    return "\n".join(lines)


def create_excel_report(
    factor_summary=None,
    coded_design=None,
    real_design=None,
    model_data=None,
    model_results=None,
    anova_df=None,
    effects_df=None,
    steepest_direction_df=None,
    steepest_path_df=None,
    executive_summary=None
):
    """
    Crea un archivo Excel con las principales salidas del aplicativo.
    """

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        if executive_summary is not None:
            summary_df = pd.DataFrame({
                "Reporte Ejecutivo": executive_summary.split("\n")
            })
            summary_df.to_excel(writer, index=False, sheet_name="Resumen_Ejecutivo")

        if factor_summary is not None:
            factor_summary.to_excel(writer, index=False, sheet_name="Factores")

        if coded_design is not None:
            coded_design.to_excel(writer, index=False, sheet_name="Diseno_Codificado")

        if real_design is not None:
            real_design.to_excel(writer, index=False, sheet_name="Diseno_Real")

        if model_data is not None:
            model_data.to_excel(writer, index=False, sheet_name="Datos_Modelo")

        if model_results is not None:
            model_results["coef_df"].to_excel(writer, index=False, sheet_name="Coeficientes")
            model_results["results_df"].to_excel(writer, index=False, sheet_name="Ajustados_Residuos")

            metrics_df = pd.DataFrame({
                "Metrica": ["R2", "R2 ajustado", "AIC", "BIC", "Ecuacion"],
                "Valor": [
                    model_results["r2"],
                    model_results["r2_adj"],
                    model_results["aic"],
                    model_results["bic"],
                    model_results["equation"]
                ]
            })
            metrics_df.to_excel(writer, index=False, sheet_name="Metricas_Modelo")

        if anova_df is not None:
            anova_df.to_excel(writer, index=False, sheet_name="ANOVA")

        if effects_df is not None:
            effects_df.to_excel(writer, index=False, sheet_name="Pareto_Efectos")

        if steepest_direction_df is not None:
            steepest_direction_df.to_excel(writer, index=False, sheet_name="Direccion_Ascenso")

        if steepest_path_df is not None:
            steepest_path_df.to_excel(writer, index=False, sheet_name="Ruta_Ascenso")

    output.seek(0)

    return output