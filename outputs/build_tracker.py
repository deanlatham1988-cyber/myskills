"""Build MORPh-branded sponsorship tracker mockups (Commercials + Delivery).

Two linked workbooks keyed on Item Ref. Visual mockups for Amz review.
"""
from __future__ import annotations
import datetime as dt
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting.rule import Rule, CellIsRule, FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.worksheet.page import PageMargins, PrintOptions

# ---------- MORPh brand ----------
NAVY = "02084B"
MAGENTA = "FD02F7"
PURPLE = "9A2CFB"
LIGHT_BG = "F5F0FA"
TABLE_ALT = "F0EDF5"
GREY = "BFBFBF"
GREY_DARK = "8A8A8A"
RED = "D7263D"
AMBER = "E89611"
GREEN = "2E7D32"
WHITE = "FFFFFF"
BLACK = "000000"

FONT_NAME = "Calibri"

# Stage colours
STAGE_FILLS = {
    "1. Initiation":         LIGHT_BG,
    "2. Production":         PURPLE,
    "3. Sponsor Draft Sent": TABLE_ALT,
    "4. Sponsor Review":     MAGENTA,
    "5. Regulatory Gate":    NAVY,
    "6. Pre-Launch":         "E8A7FF",  # magenta tint
    "7. Live":               PURPLE,
    "8. Closed":             GREY,
}
STAGE_TEXT = {
    "1. Initiation":         NAVY,
    "2. Production":         WHITE,
    "3. Sponsor Draft Sent": NAVY,
    "4. Sponsor Review":     WHITE,
    "5. Regulatory Gate":    WHITE,
    "6. Pre-Launch":         NAVY,
    "7. Live":               WHITE,
    "8. Closed":             WHITE,
}
STAGES = list(STAGE_FILLS.keys())

TYPES = ["Toolkit", "Blog", "Newsletter", "Banner", "Neighbourhood Banner", "Event"]
INVOICE_STATUSES = ["Booked", "Invoiced", "Paid"]
LEADS = ["Pooja", "Will", "Will/Colin", "Will/Chloe", "Dean", "Ariyan"]
YESNO_NA = ["Yes", "No", "N/A"]

# ---------- Data ----------
# Current 14 rows from CSV, mapped to new stage model + enriched
ROWS = [
    dict(ref="ROSTOO01", sponsor="Rosemont", type="Toolkit",
         detail="Dysphagia & Licensed Liquid Meds",
         lead="Pooja", month="February", revenue=5000, spend=0,
         draft="03.02.2026", approved="", live="",
         stage="4. Sponsor Review",
         pooja="02.04.2026 — Rosemont liaising with Iqera on final amendments before approval.",
         iqera="",
         brief="15.01.2026", target_live="28.02.2026"),
    dict(ref="PROTOO01", sponsor="Proveca", type="Toolkit",
         detail="Hypersalivation in children",
         lead="Pooja", month="March", revenue=3000, spend=0,
         draft="05.02.2026", approved="", live="",
         stage="5. Regulatory Gate",
         pooja=("Met with Caroline 04.02.26 — very happy with overall feel. "
                "Sent 05.02 for content review. 02.04.2026 — handed over to Iqera via email. "
                "Training video to Caroline once complete."),
         iqera="In progress — awaiting additional info from pharma",
         brief="20.01.2026", target_live="31.03.2026"),
    dict(ref="ASTTOO01", sponsor="Astellas", type="Toolkit",
         detail="OAB management",
         lead="Pooja", month="March", revenue=7000, spend=0,
         draft="03.02.2026", approved="", live="",
         stage="5. Regulatory Gate",
         pooja=("02.04.2026 — handed over to Iqera, submitted everything except training video "
                "on Promomats. Awaiting approval."),
         iqera="",
         brief="10.01.2026", target_live="31.03.2026"),
    dict(ref="STATOO01", sponsor="Stada", type="Toolkit",
         detail="Asthma & COPD",
         lead="Pooja", month="February", revenue=5000, spend=0,
         draft="09.03.2026", approved="16.03.2026", live="17.03.2026",
         stage="8. Closed",
         pooja="Completed — uploaded to website.",
         iqera="",
         brief="05.01.2026", target_live="28.02.2026"),
    dict(ref="PROBLO01", sponsor="Proveca", type="Blog",
         detail="Hypersalivation in children",
         lead="Pooja", month="January", revenue=7000, spend=0,
         draft="", approved="", live="",
         stage="1. Initiation",
         pooja=("Sent overview to Ryan to post on GP group. Caroline has a colleague at Proveca. "
                "Once author secured, write blog and send to Proveca."),
         iqera="",
         brief="", target_live="31.01.2026"),
    dict(ref="PROAST01", sponsor="Astellas", type="Blog",
         detail="OAB management — Richard Daniszewski",
         lead="Pooja", month="January", revenue=2500, spend=300,
         draft="20.02.2026", approved="", live="",
         stage="4. Sponsor Review",
         pooja=("Commissioned Richard to complete by 22.02. £100/hr max 3 hrs. "
                "Submitted to Astellas — awaiting approval."),
         iqera="",
         brief="01.02.2026", target_live="31.01.2026"),
    dict(ref="ROSNEW01", sponsor="Rosemont", type="Newsletter",
         detail="1 mailer to network",
         lead="Will", month="", revenue=1500, spend=0,
         draft="", approved="", live="",
         stage="1. Initiation",
         pooja="", iqera="",
         brief="", target_live=""),
    dict(ref="ROSNEI01", sponsor="Rosemont", type="Neighbourhood Banner",
         detail="2 Neighbourhoods (£450 each)",
         lead="Will/Colin", month="", revenue=900, spend=0,
         draft="", approved="", live="",
         stage="1. Initiation",
         pooja="", iqera="",
         brief="", target_live=""),
    dict(ref="CIPNEW01", sponsor="Cipla", type="Newsletter",
         detail="Owed 2 from 2025",
         lead="Will", month="", revenue=0, spend=0,
         draft="", approved="", live="",
         stage="1. Initiation",
         pooja="Awaiting Cipla to confirm details.",
         iqera="",
         brief="", target_live=""),
    dict(ref="PROBAN01", sponsor="Proveca", type="Banner",
         detail="Owed 2 from 2025",
         lead="Will", month="", revenue=0, spend=0,
         draft="", approved="", live="",
         stage="2. Production",
         pooja="Specs sent to Caroline.",
         iqera="",
         brief="", target_live=""),
    dict(ref="ASTBAN01", sponsor="Astellas", type="Banner",
         detail="",
         lead="Will", month="", revenue=1500, spend=0,
         draft="", approved="", live="",
         stage="1. Initiation",
         pooja="", iqera="",
         brief="", target_live=""),
    dict(ref="ALITOO01", sponsor="Alissa", type="Toolkit",
         detail="",
         lead="Pooja", month="", revenue=8000, spend=0,
         draft="", approved="", live="",
         stage="5. Regulatory Gate",
         pooja=("02.04.2026 — Submitted all of toolkit except training video. "
                "Handed over to Iqera, once training video completed, submit to Alissa."),
         iqera="",
         brief="", target_live=""),
    dict(ref="ASTNEI01", sponsor="Astellas", type="Neighbourhood Banner",
         detail="3 Neighbourhoods",
         lead="Will/Chloe", month="", revenue=0, spend=0,
         draft="", approved="", live="",
         stage="1. Initiation",
         pooja="", iqera="",
         brief="", target_live=""),
]

# Illustrative past items (marked [DEMO - 2025]) so Dean can see Closed state
PAST_DEMO_ROWS = [
    dict(ref="CIPTOO01", sponsor="Cipla", type="Toolkit",
         detail="[DEMO 2025] Asthma inhaler technique",
         lead="Pooja", month="September (2025)", revenue=6000, spend=0,
         draft="15.08.2025", approved="29.08.2025", live="05.09.2025",
         stage="8. Closed",
         pooja="Completed — carried over from 2025 for reference.",
         iqera="", brief="01.07.2025", target_live="30.09.2025"),
    dict(ref="ROSBLO01", sponsor="Rosemont", type="Blog",
         detail="[DEMO 2025] Paediatric liquid meds",
         lead="Pooja", month="November (2025)", revenue=2500, spend=200,
         draft="02.10.2025", approved="20.10.2025", live="05.11.2025",
         stage="8. Closed",
         pooja="Completed 2025 — author: Dr A. Shah.",
         iqera="", brief="15.09.2025", target_live="30.11.2025"),
    dict(ref="MORMEVE01", sponsor="Internal — MORPh", type="Event",
         detail="[DEMO] Dry Eye Training (illustrative event row)",
         lead="Dean", month="May", revenue=0, spend=0,
         draft="", approved="", live="",
         stage="6. Pre-Launch",
         pooja="", iqera="",
         brief="01.03.2026", target_live="15.05.2026",
         venue="London — venue TBC", delegates=45,
         dietary_captured="No", dietary_detail="",
         speaker_confirmed="Yes — Dr Chen",
         check72="No", morning_contact="N/A"),
]

ALL_ROWS = ROWS + PAST_DEMO_ROWS
OUT = Path("/Users/deanlatham/Desktop/work/morph/Morph New World/Spreadsheets")
OUT.mkdir(parents=True, exist_ok=True)
LOGO = "/Users/deanlatham/Desktop/work/morph/Morph New World/Marketing/MORPh Brand Pack/Logo/Dark/Logo-Dark.png"


# ---------- helpers ----------
def thin_border(colour=GREY):
    s = Side(style="thin", color=colour)
    return Border(left=s, right=s, top=s, bottom=s)


def set_col_widths(ws, widths: dict):
    for col, w in widths.items():
        ws.column_dimensions[col].width = w


def landscape_fit(ws, fit_width=1, fit_height=0):
    """Set sheet to print landscape, fit-to-width so PDFs render cleanly."""
    ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
    ws.page_setup.paperSize = ws.PAPERSIZE_A3
    ws.page_setup.fitToWidth = fit_width
    ws.page_setup.fitToHeight = fit_height
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_options.horizontalCentered = False
    ws.page_margins = PageMargins(left=0.3, right=0.3, top=0.5, bottom=0.5,
                                  header=0.2, footer=0.2)


def title_row(ws, row, title, subtitle="", span=12):
    ws.cell(row=row, column=1, value=title)
    ws.cell(row=row, column=1).font = Font(name=FONT_NAME, size=22, bold=True, color=NAVY)
    ws.row_dimensions[row].height = 32
    ws.merge_cells(start_row=row, end_row=row, start_column=1, end_column=span)
    if subtitle:
        ws.cell(row=row + 1, column=1, value=subtitle)
        ws.cell(row=row + 1, column=1).font = Font(name=FONT_NAME, size=11, italic=True, color=GREY_DARK)
        ws.merge_cells(start_row=row + 1, end_row=row + 1, start_column=1, end_column=span)
    # magenta underline
    ws.cell(row=row, column=1).border = Border(bottom=Side(style="medium", color=MAGENTA))


def header_row(ws, row, headers, fill=NAVY, text=WHITE):
    for c, h in enumerate(headers, start=1):
        cell = ws.cell(row=row, column=c, value=h)
        cell.font = Font(name=FONT_NAME, size=10, bold=True, color=text)
        cell.fill = PatternFill("solid", fgColor=fill)
        cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        cell.border = thin_border(NAVY)
    ws.row_dimensions[row].height = 28


def brand_cover(ws, title, subtitle):
    ws.sheet_view.showGridLines = False
    set_col_widths(ws, {get_column_letter(i): 14 for i in range(1, 14)})
    # magenta tag
    ws.cell(row=2, column=2, value="MORPH TRACKER")
    ws.cell(row=2, column=2).font = Font(name=FONT_NAME, size=9, bold=True, color=MAGENTA)
    # title
    ws.cell(row=3, column=2, value=title)
    ws.cell(row=3, column=2).font = Font(name=FONT_NAME, size=36, bold=True, color=NAVY)
    ws.row_dimensions[3].height = 54
    # subtitle
    ws.cell(row=5, column=2, value=subtitle)
    ws.cell(row=5, column=2).font = Font(name=FONT_NAME, size=14, italic=True, color=GREY_DARK)
    # magenta bar
    for col in range(2, 12):
        ws.cell(row=6, column=col).fill = PatternFill("solid", fgColor=MAGENTA)
    ws.row_dimensions[6].height = 4
    # summary card
    meta = [
        ("Version", "v0.1 — Visual mockup for review"),
        ("Owner", "Dean Latham"),
        ("Last updated", dt.date.today().strftime("%d %B %Y")),
        ("Status", "Draft — not wired; formulas illustrative only"),
        ("Purpose", "Replace 2026 CSV — align to Event Delivery Process — Amz dashboard"),
    ]
    for i, (k, v) in enumerate(meta):
        r = 9 + i
        ws.cell(row=r, column=2, value=k).font = Font(name=FONT_NAME, size=10, bold=True, color=NAVY)
        ws.cell(row=r, column=2).fill = PatternFill("solid", fgColor=LIGHT_BG)
        ws.cell(row=r, column=2).border = thin_border(LIGHT_BG)
        ws.cell(row=r, column=3, value=v).font = Font(name=FONT_NAME, size=10, color=NAVY)
        ws.cell(row=r, column=3).border = thin_border(LIGHT_BG)
        ws.merge_cells(start_row=r, end_row=r, start_column=3, end_column=10)
    # logo
    try:
        img = XLImage(LOGO)
        img.width, img.height = 180, 60
        ws.add_image(img, "J2")
    except Exception:
        pass


def stage_legend(ws, start_row, start_col=1):
    ws.cell(row=start_row, column=start_col, value="Stage colour key").font = Font(
        name=FONT_NAME, size=11, bold=True, color=NAVY
    )
    for i, s in enumerate(STAGES):
        r = start_row + 1 + i
        c = ws.cell(row=r, column=start_col, value=s)
        c.fill = PatternFill("solid", fgColor=STAGE_FILLS[s])
        c.font = Font(name=FONT_NAME, size=10, bold=True, color=STAGE_TEXT[s])
        c.border = thin_border(GREY)
        c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.row_dimensions[r].height = 20
        ws.merge_cells(start_row=r, end_row=r, start_column=start_col, end_column=start_col + 2)


def apply_stage_conditional(ws, col_letter, first_data_row, last_data_row):
    rng = f"{col_letter}{first_data_row}:{col_letter}{last_data_row}"
    for stage in STAGES:
        fill = PatternFill("solid", fgColor=STAGE_FILLS[stage])
        font = Font(name=FONT_NAME, bold=True, color=STAGE_TEXT[stage], size=10)
        rule = CellIsRule(operator="equal", formula=[f'"{stage}"'],
                          stopIfTrue=False, fill=fill, font=font)
        ws.conditional_formatting.add(rng, rule)


def apply_invoice_conditional(ws, col_letter, first, last):
    rng = f"{col_letter}{first}:{col_letter}{last}"
    palette = {"Booked": AMBER, "Invoiced": PURPLE, "Paid": GREEN}
    for v, fill_c in palette.items():
        rule = CellIsRule(operator="equal", formula=[f'"{v}"'],
                          stopIfTrue=False,
                          fill=PatternFill("solid", fgColor=fill_c),
                          font=Font(name=FONT_NAME, bold=True, color=WHITE, size=10))
        ws.conditional_formatting.add(rng, rule)


def apply_at_risk(ws, at_risk_col_letter, first, last, target_cols_to_row_highlight=None):
    """Rows where At Risk = Yes → red left border hint via fill on flag column."""
    rng = f"{at_risk_col_letter}{first}:{at_risk_col_letter}{last}"
    ws.conditional_formatting.add(
        rng,
        CellIsRule(operator="equal", formula=['"Yes"'], stopIfTrue=False,
                   fill=PatternFill("solid", fgColor=RED),
                   font=Font(name=FONT_NAME, bold=True, color=WHITE, size=10)),
    )


def grey_out_closed(ws, stage_col_letter, first, last, total_cols):
    """If Current Stage = '8. Closed' → grey + strikethrough the whole row."""
    row_range = f"A{first}:{get_column_letter(total_cols)}{last}"
    rule = FormulaRule(
        formula=[f'${stage_col_letter}{first}="8. Closed"'],
        stopIfTrue=False,
        font=Font(name=FONT_NAME, color=GREY_DARK, italic=True, strike=True, size=10),
        fill=PatternFill("solid", fgColor=LIGHT_BG),
    )
    ws.conditional_formatting.add(row_range, rule)


def add_list_validation(ws, col_letter, first, last, values):
    f = '"' + ",".join(values) + '"'
    dv = DataValidation(type="list", formula1=f, allow_blank=True, showDropDown=False)
    dv.add(f"{col_letter}{first}:{col_letter}{last}")
    ws.add_data_validation(dv)


# =========================================================================
# COMMERCIALS WORKBOOK
# =========================================================================
def build_commercials():
    wb = Workbook()
    # --- Cover
    cover = wb.active
    cover.title = "Cover"
    brand_cover(cover, "Sponsorship Commercials 2026",
                "Revenue, spend, margin & invoice tracking — Amz view")

    # --- Master
    ws = wb.create_sheet("Master")
    ws.sheet_view.showGridLines = False
    title_row(ws, 1, "Commercials — Master", "Auto-links to Delivery workbook via Item Ref", span=16)
    headers = [
        "Item Ref", "Sponsor", "Type", "Detail",
        "Revenue (ex.VAT)", "Delivery Spend", "Speaker Fee", "Venue Fee",
        "Total Cost", "Margin £", "Margin %",
        "Invoice Status", "Invoice Date", "PO / Contract Ref",
        "Current Stage (→Delivery)", "Target Live (→Delivery)",
    ]
    header_row(ws, 4, headers)
    first = 5
    for i, r in enumerate(ALL_ROWS):
        row = first + i
        rev = r.get("revenue", 0) or 0
        spend = r.get("spend", 0) or 0
        speaker = r.get("speaker_fee", 0) or 0
        venue = r.get("venue_fee", 0) or 0
        # default invoice status
        if r["stage"] == "8. Closed":
            inv = "Paid"
            inv_date = r.get("live", "")
        elif r["stage"] in ("6. Pre-Launch", "7. Live"):
            inv = "Invoiced"
            inv_date = ""
        else:
            inv = "Booked"
            inv_date = ""
        data = [
            r["ref"], r["sponsor"], r["type"], r["detail"],
            rev, spend, speaker, venue,
            f"=F{row}+G{row}+H{row}",
            f"=E{row}-I{row}",
            f'=IF(E{row}=0,"—",(E{row}-I{row})/E{row})',
            inv, inv_date, "",
            r["stage"], r.get("target_live", ""),
        ]
        for c, v in enumerate(data, start=1):
            cell = ws.cell(row=row, column=c, value=v)
            cell.font = Font(name=FONT_NAME, size=10, color=NAVY)
            cell.border = thin_border(GREY)
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            if c in (5, 6, 7, 8, 9, 10):
                cell.number_format = '£#,##0;[Red]-£#,##0;"—"'
            if c == 11:
                cell.number_format = '0.0%;[Red]-0.0%;"—"'
        # alt row shade
        if i % 2 == 1:
            for c in range(1, len(headers) + 1):
                if ws.cell(row=row, column=c).fill.fgColor.value in (None, "00000000"):
                    ws.cell(row=row, column=c).fill = PatternFill("solid", fgColor=TABLE_ALT)
    last = first + len(ALL_ROWS) - 1

    # column widths
    widths = {"A": 12, "B": 15, "C": 12, "D": 34, "E": 13, "F": 12, "G": 12, "H": 11,
              "I": 12, "J": 12, "K": 10, "L": 14, "M": 13, "N": 18, "O": 24, "P": 14}
    set_col_widths(ws, widths)

    # conditional formatting
    apply_stage_conditional(ws, "O", first, last)
    apply_invoice_conditional(ws, "L", first, last)
    grey_out_closed(ws, "O", first, last, total_cols=len(headers))

    # data validations
    add_list_validation(ws, "C", first, last, TYPES)
    add_list_validation(ws, "L", first, last, INVOICE_STATUSES)
    add_list_validation(ws, "O", first, last, STAGES)

    # Totals row
    trow = last + 2
    ws.cell(row=trow, column=1, value="TOTAL").font = Font(name=FONT_NAME, bold=True, color=WHITE)
    ws.cell(row=trow, column=1).fill = PatternFill("solid", fgColor=NAVY)
    for c in (5, 6, 7, 8, 9, 10):
        col = get_column_letter(c)
        cell = ws.cell(row=trow, column=c, value=f"=SUM({col}{first}:{col}{last})")
        cell.font = Font(name=FONT_NAME, bold=True, color=WHITE)
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.number_format = '£#,##0'
    ws.row_dimensions[trow].height = 22

    ws.freeze_panes = "C5"
    stage_legend(ws, trow + 3, 1)

    # --- Revenue by Sponsor
    rs = wb.create_sheet("Revenue by Sponsor")
    rs.sheet_view.showGridLines = False
    title_row(rs, 1, "Revenue by Sponsor", "Booked / Delivered / Outstanding — 2026", span=6)
    header_row(rs, 4, ["Sponsor", "Items", "Revenue Booked", "Delivered (Closed)", "Outstanding", "% Delivered"])
    sponsors = sorted({r["sponsor"] for r in ALL_ROWS})
    for i, sp in enumerate(sponsors):
        r = 5 + i
        items = [x for x in ALL_ROWS if x["sponsor"] == sp]
        booked = sum(x["revenue"] for x in items)
        delivered = sum(x["revenue"] for x in items if x["stage"] == "8. Closed")
        outstanding = booked - delivered
        pct = delivered / booked if booked else 0
        for c, v in enumerate([sp, len(items), booked, delivered, outstanding, pct], start=1):
            cell = rs.cell(row=r, column=c, value=v)
            cell.font = Font(name=FONT_NAME, size=10, color=NAVY)
            cell.border = thin_border(GREY)
            if c in (3, 4, 5):
                cell.number_format = '£#,##0'
            if c == 6:
                cell.number_format = '0.0%'
    # totals
    tr = 5 + len(sponsors)
    rs.cell(row=tr, column=1, value="TOTAL").font = Font(name=FONT_NAME, bold=True, color=WHITE)
    rs.cell(row=tr, column=1).fill = PatternFill("solid", fgColor=NAVY)
    for c in (2, 3, 4, 5):
        col = get_column_letter(c)
        cell = rs.cell(row=tr, column=c, value=f"=SUM({col}5:{col}{tr - 1})")
        cell.font = Font(name=FONT_NAME, bold=True, color=WHITE)
        cell.fill = PatternFill("solid", fgColor=NAVY)
        if c in (3, 4, 5):
            cell.number_format = '£#,##0'
    set_col_widths(rs, {"A": 22, "B": 8, "C": 18, "D": 18, "E": 16, "F": 14})

    # Chart — Revenue by Sponsor
    chart = BarChart()
    chart.type = "bar"
    chart.style = 10
    chart.title = "Revenue — Booked vs Delivered"
    chart.y_axis.title = None
    chart.x_axis.title = "£ GBP"
    data_ref = Reference(rs, min_col=3, max_col=4, min_row=4, max_row=4 + len(sponsors))
    cats = Reference(rs, min_col=1, min_row=5, max_row=4 + len(sponsors))
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats)
    chart.height = 10
    chart.width = 18
    rs.add_chart(chart, "H4")

    # --- Margin by Type
    mg = wb.create_sheet("Margin by Type")
    mg.sheet_view.showGridLines = False
    title_row(mg, 1, "Margin by Item Type", "Revenue vs cost — profitability view", span=5)
    header_row(mg, 4, ["Type", "Items", "Revenue", "Total Cost", "Margin £"])
    types_seen = sorted({r["type"] for r in ALL_ROWS})
    for i, t in enumerate(types_seen):
        r = 5 + i
        items = [x for x in ALL_ROWS if x["type"] == t]
        rev = sum(x["revenue"] for x in items)
        cost = sum((x.get("spend", 0) + x.get("speaker_fee", 0) + x.get("venue_fee", 0)) for x in items)
        for c, v in enumerate([t, len(items), rev, cost, rev - cost], start=1):
            cell = mg.cell(row=r, column=c, value=v)
            cell.font = Font(name=FONT_NAME, size=10, color=NAVY)
            cell.border = thin_border(GREY)
            if c in (3, 4, 5):
                cell.number_format = '£#,##0'
    set_col_widths(mg, {"A": 24, "B": 8, "C": 14, "D": 14, "E": 14})

    # --- Invoice Status
    inv = wb.create_sheet("Invoice Status")
    inv.sheet_view.showGridLines = False
    title_row(inv, 1, "Invoice Status", "Aged outstanding — drives cash flow conversation with Amz", span=6)
    header_row(inv, 4, ["Status", "Items", "Revenue Value", "% of Total"])
    total_rev = sum(r["revenue"] for r in ALL_ROWS)
    status_map = {"Booked": [], "Invoiced": [], "Paid": []}
    for r in ALL_ROWS:
        if r["stage"] == "8. Closed":
            status_map["Paid"].append(r)
        elif r["stage"] in ("6. Pre-Launch", "7. Live"):
            status_map["Invoiced"].append(r)
        else:
            status_map["Booked"].append(r)
    for i, (s, items) in enumerate(status_map.items()):
        r = 5 + i
        val = sum(x["revenue"] for x in items)
        for c, v in enumerate([s, len(items), val, (val / total_rev if total_rev else 0)], start=1):
            cell = inv.cell(row=r, column=c, value=v)
            cell.font = Font(name=FONT_NAME, size=10, color=NAVY)
            cell.border = thin_border(GREY)
            if c == 3:
                cell.number_format = '£#,##0'
            if c == 4:
                cell.number_format = '0.0%'
    apply_invoice_conditional(inv, "A", 5, 7)
    set_col_widths(inv, {"A": 16, "B": 8, "C": 16, "D": 12})

    # pie chart
    chart = PieChart()
    chart.title = "Revenue by Invoice Status"
    data_ref = Reference(inv, min_col=3, min_row=5, max_row=7)
    cats = Reference(inv, min_col=1, min_row=5, max_row=7)
    chart.add_data(data_ref)
    chart.set_categories(cats)
    chart.height = 9
    chart.width = 13
    chart.dataLabels = DataLabelList(showPercent=True)
    inv.add_chart(chart, "F4")

    for sheet_name in ("Master", "Revenue by Sponsor", "Margin by Type", "Invoice Status"):
        landscape_fit(wb[sheet_name])
    out = OUT / "sponsorship-commercials-2026.xlsx"
    wb.save(out)
    print(f"Saved: {out}")
    return out


# =========================================================================
# DELIVERY WORKBOOK
# =========================================================================
def build_delivery():
    wb = Workbook()
    cover = wb.active
    cover.title = "Cover"
    brand_cover(cover, "Sponsorship Delivery 2026",
                "Stage, lead, dates & event readiness — team view")

    # --- Master
    ws = wb.create_sheet("Master")
    ws.sheet_view.showGridLines = False
    title_row(ws, 1, "Delivery — Master",
              "Current stage, owner & dates for every sponsored item", span=18)
    headers = [
        "Item Ref", "Sponsor", "Type", "Detail Requirements",
        "Project Lead", "Current Stage",
        "Brief Agreed", "Draft Sent", "Sponsor Approved", "Iqera Status",
        "Target Live Date", "Live on Website",
        "Days in Stage", "At Risk",
        "Pooja Updates", "Iqera Updates",
    ]
    header_row(ws, 4, headers)
    first = 5
    for i, r in enumerate(ALL_ROWS):
        row = first + i
        # crude At Risk: overdue target OR 60+ days in regulatory gate w/ no live date
        at_risk = "Yes" if (r["stage"] in ("5. Regulatory Gate", "4. Sponsor Review")
                            and r["target_live"] and not r.get("live")) else "No"
        days_in_stage = 45 if at_risk == "Yes" else 12  # illustrative
        if r["stage"] == "8. Closed":
            days_in_stage = 0
            at_risk = "No"
        data = [
            r["ref"], r["sponsor"], r["type"], r["detail"],
            r["lead"], r["stage"],
            r.get("brief", ""), r.get("draft", ""),
            r.get("approved", ""), r.get("iqera", ""),
            r.get("target_live", ""), r.get("live", ""),
            days_in_stage, at_risk,
            r.get("pooja", ""), r.get("iqera_updates", r.get("iqera", "")),
        ]
        for c, v in enumerate(data, start=1):
            cell = ws.cell(row=row, column=c, value=v)
            cell.font = Font(name=FONT_NAME, size=10, color=NAVY)
            cell.border = thin_border(GREY)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
        if i % 2 == 1:
            for c in range(1, len(headers) + 1):
                if ws.cell(row=row, column=c).fill.fgColor.value in (None, "00000000"):
                    ws.cell(row=row, column=c).fill = PatternFill("solid", fgColor=TABLE_ALT)
        ws.row_dimensions[row].height = 48
    last = first + len(ALL_ROWS) - 1

    widths = {"A": 11, "B": 14, "C": 12, "D": 30, "E": 11, "F": 22,
              "G": 12, "H": 12, "I": 14, "J": 20, "K": 14, "L": 14,
              "M": 11, "N": 9, "O": 40, "P": 28}
    set_col_widths(ws, widths)

    apply_stage_conditional(ws, "F", first, last)
    apply_at_risk(ws, "N", first, last)
    grey_out_closed(ws, "F", first, last, total_cols=len(headers))

    add_list_validation(ws, "C", first, last, TYPES)
    add_list_validation(ws, "E", first, last, LEADS)
    add_list_validation(ws, "F", first, last, STAGES)
    add_list_validation(ws, "N", first, last, ["Yes", "No"])

    ws.freeze_panes = "C5"
    stage_legend(ws, last + 3, 1)

    # --- Stage Pipeline
    sp = wb.create_sheet("Stage Pipeline")
    sp.sheet_view.showGridLines = False
    title_row(sp, 1, "Stage Pipeline", "How many items sit at each stage", span=3)
    header_row(sp, 4, ["Stage", "Items", "Total Revenue"])
    for i, s in enumerate(STAGES):
        r = 5 + i
        items = [x for x in ALL_ROWS if x["stage"] == s]
        rev = sum(x["revenue"] for x in items)
        vals = [s, len(items), rev]
        for c, v in enumerate(vals, start=1):
            cell = sp.cell(row=r, column=c, value=v)
            cell.font = Font(name=FONT_NAME, size=10, color=NAVY)
            cell.border = thin_border(GREY)
            if c == 3:
                cell.number_format = '£#,##0'
        sp.cell(row=r, column=1).fill = PatternFill("solid", fgColor=STAGE_FILLS[s])
        sp.cell(row=r, column=1).font = Font(name=FONT_NAME, size=10, bold=True,
                                             color=STAGE_TEXT[s])
    set_col_widths(sp, {"A": 26, "B": 8, "C": 16})

    chart = BarChart()
    chart.type = "bar"
    chart.style = 10
    chart.title = "Item count by stage"
    data_ref = Reference(sp, min_col=2, max_col=2, min_row=4, max_row=4 + len(STAGES))
    cats = Reference(sp, min_col=1, min_row=5, max_row=4 + len(STAGES))
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats)
    chart.height = 12
    chart.width = 18
    sp.add_chart(chart, "E4")

    # --- At Risk & Overdue
    ar = wb.create_sheet("At Risk & Overdue")
    ar.sheet_view.showGridLines = False
    title_row(ar, 1, "At Risk & Overdue", "Exception view — only flagged items", span=7)
    header_row(ar, 4, ["Item Ref", "Sponsor", "Type", "Current Stage",
                       "Target Live", "Days in Stage", "Reason"])
    risky = [(i, r) for i, r in enumerate(ALL_ROWS)
             if r["stage"] in ("4. Sponsor Review", "5. Regulatory Gate")
             and r.get("target_live") and not r.get("live")]
    for j, (i, r) in enumerate(risky):
        row = 5 + j
        reason = {
            "4. Sponsor Review": "Awaiting sponsor sign-off — chase weekly",
            "5. Regulatory Gate": "With Iqera / regulatory — track clearance",
        }[r["stage"]]
        vals = [r["ref"], r["sponsor"], r["type"], r["stage"],
                r["target_live"], 45, reason]
        for c, v in enumerate(vals, start=1):
            cell = ar.cell(row=row, column=c, value=v)
            cell.font = Font(name=FONT_NAME, size=10, color=NAVY)
            cell.border = thin_border(GREY)
        ar.cell(row=row, column=4).fill = PatternFill("solid", fgColor=STAGE_FILLS[r["stage"]])
        ar.cell(row=row, column=4).font = Font(name=FONT_NAME, size=10, bold=True,
                                                color=STAGE_TEXT[r["stage"]])
        ar.cell(row=row, column=6).fill = PatternFill("solid", fgColor=RED)
        ar.cell(row=row, column=6).font = Font(name=FONT_NAME, size=10, bold=True, color=WHITE)
    set_col_widths(ar, {"A": 11, "B": 14, "C": 12, "D": 22, "E": 14, "F": 14, "G": 40})

    # --- Calendar view
    cal = wb.create_sheet("Calendar 2026")
    cal.sheet_view.showGridLines = False
    title_row(cal, 1, "2026 Delivery Calendar",
              "Auto-populated from Target Live Date — new rows appear here automatically",
              span=14)
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    # headers: Month, then up to 12 item slots
    cal_headers = ["Month"] + [f"Item {i}" for i in range(1, 13)]
    header_row(cal, 4, cal_headers)
    for i, m in enumerate(months):
        row = 5 + i
        cal.cell(row=row, column=1, value=m).font = Font(name=FONT_NAME, size=11, bold=True, color=WHITE)
        cal.cell(row=row, column=1).fill = PatternFill("solid", fgColor=NAVY)
        cal.cell(row=row, column=1).alignment = Alignment(horizontal="left", vertical="center", indent=1)
        items = [r for r in ALL_ROWS if r.get("month", "").split(" (")[0] == m]
        for j, r in enumerate(items):
            if j >= 12:
                break
            cell = cal.cell(row=row, column=2 + j,
                            value=f"{r['ref']}\n{r['sponsor']} — {r['type']}")
            cell.font = Font(name=FONT_NAME, size=9,
                             color=STAGE_TEXT[r["stage"]], bold=True)
            cell.fill = PatternFill("solid", fgColor=STAGE_FILLS[r["stage"]])
            cell.border = thin_border(GREY)
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        cal.row_dimensions[row].height = 40
    set_col_widths(cal, {"A": 14, **{get_column_letter(i): 18 for i in range(2, 14)}})
    stage_legend(cal, 19, 1)

    # --- Event Readiness
    er = wb.create_sheet("Event Readiness")
    er.sheet_view.showGridLines = False
    title_row(er, 1, "Event Readiness",
              "Pre-event checklist — red until confirmed. Ties to Event Process Stage 6.",
              span=9)
    hdr = ["Item Ref", "Sponsor / Event", "Target Date", "Venue", "Speaker",
           "72hr Check-ins", "Dietary Captured", "Morning-of Contact", "Overall"]
    header_row(er, 4, hdr)
    events = [r for r in ALL_ROWS if r["type"] == "Event"]
    if not events:
        er.cell(row=5, column=1,
                value="No events in current list — add Events to Master and they will appear here.")
        er.cell(row=5, column=1).font = Font(name=FONT_NAME, italic=True, color=GREY_DARK)
        er.merge_cells(start_row=5, end_row=5, start_column=1, end_column=9)
    for i, r in enumerate(events):
        row = 5 + i
        v = r.get("venue", "")
        sp_conf = r.get("speaker_confirmed", "No")
        c72 = r.get("check72", "No")
        diet = r.get("dietary_captured", "No")
        morning = r.get("morning_contact", "No")
        overall = "Ready" if all(x == "Yes" for x in [bool(v), sp_conf == "Yes",
                                                      c72 == "Yes", diet == "Yes",
                                                      morning == "Yes"]) else "Not Ready"
        vals = [r["ref"], f'{r["sponsor"]} — {r["detail"]}',
                r.get("target_live", ""), v or "—",
                sp_conf, c72, diet, morning, overall]
        for c, val in enumerate(vals, start=1):
            cell = er.cell(row=row, column=c, value=val)
            cell.font = Font(name=FONT_NAME, size=10, color=NAVY)
            cell.border = thin_border(GREY)
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            if c in (5, 6, 7, 8):
                if val == "Yes":
                    cell.fill = PatternFill("solid", fgColor=GREEN)
                    cell.font = Font(name=FONT_NAME, size=10, bold=True, color=WHITE)
                elif val == "No":
                    cell.fill = PatternFill("solid", fgColor=RED)
                    cell.font = Font(name=FONT_NAME, size=10, bold=True, color=WHITE)
                else:
                    cell.fill = PatternFill("solid", fgColor=GREY)
                    cell.font = Font(name=FONT_NAME, size=10, bold=True, color=WHITE)
            if c == 9:
                colour = GREEN if val == "Ready" else AMBER
                cell.fill = PatternFill("solid", fgColor=colour)
                cell.font = Font(name=FONT_NAME, size=10, bold=True, color=WHITE)
        er.row_dimensions[row].height = 30
    set_col_widths(er, {"A": 12, "B": 32, "C": 14, "D": 22, "E": 14, "F": 16,
                        "G": 16, "H": 18, "I": 12})

    # Callout box about dietary
    crow = 5 + max(len(events), 1) + 2
    er.cell(row=crow, column=1,
            value="DIETARY CAPTURE — NON-NEGOTIABLE").font = Font(
        name=FONT_NAME, size=10, bold=True, color=NAVY)
    er.cell(row=crow, column=1).fill = PatternFill("solid", fgColor=LIGHT_BG)
    er.merge_cells(start_row=crow, end_row=crow, start_column=1, end_column=9)
    er.cell(row=crow + 1, column=1,
            value=("Dietary requirements must be captured for every delegate before event day. "
                   "Red flag persists until Dietary Captured = Yes. Ties to Event Delivery "
                   "Process Stage 6 — Pre-Event Preparation.")).font = Font(
        name=FONT_NAME, size=10, color=NAVY, italic=True)
    er.cell(row=crow + 1, column=1).fill = PatternFill("solid", fgColor=LIGHT_BG)
    er.cell(row=crow + 1, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    er.merge_cells(start_row=crow + 1, end_row=crow + 1, start_column=1, end_column=9)
    er.row_dimensions[crow + 1].height = 40

    for sheet_name in ("Master", "Stage Pipeline", "At Risk & Overdue",
                       "Calendar 2026", "Event Readiness"):
        landscape_fit(wb[sheet_name])
    out = OUT / "sponsorship-delivery-2026.xlsx"
    wb.save(out)
    print(f"Saved: {out}")
    return out


if __name__ == "__main__":
    c = build_commercials()
    d = build_delivery()
    print("Done.")
    print(f"  Commercials: {c}")
    print(f"  Delivery:    {d}")
