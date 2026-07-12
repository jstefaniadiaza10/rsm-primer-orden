from io import BytesIO
from datetime import datetime

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image
)


NAVY = colors.HexColor("#0F1E46")
BLUE = colors.HexColor("#1E3A8A")
GREEN = colors.HexColor("#10B981")
LIGHT_BG = colors.HexColor("#F8FAFC")
BORDER = colors.HexColor("#E5E7EB")
TEXT = colors.HexColor("#1F2937")
MUTED = colors.HexColor("#64748B")


def _safe_text(value):
    if value is None:
        return ""
    text = str(value)
    text = text.replace("ᵏ", "^k")
    text = text.replace("2ᵏ", "2^k")
    return text


def _pretty_name(value):
    text = _safe_text(value)
    return text.replace("_", " ")


def _fmt(value, decimals=4):
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass

    if isinstance(value, (int, float, np.integer, np.floating)):
        return f"{float(value):.{decimals}f}"

    return _safe_text(value)


def _short(value, max_len=28):
    text = _safe_text(value)
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def _build_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=30,
            leading=34,
            textColor=colors.white,
            alignment=TA_LEFT,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CoverSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=12,
            leading=18,
            textColor=colors.white,
            alignment=TA_LEFT,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=22,
            textColor=BLUE,
            spaceBefore=8,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SubTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=TEXT,
            spaceBefore=6,
            spaceAfter=4,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=13,
            textColor=TEXT,
            spaceAfter=6,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Small",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9,
            textColor=TEXT,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableHeader",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.1,
            leading=8,
            textColor=colors.white,
            alignment=TA_LEFT,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableCell",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=7.0,
            leading=8,
            textColor=TEXT,
            alignment=TA_LEFT,
        )
    )

    styles.add(
        ParagraphStyle(
            name="KpiNumber",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            textColor=BLUE,
            alignment=TA_CENTER,
        )
    )

    styles.add(
        ParagraphStyle(
            name="KpiLabel",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9,
            textColor=MUTED,
            alignment=TA_CENTER,
        )
    )

    return styles


def _header_footer(canvas, doc):
    canvas.saveState()

    width, height = A4

    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 1.25 * cm, width, 1.25 * cm, fill=1, stroke=0)

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(1.6 * cm, height - 0.78 * cm, "RSM Primer Orden | Reporte Ejecutivo")

    canvas.setFont("Helvetica", 7.5)
    canvas.drawRightString(
        width - 1.6 * cm,
        height - 0.78 * cm,
        datetime.now().strftime("%d/%m/%Y")
    )

    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(
        1.6 * cm,
        0.75 * cm,
        "Aplicativo de Superficie de Respuesta de Primer Orden"
    )
    canvas.drawRightString(
        width - 1.6 * cm,
        0.75 * cm,
        f"Página {doc.page}"
    )

    canvas.restoreState()


def _df_to_table(df, styles, max_rows=12, max_cols=7, col_widths=None):
    if df is None or len(df) == 0:
        return Paragraph("No disponible.", styles["Body"])

    table_df = df.copy()

    if len(table_df.columns) > max_cols:
        table_df = table_df.iloc[:, :max_cols]

    if len(table_df) > max_rows:
        table_df = table_df.head(max_rows)

    headers = [
        Paragraph(_short(col, 32), styles["TableHeader"])
        for col in table_df.columns
    ]

    rows = []
    for _, row in table_df.iterrows():
        rows.append([
            Paragraph(_short(_fmt(value), 34), styles["TableCell"])
            for value in row.values
        ])

    data = [headers] + rows

    if col_widths is None:
        usable_width = 17.5 * cm
        col_widths = [usable_width / len(headers)] * len(headers)

    table = Table(data, repeatRows=1, colWidths=col_widths)

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.35, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )

    return table


def _kpi_table(kpis, styles):
    row_top = []
    row_bottom = []

    for value, label in kpis:
        row_top.append(Paragraph(_safe_text(value), styles["KpiNumber"]))
        row_bottom.append(Paragraph(_safe_text(label), styles["KpiLabel"]))

    table = Table(
        [row_top, row_bottom],
        colWidths=[17.5 * cm / len(kpis)] * len(kpis),
        rowHeights=[0.85 * cm, 0.45 * cm],
    )

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )

    return table


def _matplotlib_image(fig, width=16.5 * cm):
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=170, bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)

    image = Image(buffer)
    ratio = image.imageHeight / image.imageWidth
    image.drawWidth = width
    image.drawHeight = width * ratio

    return image


def _chart_pareto(effects_df):
    if effects_df is None or effects_df.empty:
        return None

    factor_col = "Parámetro" if "Parámetro" in effects_df.columns else effects_df.columns[0]
    effect_col = "Efecto absoluto" if "Efecto absoluto" in effects_df.columns else None

    if effect_col is None:
        return None

    plot_df = effects_df[[factor_col, effect_col]].copy()
    plot_df[factor_col] = plot_df[factor_col].apply(_pretty_name)
    plot_df = plot_df.sort_values(effect_col, ascending=True)

    fig, ax = plt.subplots(figsize=(7.4, 3.7))
    ax.barh(plot_df[factor_col], plot_df[effect_col], color="#1E3A8A")
    ax.set_title("Pareto de efectos absolutos", fontsize=12, fontweight="bold")
    ax.set_xlabel("Efecto absoluto")
    ax.set_ylabel("Factor")
    ax.grid(axis="x", alpha=0.25)

    for index, value in enumerate(plot_df[effect_col]):
        ax.text(value, index, f" {value:.3f}", va="center", fontsize=8)

    fig.tight_layout()
    return _matplotlib_image(fig)


def _chart_observed_vs_fitted(model_results, response_col="Respuesta"):
    if not model_results or "results_df" not in model_results:
        return None

    df = model_results["results_df"].copy()

    if response_col not in df.columns or "Ajustado" not in df.columns:
        return None

    observed = pd.to_numeric(df[response_col], errors="coerce")
    fitted = pd.to_numeric(df["Ajustado"], errors="coerce")

    valid = ~(observed.isna() | fitted.isna())
    observed = observed[valid]
    fitted = fitted[valid]

    if len(observed) == 0:
        return None

    min_value = min(observed.min(), fitted.min())
    max_value = max(observed.max(), fitted.max())

    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    ax.scatter(fitted, observed, color="#1E3A8A", alpha=0.85)
    ax.plot([min_value, max_value], [min_value, max_value], color="#10B981", linewidth=2)

    ax.set_title("Valores observados vs ajustados", fontsize=12, fontweight="bold")
    ax.set_xlabel("Respuesta ajustada por el modelo")
    ax.set_ylabel("Respuesta observada")
    ax.grid(alpha=0.25)

    fig.tight_layout()
    return _matplotlib_image(fig)


def _chart_residuals(model_results):
    if not model_results or "results_df" not in model_results:
        return None

    df = model_results["results_df"].copy()

    if "Ajustado" not in df.columns or "Residuo" not in df.columns:
        return None

    fitted = pd.to_numeric(df["Ajustado"], errors="coerce")
    residuals = pd.to_numeric(df["Residuo"], errors="coerce")

    valid = ~(fitted.isna() | residuals.isna())
    fitted = fitted[valid]
    residuals = residuals[valid]

    if len(fitted) == 0:
        return None

    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    ax.scatter(fitted, residuals, color="#1E3A8A", alpha=0.85)
    ax.axhline(0, color="#10B981", linewidth=2)

    ax.set_title("Diagnóstico: residuos vs ajustados", fontsize=12, fontweight="bold")
    ax.set_xlabel("Respuesta ajustada")
    ax.set_ylabel("Residuo")
    ax.grid(alpha=0.25)

    fig.tight_layout()
    return _matplotlib_image(fig)


def _chart_steepest(steepest_path_df):
    if steepest_path_df is None or steepest_path_df.empty:
        return None

    if "Paso" not in steepest_path_df.columns or "Respuesta predicha" not in steepest_path_df.columns:
        return None

    plot_df = steepest_path_df.copy()
    plot_df["Paso"] = pd.to_numeric(plot_df["Paso"], errors="coerce")
    plot_df["Respuesta predicha"] = pd.to_numeric(plot_df["Respuesta predicha"], errors="coerce")
    plot_df = plot_df.dropna(subset=["Paso", "Respuesta predicha"])

    if plot_df.empty:
        return None

    fig, ax = plt.subplots(figsize=(7.4, 3.7))
    ax.plot(
        plot_df["Paso"],
        plot_df["Respuesta predicha"],
        marker="o",
        linewidth=2.4,
        color="#1E3A8A"
    )

    ax.set_title("Ruta de ascenso más pronunciado", fontsize=12, fontweight="bold")
    ax.set_xlabel("Paso experimental")
    ax.set_ylabel("Respuesta predicha")
    ax.grid(alpha=0.25)

    fig.tight_layout()
    return _matplotlib_image(fig)


def _cover_page(story, styles, response_label, optimization_goal):
    methodology = "Diseño factorial 2^k + puntos centrales + modelo lineal"

    cover_box = Table(
        [
            [
                Paragraph(
                    "REPORTE EJECUTIVO",
                    styles["CoverTitle"]
                )
            ],
            [
                Paragraph(
                    "Análisis experimental mediante metodología de superficie de respuesta de primer orden",
                    styles["CoverSubtitle"]
                )
            ],
        ],
        colWidths=[17.5 * cm],
        rowHeights=[1.3 * cm, 1.1 * cm],
    )

    cover_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("BOX", (0, 0), (-1, -1), 0, NAVY),
                ("LEFTPADDING", (0, 0), (-1, -1), 22),
                ("RIGHTPADDING", (0, 0), (-1, -1), 22),
                ("TOPPADDING", (0, 0), (-1, -1), 14),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )

    story.append(cover_box)
    story.append(Spacer(1, 1.0 * cm))

    info_df = pd.DataFrame(
        [
            ["Variable respuesta", response_label],
            ["Objetivo del estudio", optimization_goal],
            ["Metodología", methodology],
            ["Fecha de generación", datetime.now().strftime("%d/%m/%Y %H:%M")],
        ],
        columns=["Campo", "Detalle"]
    )

    story.append(
        _df_to_table(
            info_df,
            styles,
            max_rows=10,
            max_cols=2,
            col_widths=[5.0 * cm, 12.5 * cm]
        )
    )

    story.append(Spacer(1, 0.8 * cm))

    story.append(
        Paragraph(
            (
                "Este documento consolida los resultados del diseño experimental, ajuste del modelo, "
                "evaluación ANOVA, diagnóstico de residuos, Pareto de efectos y ruta de mejora mediante "
                "ascenso más pronunciado. El reporte está orientado a apoyar decisiones técnicas y gerenciales."
            ),
            styles["Body"]
        )
    )

    story.append(PageBreak())


def _get_anova_pvalue(anova_df):
    if anova_df is None or anova_df.empty:
        return None

    try:
        model_row = anova_df[anova_df["Fuente"] == "Modelo"].iloc[0]
        return model_row["p-valor"]
    except Exception:
        return None


def _get_priority_factor(effects_df):
    if effects_df is None or effects_df.empty:
        return "No disponible", None

    factor_col = "Parámetro" if "Parámetro" in effects_df.columns else effects_df.columns[0]
    effect_col = "Efecto estimado" if "Efecto estimado" in effects_df.columns else None

    factor = effects_df.iloc[0][factor_col]
    effect = effects_df.iloc[0][effect_col] if effect_col else None

    return _pretty_name(factor), effect


def _simplify_steepest_path(steepest_path_df):
    if steepest_path_df is None or steepest_path_df.empty:
        return steepest_path_df

    df = steepest_path_df.copy()

    selected_cols = []

    for col in ["Paso", "Respuesta predicha"]:
        if col in df.columns:
            selected_cols.append(col)

    real_cols = [col for col in df.columns if " real" in col.lower() or col.lower().endswith("_real")]

    selected_cols.extend(real_cols)

    if not selected_cols:
        return df.head(8)

    return df[selected_cols].head(8)


def create_management_pdf_report(
    response_label,
    optimization_goal,
    factor_summary=None,
    coded_design=None,
    real_design=None,
    model_data=None,
    model_results=None,
    anova_df=None,
    effects_df=None,
    steepest_direction_df=None,
    steepest_path_df=None,
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.7 * cm,
        bottomMargin=1.35 * cm,
    )

    styles = _build_styles()
    story = []

    response_label = _safe_text(response_label or "Respuesta")
    optimization_goal = _safe_text(optimization_goal or "No definido")

    _cover_page(
        story=story,
        styles=styles,
        response_label=response_label,
        optimization_goal=optimization_goal
    )

    r2 = model_results.get("r2") if model_results else None
    r2_adj = model_results.get("r2_adj") if model_results else None
    anova_p = _get_anova_pvalue(anova_df)
    priority_factor, priority_effect = _get_priority_factor(effects_df)

    story.append(Paragraph("1. Resumen ejecutivo", styles["SectionTitle"]))

    story.append(
        _kpi_table(
            [
                [_fmt(r2), "R²"],
                [_fmt(r2_adj), "R² ajustado"],
                [_fmt(anova_p), "ANOVA p-valor"],
                [_short(priority_factor, 24), "Factor prioritario"],
            ],
            styles
        )
    )

    story.append(Spacer(1, 0.35 * cm))

    story.append(
        Paragraph(
            (
                f"El modelo lineal de primer orden fue ajustado para explicar la variable respuesta "
                f"<b>{response_label}</b>, con objetivo declarado de <b>{optimization_goal.lower()}</b>."
            ),
            styles["Body"]
        )
    )

    if r2 is not None and r2_adj is not None:
        story.append(
            Paragraph(
                (
                    f"El ajuste alcanzó un R² de <b>{_fmt(r2)}</b> y un R² ajustado de "
                    f"<b>{_fmt(r2_adj)}</b>, lo que permite evaluar preliminarmente la capacidad "
                    f"explicativa del modelo dentro de la región experimental estudiada."
                ),
                styles["Body"]
            )
        )

    if anova_p is not None:
        if float(anova_p) < 0.05:
            anova_text = (
                f"El ANOVA global resultó estadísticamente significativo "
                f"(p = <b>{_fmt(anova_p)}</b>), por lo que existe evidencia de que al menos un factor "
                f"influye sobre <b>{response_label}</b>."
            )
        else:
            anova_text = (
                f"El ANOVA global no resultó estadísticamente significativo "
                f"(p = <b>{_fmt(anova_p)}</b>). Se recomienda revisar el diseño, el número de corridas "
                f"o la variabilidad experimental."
            )

        story.append(Paragraph(anova_text, styles["Body"]))

    if priority_factor != "No disponible":
        effect_text = f", con efecto estimado de <b>{_fmt(priority_effect)}</b>" if priority_effect is not None else ""
        story.append(
            Paragraph(
                f"El Pareto de efectos identificó como factor prioritario a <b>{priority_factor}</b>{effect_text}.",
                styles["Body"]
            )
        )

    if steepest_path_df is not None and not steepest_path_df.empty and "Respuesta predicha" in steepest_path_df.columns:
        try:
            change = (
                float(steepest_path_df["Respuesta predicha"].iloc[-1])
                - float(steepest_path_df["Respuesta predicha"].iloc[0])
            )

            story.append(
                Paragraph(
                    (
                        f"La ruta de ascenso más pronunciado propone nuevas corridas experimentales "
                        f"con un cambio predicho acumulado de <b>{_fmt(change)}</b> unidades en "
                        f"<b>{response_label}</b> dentro de los pasos evaluados."
                    ),
                    styles["Body"]
                )
            )
        except Exception:
            pass

    story.append(
        Paragraph(
            (
                "La decisión recomendada es ejecutar las corridas propuestas, registrar la respuesta real "
                "y confirmar experimentalmente la mejora antes de escalar o modificar condiciones de proceso."
            ),
            styles["Body"]
        )
    )

    story.append(Spacer(1, 0.35 * cm))

    story.append(Paragraph("2. Diseño experimental", styles["SectionTitle"]))

    story.append(
        Paragraph(
            (
                "El estudio se desarrolló bajo un diseño factorial completo de primer orden, incluyendo puntos "
                "centrales para apoyar la evaluación preliminar del comportamiento de la respuesta dentro de la región experimental."
            ),
            styles["Body"]
        )
    )

    if factor_summary is not None:
        story.append(_df_to_table(factor_summary, styles, max_rows=12, max_cols=5))
        story.append(Spacer(1, 0.25 * cm))

    story.append(Paragraph("3. Modelo lineal de primer orden", styles["SectionTitle"]))

    if model_results and model_results.get("equation"):
        equation = _safe_text(model_results.get("equation"))
        story.append(
            Paragraph(
                f"<b>Ecuación estimada:</b> {equation}",
                styles["Body"]
            )
        )

    if model_results and "coef_df" in model_results:
        story.append(
            _df_to_table(
                model_results["coef_df"],
                styles,
                max_rows=10,
                max_cols=5
            )
        )

    story.append(PageBreak())

    story.append(Paragraph("4. Visualizaciones del modelo", styles["SectionTitle"]))

    story.append(
        Paragraph(
            (
                "Los gráficos siguientes permiten evaluar visualmente el ajuste del modelo, el comportamiento "
                "de los residuos y la importancia relativa de los factores."
            ),
            styles["Body"]
        )
    )

    chart_observed = _chart_observed_vs_fitted(model_results)
    chart_residuals = _chart_residuals(model_results)

    if chart_observed is not None:
        story.append(chart_observed)
        story.append(Spacer(1, 0.25 * cm))

    if chart_residuals is not None:
        story.append(chart_residuals)
        story.append(Spacer(1, 0.25 * cm))

    story.append(Paragraph("5. Evaluación ANOVA", styles["SectionTitle"]))

    story.append(
        Paragraph(
            (
                f"El ANOVA evalúa la significancia global del modelo lineal y permite determinar si los factores "
                f"considerados explican una proporción relevante de la variabilidad observada en <b>{response_label}</b>."
            ),
            styles["Body"]
        )
    )

    if anova_df is not None:
        story.append(_df_to_table(anova_df, styles, max_rows=5, max_cols=6))

    story.append(PageBreak())

    story.append(Paragraph("6. Pareto de efectos", styles["SectionTitle"]))

    story.append(
        Paragraph(
            (
                "El gráfico Pareto prioriza los factores según su efecto absoluto sobre la variable respuesta. "
                "Los factores ubicados en la parte superior son los más influyentes dentro de la región experimental estudiada."
            ),
            styles["Body"]
        )
    )

    pareto_chart = _chart_pareto(effects_df)

    if pareto_chart is not None:
        story.append(pareto_chart)
        story.append(Spacer(1, 0.25 * cm))

    if effects_df is not None:
        story.append(_df_to_table(effects_df, styles, max_rows=10, max_cols=6))

    story.append(Spacer(1, 0.35 * cm))

    story.append(Paragraph("7. Ascenso más pronunciado", styles["SectionTitle"]))

    story.append(
        Paragraph(
            (
                "La ruta de ascenso más pronunciado propone nuevas condiciones experimentales en la dirección "
                "de mejora estimada por el modelo de primer orden. Estas corridas deben validarse experimentalmente "
                "antes de tomar decisiones definitivas."
            ),
            styles["Body"]
        )
    )

    steepest_chart = _chart_steepest(steepest_path_df)

    if steepest_chart is not None:
        story.append(steepest_chart)
        story.append(Spacer(1, 0.25 * cm))

    if steepest_direction_df is not None:
        story.append(Paragraph("Dirección recomendada por factor", styles["SubTitle"]))
        story.append(_df_to_table(steepest_direction_df, styles, max_rows=8, max_cols=5))
        story.append(Spacer(1, 0.25 * cm))

    if steepest_path_df is not None:
        story.append(Paragraph("Corridas experimentales propuestas", styles["SubTitle"]))

        simplified_path = _simplify_steepest_path(steepest_path_df)

        story.append(
            _df_to_table(
                simplified_path,
                styles,
                max_rows=8,
                max_cols=7
            )
        )

    story.append(Spacer(1, 0.35 * cm))

    story.append(Paragraph("8. Recomendación gerencial final", styles["SectionTitle"]))

    story.append(
        Paragraph(
            (
                "Se recomienda ejecutar las corridas sugeridas por la ruta de ascenso más pronunciado, "
                "comparar la respuesta observada contra la respuesta predicha y documentar la mejora real. "
                "Si la respuesta deja de mejorar, el comportamiento del proceso podría requerir una nueva región "
                "experimental o un diseño de segundo orden. Este aplicativo se mantiene deliberadamente en el alcance "
                "de modelos de primer orden."
            ),
            styles["Body"]
        )
    )

    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)

    buffer.seek(0)
    return buffer.getvalue()