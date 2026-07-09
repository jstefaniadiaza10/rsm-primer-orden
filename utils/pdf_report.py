from io import BytesIO
from datetime import datetime

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


# =====================================================
# CONFIGURACIÓN VISUAL
# =====================================================

NAVY = colors.HexColor("#1E3A8A")
DARK_NAVY = colors.HexColor("#0F1E46")
GREEN = colors.HexColor("#10B981")
LIGHT_BG = colors.HexColor("#F8FAFC")
TEXT = colors.HexColor("#1F2937")
MUTED = colors.HexColor("#64748B")
BORDER = colors.HexColor("#E5E7EB")


def _fmt(value, decimals=4):
    """
    Formatea valores numéricos para el PDF.
    """

    try:
        if pd.isna(value):
            return ""
        if isinstance(value, (int, float)):
            return f"{value:.{decimals}f}"
        return str(value)
    except Exception:
        return str(value)


def _safe_text(value):
    if value is None:
        return ""
    return str(value)


def _build_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=32,
            textColor=colors.white,
            alignment=TA_LEFT,
            spaceAfter=16,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CoverSubtitle",
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
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=20,
            textColor=NAVY,
            spaceBefore=14,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyCustom",
            fontName="Helvetica",
            fontSize=9.5,
            leading=14,
            textColor=TEXT,
            alignment=TA_LEFT,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SmallMuted",
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=MUTED,
        )
    )

    styles.add(
        ParagraphStyle(
            name="KpiValue",
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=NAVY,
            alignment=TA_CENTER,
        )
    )

    styles.add(
        ParagraphStyle(
            name="KpiLabel",
            fontName="Helvetica",
            fontSize=7.5,
            leading=10,
            textColor=MUTED,
            alignment=TA_CENTER,
        )
    )

    return styles


def _header_footer(canvas, doc):
    """
    Encabezado y pie de página.
    """

    canvas.saveState()

    width, height = A4

    # Header
    canvas.setFillColor(DARK_NAVY)
    canvas.rect(0, height - 1.05 * cm, width, 1.05 * cm, fill=1, stroke=0)

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(1.4 * cm, height - 0.65 * cm, "RSM Primer Orden | Reporte Ejecutivo")

    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(
        width - 1.4 * cm,
        height - 0.65 * cm,
        datetime.now().strftime("%d/%m/%Y")
    )

    # Footer
    canvas.setStrokeColor(BORDER)
    canvas.line(1.4 * cm, 1.15 * cm, width - 1.4 * cm, 1.15 * cm)

    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.4 * cm, 0.75 * cm, "Aplicativo de Superficie de Respuesta de Primer Orden")
    canvas.drawRightString(width - 1.4 * cm, 0.75 * cm, f"Página {doc.page}")

    canvas.restoreState()


def _cover_page(response_label, optimization_goal, styles):
    """
    Portada gerencial.
    """

    elements = []

    title_table = Table(
        [
            [
                Paragraph("REPORTE EJECUTIVO", styles["CoverTitle"]),
            ],
            [
                Paragraph(
                    "Análisis experimental mediante metodología de superficie de respuesta de primer orden",
                    styles["CoverSubtitle"],
                )
            ],
        ],
        colWidths=[17.2 * cm],
        rowHeights=[2.0 * cm, 1.3 * cm],
    )

    title_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), DARK_NAVY),
                ("BOX", (0, 0), (-1, -1), 0, DARK_NAVY),
                ("LEFTPADDING", (0, 0), (-1, -1), 22),
                ("RIGHTPADDING", (0, 0), (-1, -1), 22),
                ("TOPPADDING", (0, 0), (-1, -1), 18),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
            ]
        )
    )

    elements.append(title_table)
    elements.append(Spacer(1, 1.0 * cm))

    info_data = [
        ["Variable respuesta", response_label],
        ["Objetivo del estudio", optimization_goal],
        ["Metodología", "Diseño factorial 2ᵏ + puntos centrales + modelo lineal"],
        ["Fecha de generación", datetime.now().strftime("%d/%m/%Y %H:%M")],
    ]

    info_table = Table(info_data, colWidths=[5.0 * cm, 12.2 * cm])

    info_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), LIGHT_BG),
                ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elements.append(info_table)
    elements.append(Spacer(1, 1.0 * cm))

    elements.append(
        Paragraph(
            "Este documento consolida los resultados del diseño experimental, ajuste del modelo, "
            "evaluación ANOVA, diagnóstico de residuos, Pareto de efectos y ruta de mejora mediante "
            "ascenso más pronunciado. El reporte está orientado a apoyar decisiones técnicas y gerenciales.",
            styles["BodyCustom"],
        )
    )

    elements.append(PageBreak())

    return elements


def _kpi_table(kpis, styles):
    """
    Crea tarjetas KPI compactas.
    """

    row = []

    for label, value in kpis:
        cell = [
            Paragraph(_safe_text(value), styles["KpiValue"]),
            Paragraph(_safe_text(label), styles["KpiLabel"]),
        ]
        row.append(cell)

    table = Table([row], colWidths=[4.1 * cm] * len(row))

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    return table


def _df_to_table(df, max_rows=12, decimals=4):
    """
    Convierte un DataFrame a tabla ReportLab.
    """

    if df is None or len(df) == 0:
        return None

    temp = df.copy().head(max_rows)

    for col in temp.columns:
        temp[col] = temp[col].apply(lambda x: _fmt(x, decimals=decimals))

    data = [list(temp.columns)] + temp.values.tolist()

    col_count = len(temp.columns)
    col_width = 17.2 * cm / max(col_count, 1)

    table = Table(data, colWidths=[col_width] * col_count, repeatRows=1)

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 7),
                ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )

    return table


def _decision_text(model_results, anova_df, effects_df, steepest_path_df, response_label, optimization_goal):
    """
    Construye una conclusión ejecutiva.
    """

    paragraphs = []

    r2 = model_results.get("r2", None)
    r2_adj = model_results.get("r2_adj", None)

    paragraphs.append(
        f"El modelo lineal de primer orden fue ajustado para explicar la variable respuesta "
        f"<b>{response_label}</b>, con objetivo declarado de <b>{optimization_goal.lower()}</b>."
    )

    if r2 is not None and r2_adj is not None:
        paragraphs.append(
            f"El ajuste alcanzó un R² de <b>{r2:.4f}</b> y un R² ajustado de "
            f"<b>{r2_adj:.4f}</b>, lo que permite evaluar preliminarmente la capacidad "
            f"explicativa del modelo dentro de la región experimental estudiada."
        )

    if anova_df is not None:
        try:
            model_row = anova_df[anova_df["Fuente"] == "Modelo"].iloc[0]
            p_value = model_row["p-valor"]

            if p_value < 0.05:
                paragraphs.append(
                    f"El ANOVA global resultó estadísticamente significativo "
                    f"(p = <b>{p_value:.4f}</b>), por lo que existe evidencia de que "
                    f"al menos un factor influye sobre <b>{response_label}</b>."
                )
            else:
                paragraphs.append(
                    f"El ANOVA global no resultó significativo al 5% "
                    f"(p = <b>{p_value:.4f}</b>). Se recomienda cautela antes de tomar decisiones "
                    f"operativas basadas únicamente en este modelo."
                )
        except Exception:
            pass

    if effects_df is not None and not effects_df.empty:
        top = effects_df.iloc[0]
        paragraphs.append(
            f"El Pareto de efectos identificó como factor prioritario a "
            f"<b>{top['Parámetro']}</b>, con efecto estimado de "
            f"<b>{top['Efecto estimado']:.4f}</b>."
        )

    if steepest_path_df is not None and not steepest_path_df.empty:
        first = steepest_path_df.iloc[0]["Respuesta predicha"]
        last = steepest_path_df.iloc[-1]["Respuesta predicha"]
        delta = last - first

        paragraphs.append(
            f"La ruta de ascenso más pronunciado propone nuevas corridas experimentales "
            f"con un cambio predicho acumulado de <b>{delta:.4f}</b> unidades en "
            f"<b>{response_label}</b> dentro de los pasos evaluados."
        )

    paragraphs.append(
        "La decisión recomendada es ejecutar las corridas propuestas, registrar la respuesta real "
        "y confirmar experimentalmente la mejora antes de escalar o modificar condiciones de proceso."
    )

    return paragraphs


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
    """
    Genera un reporte PDF profesional orientado a gerencia.
    """

    output = BytesIO()

    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=1.4 * cm,
        leftMargin=1.4 * cm,
        topMargin=1.7 * cm,
        bottomMargin=1.4 * cm,
        title="Reporte Ejecutivo RSM Primer Orden",
    )

    styles = _build_styles()
    elements = []

    elements.extend(_cover_page(response_label, optimization_goal, styles))

    # =====================================================
    # 1. RESUMEN EJECUTIVO
    # =====================================================

    elements.append(Paragraph("1. Resumen ejecutivo", styles["SectionTitle"]))

    kpis = []

    if model_results is not None:
        kpis.append(("R²", _fmt(model_results.get("r2"), 4)))
        kpis.append(("R² ajustado", _fmt(model_results.get("r2_adj"), 4)))

    if anova_df is not None:
        try:
            model_row = anova_df[anova_df["Fuente"] == "Modelo"].iloc[0]
            kpis.append(("ANOVA p-valor", _fmt(model_row["p-valor"], 4)))
        except Exception:
            pass

    if effects_df is not None and not effects_df.empty:
        kpis.append(("Factor prioritario", effects_df.iloc[0]["Parámetro"]))

    if len(kpis) >= 2:
        elements.append(_kpi_table(kpis[:4], styles))
        elements.append(Spacer(1, 0.35 * cm))

    decision_paragraphs = _decision_text(
        model_results=model_results or {},
        anova_df=anova_df,
        effects_df=effects_df,
        steepest_path_df=steepest_path_df,
        response_label=response_label,
        optimization_goal=optimization_goal,
    )

    for p in decision_paragraphs:
        elements.append(Paragraph(p, styles["BodyCustom"]))
        elements.append(Spacer(1, 0.12 * cm))

    # =====================================================
    # 2. DISEÑO EXPERIMENTAL
    # =====================================================

    elements.append(Paragraph("2. Diseño experimental", styles["SectionTitle"]))

    elements.append(
        Paragraph(
            "El estudio se desarrolló bajo un diseño factorial completo de primer orden, "
            "incluyendo puntos centrales para apoyar la evaluación preliminar del comportamiento "
            "de la respuesta dentro de la región experimental.",
            styles["BodyCustom"],
        )
    )

    elements.append(Spacer(1, 0.2 * cm))

    table = _df_to_table(factor_summary, max_rows=10, decimals=4)
    if table:
        elements.append(table)

    # =====================================================
    # 3. MODELO LINEAL
    # =====================================================

    if model_results is not None:

        elements.append(Paragraph("3. Modelo lineal de primer orden", styles["SectionTitle"]))

        elements.append(
            Paragraph(
                f"<b>Ecuación estimada:</b> {model_results.get('equation', '')}",
                styles["BodyCustom"],
            )
        )

        elements.append(Spacer(1, 0.2 * cm))

        coef_table = _df_to_table(model_results.get("coef_df"), max_rows=12, decimals=4)
        if coef_table:
            elements.append(coef_table)

    # =====================================================
    # 4. ANOVA
    # =====================================================

    if anova_df is not None:

        elements.append(Paragraph("4. Evaluación ANOVA", styles["SectionTitle"]))

        elements.append(
            Paragraph(
                "El ANOVA evalúa la significancia global del modelo lineal y permite determinar "
                "si los factores considerados explican una proporción relevante de la variabilidad "
                f"observada en <b>{response_label}</b>.",
                styles["BodyCustom"],
            )
        )

        elements.append(Spacer(1, 0.2 * cm))

        anova_table = _df_to_table(anova_df, max_rows=10, decimals=4)
        if anova_table:
            elements.append(anova_table)

    # =====================================================
    # 5. PARETO
    # =====================================================

    if effects_df is not None:

        elements.append(PageBreak())
        elements.append(Paragraph("5. Pareto de efectos", styles["SectionTitle"]))

        elements.append(
            Paragraph(
                "La tabla siguiente prioriza los factores según su efecto absoluto sobre la variable "
                "respuesta. Esta información permite enfocar la toma de decisiones en las variables "
                "de mayor impacto.",
                styles["BodyCustom"],
            )
        )

        elements.append(Spacer(1, 0.2 * cm))

        cols = [
            "Ranking",
            "Parámetro",
            "Efecto estimado",
            "Efecto absoluto",
            "Importancia relativa (%)",
            "Dirección",
        ]

        available_cols = [c for c in cols if c in effects_df.columns]
        effects_table = _df_to_table(effects_df[available_cols], max_rows=12, decimals=4)

        if effects_table:
            elements.append(effects_table)

    # =====================================================
    # 6. ASCENSO
    # =====================================================

    if steepest_direction_df is not None or steepest_path_df is not None:

        elements.append(Paragraph("6. Ascenso más pronunciado", styles["SectionTitle"]))

        elements.append(
            Paragraph(
                "La ruta de ascenso más pronunciado propone nuevas condiciones experimentales "
                "en la dirección de mejora estimada por el modelo de primer orden. Estas corridas "
                "deben validarse experimentalmente antes de tomar decisiones definitivas.",
                styles["BodyCustom"],
            )
        )

        elements.append(Spacer(1, 0.2 * cm))

        if steepest_direction_df is not None:
            elements.append(Paragraph("Dirección recomendada por factor", styles["BodyCustom"]))
            elements.append(Spacer(1, 0.1 * cm))
            direction_table = _df_to_table(steepest_direction_df, max_rows=10, decimals=4)
            if direction_table:
                elements.append(direction_table)
                elements.append(Spacer(1, 0.25 * cm))

        if steepest_path_df is not None:
            elements.append(Paragraph("Corridas experimentales propuestas", styles["BodyCustom"]))
            elements.append(Spacer(1, 0.1 * cm))
            path_table = _df_to_table(steepest_path_df, max_rows=12, decimals=4)
            if path_table:
                elements.append(path_table)

    # =====================================================
    # 7. CIERRE
    # =====================================================

    elements.append(Paragraph("7. Recomendación gerencial final", styles["SectionTitle"]))

    elements.append(
        Paragraph(
            "Se recomienda ejecutar las corridas sugeridas por la ruta de ascenso más pronunciado, "
            "comparar la respuesta observada contra la respuesta predicha y documentar la mejora real. "
            "Si la respuesta deja de mejorar, el comportamiento del proceso podría requerir una nueva "
            "región experimental o un diseño de segundo orden. Este aplicativo se mantiene deliberadamente "
            "en el alcance de modelos de primer orden.",
            styles["BodyCustom"],
        )
    )

    doc.build(
        elements,
        onFirstPage=_header_footer,
        onLaterPages=_header_footer,
    )

    output.seek(0)

    return output