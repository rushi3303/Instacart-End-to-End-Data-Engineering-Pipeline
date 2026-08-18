import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable


def create_txt_bytes(text):
    """
    Returns UTF-8 encoded bytes for TXT report download.
    """
    return text.encode("utf-8")


def create_pdf_bytes(report_data):
    """
    Generates a clean PDF document using ReportLab and returns bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        textColor=colors.HexColor("#1A2B4C"),
        spaceAfter=6
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=colors.HexColor("#0D5C75"),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2C3E50")
    )

    elements = []

    # Title & Metadata Header
    elements.append(Paragraph(report_data.get("title", "AI DATA ENGINEERING AGENT REPORT"), title_style))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1A2B4C"), spaceAfter=10))

    meta_text = (
        f"<b>Question:</b> {report_data.get('question', '')}<br/>"
        f"<b>Generated Timestamp:</b> {report_data.get('timestamp', '')}<br/>"
        f"<b>Selected Tool:</b> {report_data.get('intent', '')}"
    )
    elements.append(Paragraph(meta_text, body_style))
    elements.append(Spacer(1, 10))

    # 1. Agent Decision
    elements.append(Paragraph("1. AGENTIC AI DECISION", heading_style))
    elements.append(Paragraph(f"<b>Reasoning:</b> {report_data.get('reasoning', '')}", body_style))
    elements.append(Spacer(1, 10))

    # 2. AI Insights
    elements.append(Paragraph("2. AI INSIGHTS (INSIGHT AGENT)", heading_style))
    for ins in report_data.get("insights", []):
        elements.append(Paragraph(f"• {ins}", body_style))
    elements.append(Spacer(1, 10))

    # 3. Recommended Actions
    elements.append(Paragraph("3. RECOMMENDED ACTIONS (ACTION AGENT)", heading_style))
    for act in report_data.get("actions", []):
        elements.append(Paragraph(f"{act}", body_style))
    elements.append(Spacer(1, 10))

    # 4. Power BI Visualization Recommendation
    elements.append(Paragraph("4. POWER BI VISUALIZATION RECOMMENDATION", heading_style))
    viz = report_data.get("visualization_info", {})
    elements.append(Paragraph(f"<b>Recommended Chart:</b> {viz.get('chart_type', '')}", body_style))
    elements.append(Paragraph(f"<b>Why Suitable:</b> {viz.get('reasoning', '')}", body_style))
    elements.append(Spacer(1, 10))

    # Footer
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7"), spaceBefore=15, spaceAfter=8))
    elements.append(Paragraph("Instacart Data Engineering Copilot | End-to-End Pipeline Verification", body_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
