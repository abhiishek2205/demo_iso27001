#!/usr/bin/env python3
"""Build the ISO/IEC 27001:2022 gap assessment report for SecurePay Technologies.

Reads the CSV files in ../data, renders charts with matplotlib into ../report/charts
and assembles a client-style PDF with reportlab at
../report/ISO27001_Gap_Assessment_SecurePay.pdf.

Usage:
    python scripts/build_report.py [--author "Your Name"]

This is a self-directed assessment of a fictional organisation, not a real client
engagement.
"""
import argparse
import csv
from collections import Counter, OrderedDict
from pathlib import Path
from xml.sax.saxutils import escape

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch, Rectangle  # noqa: E402

from reportlab.lib import colors  # noqa: E402
from reportlab.lib.enums import TA_CENTER, TA_LEFT  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import (  # noqa: E402
    BaseDocTemplate, CondPageBreak, Frame, Image, KeepTogether, NextPageTemplate,
    PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT_DIR = ROOT / "report"
CHART_DIR = OUT_DIR / "charts"
PDF_PATH = OUT_DIR / "ISO27001_Gap_Assessment_SecurePay.pdf"

REPORT_DATE = "27 October 2026"
VERSION = "1.0 (Final)"
CLIENT = "SecurePay Technologies Pvt. Ltd."
TITLE = "ISO/IEC 27001:2022 Security Controls Gap Assessment"

# ----------------------------------------------------------------- palette
NAVY = colors.HexColor("#1B2A41")
ACCENT = colors.HexColor("#2A78D6")
INK = colors.HexColor("#1F2328")
MUTED = colors.HexColor("#5B6270")
RULE = colors.HexColor("#D0D4DA")
PANEL = colors.HexColor("#F3F5F8")
WHITE = colors.white

# Status colours (good / warning / serious / critical). Text-on-tint pairs keep
# contrast high in print; the label always carries the meaning, never colour alone.
STATUS_HEX = {"good": "#0CA30C", "warning": "#FAB219", "serious": "#EC835A", "critical": "#D03B3B", "na": "#9AA0A6"}
TINT = {
    "Conformant": ("#DDF2DD", "#0B5D0B"), "Implemented": ("#DDF2DD", "#0B5D0B"),
    "Partially conformant": ("#FDEFC9", "#6B4A00"), "Partially implemented": ("#FDEFC9", "#6B4A00"),
    "Non-conformant": ("#F7D9D9", "#8E1F1F"), "Not implemented": ("#F7D9D9", "#8E1F1F"),
    "Not applicable": ("#ECEDEF", "#3C4047"),
    "Low": ("#DDF2DD", "#0B5D0B"), "Medium": ("#FDEFC9", "#6B4A00"),
    "High": ("#FBE0D4", "#8A3A17"), "Critical": ("#D03B3B", "#FFFFFF"),
}
STATUS_ORDER = ["Conformant", "Partially conformant", "Non-conformant"]
STATUS_COLOR = {"Conformant": STATUS_HEX["good"], "Partially conformant": STATUS_HEX["warning"],
                "Non-conformant": STATUS_HEX["critical"]}
THEMES = ["Organizational", "People", "Physical", "Technological"]
THEME_PREFIX = {"Organizational": "A.5", "People": "A.6", "Physical": "A.7", "Technological": "A.8"}
PHASES = ["0-3 months", "3-6 months", "6-12 months"]
MATURITY_TARGET = 3

# --------------------------------------------------------------- data load

def load(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def band(score):
    return "Critical" if score >= 20 else "High" if score >= 12 else "Medium" if score >= 6 else "Low"


def dash(text):
    """Use proper en dashes in month ranges for typeset output."""
    return text.replace("0-3 months", "0–3 months").replace("3-6 months", "3–6 months") \
               .replace("6-12 months", "6–12 months")


# ------------------------------------------------------------------ charts

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Liberation Sans", "Arial", "Helvetica", "DejaVu Sans"], "font.size": 9, "axes.edgecolor": "#C3C2B7",
    "axes.labelcolor": "#1F2328", "xtick.color": "#5B6270", "ytick.color": "#1F2328",
    "axes.spines.top": False, "axes.spines.right": False,
})


def chart_conformance_by_theme(controls, path):
    counts = {t: Counter(c["status"] for c in controls if c["theme"] == t) for t in THEMES}
    fig, ax = plt.subplots(figsize=(7.0, 2.9), dpi=200)
    ys = list(range(len(THEMES)))[::-1]
    for y, theme in zip(ys, THEMES):
        left = 0
        for st in STATUS_ORDER:
            n = counts[theme][st]
            if not n:
                continue
            ax.barh(y, n, left=left, height=0.58, color=STATUS_COLOR[st], edgecolor="white", linewidth=2)
            ax.text(left + n / 2, y, str(n), ha="center", va="center", fontsize=9, fontweight="bold",
                    color="#0B0B0B" if st == "Partially conformant" else "white")
            left += n
        ax.text(left + 0.12, y, f"n = {left}", va="center", fontsize=8.5, color="#5B6270")
    ax.set_yticks(ys)
    ax.set_yticklabels([f"{t} ({THEME_PREFIX[t]})" for t in THEMES])
    ax.set_xlabel("Number of controls assessed")
    ax.set_xlim(0, max(sum(c.values()) for c in counts.values()) + 1.2)
    ax.xaxis.grid(True, color="#E1E0D9", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    ax.legend(handles=[Patch(color=STATUS_COLOR[s], label=s) for s in STATUS_ORDER], ncol=3,
              loc="lower center", bbox_to_anchor=(0.45, 1.0), frameon=False, fontsize=8.5)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def chart_maturity_by_theme(controls, path):
    avgs = []
    for t in THEMES:
        vals = [int(c["maturity_current"]) for c in controls if c["theme"] == t]
        avgs.append(sum(vals) / len(vals))
    overall = sum(int(c["maturity_current"]) for c in controls) / len(controls)
    labels = THEMES + ["Overall"]
    vals = avgs + [overall]
    fig, ax = plt.subplots(figsize=(7.0, 2.6), dpi=200)
    ys = list(range(len(labels)))[::-1]
    for y, v, lab in zip(ys, vals, labels):
        ax.barh(y, v, height=0.55, color="#1B2A41" if lab == "Overall" else "#2A78D6")
        ax.text(v + 0.06, y, f"{v:.1f}", va="center", fontsize=9, color="#1F2328", fontweight="bold")
    ax.axvline(MATURITY_TARGET, color="#5B6270", linestyle=(0, (4, 3)), linewidth=1.2)
    ax.text(MATURITY_TARGET + 0.05, ys[0] + 0.45, "12-month target: 3.0 (Defined)", fontsize=8, color="#5B6270")
    ax.set_yticks(ys)
    ax.set_yticklabels(labels)
    ax.set_xlim(0, 5)
    ax.set_xticks(range(6))
    ax.set_xticklabels(["0\nNon-existent", "1\nInitial", "2\nRepeatable", "3\nDefined", "4\nManaged",
                        "5\nOptimised"], fontsize=7.5)
    ax.xaxis.grid(True, color="#E1E0D9", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


HEAT_TINT = {"Low": "#BFE6BF", "Medium": "#FDE3A0", "High": "#F6C3A8", "Critical": "#EBA0A0"}


def chart_heatmap(risks, path, lkey, ikey, title):
    cells = {}
    for r in risks:
        cells.setdefault((int(r[lkey]), int(r[ikey])), []).append(r["risk_id"])
    fig, ax = plt.subplots(figsize=(4.6, 4.4), dpi=200)
    for L in range(1, 6):
        for I in range(1, 6):
            s = L * I
            ax.add_patch(Rectangle((I - 0.5, L - 0.5), 1, 1, facecolor=HEAT_TINT[band(s)],
                                   edgecolor="white", linewidth=2))
            ax.text(I - 0.42, L + 0.40, str(s), fontsize=6.5, color="#5B6270", va="top")
            ids = cells.get((L, I))
            if ids:
                lines = ["  ".join(ids[k:k + 2]) for k in range(0, len(ids), 2)] if len(ids) > 2 else ids
                ax.text(I + 0.04, L - 0.06, "\n".join(lines), ha="center", va="center",
                        fontsize=8.5 if len(ids) <= 2 else 7.2,
                        fontweight="bold", color="#1F2328", linespacing=1.15)
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)
    ax.set_aspect("equal")
    ax.set_xticks(range(1, 6))
    ax.set_xticklabels(["1\nNegligible", "2\nMinor", "3\nModerate", "4\nMajor", "5\nSevere"], fontsize=7)
    ax.set_yticks(range(1, 6))
    ax.set_yticklabels(["1 Rare", "2 Unlikely", "3 Possible", "4 Likely", "5 Almost\ncertain"], fontsize=7)
    ax.set_xlabel("Impact", fontsize=8.5)
    ax.set_ylabel("Likelihood", fontsize=8.5)
    ax.set_title(title, fontsize=9.5, fontweight="bold", color="#1F2328", loc="left")
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0)
    ax.legend(handles=[Patch(facecolor=HEAT_TINT[b], label=f"{b} ({rng})") for b, rng in
                       [("Low", "1-5"), ("Medium", "6-10"), ("High", "12-16"), ("Critical", "20-25")]],
              ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.2), frameon=False, fontsize=7)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def chart_soa(soa, path):
    order = ["Implemented", "Partially implemented", "Not implemented", "Not applicable"]
    col = [STATUS_HEX["good"], STATUS_HEX["warning"], STATUS_HEX["critical"], STATUS_HEX["na"]]
    cnt = Counter(r["implementation_status"] for r in soa)
    fig, ax = plt.subplots(figsize=(7.0, 2.1), dpi=200)
    ys = list(range(len(order)))[::-1]
    for y, st, c in zip(ys, order, col):
        ax.barh(y, cnt[st], height=0.55, color=c)
        ax.text(cnt[st] + 0.6, y, f"{cnt[st]}  ({cnt[st] / len(soa):.0%})", va="center", fontsize=8.5,
                color="#1F2328")
    ax.set_yticks(ys)
    ax.set_yticklabels(order)
    ax.set_xlabel(f"Number of Annex A controls (total {len(soa)})")
    ax.set_xlim(0, max(cnt.values()) + 10)
    ax.xaxis.grid(True, color="#E1E0D9", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------ styles

def make_styles():
    s = {}
    base = dict(fontName="Helvetica", fontSize=9.5, leading=13.2, textColor=INK)
    s["body"] = ParagraphStyle("body", spaceAfter=6, **base)
    s["bodyj"] = ParagraphStyle("bodyj", parent=s["body"])
    s["small"] = ParagraphStyle("small", fontName="Helvetica", fontSize=8, leading=10.2, textColor=INK)
    s["smallb"] = ParagraphStyle("smallb", parent=s["small"], fontName="Helvetica-Bold")
    s["tiny"] = ParagraphStyle("tiny", fontName="Helvetica", fontSize=7.2, leading=9, textColor=INK)
    s["tinyb"] = ParagraphStyle("tinyb", parent=s["tiny"], fontName="Helvetica-Bold")
    s["th"] = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=WHITE)
    s["thtiny"] = ParagraphStyle("thtiny", parent=s["th"], fontSize=7.2, leading=9)
    s["caption"] = ParagraphStyle("caption", fontName="Helvetica-Oblique", fontSize=8, leading=10,
                                  textColor=MUTED, spaceBefore=2, spaceAfter=10)
    s["bullet"] = ParagraphStyle("bullet", parent=s["body"], leftIndent=12, bulletIndent=2, spaceAfter=3)
    s["H1"] = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=NAVY,
                             spaceBefore=0, spaceAfter=10)
    s["H2"] = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=NAVY,
                             spaceBefore=10, spaceAfter=5)
    s["H2n"] = ParagraphStyle("H2n", parent=s["H2"])  # same look as H2, kept out of the TOC
    s["H3"] = ParagraphStyle("H3", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=INK,
                             spaceBefore=6, spaceAfter=4)
    s["tile_n"] = ParagraphStyle("tile_n", fontName="Helvetica-Bold", fontSize=18, leading=21,
                                 textColor=NAVY, alignment=TA_CENTER)
    s["tile_l"] = ParagraphStyle("tile_l", fontName="Helvetica", fontSize=7.5, leading=9.2,
                                 textColor=MUTED, alignment=TA_CENTER)
    s["callout"] = ParagraphStyle("callout", parent=s["body"], fontSize=9, leading=12.5, spaceAfter=0)
    return s


ST = make_styles()


def P(text, style="body"):
    """Paragraph from plain text (escaped)."""
    return Paragraph(escape(dash(str(text))), ST[style] if isinstance(style, str) else style)


def M(markup, style="body"):
    """Paragraph from trusted inline markup."""
    return Paragraph(dash(markup), ST[style] if isinstance(style, str) else style)


def bullets(items, style="bullet", markup=False):
    return [Paragraph(dash(i) if markup else escape(dash(i)), ST[style], bulletText="•") for i in items]


def chip(text, style="smallb"):
    bg, fg = TINT.get(text, ("#ECEDEF", "#1F2328"))
    st = ParagraphStyle("chip_" + text + style, parent=ST[style], textColor=colors.HexColor(fg))
    return Paragraph(escape(text), st), colors.HexColor(bg)


def data_table(header, rows, widths, font="small", zebra=True, extra=None, head_style="th", pad=3.2):
    """Table with navy header row, wrapped cells and optional status chip colouring.

    rows: list of lists; a cell may be a str (escaped), a Flowable, or ('chip', text).
    """
    body = [[Paragraph(escape(h), ST[head_style]) for h in header]]
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    for ri, row in enumerate(rows, start=1):
        out = []
        for ci, cell in enumerate(row):
            if isinstance(cell, tuple) and cell[0] == "chip":
                para, bg = chip(cell[1], font + "b" if font + "b" in ST else "smallb")
                out.append(para)
                cmds.append(("BACKGROUND", (ci, ri), (ci, ri), bg))
            elif isinstance(cell, str):
                out.append(P(cell, font))
            else:
                out.append(cell)
        body.append(out)
        if zebra and ri % 2 == 0:
            cmds.append(("BACKGROUND", (0, ri), (-1, ri), PANEL))
    # chip backgrounds must win over zebra striping: re-append them last
    chip_cmds = [c for c in cmds if c[0] == "BACKGROUND" and c[1][1] > 0 and c[1] == c[2]]
    cmds = [c for c in cmds if c not in chip_cmds] + chip_cmds
    if extra:
        cmds += extra
    t = Table(body, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle(cmds))
    return t


def figure(path, width_mm, caption=None):
    from reportlab.lib.utils import ImageReader
    iw, ih = ImageReader(str(path)).getSize()
    w = width_mm * mm
    img = Image(str(path), width=w, height=w * ih / iw)
    img.hAlign = "CENTER"
    return [img, P(caption, "caption")] if caption else [img]


def callout(flowables, bg=PANEL, bar=ACCENT, width=174 * mm):
    t = Table([[flowables]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3, bar),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


# ----------------------------------------------------------- doc template

class ReportDoc(BaseDocTemplate):
    def __init__(self, filename, author, **kw):
        super().__init__(filename, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                         topMargin=22 * mm, bottomMargin=20 * mm, title=TITLE,
                         author=author, subject=f"{CLIENT} (fictional) - self-directed assessment", **kw)
        self.author_name = author
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="body",
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[frame], onPage=self.draw_cover),
            PageTemplate(id="body", frames=[frame], onPage=self.draw_body),
        ])
        self._heading_seq = 0

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in ("H1", "H2"):
            level = 0 if flowable.style.name == "H1" else 1
            text = flowable.getPlainText()
            self._heading_seq += 1
            key = f"h{self._heading_seq}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=level > 0)
            self.notify("TOCEntry", (level, text, self.page, key))

    def handle_documentBegin(self):
        self._heading_seq = 0
        super().handle_documentBegin()

    # -- page decorations
    def draw_cover(self, c, doc):
        w, h = A4
        c.saveState()
        c.setFillColor(NAVY)
        c.rect(0, h - 120 * mm, w, 120 * mm, stroke=0, fill=1)
        c.setFillColor(ACCENT)
        c.rect(0, h - 123 * mm, w, 3 * mm, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#AFC3DD"))
        c.setFont("Helvetica-Bold", 10)
        c.drawString(20 * mm, h - 30 * mm, "SECURITY CONTROLS & RISK ASSESSMENT")
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 25)
        c.drawString(20 * mm, h - 52 * mm, "ISO/IEC 27001:2022")
        c.drawString(20 * mm, h - 63 * mm, "Security Controls Gap Assessment")
        c.setFont("Helvetica", 13)
        c.drawString(20 * mm, h - 80 * mm, CLIENT)
        c.setFillColor(colors.HexColor("#AFC3DD"))
        c.setFont("Helvetica", 10.5)
        c.drawString(20 * mm, h - 88 * mm, "Annex A controls assessment, risk assessment, Statement of Applicability")
        c.drawString(20 * mm, h - 94.5 * mm, "and prioritised remediation roadmap")

        y = h - 145 * mm
        c.setFillColor(INK)
        rows = [("Client", f"{CLIENT} (fictional organisation)"), ("Report date", REPORT_DATE),
                ("Version", VERSION), ("Prepared by", doc.author_name),
                ("Classification", "Confidential - illustrative portfolio document")]
        for k, v in rows:
            c.setFont("Helvetica-Bold", 9.5)
            c.setFillColor(MUTED)
            c.drawString(20 * mm, y, k.upper())
            c.setFont("Helvetica", 11)
            c.setFillColor(INK)
            c.drawString(62 * mm, y, v)
            y -= 9 * mm

        # disclaimer box
        bx, by, bw, bh = 20 * mm, 22 * mm, w - 40 * mm, 34 * mm
        c.setFillColor(colors.HexColor("#FFF6DD"))
        c.setStrokeColor(colors.HexColor("#E0B84A"))
        c.setLineWidth(0.8)
        c.rect(bx, by, bw, bh, stroke=1, fill=1)
        para = Paragraph(
            "<b>Important notice.</b> This is a <b>self-directed assessment of a fictional organisation</b>, "
            "prepared as an academic and portfolio exercise. It is <b>not a real client engagement</b>. "
            "SecurePay Technologies, its people, systems, incidents and findings are invented, and the current "
            "state is based on assumed conditions. No interviews, system access or evidence sampling were "
            "performed. ISO/IEC 27001:2022 requirements are paraphrased; refer to the licensed standard for "
            "authoritative text.",
            ParagraphStyle("disc", fontName="Helvetica", fontSize=8.6, leading=11.4, textColor=INK))
        _, ph = para.wrap(bw - 10 * mm, bh)
        para.drawOn(c, bx + 5 * mm, by + (bh - ph) / 2)
        c.restoreState()

    def draw_body(self, c, doc):
        w, h = A4
        c.saveState()
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        c.line(18 * mm, h - 14 * mm, w - 18 * mm, h - 14 * mm)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(MUTED)
        c.drawString(18 * mm, h - 12 * mm, f"{CLIENT} (fictional)  |  {TITLE}")
        c.drawRightString(w - 18 * mm, h - 12 * mm, "Confidential - illustrative")
        c.line(18 * mm, 13 * mm, w - 18 * mm, 13 * mm)
        c.drawString(18 * mm, 9 * mm, "Self-directed assessment of a fictional organisation - not a real client engagement")
        c.setFont("Helvetica-Bold", 8)
        c.drawRightString(w - 18 * mm, 9 * mm, f"Page {doc.page}")
        c.restoreState()


# ------------------------------------------------------------------ content

def build_story(d):
    controls, clauses, risks, soa, roadmap, assumptions = (
        d["controls"], d["clauses"], d["risks"], d["soa"], d["roadmap"], d["assumptions"])
    story = []
    W = 174 * mm
    n = len(controls)
    sc = Counter(c["status"] for c in controls)
    score = (sc["Conformant"] + 0.5 * sc["Partially conformant"]) / n
    mat = sum(int(c["maturity_current"]) for c in controls) / n
    rr = Counter(r["rating"] for r in risks)
    by_theme = {t: [c for c in controls if c["theme"] == t] for t in THEMES}
    new_assessed = [c for c in controls if c["new_in_2022"] == "Y"]
    soa_cnt = Counter(r["implementation_status"] for r in soa)
    applicable = [r for r in soa if r["applicable"] == "Y"]

    # ---- cover + document control / TOC
    story += [NextPageTemplate("body"), PageBreak()]
    story.append(M("About this document", ParagraphStyle("AH", parent=ST["H1"])))
    story.append(M("Document control", "H3"))
    story.append(data_table(["Version", "Date", "Author", "Description"],
                            [["0.1", "06 October 2026", d["author"], "Scoping and organisation profile"],
                             ["0.9", "20 October 2026", d["author"], "Draft findings, risk register and SoA"],
                             [VERSION, REPORT_DATE, d["author"], "Final report with remediation roadmap"]],
                            [24 * mm, 34 * mm, 40 * mm, 76 * mm]))
    story.append(Spacer(1, 4 * mm))
    story.append(M("Intended distribution (illustrative)", "H3"))
    story.append(data_table(["Role", "Purpose"], [
        ["CEO (report sponsor)", "Approval of roadmap, risk treatment and risk acceptance decisions"],
        ["CTO (interim security owner)", "Ownership of technical remediation"],
        ["Head of Legal & Compliance", "DPDP, RBI and contractual obligations"],
        ["Board / investors (summary only)", "Oversight of security risk and certification plans"],
    ], [60 * mm, 114 * mm]))
    story.append(Spacer(1, 4 * mm))
    story.append(M("Basis of preparation", "H3"))
    story.append(P(
        "This report presents a security controls gap assessment and risk assessment of SecurePay Technologies "
        "against ISO/IEC 27001:2022. It is a self-directed exercise prepared by the author for learning and "
        "portfolio purposes. SecurePay is a fictional organisation; its profile, systems, incidents and current "
        "state are realistic assumptions for an early-stage Indian fintech and are listed in Appendix C. It is "
        "not based on a real client engagement, and no real organisation's information was used."))
    story.append(P(
        "Control requirements are paraphrased in plain English and do not reproduce the text of ISO/IEC 27001 or "
        "ISO/IEC 27002. Readers who need the authoritative requirements should consult the licensed standards. "
        "References to Indian laws, RBI directions, CERT-In directions and PCI DSS are summaries for context and "
        "are not legal advice."))
    story.append(P(
        "All tables and charts are generated from the CSV files in the project's data/ folder by "
        "scripts/build_report.py, so the report, the data and the README stay consistent."))
    story.append(PageBreak())
    story.append(M("Contents", ParagraphStyle("TOCH", parent=ST["H1"])))
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("toc0", fontName="Helvetica-Bold", fontSize=10, leading=15, textColor=NAVY,
                       leftIndent=0, firstLineIndent=0),
        ParagraphStyle("toc1", fontName="Helvetica", fontSize=9, leading=12.5, textColor=INK,
                       leftIndent=14, firstLineIndent=0),
    ]
    toc.dotsMinLevel = 0
    story.append(toc)
    story.append(PageBreak())

    # ================================================================ 1
    story.append(M("1. Executive summary", "H1"))
    story.append(P(
        f"{CLIENT} ('SecurePay') is a 50-person Bengaluru fintech that processes online card and UPI payments "
        "for about 1,200 small and medium merchants as an RBI-authorised (in-principle) online Payment "
        "Aggregator. It is preparing for PCI DSS v4.0.1 assessment and DPDP Act readiness, and its partner banks "
        "increasingly ask for ISO/IEC 27001 assurance. This self-directed gap assessment examined 20 Annex A "
        "controls across all four 2022 themes, reviewed management-system Clauses 4–10, built a risk "
        "register for the top eight information security risks and drafted a Statement of Applicability (SoA) "
        "for all 93 Annex A controls."))

    tiles = [
        (f"{n}", "Annex A controls\nassessed in detail"),
        (f"{score:.1%}", "Conformance score\n(partial = half credit)"),
        (f"{mat:.1f} / 5", "Average maturity\n(target 3.0)"),
        (f"{sc['Non-conformant']}", "Non-conformant\ncontrols"),
        (f"{rr['Critical'] + rr['High']} of {len(risks)}", "Top risks rated\nHigh or Critical"),
    ]
    tile_row = [[M(f"{a}", "tile_n"), M(escape(b).replace("\n", "<br/>"), "tile_l")] for a, b in tiles]
    t = Table([[x[0] for x in tile_row], [x[1] for x in tile_row]], colWidths=[W / 5] * 5)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PANEL), ("LINEAFTER", (0, 0), (-2, -1), 2, WHITE),
        ("LINEABOVE", (0, 0), (-1, 0), 2.5, ACCENT),
        ("TOPPADDING", (0, 0), (-1, 0), 9), ("BOTTOMPADDING", (0, 1), (-1, 1), 9),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story += [Spacer(1, 3 * mm), t, Spacer(1, 5 * mm)]

    story.append(M("Overall maturity: Developing", "H2n"))
    story.append(P(
        f"Of the {n} controls assessed, {sc['Conformant']} ({sc['Conformant'] / n:.0%}) are conformant, "
        f"{sc['Partially conformant']} ({sc['Partially conformant'] / n:.0%}) are partially conformant and "
        f"{sc['Non-conformant']} ({sc['Non-conformant'] / n:.0%}) are non-conformant. Average control maturity is "
        f"{mat:.1f} on a 0–5 scale, between 'Initial' and 'Repeatable'. This is typical for a fast-growing "
        "start-up: good engineering habits and cloud-native foundations, but no formal Information Security "
        "Management System (ISMS). Security depends on a few capable individuals rather than on approved "
        "policies, assigned roles, risk-based planning and monitoring. Clauses 6 (Planning), 9 (Performance "
        "evaluation) and 10 (Improvement) are not yet in place, so SecurePay is not currently ready for "
        "certification."))

    story.append(M("Headline findings", "H2n"))
    story += bullets([
        "<b>Privileged access is the most serious gap (Critical).</b> Five engineers hold permanent AWS "
        "administrator rights, the root account and the production database superuser are shared, and "
        "privileged activity is neither reviewed nor monitored (A.8.2).",
        "<b>Attacks would likely go unnoticed and unreported.</b> Security logs are not monitored, GuardDuty "
        "is off and there is no incident response plan. A real credential-stuffing attack in March 2026 was "
        "found only through a merchant complaint after about 19 hours, well beyond CERT-In's 6-hour "
        "reporting window (A.8.16, A.5.24).",
        "<b>Customer personal data is exposed through the support vendor.</b> The outsourced BPO uses shared "
        "logins without MFA, was never security-assessed and has no security clauses in its contract "
        "(A.5.19, A.8.5).",
        "<b>DPDP Act readiness is low.</b> There is no personal data inventory, retention schedule, rights "
        "handling or breach notification procedure, and production data is copied into staging (A.5.34).",
        "<b>Application security lags the platform's risk.</b> Four High VAPT findings have been open for nine "
        "months and nine hard-coded secrets were found in source code history (A.8.8, A.8.28).",
        "<b>There are real strengths to build on.</b> Encryption and tokenisation (A.8.24), tested cross-region "
        "backups (A.8.13), background screening (A.6.1), managed and encrypted laptops (A.6.7) and office entry "
        "controls (A.7.2) are conformant, and 70% of infrastructure is already defined as code.",
    ], markup=True)

    story.append(CondPageBreak(60 * mm))
    story.append(M("Top three priorities (next 90 days)", "H2n"))
    pri = [
        ["1", "Lock down privileged access and authentication",
         "Just-in-time SSO admin roles, root locked with hardware MFA, individual database credentials, MFA on "
         "the Ops Console and vendor accounts.", "A.8.2, A.8.5", "R01, R02"],
        ["2", "Build basic detection and incident response",
         "Enable GuardDuty and 10–15 priority alerts, keep logs for one year, approve an incident response "
         "plan with a CERT-In/DPDP/RBI notification matrix and run a tabletop exercise.",
         "A.8.16, A.5.24", "R04"],
        ["3", "Establish governance and close exploitable application gaps",
         "Approve the security policy and appoint an Information Security Manager; close open High VAPT "
         "findings, rotate exposed secrets and set remediation SLAs.", "A.5.1, A.8.8, A.8.28", "R03"],
    ]
    story.append(data_table(["#", "Priority", "Key actions", "Controls", "Risks"], pri,
                            [8 * mm, 42 * mm, 82 * mm, 24 * mm, 18 * mm]))
    story.append(Spacer(1, 4 * mm))
    story.append(callout([P(
        "If these priorities and the 3–6 month actions are delivered, we estimate average maturity rises "
        "from 1.7 to about 3.0, every risk in the register falls to Medium or below, and SecurePay can approach "
        "a certification Stage 1 audit in about 12 months.", "callout")]))
    story.append(M("Results at a glance", "H2n"))
    story += figure(CHART_DIR / "conformance_by_theme.png", 150,
                    "Exhibit - Conformance status of the 20 assessed controls by Annex A theme (detail in section 4)")

    # ================================================================ 2
    story.append(PageBreak())
    story.append(M("2. Scope, objectives and methodology", "H1"))
    story.append(M("2.1 Objectives", "H2"))
    story += bullets([
        "Determine SecurePay's current conformance with a risk-relevant sample of ISO/IEC 27001:2022 Annex A "
        "controls and the ISMS requirements of Clauses 4–10.",
        "Identify, rate and prioritise the information security risks that come from the gaps found.",
        "Produce a Statement of Applicability covering all 93 Annex A controls as a basis for the future ISMS.",
        "Recommend a practical, prioritised remediation roadmap with owners and effort estimates.",
    ])
    story.append(M("2.2 Scope", "H2"))
    scope_rows = [
        ["Organisation", "SecurePay Technologies Pvt. Ltd. (all 50 employees) and the outsourced customer support "
                         "vendor where it handles SecurePay data."],
        ["Locations", "Bengaluru office (single floor, managed building); remote and hybrid working; AWS "
                      "ap-south-1 (Mumbai) and ap-south-2 (Hyderabad)."],
        ["Systems", "Payment API, hosted checkout, merchant dashboard, internal Ops Console, AWS production and "
                    "non-production accounts, GitHub and CI/CD, Google Workspace, SaaS helpdesk, endpoints."],
        ["Annex A controls", f"20 of 93 controls across the four themes (Organizational {len(by_theme['Organizational'])}, "
                             f"People {len(by_theme['People'])}, Physical {len(by_theme['Physical'])}, Technological "
                             f"{len(by_theme['Technological'])}), including {len(new_assessed)} of the 11 controls new in "
                             "2022: " + ", ".join(c["control_id"] for c in new_assessed) + "."],
        ["Clauses", "High-level review of Clauses 4–10 (status and principal gap)."],
        ["Out of scope", "Technical testing (VAPT, configuration review), physical inspection of AWS data "
                         "centres (inherited controls), PCI DSS and DPDP compliance opinions."],
    ]
    story.append(data_table(["Dimension", "In scope"], scope_rows, [32 * mm, 142 * mm]))
    story.append(Spacer(1, 3 * mm))
    story.append(P(
        "Controls were selected for their relevance to a cloud-hosted payment business: governance foundations "
        "(policy, inventory), the third-party and cloud dependencies SecurePay relies on, the regulatory "
        "drivers (privacy, incident reporting) and the technical controls that most directly protect payment "
        "and personal data (identity, vulnerabilities, configuration, monitoring, cryptography, backup and "
        "secure coding)."))

    story.append(M("2.3 Assessment approach", "H2"))
    story.append(data_table(["Phase", "Activities", "Output"], [
        ["1. Plan and scope", "Agree objectives, scope and control sample; define rating scales and risk "
                              "appetite.", "Scope statement, rating scales"],
        ["2. Understand context", "Build the organisation profile: business model, assets, systems, data "
                                  "flows, regulatory obligations and stakeholders.", "Organisation profile"],
        ["3. Assess controls", "For each control, compare the paraphrased requirement with the (assumed) "
                               "current state, list the evidence an assessor would request, rate conformance "
                               "and maturity and record the gap.", "Detailed findings (section 6)"],
        ["4. Assess risk", "Identify asset-threat-vulnerability scenarios from the gaps, score likelihood and "
                           "impact, choose a treatment and estimate target risk.", "Risk register, heat maps"],
        ["5. Report and plan", "Draft the SoA, prioritise recommendations into a 12-month roadmap with "
                               "owners and effort, and present results.", "This report, SoA, roadmap"],
    ], [34 * mm, 100 * mm, 40 * mm]))

    story.append(CondPageBreak(70 * mm))
    story.append(M("2.4 Rating scales", "H2"))
    story.append(P("Each control receives a conformance status, a maturity score (current and 12-month target) "
                   "and a risk rating for the gap. Full definitions are in Appendix A."))
    story.append(data_table(["Status", "Meaning"], [
        [("chip", "Conformant"), "Control is designed and operating as required; at most minor observations."],
        [("chip", "Partially conformant"), "Control exists in part or informally; significant elements are "
                                           "missing, undocumented or inconsistently applied."],
        [("chip", "Non-conformant"), "Control is absent or so ineffective that the requirement is not met."],
    ], [40 * mm, 134 * mm]))
    story.append(Spacer(1, 3 * mm))
    story.append(P(
        "Risk = Likelihood (1–5) × Impact (1–5), giving a score of 1–25. Bands: Low 1–5, "
        "Medium 6–10, High 12–16, Critical 20–25. Assumed risk appetite: SecurePay has a low appetite "
        "for risks to payment and personal data and to regulatory standing. Risks scored 12 or more (High and "
        "Critical) must be treated; Medium risks may be accepted with documented CEO sign-off; Low risks are "
        "accepted and monitored. Treatment options are mitigate, transfer, avoid or accept."))

    story.append(M("2.5 Limitations", "H2"))
    story += bullets([
        "This is a self-directed assessment of a fictional organisation. The current state is assumed, not "
        "observed; no interviews, walkthroughs, evidence sampling or technical testing were performed.",
        "Twenty of 93 controls were assessed in detail. SoA statuses for the other controls are indicative "
        "only and should be validated before an ISMS is formalised.",
        "Findings reflect a point in time (October 2026); conditions may change.",
        "Regulatory references are summarised for context and are not legal advice.",
    ])

    # ================================================================ 3
    story.append(PageBreak())
    story.append(M("3. Organisation overview", "H1"))
    story.append(P(
        "The full profile is in org-profile.md in the project repository. This section summarises the points "
        "that shape the assessment."))
    story.append(data_table(["Attribute", "Detail"], [
        ["Business", "Online Payment Aggregator (RBI in-principle authorisation). Hosted checkout, payment links, "
                     "UPI and card acceptance, and T+1 settlement for about 1,200 SME merchants."],
        ["Scale", "About 0.9 million transactions and INR 180 crore gross transaction value a month; Series A "
                  "funded; founded 2021."],
        ["People", "50 employees: Engineering 20, Operations & Risk 10, Sales & Partnerships 6, Product & Design 5, "
                   "Leadership 4, Finance/Legal/Compliance 3, HR & Admin 2. Plus 12 outsourced support agents."],
        ["Technology", "AWS (ECS Fargate, RDS PostgreSQL Multi-AZ, S3, KMS, WAF) in Mumbai, backups in Hyderabad; "
                       "Node.js and React; GitHub and GitHub Actions; Terraform; Google Workspace; Slack; SaaS "
                       "helpdesk."],
        ["Security posture", "No formal ISMS or dedicated security role; the CTO is the de facto security owner. "
                             "Annual VAPT by a CERT-In empanelled auditor; PCI DSS QSA pre-assessment completed."],
    ], [32 * mm, 142 * mm]))

    story.append(M("3.1 Key information assets", "H2"))
    story.append(data_table(["Asset", "Description", "Classification"], [
        ["Transaction data", "Payment records, card tokens, last-4 digits, UPI IDs, amounts, merchant IDs", "Restricted"],
        ["Merchant KYC data", "PAN, GST, bank account proof, masked Aadhaar, director details (S3)", "Restricted"],
        ["Customer personal data", "Payer names, phone numbers, email addresses (checkout and support)", "Confidential"],
        ["Settlement and payout data", "Daily settlement files, merchant bank accounts, payout instructions", "Restricted"],
        ["Source code and secrets", "Payment platform code, Terraform, API keys for banks and partners", "Restricted"],
        ["Security and audit logs", "CloudTrail, application and load balancer logs", "Confidential"],
        ["Corporate information", "Contracts, board papers, HR records, financials", "Confidential"],
    ], [42 * mm, 102 * mm, 30 * mm]))

    story.append(CondPageBreak(60 * mm))
    story.append(M("3.2 Principal data flows", "H2"))
    story.append(data_table(["Flow", "Path", "Key protection"], [
        ["Card checkout", "Payer browser -> hosted checkout -> partner processor hosted fields (PCI L1) -> token -> "
                          "Payment API -> acquiring bank -> card network", "TLS 1.2+, tokenisation, no PAN storage"],
        ["UPI payment", "Payer app -> sponsor bank PSP -> NPCI -> Payment API callback", "Signed callbacks, TLS"],
        ["Merchant onboarding", "Merchant uploads KYC -> S3 -> KYC verification API -> Ops review in Ops Console",
         "KMS encryption, Aadhaar masking"],
        ["Settlement", "Acquiring bank settlement file (SFTP) -> reconciliation -> payout via bank API",
         "SFTP, single approver (gap)"],
        ["Customer support", "Customer/merchant -> SaaS helpdesk -> SupportCo agents -> support console",
         "Shared logins, no MFA (gap)"],
        ["Software delivery", "GitHub -> GitHub Actions -> Amazon ECR -> ECS production", "Peer review, separate accounts"],
    ], [30 * mm, 98 * mm, 46 * mm]))

    story.append(M("3.3 Regulatory and contractual obligations", "H2"))
    story.append(data_table(["Obligation", "Relevance to SecurePay"], [
        ["Digital Personal Data Protection Act, 2023 and DPDP Rules, 2025",
         "SecurePay is a Data Fiduciary: reasonable security safeguards, breach intimation, retention limits, "
         "Data Principal rights; penalties up to INR 250 crore per breach of safeguards."],
        ["RBI Guidelines on Regulation of Payment Aggregators and Payment Gateways (2020, as amended)",
         "Authorisation conditions, baseline technology and security recommendations, no storage of card data, "
         "incident reporting."],
        ["RBI directive on storage of payment system data (2018)", "Payment data must be stored only in India."],
        ["CERT-In Directions under section 70B of the IT Act (April 2022)",
         "Report specified incidents within 6 hours; keep ICT logs for 180 days in India; synchronise clocks."],
        ["PCI DSS v4.0.1", "Service provider handling card data in transit; card network and acquirer requirement."],
        ["Information Technology Act, 2000", "Section 43A liability and offences relating to computer systems."],
        ["Partner bank and merchant contracts", "Security questionnaires, audit rights, breach notification clauses."],
    ], [62 * mm, 112 * mm]))

    story.append(CondPageBreak(50 * mm))
    story.append(M("3.4 Stakeholders and interested parties", "H2"))
    story.append(P(
        "Internal: CEO (accountable executive), CTO (interim security owner), CFO, Head of Legal & Compliance, Head "
        "of Customer Operations, Engineering Lead, Cloud & DevOps Lead, HR & Admin Manager and all staff. External: "
        "RBI, CERT-In, Data Protection Board of India, acquiring and sponsor banks, card networks (via acquirer), "
        "NPCI (via sponsor bank), merchants, payers (Data Principals), investors, SupportCo, AWS and other "
        "suppliers, the PCI QSA and VAPT auditors."))

    # ================================================================ 4
    story.append(PageBreak())
    story.append(M("4. Maturity overview", "H1"))
    story.append(P("The table and charts below summarise conformance status and maturity by Annex A theme."))
    rows = []
    for t in THEMES:
        cs = Counter(c["status"] for c in by_theme[t])
        k = len(by_theme[t])
        m_avg = sum(int(c["maturity_current"]) for c in by_theme[t]) / k
        rows.append([f"{t} ({THEME_PREFIX[t]})", str(k)] +
                    [f"{cs[s]} ({cs[s] / k:.0%})" for s in STATUS_ORDER] + [f"{m_avg:.1f}"])
    rows.append(["Total", str(n)] + [f"{sc[s]} ({sc[s] / n:.0%})" for s in STATUS_ORDER] + [f"{mat:.1f}"])
    story.append(data_table(["Theme", "Assessed", "Conformant", "Partially conformant", "Non-conformant",
                             "Avg maturity"], rows,
                            [44 * mm, 20 * mm, 27 * mm, 33 * mm, 29 * mm, 21 * mm],
                            extra=[("FONTNAME", (0, len(rows)), (-1, len(rows)), "Helvetica-Bold"),
                                   ("LINEABOVE", (0, len(rows)), (-1, len(rows)), 1, NAVY)]))
    story.append(Spacer(1, 4 * mm))
    story += figure(CHART_DIR / "conformance_by_theme.png", 160,
                    "Figure 1 - Conformance status by Annex A theme (number of controls assessed)")
    story += figure(CHART_DIR / "maturity_by_theme.png", 160,
                    "Figure 2 - Average control maturity by theme against the 12-month target")
    story.append(M("Observations", "H2n"))
    story += bullets([
        f"<b>Organizational controls are weakest</b> (average maturity "
        f"{sum(int(c['maturity_current']) for c in by_theme['Organizational']) / len(by_theme['Organizational']):.1f}). "
        "None is fully conformant: governance, supplier management, incident preparation, threat intelligence "
        "and privacy all need structure.",
        "<b>Technological controls are mixed.</b> Cloud-native choices give strong encryption and backup, but "
        "identity, vulnerability management and monitoring lag behind the risk of a payment platform.",
        "<b>People controls are relatively strong</b> thanks to standard Indian HR practice (background "
        "verification) and a managed laptop fleet; awareness training is the gap.",
        "<b>Physical exposure is limited</b> because SecurePay runs no data centre, but laptop re-use and disposal "
        "is uncontrolled.",
        f"<b>The 2022 controls are a blind spot:</b> of the {len(new_assessed)} new controls assessed, "
        f"{sum(c['status'] == 'Conformant' for c in new_assessed)} are conformant and "
        f"{sum(c['status'] == 'Non-conformant' for c in new_assessed)} are non-conformant.",
    ], markup=True)

    # ================================================================ 5
    story.append(PageBreak())
    story.append(M("5. Clauses 4–10 summary", "H1"))
    story.append(P(
        "Clauses 4–10 set out the management system an organisation must run to be certified, separate "
        "from the Annex A controls. SecurePay has no formal ISMS, so most clause requirements are partially met "
        "at best. The table gives one line per clause."))
    story.append(data_table(["Clause", "Status", "Current state", "Principal gap"],
                            [[f"{c['clause']}. {c['title']}", ("chip", c["status"]), c["current_state"], c["gap"]]
                             for c in clauses], [36 * mm, 28 * mm, 50 * mm, 60 * mm]))
    cc = Counter(c["status"] for c in clauses)
    story.append(Spacer(1, 3 * mm))
    story.append(callout([P(
        f"Summary: {cc['Conformant']} conformant, {cc['Partially conformant']} partially conformant, "
        f"{cc['Non-conformant']} non-conformant. The missing risk assessment and treatment process (Clause 6) and "
        "the absence of internal audit and management review (Clause 9) would each be major nonconformities at "
        "a certification audit. This report's risk register and SoA are a first step towards Clause 6.",
        "callout")]))

    # ================================================================ 6
    story.append(PageBreak())
    story.append(M("6. Detailed Annex A findings", "H1"))
    story.append(P("Summary of the 20 controls assessed. Controls marked * are new in ISO/IEC 27001:2022."))
    story.append(data_table(["Control", "Name", "Theme", "Status", "Risk"],
                            [[c["control_id"] + ("*" if c["new_in_2022"] == "Y" else ""), c["control_name"],
                              c["theme"], ("chip", c["status"]), ("chip", c["risk_rating"])] for c in controls],
                            [18 * mm, 76 * mm, 26 * mm, 32 * mm, 22 * mm]))
    for t in THEMES:
        heading = M(f"6.{THEMES.index(t) + 1} {t} controls ({THEME_PREFIX[t]})", "H2")
        for i, c in enumerate(by_theme[t]):
            card = finding_card(c, W)
            story.append(KeepTogether([heading, card]) if i == 0 else card)
            story.append(Spacer(1, 5 * mm))

    # ================================================================ 7
    story.append(PageBreak())
    story.append(M("7. Risk assessment", "H1"))
    story.append(P(
        "Risks were identified as asset-threat-vulnerability scenarios that follow from the control gaps. Each "
        "was scored for likelihood and impact (scales in Appendix A) before treatment, a treatment option was "
        "chosen in line with the assumed risk appetite, and a target score was estimated assuming the treatment "
        "plan is delivered."))
    heat = Table([[figure(CHART_DIR / "risk_heatmap.png", 84), figure(CHART_DIR / "risk_heatmap_target.png", 84)]],
                 colWidths=[W / 2, W / 2])
    heat.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    story.append(heat)
    story.append(P("Figure 3 - Risk heat maps: inherent risk (left) and target risk after treatment (right). "
                   "Cells show the risk score; labels identify risks in the register.", "caption"))
    story.append(M("7.1 Risk register summary", "H2"))
    story.append(data_table(
        ["ID", "Risk", "L", "I", "Score", "Rating", "Treatment", "Owner", "Target"],
        [[r["risk_id"], r["risk_title"], r["likelihood"], r["impact"], r["score"], ("chip", r["rating"]),
          r["treatment"], r["owner"], ("chip", f"{r['target_rating']}")] for r in risks],
        [10 * mm, 56 * mm, 7 * mm, 7 * mm, 11 * mm, 17 * mm, 17 * mm, 30 * mm, 19 * mm],
        extra=[("ALIGN", (2, 1), (4, -1), "CENTER")]))
    story.append(Spacer(1, 2 * mm))
    story.append(P(f"L = likelihood, I = impact. Target = rating after the treatment plan (scores in section 7.2). "
                   f"Inherent profile: {rr['Critical']} Critical, {rr['High']} High, {rr['Medium']} Medium, "
                   f"{rr['Low']} Low.", "small"))

    story.append(CondPageBreak(80 * mm))
    story.append(M("7.2 Risk scenarios and treatment plans", "H2"))
    for r in risks:
        rows = [
            ["Asset", r["asset"]], ["Threat", r["threat"]], ["Vulnerability", r["vulnerability"]],
            ["Related controls", r["related_controls"]],
            ["Treatment", f"{r['treatment']}: {r['treatment_plan']}"],
            ["Owner / target", f"{r['owner']}. Target L{r['target_likelihood']} x I{r['target_impact']} = "
                               f"{r['target_score']} ({r['target_rating']})"],
        ]
        head = Table([[M(f"<b>{escape(r['risk_id'])}  {escape(r['risk_title'])}</b>",
                         ParagraphStyle("rh", parent=ST["small"], textColor=WHITE)),
                       chip(r["rating"])[0],
                       M(f"<b>{r['likelihood']} x {r['impact']} = {r['score']}</b>",
                         ParagraphStyle("rs", parent=ST["small"], textColor=WHITE))]],
                     colWidths=[118 * mm, 26 * mm, 30 * mm])
        head.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY),
                                  ("BACKGROUND", (1, 0), (1, 0), chip(r["rating"])[1]),
                                  ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
        body = Table([[P(k, "smallb"), P(v, "small")] for k, v in rows], colWidths=[30 * mm, 144 * mm])
        body.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
                                  ("BACKGROUND", (0, 0), (0, -1), PANEL),
                                  ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
        story.append(KeepTogether([head, body, Spacer(1, 4 * mm)]))

    # ================================================================ 8
    story.append(PageBreak())
    story.append(M("8. Statement of Applicability", "H1"))
    story.append(P(
        f"The SoA records, for every one of the 93 Annex A controls, whether it is applicable, why, and its "
        f"implementation status. {len(applicable)} controls are applicable and {len(soa) - len(applicable)} are "
        f"excluded with justification. The 20 controls assessed in detail carry their assessed status; the "
        f"remaining statuses are indicative and must be confirmed when the ISMS is formalised. The full SoA is in "
        f"Appendix B and in data/soa.csv."))
    rows = []
    for t in THEMES:
        sub = [r for r in soa if r["theme"] == t]
        cn = Counter(r["implementation_status"] for r in sub)
        rows.append([f"{t} ({THEME_PREFIX[t]})", str(len(sub)), str(cn["Implemented"]),
                     str(cn["Partially implemented"]), str(cn["Not implemented"]), str(cn["Not applicable"])])
    rows.append(["Total", str(len(soa)), str(soa_cnt["Implemented"]), str(soa_cnt["Partially implemented"]),
                 str(soa_cnt["Not implemented"]), str(soa_cnt["Not applicable"])])
    story.append(data_table(["Theme", "Controls", "Implemented", "Partially impl.", "Not implemented", "Not applicable"],
                            rows, [48 * mm, 22 * mm, 25 * mm, 27 * mm, 28 * mm, 24 * mm],
                            extra=[("FONTNAME", (0, len(rows)), (-1, len(rows)), "Helvetica-Bold"),
                                   ("LINEABOVE", (0, len(rows)), (-1, len(rows)), 1, NAVY),
                                   ("ALIGN", (1, 1), (-1, -1), "CENTER")]))
    story.append(Spacer(1, 4 * mm))
    story += figure(CHART_DIR / "soa_status.png", 155, "Figure 4 - Implementation status of all 93 Annex A controls")
    story.append(M("8.1 Exclusions", "H2"))
    story.append(data_table(["Control", "Name", "Justification for exclusion"],
                            [[r["control_id"], r["control_name"], r["justification"]] for r in soa
                             if r["applicable"] == "N"], [18 * mm, 48 * mm, 108 * mm]))
    story.append(Spacer(1, 3 * mm))
    story.append(P(
        "Physical data centre controls (for example A.7.1, A.7.5 and A.7.11) remain applicable but are largely "
        "inherited from AWS. SecurePay should verify them each year through AWS Artifact (SOC 2 and PCI DSS AOC) "
        "rather than exclude them."))

    # ================================================================ 9
    story.append(PageBreak())
    story.append(M("9. Prioritised remediation roadmap", "H1"))
    story.append(P(
        "Recommendations are sequenced by risk reduction and dependency. Quick wins in the first three months "
        "target the Critical and High risks with mostly configuration and governance changes; the next two "
        "phases build repeatable processes and then the capabilities needed for certification. Effort is "
        "indicative internal person-days."))
    for i, ph in enumerate(PHASES):
        items = [r for r in roadmap if r["phase"] == ph]
        label = ["Phase 1 - Quick wins", "Phase 2 - Build core processes", "Phase 3 - Mature and certify"][i]
        story.append(CondPageBreak(50 * mm))
        story.append(M(f"9.{i + 1} {label} ({ph})", "H2"))
        story.append(data_table(["ID", "Initiative", "Controls / risks", "Effort", "Owner", "Success measure"],
                                [[r["id"], r["initiative"], f"{r['related_controls']} | {r['related_risks']}",
                                  r["effort"], r["owner"], r["success_measure"]] for r in items],
                                [9 * mm, 58 * mm, 25 * mm, 24 * mm, 25 * mm, 33 * mm], font="tiny",
                                head_style="thtiny"))
    story.append(Spacer(1, 4 * mm))
    story.append(callout([P(
        "Dependencies: appoint the Information Security Manager (Q5) first, since that role owns most Phase 2 and 3 "
        "items. Supplier (M1) and DPDP (M2) work need Legal capacity in parallel. The MDR/SIEM decision (L1) should "
        "build on the alert use cases proven in Q3.", "callout")]))

    # ================================================================ 10
    story.append(PageBreak())
    story.append(M("10. Conclusion", "H1"))
    story.append(P(
        "SecurePay has the technical building blocks of a secure payment platform: data stays in India, card "
        "data is tokenised, encryption and backups are sound, laptops are managed and staff are screened. What "
        "it lacks is the management system that makes security deliberate and provable. Policies are unapproved, "
        "nobody owns security formally, risks are not assessed, and nothing is monitored, audited or improved "
        "systematically."))
    story.append(P(
        "The most urgent exposures are privileged access to production, the inability to detect and report "
        "incidents within regulatory deadlines, and personal data held by an unassessed support vendor. All "
        "three can be reduced substantially within 90 days, mainly through configuration and governance work "
        "rather than new tools."))
    story.append(P(
        "We recommend that leadership approve the roadmap in section 9, appoint an Information Security Manager "
        "now, and track progress monthly through a security steering group. On that path, SecurePay can expect "
        "to reach a 'Defined' maturity level and be ready for an ISO/IEC 27001 Stage 1 audit in about 12 months, "
        "while making clear progress on its PCI DSS, DPDP and RBI obligations."))
    story.append(Spacer(1, 6 * mm))
    story.append(callout([P(
        "Reminder: this report concerns a fictional organisation and assumed conditions. It was prepared as a "
        "self-directed portfolio exercise and is not the output of a real client engagement.", "callout")],
        bg=colors.HexColor("#FFF6DD"), bar=colors.HexColor("#E0B84A")))

    # ================================================================ Appendices
    story.append(PageBreak())
    story.append(M("Appendix A - Rating definitions", "H1"))
    story.append(M("A.1 Maturity scale (CMMI-inspired)", "H2n"))
    story.append(data_table(["Level", "Name", "Description"], [
        ["0", "Non-existent", "No recognisable process or control."],
        ["1", "Initial", "Ad hoc and person-dependent; undocumented; results vary."],
        ["2", "Repeatable", "Practised consistently by some teams but not documented, approved or measured."],
        ["3", "Defined", "Documented, approved, communicated and applied consistently across the organisation."],
        ["4", "Managed", "Measured with metrics, monitored and reviewed; deviations are corrected."],
        ["5", "Optimised", "Continuously improved and automated, using metrics and threat intelligence."],
    ], [14 * mm, 28 * mm, 132 * mm]))
    story.append(M("A.2 Likelihood scale", "H2n"))
    story.append(data_table(["Score", "Rating", "Description"], [
        ["1", "Rare", "Not expected in the next 3 years; requires exceptional circumstances."],
        ["2", "Unlikely", "Could occur within 3 years; few enabling weaknesses."],
        ["3", "Possible", "Could occur within the next year; known weaknesses exist."],
        ["4", "Likely", "Expected within the next year; weaknesses are known to attackers or have been exploited."],
        ["5", "Almost certain", "Expected within months, or already occurring."],
    ], [14 * mm, 28 * mm, 132 * mm]))
    story.append(CondPageBreak(60 * mm))
    story.append(M("A.3 Impact scale", "H2n"))
    story.append(data_table(["Score", "Rating", "Financial", "Regulatory / legal", "Customers and data",
                             "Operations"], [
        ["1", "Negligible", "< INR 5 lakh", "None", "No personal data affected", "< 15 min disruption"],
        ["2", "Minor", "INR 5-25 lakh", "Informal query", "< 1,000 records", "< 1 h outage"],
        ["3", "Moderate", "INR 25 lakh-1 crore", "Regulatory inquiry or audit observation", "1,000-10,000 records",
         "1-4 h outage"],
        ["4", "Major", "INR 1-5 crore", "Formal regulatory action, penalty, PCI non-compliance",
         "10,000-100,000 records; merchant churn", "4-24 h outage"],
        ["5", "Severe", "> INR 5 crore", "DPDP penalty, RBI suspension of authorisation",
         "> 100,000 records; national media", "> 24 h outage"],
    ], [12 * mm, 20 * mm, 28 * mm, 42 * mm, 40 * mm, 32 * mm], font="tiny", head_style="thtiny"))
    story.append(M("A.4 Risk rating bands and treatment", "H2n"))
    story.append(data_table(["Score", "Rating", "Required response"], [
        ["20-25", ("chip", "Critical"), "Immediate treatment; CEO informed within 24 hours; tracked weekly."],
        ["12-16", ("chip", "High"), "Treatment plan within 30 days; above appetite; tracked monthly."],
        ["6-10", ("chip", "Medium"), "Treat or formally accept with CEO sign-off; reviewed quarterly."],
        ["1-5", ("chip", "Low"), "Accept and monitor through normal operations."],
    ], [20 * mm, 26 * mm, 128 * mm]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("Treatment options: Mitigate (reduce likelihood or impact with controls), Transfer (shift "
                   "financial impact, e.g. insurance or contract), Avoid (stop the activity that creates the risk), "
                   "Accept (retain the risk with documented approval)."))

    story.append(PageBreak())
    story.append(M("Appendix B - Statement of Applicability (all 93 controls)", "H1"))
    story.append(P("* = control new in ISO/IEC 27001:2022. Bold IDs were assessed in detail in section 6. Statuses "
                   "of other controls are indicative.", "small"))
    story.append(Spacer(1, 2 * mm))
    srows = []
    for r in soa:
        idp = M(("<b>%s</b>" if r["assessed_in_detail"] == "Y" else "%s") %
                escape(r["control_id"] + ("*" if r["new_in_2022"] == "Y" else "")), "tiny")
        srows.append([idp, r["control_name"], r["applicable"], r["justification"],
                      ("chip", r["implementation_status"])])
    story.append(data_table(["Control", "Name", "Appl.", "Justification", "Implementation status"], srows,
                            [14 * mm, 46 * mm, 9 * mm, 74 * mm, 31 * mm], font="tiny", head_style="thtiny", pad=1.8,
                            extra=[("ALIGN", (2, 1), (2, -1), "CENTER")]))

    story.append(PageBreak())
    story.append(M("Appendix C - Assumptions", "H1"))
    story.append(data_table(["ID", "Assumption"], [[a["id"], a["assumption"]] for a in assumptions],
                            [16 * mm, 158 * mm]))
    story.append(Spacer(1, 6 * mm))
    story.append(M("Appendix D - Glossary", "H1"))
    terms = [
        ("AOC", "Attestation of Compliance (PCI DSS)"), ("ASV", "Approved Scanning Vendor (PCI DSS)"),
        ("BEC", "Business email compromise"), ("CERT-In", "Indian Computer Emergency Response Team"),
        ("CIS", "Center for Internet Security"), ("DPA", "Data processing agreement"),
        ("DPDP", "Digital Personal Data Protection Act, 2023"), ("IDOR", "Insecure direct object reference"),
        ("ISMS", "Information Security Management System"), ("MDR", "Managed detection and response"),
        ("MFA", "Multi-factor authentication"), ("PA", "Payment Aggregator (RBI-regulated)"),
        ("PCI DSS", "Payment Card Industry Data Security Standard"), ("RPO / RTO", "Recovery point / time objective"),
        ("SAST / SCA", "Static app. security testing / software composition analysis"),
        ("SIEM", "Security information and event management"), ("SoA", "Statement of Applicability"),
        ("VAPT", "Vulnerability assessment and penetration testing"),
    ]
    half = (len(terms) + 1) // 2
    pairs = [list(terms[i]) + (list(terms[i + half]) if i + half < len(terms) else ["", ""]) for i in range(half)]
    story.append(data_table(["Term", "Meaning", "Term", "Meaning"], pairs, [20 * mm, 67 * mm, 20 * mm, 67 * mm],
                            extra=[("LINEBEFORE", (2, 0), (2, -1), 1, WHITE)]))
    return story


def finding_card(c, W):
    """One control finding rendered as a compact, client-style card."""
    status_p, status_bg = chip(c["status"])
    risk_p, risk_bg = chip(c["risk_rating"])
    title = f"{c['control_id']}  {c['control_name']}"
    head = Table([[M(f"<b>{escape(title)}</b>", ParagraphStyle("ch", parent=ST["body"], textColor=WHITE,
                                                                spaceAfter=0)),
                   M("NEW IN 2022" if c["new_in_2022"] == "Y" else "",
                     ParagraphStyle("nw", parent=ST["tinyb"], textColor=colors.HexColor("#AFC3DD"),
                                    alignment=2))]],
                 colWidths=[W - 30 * mm, 30 * mm])
    head.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                              ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6)]))
    lab = ParagraphStyle("ml", parent=ST["tiny"], textColor=MUTED)
    meta = Table([[M("THEME", lab), M("STATUS", lab), M("GAP RISK", lab), M("MATURITY (CURRENT / TARGET)", lab),
                   M("OWNER / TIMELINE", lab)],
                  [P(c["theme"], "smallb"), status_p, risk_p,
                   P(f"{c['maturity_current']} / {c['maturity_target']}", "smallb"),
                   P(f"{c['owner']} | {c['roadmap_phase']}", "small")]],
                 colWidths=[26 * mm, 34 * mm, 20 * mm, 34 * mm, W - 114 * mm])
    meta.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PANEL),
                              ("BACKGROUND", (1, 1), (1, 1), status_bg), ("BACKGROUND", (2, 1), (2, 1), risk_bg),
                              ("VALIGN", (0, 0), (-1, -1), "TOP"),
                              ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                              ("LINEAFTER", (0, 0), (-2, -1), 1.5, WHITE)]))
    rows = [("Requirement (paraphrased)", c["requirement"]), ("Current state (assumed)", c["current_state"]),
            ("Evidence requested", c["evidence_requested"]), ("Gap", c["gap"]),
            ("Recommendation", c["recommendation"])]
    body = Table([[P(k, "smallb"), P(v, "small")] for k, v in rows], colWidths=[34 * mm, W - 34 * mm])
    body.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
                              ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                              ("LEFTPADDING", (0, 0), (-1, -1), 5)]))
    # Keep header + meta + first rows together; the body may split across pages if needed.
    return KeepTogether([head, meta, body])


# --------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--author", default="Abhishek", help="name shown as report author")
    args = ap.parse_args()

    d = {"controls": load("controls.csv"), "clauses": load("clauses.csv"), "risks": load("risk-register.csv"),
         "soa": load("soa.csv"), "roadmap": load("roadmap.csv"), "assumptions": load("assumptions.csv"),
         "author": args.author}

    # light integrity checks so the report never silently disagrees with its data
    assert len(d["soa"]) == 93, "SoA must list all 93 Annex A controls"
    assert len(d["controls"]) == 20, "expected 20 assessed controls"
    for r in d["risks"]:
        assert int(r["score"]) == int(r["likelihood"]) * int(r["impact"]), r["risk_id"]
        assert r["rating"] == band(int(r["score"])), r["risk_id"]

    CHART_DIR.mkdir(parents=True, exist_ok=True)
    chart_conformance_by_theme(d["controls"], CHART_DIR / "conformance_by_theme.png")
    chart_maturity_by_theme(d["controls"], CHART_DIR / "maturity_by_theme.png")
    chart_heatmap(d["risks"], CHART_DIR / "risk_heatmap.png", "likelihood", "impact", "Inherent risk")
    chart_heatmap(d["risks"], CHART_DIR / "risk_heatmap_target.png", "target_likelihood", "target_impact",
                  "Target risk (after treatment)")
    chart_soa(d["soa"], CHART_DIR / "soa_status.png")

    doc = ReportDoc(str(PDF_PATH), author=args.author)
    doc.multiBuild(build_story(d))
    sc = Counter(c["status"] for c in d["controls"])
    print(f"Charts written to {CHART_DIR.relative_to(ROOT)}/")
    print(f"Report written to {PDF_PATH.relative_to(ROOT)} ({doc.page} pages)")
    print("Status counts:", dict(OrderedDict((s, sc[s]) for s in STATUS_ORDER)))


if __name__ == "__main__":
    main()
