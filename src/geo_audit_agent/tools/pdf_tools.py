"""PDF generation tool \u2014 creates professional GEO audit reports using ReportLab.

Runs inside OpenSandbox via run_in_sandbox.
"""

import json
from datetime import datetime
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as pdf_canvas

# ---------------------------------------------------------------------------
# PDF Report Sections
# ----------------------------------------------------------------------------

def build_pdf_script(audit_data: dict[str, Any], output_path: str) -> str:
    """Build a Python script that generates the PDF report using ReportLab.

    Args:
        audit_data: Audit results dict with scores, findings, recommendations
        output_path: Path where PDF should be saved

    Returns:
        Python script string to run via run_in_sandbox
    """
    data_json = json.dumps(audit_data, indent=2)

    script = f'''
import json
import math
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as pdf_canvas

# \u2500\u2500\u2500 Color Palette \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
C_DARK_BLUE  = colors.HexColor("#1A2B4A")
C_MID_BLUE   = colors.HexColor("#2E5FAC")
C_LIGHT_BLUE = colors.HexColor("#E8F0FB")
C_ACCENT     = colors.HexColor("#F5A623")
C_RED        = colors.HexColor("#E53935")
C_ORANGE     = colors.HexColor("#FB8C00")
C_YELLOW     = colors.HexColor("#FDD835")
C_GREEN      = colors.HexColor("#43A047")
C_GREY       = colors.HexColor("#757575")
C_LIGHT_GREY = colors.HexColor("#F5F5F5")
C_WHITE      = colors.white

W, H = A4  # 595.27 x 841.89 points
MARGIN = 20 * mm

# \u2500\u2500\u2500 Load Audit Data \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
audit_data = json.loads({json.dumps(data_json)})

# \u2500\u2500\u2500 Drawing Helpers \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

def draw_gauge(c, x, y, radius, score, label):
    """Draw a semi-circular gauge with score."""
    # Background arc
    c.setFillColor(C_LIGHT_GREY)
    c.setStrokeColor(C_LIGHT_GREY)
    c.setLineWidth(12)
    c.arc(x - radius, y - radius, x + radius, y + radius, startAng=180, extent=180)
    c.stroke()

    # Score arc
    if score >= 70:
        color = C_GREEN
    elif score >= 40:
        color = C_ORANGE
    else:
        color = C_RED

    c.setFillColor(color)
    c.setStrokeColor(color)
    c.setLineWidth(12)
    c.arc(x - radius, y - radius, x + radius, y + radius,
          startAng=180, extent=180 * score / 100)
    c.stroke()

    # Score text
    c.setFillColor(C_DARK_BLUE)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(x, y - 8, f"{{score}}/100")

    # Label
    c.setFont("Helvetica", 10)
    c.setFillColor(C_GREY)
    c.drawCentredString(x, y - 22, label)


def draw_section_header(c, y, title):
    """Draw a section header with accent bar."""
    c.setFillColor(C_DARK_BLUE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, y, title)
    c.setFillColor(C_MID_BLUE)
    c.rect(MARGIN, y - 4, 60, 3, fill=1, stroke=0)
    return y - 15


def draw_finding(c, y, finding, width):
    """Draw a single finding row."""
    severity = finding.get("severity", "low")
    color = {{"high": C_RED, "medium": C_ORANGE, "low": C_GREEN}}.get(severity, C_GREY)

    # Severity dot
    c.setFillColor(color)
    c.circle(MARGIN + 4, y + 3, 4, fill=1, stroke=0)

    # Issue text
    c.setFillColor(C_DARK_BLUE)
    c.setFont("Helvetica-Bold", 9)
    issue = finding.get("issue", "")
    if len(issue) > 80:
        issue = issue[:77] + "..."
    c.drawString(MARGIN + 12, y, issue)

    # Recommendation
    c.setFont("Helvetica", 8)
    c.setFillColor(C_GREY)
    rec = finding.get("recommendation", "")
    if len(rec) > width:
        rec = rec[: width - 3] + "..."
    c.drawString(MARGIN + 12, y - 10, rec)

    return y - 22


# \u2500\u2500\u2500 Main PDF Generation \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
audit_data = json.loads({json.dumps(data_json)})

def generate_pdf():
    c = pdf_canvas.Canvas({json.dumps(output_path)}, pagesize=A4)
    page_num = [1]

    def new_page():
        c.showPage()
        page_num[0] += 1
        return H - MARGIN

    def footer():
        c.setFont("Helvetica", 8)
        c.setFillColor(C_GREY)
        c.drawCentredString(W / 2, 12, f"GEO Audit Report \u2014 Page {{page_num[0]}}")

    # \u2500\u2500 PAGE 1: Cover \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
    y = H - MARGIN

    # Header bar
    c.setFillColor(C_DARK_BLUE)
    c.rect(0, y - 40, W, 40, fill=1, stroke=0)
    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(W / 2, y - 28, "GEO / SEO AUDIT REPORT")
    y -= 60

    site_url = audit_data.get("url", "Unknown")
    c.setFillColor(C_DARK_BLUE)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(W / 2, y, site_url)
    y -= 20

    c.setFont("Helvetica", 10)
    c.setFillColor(C_GREY)
    c.drawCentredString(W / 2, y, f"Audited: {{datetime.now().strftime('%B %d, %Y')}}")
    y -= 40

    # Overall score gauge
    overall = audit_data.get("overall_score", 0)
    draw_gauge(c, W / 2, y - 60, 70, overall, "OVERALL GEO SCORE")

    y -= 110
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(C_DARK_BLUE)
    c.drawCentredString(W / 2, y, "5-Category Breakdown")

    # Category gauges
    categories = [
        ("AI Visibility", audit_data.get("ai_visibility_score", 0)),
        ("Technical SEO", audit_data.get("technical_seo_score", 0)),
        ("Content Quality", audit_data.get("content_quality_score", 0)),
        ("Schema Markup", audit_data.get("schema_markup_score", 0)),
        ("Platform Ready", audit_data.get("platform_readiness_score", 0)),
    ]

    x_start = MARGIN + 10
    x_step = (W - 2 * MARGIN) / 5
    for i, (cat, score) in enumerate(categories):
        draw_gauge(c, x_start + x_step * i + x_step / 2, y - 40, 25, score, cat)

    footer()

    # \u2500\u2500 PAGE 2+: Findings \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
    y = new_page()
    y = draw_section_header(c, y, "Executive Summary")
    y -= 8

    summary = audit_data.get("executive_summary", "No summary available.")
    c.setFont("Helvetica", 10)
    c.setFillColor(C_DARK_BLUE)

    # Wrap text manually (simple word wrap)
    words = summary.split()
    line = ""
    max_w = W - 2 * MARGIN
    for word in words:
        test = line + " " + word if line else word
        if c.stringWidth(test, "Helvetica", 10) < max_w:
            line = test
        else:
            c.drawString(MARGIN, y, line)
            y -= 13
            line = word
            if y < MARGIN + 20:
                y = new_page()
    if line:
        c.drawString(MARGIN, y, line)
        y -= 13

    y -= 10

    # Findings per category
    findings_by_cat = {{
        "AI Visibility": audit_data.get("ai_visibility_findings", []),
        "Technical SEO": audit_data.get("technical_seo_findings", []),
        "Content Quality": audit_data.get("content_quality_findings", []),
        "Schema Markup": audit_data.get("schema_markup_findings", []),
        "Platform Readiness": audit_data.get("platform_readiness_findings", []),
    }}

    for cat_name, findings in findings_by_cat.items():
        if not findings:
            continue
        if y < MARGIN + 80:
            y = new_page()
        y = draw_section_header(c, y, cat_name)
        for f in findings[:5]:  # max 5 per category
            y = draw_finding(c, y, f, W - 2 * MARGIN)
            if y < MARGIN + 20:
                y = new_page()
        y -= 5

    # \u2500\u2500 Final Page: Recommendations \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n    if y < MARGIN + 100:
        y = new_page()

    y = draw_section_header(c, y, "Top Recommendations")
    y -= 8

    all_recs = audit_data.get("top_recommendations", [])
    for i, rec in enumerate(all_recs[:10], 1):
        c.setFillColor(C_MID_BLUE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(MARGIN, y, f"{{i}}. {{rec}}")
        y -= 14
        if y < MARGIN + 20:
            y = new_page()

    footer()
    c.save()
    print(f"PDF saved: {{json.dumps(output_path)}}")

generate_pdf()
'''
    return script
