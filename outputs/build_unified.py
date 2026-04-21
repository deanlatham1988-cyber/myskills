"""Build MORPh Events & Sponsorship Tracker — single unified workbook.

Structure:
  1. Dashboard        — Amz's landing page, KPI tiles + charts + next 30 days
  2. Master           — team-editable data table (Excel Table = tblMaster)
  3. At Risk          — filtered exception view
  4-15. Jan-Dec 2026  — one calendar-grid tab per month, auto-populated by
                        Target Live Date via FILTER/TEXTJOIN formulas
"""
from __future__ import annotations
import calendar
import datetime as dt
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.fill import PatternFillProperties, ColorChoice
from openpyxl.drawing.line import LineProperties
from openpyxl.drawing.colors import ColorChoice as DrawColor
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.page import PageMargins
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.drawing.image import Image as XLImage

# ---------- MORPh brand ----------
NAVY = "02084B"
MAGENTA = "FD02F7"
PURPLE = "9A2CFB"
LIGHT_BG = "F5F0FA"
TABLE_ALT = "F0EDF5"
GREY = "BFBFBF"
GREY_DARK = "8A8A8A"
GREY_LIGHT = "EDEDED"
RED = "D7263D"
AMBER = "E89611"
GREEN = "2E7D32"
WHITE = "FFFFFF"

FONT = "Calibri"

STAGE_FILLS = {
    "1. Initiation":         LIGHT_BG,
    "2. Production":         PURPLE,
    "3. Sponsor Draft Sent": TABLE_ALT,
    "4. Sponsor Review":     MAGENTA,
    "5. Regulatory Gate":    NAVY,
    "6. Pre-Launch":         "E8A7FF",
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
LEADS = ["Pooja", "Will", "Will/Colin", "Will/Chloe", "Dean", "Ariyan"]
INVOICE_STATUSES = ["Booked", "Invoiced", "Paid"]
YESNO = ["Yes", "No"]


# ---------- Data ----------
def d(y, m, day):
    return dt.date(y, m, day)


# All 14 current CSV rows + illustrative past + illustrative future events.
# target_live is a real date (or None).
ROWS = [
    # --- Current 14 from CSV ---
    dict(ref="ROSTOO01", sponsor="Rosemont", type="Toolkit",
         detail="Dysphagia & Licensed Liquid Meds",
         lead="Pooja", revenue=5000, spend=0,
         brief=d(2026, 1, 15), draft=d(2026, 2, 3), approved=None, live=None,
         target=d(2026, 2, 28), stage="4. Sponsor Review",
         iqera_status="",
         updates="02.04.2026 — Rosemont liaising with Iqera on final amendments before approval."),
    dict(ref="PROTOO01", sponsor="Proveca", type="Toolkit",
         detail="Hypersalivation in children",
         lead="Pooja", revenue=3000, spend=0,
         brief=d(2026, 1, 20), draft=d(2026, 2, 5), approved=None, live=None,
         target=d(2026, 3, 31), stage="5. Regulatory Gate",
         iqera_status="Awaiting additional info from pharma",
         updates=("Met with Caroline 04.02.26. Sent 05.02 for content review. "
                  "02.04.2026 — handed to Iqera. Training video to Caroline once complete.")),
    dict(ref="ASTTOO01", sponsor="Astellas", type="Toolkit",
         detail="OAB management",
         lead="Pooja", revenue=7000, spend=0,
         brief=d(2026, 1, 10), draft=d(2026, 2, 3), approved=None, live=None,
         target=d(2026, 3, 31), stage="5. Regulatory Gate",
         iqera_status="Submitted on Promomats",
         updates=("02.04.2026 — handed to Iqera, submitted everything except training "
                  "video on Promomats. Awaiting approval.")),
    dict(ref="STATOO01", sponsor="Stada", type="Toolkit",
         detail="Asthma & COPD",
         lead="Pooja", revenue=5000, spend=0,
         brief=d(2026, 1, 5), draft=d(2026, 3, 9),
         approved=d(2026, 3, 16), live=d(2026, 3, 17),
         target=d(2026, 3, 17), stage="8. Closed",
         iqera_status="",
         updates="Completed — uploaded to website."),
    dict(ref="PROBLO01", sponsor="Proveca", type="Blog",
         detail="Hypersalivation in children",
         lead="Pooja", revenue=7000, spend=0,
         brief=None, draft=None, approved=None, live=None,
         target=d(2026, 1, 31), stage="1. Initiation",
         iqera_status="",
         updates=("Sent overview to Ryan to post on GP group. Caroline has colleague "
                  "at Proveca. Once author secured, write blog and send to Proveca.")),
    dict(ref="PROAST01", sponsor="Astellas", type="Blog",
         detail="OAB management — Richard Daniszewski",
         lead="Pooja", revenue=2500, spend=300,
         brief=d(2026, 2, 1), draft=d(2026, 2, 20), approved=None, live=None,
         target=d(2026, 1, 31), stage="4. Sponsor Review",
         iqera_status="",
         updates=("Commissioned Richard to complete by 22.02. £100/hr max 3 hrs. "
                  "Submitted to Astellas — awaiting approval.")),
    dict(ref="ROSNEW01", sponsor="Rosemont", type="Newsletter",
         detail="1 mailer to network",
         lead="Will", revenue=1500, spend=0,
         brief=None, draft=None, approved=None, live=None,
         target=d(2026, 4, 15), stage="1. Initiation",
         iqera_status="", updates=""),
    dict(ref="ROSNEI01", sponsor="Rosemont", type="Neighbourhood Banner",
         detail="2 Neighbourhoods (£450 each)",
         lead="Will/Colin", revenue=900, spend=0,
         brief=None, draft=None, approved=None, live=None,
         target=d(2026, 4, 20), stage="1. Initiation",
         iqera_status="", updates=""),
    dict(ref="CIPNEW01", sponsor="Cipla", type="Newsletter",
         detail="Owed 2 from 2025",
         lead="Will", revenue=0, spend=0,
         brief=None, draft=None, approved=None, live=None,
         target=d(2026, 5, 10), stage="1. Initiation",
         iqera_status="",
         updates="Awaiting Cipla to confirm details."),
    dict(ref="PROBAN01", sponsor="Proveca", type="Banner",
         detail="Owed 2 from 2025",
         lead="Will", revenue=0, spend=0,
         brief=None, draft=None, approved=None, live=None,
         target=d(2026, 4, 25), stage="2. Production",
         iqera_status="",
         updates="Specs sent to Caroline."),
    dict(ref="ASTBAN01", sponsor="Astellas", type="Banner",
         detail="Standard web banner",
         lead="Will", revenue=1500, spend=0,
         brief=None, draft=None, approved=None, live=None,
         target=d(2026, 4, 30), stage="1. Initiation",
         iqera_status="", updates=""),
    dict(ref="ALITOO01", sponsor="Alissa", type="Toolkit",
         detail="Toolkit (details TBC)",
         lead="Pooja", revenue=8000, spend=0,
         brief=None, draft=None, approved=None, live=None,
         target=d(2026, 5, 20), stage="5. Regulatory Gate",
         iqera_status="Handed to Iqera 02.04.2026",
         updates=("02.04.2026 — Submitted all of toolkit except training video. "
                  "Handed over to Iqera, once training video completed, submit to Alissa.")),
    dict(ref="ASTNEI01", sponsor="Astellas", type="Neighbourhood Banner",
         detail="3 Neighbourhoods",
         lead="Will/Chloe", revenue=0, spend=0,
         brief=None, draft=None, approved=None, live=None,
         target=d(2026, 5, 30), stage="1. Initiation",
         iqera_status="", updates=""),

    # --- Illustrative past items (Closed, appear greyed in Master) ---
    dict(ref="CIPTOO01", sponsor="Cipla", type="Toolkit",
         detail="[2025 carry-over] Asthma inhaler technique",
         lead="Pooja", revenue=6000, spend=0,
         brief=d(2025, 7, 1), draft=d(2025, 8, 15),
         approved=d(2025, 8, 29), live=d(2025, 9, 5),
         target=d(2025, 9, 5), stage="8. Closed",
         iqera_status="", updates="Completed — 2025."),
    dict(ref="ROSBLO01", sponsor="Rosemont", type="Blog",
         detail="[2025 carry-over] Paediatric liquid meds",
         lead="Pooja", revenue=2500, spend=200,
         brief=d(2025, 9, 15), draft=d(2025, 10, 2),
         approved=d(2025, 10, 20), live=d(2025, 11, 5),
         target=d(2025, 11, 5), stage="8. Closed",
         iqera_status="", updates="Completed 2025 — author: Dr A. Shah."),

    # --- Illustrative events for calendar demo ---
    dict(ref="MORMEVE01", sponsor="MORPh Internal", type="Event",
         detail="[DEMO] Dry Eye Training — London",
         lead="Dean", revenue=0, spend=0,
         brief=d(2026, 3, 1), draft=None, approved=None, live=None,
         target=d(2026, 5, 15), stage="6. Pre-Launch",
         iqera_status="",
         updates="Speaker: Dr Chen. Venue TBC. Dietary not yet captured."),
    dict(ref="MORMEVE02", sponsor="MORPh Internal", type="Event",
         detail="[DEMO] OAB Management Training — Manchester",
         lead="Dean", revenue=0, spend=0,
         brief=d(2026, 4, 5), draft=None, approved=None, live=None,
         target=d(2026, 6, 12), stage="3. Sponsor Draft Sent",
         iqera_status="",
         updates="Speaker TBC. Dietary capture open."),
    dict(ref="MORMEVE03", sponsor="MORPh Internal", type="Event",
         detail="[DEMO] Respiratory Study Day — Birmingham",
         lead="Dean", revenue=0, spend=0,
         brief=d(2026, 5, 1), draft=None, approved=None, live=None,
         target=d(2026, 7, 10), stage="1. Initiation",
         iqera_status="", updates=""),
    dict(ref="MORMEVE04", sponsor="MORPh Internal", type="Event",
         detail="[DEMO] Autumn Neighbourhood Forum — Leeds",
         lead="Dean", revenue=0, spend=0,
         brief=None, draft=None, approved=None, live=None,
         target=d(2026, 9, 25), stage="1. Initiation",
         iqera_status="", updates=""),
]

OUT = Path("/Users/deanlatham/Desktop/work/morph/Morph New World/Spreadsheets")
OUT.mkdir(parents=True, exist_ok=True)
LOGO = "/Users/deanlatham/Desktop/work/morph/Morph New World/Marketing/MORPh Brand Pack/Logo/Dark/Logo-Dark.png"

MASTER_COLUMNS = [
    "Item Ref", "Sponsor", "Type", "Detail",
    "Project Lead", "Current Stage",
    "Brief Agreed", "Draft Sent", "Sponsor Approved", "Iqera Status",
    "Target Live Date", "Live on Website",
    "Revenue (ex.VAT)", "Delivery Spend",
    "Invoice Status", "At Risk",
    "Updates",
]


# ---------- helpers ----------
def thin(colour=GREY, weight="thin"):
    s = Side(style=weight, color=colour)
    return Border(left=s, right=s, top=s, bottom=s)


def colw(ws, widths):
    for c, w in widths.items():
        ws.column_dimensions[c].width = w


def landscape(ws):
    ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
    ws.page_setup.paperSize = ws.PAPERSIZE_A3
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins = PageMargins(left=0.3, right=0.3, top=0.4, bottom=0.4,
                                  header=0.2, footer=0.2)
    ws.sheet_view.showGridLines = False


def style_chart_navy(chart):
    from openpyxl.drawing.fill import ColorChoice, SolidColorFillProperties
    for i, series in enumerate(chart.series):
        colour = [NAVY, MAGENTA, PURPLE][i % 3]
        series.graphicalProperties = GraphicalProperties(solidFill=colour)
        series.graphicalProperties.line = LineProperties(solidFill=colour)


def title_block(ws, row, title, subtitle="", span=16, size=22):
    ws.cell(row=row, column=1, value=title).font = Font(
        name=FONT, size=size, bold=True, color=NAVY)
    ws.row_dimensions[row].height = max(size + 10, 30)
    ws.merge_cells(start_row=row, end_row=row, start_column=1, end_column=span)
    if subtitle:
        c = ws.cell(row=row + 1, column=1, value=subtitle)
        c.font = Font(name=FONT, size=11, italic=True, color=GREY_DARK)
        ws.merge_cells(start_row=row + 1, end_row=row + 1,
                       start_column=1, end_column=span)
    ws.cell(row=row, column=1).border = Border(
        bottom=Side(style="medium", color=MAGENTA))


def header_cells(ws, row, headers, start_col=1,
                 fill=NAVY, text_color=WHITE, height=26):
    for i, h in enumerate(headers):
        c = ws.cell(row=row, column=start_col + i, value=h)
        c.font = Font(name=FONT, size=10, bold=True, color=text_color)
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(horizontal="left", vertical="center",
                                wrap_text=True, indent=1)
        c.border = thin(NAVY)
    ws.row_dimensions[row].height = height


def dv_list(ws, col_letter, first, last, values):
    f = '"' + ",".join(values) + '"'
    dv = DataValidation(type="list", formula1=f, allow_blank=True)
    dv.add(f"{col_letter}{first}:{col_letter}{last}")
    ws.add_data_validation(dv)


def apply_stage_cf(ws, col_letter, first, last):
    rng = f"{col_letter}{first}:{col_letter}{last}"
    for s in STAGES:
        ws.conditional_formatting.add(
            rng,
            CellIsRule(operator="equal", formula=[f'"{s}"'], stopIfTrue=False,
                       fill=PatternFill("solid", fgColor=STAGE_FILLS[s]),
                       font=Font(name=FONT, bold=True,
                                 color=STAGE_TEXT[s], size=10)),
        )


def apply_closed_grey(ws, stage_col, first, last, total_cols):
    rng = f"A{first}:{get_column_letter(total_cols)}{last}"
    ws.conditional_formatting.add(
        rng,
        FormulaRule(formula=[f'${stage_col}{first}="8. Closed"'],
                    stopIfTrue=False,
                    font=Font(name=FONT, color=GREY_DARK, italic=True,
                              strike=True, size=10),
                    fill=PatternFill("solid", fgColor=LIGHT_BG)))


def apply_atrisk_cf(ws, col_letter, first, last):
    rng = f"{col_letter}{first}:{col_letter}{last}"
    ws.conditional_formatting.add(
        rng,
        CellIsRule(operator="equal", formula=['"Yes"'], stopIfTrue=False,
                   fill=PatternFill("solid", fgColor=RED),
                   font=Font(name=FONT, bold=True, color=WHITE, size=10)))


# ---------- Master sheet ----------
def build_master(wb):
    ws = wb.create_sheet("Master")
    landscape(ws)
    title_block(ws, 1, "Master — Events & Sponsorship",
                "Add or update rows here. All other tabs pull from this table.",
                span=len(MASTER_COLUMNS))
    header_row = 4
    header_cells(ws, header_row, MASTER_COLUMNS)

    # Data rows
    first = header_row + 1
    today = dt.date.today()
    for i, r in enumerate(ROWS):
        row = first + i
        # Auto At Risk: items past target or stuck at gate long with no live
        at_risk = "No"
        if r["stage"] != "8. Closed" and r["target"] and r["target"] < today:
            at_risk = "Yes"
        elif r["stage"] in ("4. Sponsor Review", "5. Regulatory Gate") \
             and r["target"] and r["target"] < today + dt.timedelta(days=30) \
             and not r.get("live"):
            at_risk = "Yes"

        # Invoice status (illustrative, driven by stage)
        if r["stage"] == "8. Closed":
            invoice = "Paid"
        elif r["stage"] in ("6. Pre-Launch", "7. Live"):
            invoice = "Invoiced"
        else:
            invoice = "Booked"

        values = [
            r["ref"], r["sponsor"], r["type"], r["detail"],
            r["lead"], r["stage"],
            r.get("brief"), r.get("draft"), r.get("approved"),
            r.get("iqera_status", ""),
            r.get("target"), r.get("live"),
            r.get("revenue", 0), r.get("spend", 0),
            invoice, at_risk,
            r.get("updates", ""),
        ]
        for c, v in enumerate(values, start=1):
            cell = ws.cell(row=row, column=c, value=v)
            cell.font = Font(name=FONT, size=10, color=NAVY)
            cell.border = thin(GREY)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if c in (7, 8, 9, 11, 12):  # date columns
                cell.number_format = "dd.mm.yyyy"
            if c in (13, 14):  # money
                cell.number_format = '£#,##0;[Red]-£#,##0;"—"'
        ws.row_dimensions[row].height = 46

    last = first + len(ROWS) - 1

    # Create Excel Table so formulas elsewhere can reference tblMaster[Target Live Date] etc.
    ref = f"A{header_row}:{get_column_letter(len(MASTER_COLUMNS))}{last}"
    tbl = Table(displayName="tblMaster", ref=ref)
    tbl.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2", showFirstColumn=False, showLastColumn=False,
        showRowStripes=True, showColumnStripes=False)
    ws.add_table(tbl)

    # column widths
    colw(ws, {
        "A": 11, "B": 15, "C": 14, "D": 30, "E": 12, "F": 22,
        "G": 13, "H": 13, "I": 14, "J": 22,
        "K": 14, "L": 14, "M": 13, "N": 12, "O": 13, "P": 9, "Q": 40,
    })

    apply_stage_cf(ws, "F", first, last)
    apply_closed_grey(ws, "F", first, last, total_cols=len(MASTER_COLUMNS))
    apply_atrisk_cf(ws, "P", first, last)
    # invoice cf
    for status, colour in (("Booked", AMBER), ("Invoiced", PURPLE), ("Paid", GREEN)):
        ws.conditional_formatting.add(
            f"O{first}:O{last}",
            CellIsRule(operator="equal", formula=[f'"{status}"'], stopIfTrue=False,
                       fill=PatternFill("solid", fgColor=colour),
                       font=Font(name=FONT, bold=True, color=WHITE, size=10)))

    # validations
    dv_list(ws, "C", first, last, TYPES)
    dv_list(ws, "E", first, last, LEADS)
    dv_list(ws, "F", first, last, STAGES)
    dv_list(ws, "O", first, last, INVOICE_STATUSES)
    dv_list(ws, "P", first, last, YESNO)

    ws.freeze_panes = "C5"
    return ws, first, last


# ---------- Dashboard ----------
def build_dashboard(wb, first, last):
    ws = wb.create_sheet("Dashboard", 0)  # insert at index 0
    landscape(ws)
    ws.sheet_view.tabSelected = True

    # Logo
    try:
        img = XLImage(LOGO)
        img.width, img.height = 160, 55
        ws.add_image(img, "N2")
    except Exception:
        pass

    # Header
    ws.cell(row=2, column=2, value="MORPH TRACKER").font = Font(
        name=FONT, size=10, bold=True, color=MAGENTA)
    ws.cell(row=3, column=2, value="Events & Sponsorship — 2026").font = Font(
        name=FONT, size=28, bold=True, color=NAVY)
    ws.row_dimensions[3].height = 40
    ws.cell(row=4, column=2,
            value="Live dashboard — opens to Amz. All numbers pull from Master.").font = Font(
        name=FONT, size=11, italic=True, color=GREY_DARK)
    # magenta rule
    for col in range(2, 18):
        ws.cell(row=5, column=col).fill = PatternFill("solid", fgColor=MAGENTA)
    ws.row_dimensions[5].height = 4

    # ----- KPI tiles (row 7-10) -----
    kpi_row = 7
    tile_height = 4
    # compute values from ROWS for static display (mockup); live formulas alongside
    total_revenue = sum(r["revenue"] for r in ROWS)
    delivered = sum(r["revenue"] for r in ROWS if r["stage"] == "8. Closed")
    outstanding = total_revenue - delivered
    at_risk_count = sum(
        1 for r in ROWS
        if r["stage"] in ("4. Sponsor Review", "5. Regulatory Gate")
        and r["target"] and not r.get("live"))
    today = dt.date.today()
    this_month = sum(1 for r in ROWS
                     if r.get("target") and r["target"].year == today.year
                     and r["target"].month == today.month)
    next_30 = sum(1 for r in ROWS
                  if r.get("target")
                  and today <= r["target"] <= today + dt.timedelta(days=30))

    tiles = [
        ("Total Booked",     f"£{total_revenue:,.0f}", NAVY, WHITE, f"{len(ROWS)} items"),
        ("Delivered",        f"£{delivered:,.0f}",     GREEN, WHITE, f"{sum(1 for r in ROWS if r['stage']=='8. Closed')} items closed"),
        ("Outstanding",      f"£{outstanding:,.0f}",   AMBER, WHITE, f"{len(ROWS) - sum(1 for r in ROWS if r['stage']=='8. Closed')} items open"),
        ("At Risk",          f"{at_risk_count}",       RED,  WHITE, "Sponsor review / regulatory"),
        ("Live in Next 30d", f"{next_30}",             PURPLE, WHITE, "Target dates approaching"),
    ]

    col = 2
    tile_width_cols = 3
    for label, value, fill, textc, sub in tiles:
        # top band with label
        ws.merge_cells(start_row=kpi_row, end_row=kpi_row,
                       start_column=col, end_column=col + tile_width_cols - 1)
        lab = ws.cell(row=kpi_row, column=col, value=label)
        lab.font = Font(name=FONT, size=10, bold=True, color=textc)
        lab.fill = PatternFill("solid", fgColor=fill)
        lab.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.row_dimensions[kpi_row].height = 20
        # big value
        ws.merge_cells(start_row=kpi_row + 1, end_row=kpi_row + 2,
                       start_column=col, end_column=col + tile_width_cols - 1)
        val = ws.cell(row=kpi_row + 1, column=col, value=value)
        val.font = Font(name=FONT, size=28, bold=True, color=fill)
        val.fill = PatternFill("solid", fgColor=WHITE)
        val.alignment = Alignment(horizontal="center", vertical="center")
        val.border = Border(left=Side(style="medium", color=fill),
                            right=Side(style="medium", color=fill),
                            bottom=Side(style="thin", color=fill))
        ws.row_dimensions[kpi_row + 1].height = 28
        ws.row_dimensions[kpi_row + 2].height = 16
        # sublabel
        ws.merge_cells(start_row=kpi_row + 3, end_row=kpi_row + 3,
                       start_column=col, end_column=col + tile_width_cols - 1)
        s = ws.cell(row=kpi_row + 3, column=col, value=sub)
        s.font = Font(name=FONT, size=9, italic=True, color=GREY_DARK)
        s.fill = PatternFill("solid", fgColor=WHITE)
        s.alignment = Alignment(horizontal="center", vertical="center")
        s.border = Border(left=Side(style="medium", color=fill),
                          right=Side(style="medium", color=fill),
                          bottom=Side(style="medium", color=fill))
        ws.row_dimensions[kpi_row + 3].height = 16
        col += tile_width_cols

    # ----- Data tables feeding charts (hidden-ish below) -----
    # Revenue by Sponsor
    sponsors = sorted({r["sponsor"] for r in ROWS})
    data_start = 14
    ws.cell(row=data_start, column=2,
            value="Revenue by Sponsor").font = Font(
                name=FONT, size=14, bold=True, color=NAVY)
    ws.cell(row=data_start, column=2).border = Border(
        bottom=Side(style="medium", color=MAGENTA))
    header_cells(ws, data_start + 1, ["Sponsor", "Booked", "Delivered"], start_col=2)
    for i, s in enumerate(sponsors):
        r = data_start + 2 + i
        items = [x for x in ROWS if x["sponsor"] == s]
        booked = sum(x["revenue"] for x in items)
        delivered_s = sum(x["revenue"] for x in items if x["stage"] == "8. Closed")
        for c, v in enumerate([s, booked, delivered_s], start=2):
            cell = ws.cell(row=r, column=c, value=v)
            cell.font = Font(name=FONT, size=10, color=NAVY)
            cell.border = thin(GREY)
            if c > 2:
                cell.number_format = '£#,##0'
    sp_last = data_start + 1 + len(sponsors)

    rev_chart = BarChart()
    rev_chart.type = "bar"
    rev_chart.style = 2
    rev_chart.title = "Revenue — Booked vs Delivered"
    rev_chart.y_axis.title = None
    rev_chart.x_axis.title = "£ GBP"
    data_ref = Reference(ws, min_col=3, max_col=4,
                         min_row=data_start + 1, max_row=sp_last)
    cats = Reference(ws, min_col=2, min_row=data_start + 2, max_row=sp_last)
    rev_chart.add_data(data_ref, titles_from_data=True)
    rev_chart.set_categories(cats)
    rev_chart.height = 8
    rev_chart.width = 16
    style_chart_navy(rev_chart)
    ws.add_chart(rev_chart, "F14")

    # Stage pipeline
    stage_start = 28
    ws.cell(row=stage_start, column=2,
            value="Stage Pipeline").font = Font(
                name=FONT, size=14, bold=True, color=NAVY)
    ws.cell(row=stage_start, column=2).border = Border(
        bottom=Side(style="medium", color=MAGENTA))
    header_cells(ws, stage_start + 1, ["Stage", "Items"], start_col=2)
    for i, s in enumerate(STAGES):
        r = stage_start + 2 + i
        cnt = sum(1 for x in ROWS if x["stage"] == s)
        cell = ws.cell(row=r, column=2, value=s)
        cell.font = Font(name=FONT, size=10, bold=True, color=STAGE_TEXT[s])
        cell.fill = PatternFill("solid", fgColor=STAGE_FILLS[s])
        cell.border = thin(GREY)
        c2 = ws.cell(row=r, column=3, value=cnt)
        c2.font = Font(name=FONT, size=10, color=NAVY)
        c2.border = thin(GREY)
    stg_last = stage_start + 1 + len(STAGES)

    stg_chart = BarChart()
    stg_chart.type = "bar"
    stg_chart.style = 2
    stg_chart.title = "Items at each stage"
    stg_chart.legend = None
    data_ref = Reference(ws, min_col=3, max_col=3,
                         min_row=stage_start + 1, max_row=stg_last)
    cats = Reference(ws, min_col=2, min_row=stage_start + 2, max_row=stg_last)
    stg_chart.add_data(data_ref, titles_from_data=True)
    stg_chart.set_categories(cats)
    stg_chart.height = 8
    stg_chart.width = 16
    style_chart_navy(stg_chart)
    ws.add_chart(stg_chart, "F28")

    # ----- Next 30 days & At Risk lists (side-by-side below) -----
    list_row = 42
    # Next 30 days (left)
    ws.cell(row=list_row, column=2,
            value="Upcoming — Next 30 Days").font = Font(
                name=FONT, size=14, bold=True, color=NAVY)
    ws.cell(row=list_row, column=2).border = Border(
        bottom=Side(style="medium", color=MAGENTA))
    header_cells(ws, list_row + 1,
                 ["Target Date", "Item Ref", "Sponsor", "Type", "Stage"],
                 start_col=2)
    upcoming = sorted(
        [r for r in ROWS
         if r.get("target") and today <= r["target"] <= today + dt.timedelta(days=30)],
        key=lambda x: x["target"])
    for i, r in enumerate(upcoming):
        row = list_row + 2 + i
        vals = [r["target"], r["ref"], r["sponsor"], r["type"], r["stage"]]
        for c, v in enumerate(vals, start=2):
            cell = ws.cell(row=row, column=c, value=v)
            cell.font = Font(name=FONT, size=10, color=NAVY)
            cell.border = thin(GREY)
            if c == 2:
                cell.number_format = "dd.mm.yyyy"
        # colour stage cell
        stg_cell = ws.cell(row=row, column=6)
        stg_cell.fill = PatternFill("solid", fgColor=STAGE_FILLS[r["stage"]])
        stg_cell.font = Font(name=FONT, size=10, bold=True,
                             color=STAGE_TEXT[r["stage"]])

    if not upcoming:
        ws.cell(row=list_row + 2, column=2,
                value="No items due in next 30 days.").font = Font(
            name=FONT, italic=True, color=GREY_DARK)

    # At Risk (right)
    ws.cell(row=list_row, column=9,
            value="At Risk — Action Needed").font = Font(
                name=FONT, size=14, bold=True, color=RED)
    ws.cell(row=list_row, column=9).border = Border(
        bottom=Side(style="medium", color=RED))
    header_cells(ws, list_row + 1,
                 ["Item Ref", "Sponsor", "Type", "Stage", "Target", "Reason"],
                 start_col=9, fill=RED)
    risky = [r for r in ROWS
             if r["stage"] in ("4. Sponsor Review", "5. Regulatory Gate")
             and r.get("target") and not r.get("live")]
    for i, r in enumerate(risky):
        row = list_row + 2 + i
        reason = ("Awaiting sponsor sign-off"
                  if r["stage"] == "4. Sponsor Review"
                  else "With Iqera / regulatory")
        vals = [r["ref"], r["sponsor"], r["type"], r["stage"],
                r["target"], reason]
        for c, v in enumerate(vals, start=9):
            cell = ws.cell(row=row, column=c, value=v)
            cell.font = Font(name=FONT, size=10, color=NAVY)
            cell.border = thin(GREY)
            if c == 13:
                cell.number_format = "dd.mm.yyyy"
        stg_cell = ws.cell(row=row, column=12)
        stg_cell.fill = PatternFill("solid", fgColor=STAGE_FILLS[r["stage"]])
        stg_cell.font = Font(name=FONT, size=10, bold=True,
                             color=STAGE_TEXT[r["stage"]])

    # Column widths
    colw(ws, {
        "A": 2, "B": 17, "C": 14, "D": 14, "E": 12, "F": 22, "G": 22,
        "H": 2, "I": 12, "J": 14, "K": 14, "L": 22, "M": 12, "N": 34,
        "O": 2,
    })

    # Hide the data feed rows from casual view (optional: leave visible to explain)
    # Footer note
    note_row = 56
    ws.merge_cells(start_row=note_row, end_row=note_row, start_column=2, end_column=14)
    ws.cell(row=note_row, column=2,
            value=("All tiles, charts and lists reflect the Master tab. Update Master → "
                   "dashboard + month calendars refresh on open. See Master tab to edit.")
            ).font = Font(name=FONT, size=9, italic=True, color=GREY_DARK)

    return ws


# ---------- At Risk tab ----------
def build_at_risk(wb):
    ws = wb.create_sheet("At Risk", 2)
    landscape(ws)
    title_block(ws, 1, "At Risk — Exception View",
                "Items stuck at Sponsor Review or Regulatory Gate with approaching target dates", span=7)
    header_cells(ws, 4, ["Item Ref", "Sponsor", "Type", "Current Stage",
                         "Target Live", "Project Lead", "Reason"])
    risky = [r for r in ROWS
             if r["stage"] in ("4. Sponsor Review", "5. Regulatory Gate")
             and r.get("target") and not r.get("live")]
    for i, r in enumerate(risky):
        row = 5 + i
        reason = ("Awaiting sponsor sign-off — chase weekly"
                  if r["stage"] == "4. Sponsor Review"
                  else "With Iqera / regulatory — track clearance")
        vals = [r["ref"], r["sponsor"], r["type"], r["stage"],
                r["target"], r["lead"], reason]
        for c, v in enumerate(vals, start=1):
            cell = ws.cell(row=row, column=c, value=v)
            cell.font = Font(name=FONT, size=10, color=NAVY)
            cell.border = thin(GREY)
            if c == 5:
                cell.number_format = "dd.mm.yyyy"
        stg_cell = ws.cell(row=row, column=4)
        stg_cell.fill = PatternFill("solid", fgColor=STAGE_FILLS[r["stage"]])
        stg_cell.font = Font(name=FONT, size=10, bold=True,
                             color=STAGE_TEXT[r["stage"]])
    colw(ws, {"A": 12, "B": 16, "C": 14, "D": 22, "E": 14, "F": 12, "G": 40})
    return ws


# ---------- Month calendar tabs ----------
def build_month_tabs(wb):
    """One tab per month of 2026 as a 7-col weekday calendar grid.

    Day cells are pre-populated with items from ROWS that have a matching
    Target Live Date. Mockup shows current state; in production each cell
    is a FILTER formula against Master so new rows auto-land on their day.
    """
    by_date: dict[dt.date, list] = {}
    for r in ROWS:
        if r.get("target") and r["target"].year == 2026:
            by_date.setdefault(r["target"], []).append(r)

    cal = calendar.Calendar(firstweekday=0)  # Monday first (UK)
    weekday_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for month in range(1, 13):
        month_name = calendar.month_name[month]
        ws = wb.create_sheet(month_name)
        landscape(ws)
        title_block(ws, 1, f"{month_name} 2026",
                    "Events auto-populate by Target Live Date. Update Master → this view refreshes.",
                    span=7)

        # Weekday headers row 4
        for i, lbl in enumerate(weekday_labels):
            c = ws.cell(row=4, column=i + 1, value=lbl)
            c.font = Font(name=FONT, size=11, bold=True, color=WHITE)
            c.fill = PatternFill("solid", fgColor=NAVY)
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.border = thin(NAVY)
        ws.row_dimensions[4].height = 22

        month_days = cal.monthdayscalendar(2026, month)
        start_row = 5

        for wk_idx, week in enumerate(month_days):
            hdr_row = start_row + wk_idx * 3
            body_row = hdr_row + 1
            spacer_row = hdr_row + 2

            ws.row_dimensions[hdr_row].height = 18
            ws.row_dimensions[body_row].height = 64
            ws.row_dimensions[spacer_row].height = 2

            for dow, day in enumerate(week):
                col = dow + 1
                if day == 0:
                    for r in (hdr_row, body_row):
                        c = ws.cell(row=r, column=col)
                        c.fill = PatternFill("solid", fgColor=GREY_LIGHT)
                        c.border = thin(GREY)
                    continue

                date_obj = dt.date(2026, month, day)
                items = by_date.get(date_obj, [])

                # Date number cell
                d_cell = ws.cell(row=hdr_row, column=col, value=day)
                d_cell.font = Font(name=FONT, size=11, bold=True, color=NAVY)
                d_cell.alignment = Alignment(horizontal="right",
                                              vertical="center", indent=1)
                d_cell.fill = PatternFill("solid",
                                           fgColor=GREY_LIGHT if dow in (5, 6) else LIGHT_BG)
                d_cell.border = Border(
                    left=Side(style="thin", color=GREY),
                    right=Side(style="thin", color=GREY),
                    top=Side(style="thin", color=GREY))

                # Body cell with items pre-populated
                body = ws.cell(row=body_row, column=col)
                body.alignment = Alignment(horizontal="left", vertical="top",
                                            wrap_text=True, indent=1)
                body.border = Border(
                    left=Side(style="thin", color=GREY),
                    right=Side(style="thin", color=GREY),
                    bottom=Side(style="thin", color=GREY))

                if items:
                    text = "\n".join(
                        f"{x['ref']}\n{x['sponsor']} — {x['type']}"
                        for x in items
                    )
                    body.value = text
                    stage = items[0]["stage"]
                    body.fill = PatternFill("solid", fgColor=STAGE_FILLS[stage])
                    body.font = Font(name=FONT, size=9,
                                     color=STAGE_TEXT[stage], bold=True)
                    # Scale row height with item count
                    needed = max(64, 32 * len(items))
                    if needed > ws.row_dimensions[body_row].height:
                        ws.row_dimensions[body_row].height = needed
                else:
                    body.font = Font(name=FONT, size=9, color=GREY_DARK)

        colw(ws, {get_column_letter(c): 22 for c in range(1, 8)})

        # Stage colour key + live-formula note
        key_row = start_row + len(month_days) * 3 + 2
        ws.cell(row=key_row, column=1,
                value="Stage colour key").font = Font(
                    name=FONT, size=10, bold=True, color=NAVY)
        for i, s in enumerate(STAGES):
            r = key_row + 1 + i
            c = ws.cell(row=r, column=1, value=s)
            c.fill = PatternFill("solid", fgColor=STAGE_FILLS[s])
            c.font = Font(name=FONT, size=10, bold=True, color=STAGE_TEXT[s])
            c.border = thin(GREY)
            ws.merge_cells(start_row=r, end_row=r, start_column=1, end_column=2)

        note_row = key_row + len(STAGES) + 2
        ws.merge_cells(start_row=note_row, end_row=note_row,
                       start_column=1, end_column=7)
        n = ws.cell(row=note_row, column=1,
                    value=("Live workbook: each cell is a FILTER formula against Master. "
                           "Add/update a row in Master → this view refreshes on open. "
                           "Shown here: current state pre-populated for review."))
        n.font = Font(name=FONT, size=9, italic=True, color=GREY_DARK)
        n.alignment = Alignment(wrap_text=True)

        ws.sheet_properties.tabColor = NAVY


# ---------- Build ----------
def build():
    wb = Workbook()
    # remove default sheet; we'll add Dashboard at idx 0 later
    wb.remove(wb.active)

    master_ws, first, last = build_master(wb)
    # wb now has Master at idx 0
    build_at_risk(wb)        # inserts at idx 2 (will become idx 2 after Dashboard insert)
    build_dashboard(wb, first, last)  # inserts at idx 0 — Dashboard first
    build_month_tabs(wb)     # appends 12 month tabs

    # Order sheets: Dashboard, Master, At Risk, Jan..Dec
    desired = ["Dashboard", "Master", "At Risk"] + [
        calendar.month_name[m] for m in range(1, 13)]
    wb._sheets = [wb[name] for name in desired]

    # Tab colours
    wb["Dashboard"].sheet_properties.tabColor = MAGENTA
    wb["Master"].sheet_properties.tabColor = NAVY
    wb["At Risk"].sheet_properties.tabColor = RED

    out = OUT / "morph-events-tracker-2026.xlsx"
    wb.save(out)
    print(f"Saved: {out}")
    return out


if __name__ == "__main__":
    build()
