"""Build MORPh Events & Sponsorship Tracker v2 — unified, RAG-driven.

Reads /Users/deanlatham/Desktop/2026 calendar.xlsx (all 12 tabs) and produces
one workbook in MORPh New World/Spreadsheets/ with:

  1. Dashboard      — KPIs, RAG distribution, charts, close-out queue, upcoming
  2. Master         — every 2026 item (events + non-event + cancelled)
  3. RAG Rules      — documented thresholds (10w / 8w / 2w)
  4. At Risk        — Red + Amber items
  5. Close-out      — past events missing survey/certs/slides/invoice
  6-17. Jan-Dec     — calendar grids, events coloured by RAG

RAG model (time-based, aligned to Event Delivery Process):
  Black — past + not fully closed        (close-out queue)
  Red   — event within 2 weeks           (2-week cut-off window)
  Amber — 2-8 weeks out                  (pre-event comms / prep window)
  Green — 8-10 weeks out                 (marketing activation window)
  White — >10 weeks out                  (not in realm yet)

Close-out complete = all of:
  Uploaded to website, Speaker Slides, Honoraria Form, Sponsor Invoice #
"""
from __future__ import annotations
import calendar
import datetime as dt
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.page import PageMargins
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.drawing.image import Image as XLImage
from openpyxl.comments import Comment

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
BLACK = "1B1B1B"
FONT = "Calibri"

# ---------- Stages & RAG ----------
STAGES = [
    "1. Initiation", "2. Production", "3. Marketing Activation",
    "4. Pre-Event Comms", "5. Two-Week Cut-Off", "6. Pre-Event Prep",
    "7. Event Day", "8. Closed", "X. Cancelled",
]
STAGE_FILLS = {
    "1. Initiation":          LIGHT_BG,
    "2. Production":          PURPLE,
    "3. Marketing Activation": MAGENTA,
    "4. Pre-Event Comms":     "E8A7FF",
    "5. Two-Week Cut-Off":    AMBER,
    "6. Pre-Event Prep":      NAVY,
    "7. Event Day":           GREEN,
    "8. Closed":              GREY,
    "X. Cancelled":           "555555",
}
STAGE_TEXT = {
    "1. Initiation":          NAVY,
    "2. Production":          WHITE,
    "3. Marketing Activation": WHITE,
    "4. Pre-Event Comms":     NAVY,
    "5. Two-Week Cut-Off":    WHITE,
    "6. Pre-Event Prep":      WHITE,
    "7. Event Day":           WHITE,
    "8. Closed":              NAVY,      # was WHITE — poor contrast on grey
    "X. Cancelled":           WHITE,
}

RAG_ORDER = ["Black", "Red", "Amber", "Green", "White"]
RAG_FILLS = {"Black": BLACK, "Red": RED, "Amber": AMBER,
             "Green": GREEN, "White": WHITE}
RAG_TEXT = {"Black": WHITE, "Red": WHITE, "Amber": WHITE,
            "Green": WHITE, "White": NAVY}
RAG_LABEL = {
    "Black": "Close-out needed",
    "Red": "≤ 2 weeks",
    "Amber": "2–8 weeks",
    "Green": "8–10 weeks",
    "White": "> 10 weeks",
}

TYPES_EVENT = ["Event"]
TYPES_CONTENT = ["Toolkit", "Blog", "Newsletter", "Banner", "Neighbourhood Banner"]
ALL_TYPES = TYPES_EVENT + TYPES_CONTENT + ["Marker"]
INVOICE_STATUSES = ["Booked", "Invoiced", "Paid", "—"]
YESNO = ["Yes", "No"]

TODAY = dt.date.today()
SRC = Path("/Users/deanlatham/Desktop/2026 calendar.xlsx")
OUT = Path("/Users/deanlatham/Desktop/work/morph/Morph New World/Spreadsheets")
LOGO = "/Users/deanlatham/Desktop/work/morph/Morph New World/Marketing/MORPh Brand Pack/Logo/Dark/Logo-Dark.png"


# =========================================================================
# Data extraction
# =========================================================================
def _to_date(v):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    return None


def _yes(v):
    """True-ish: value populated with something meaningful."""
    if v is None:
        return False
    s = str(v).strip().lower()
    if s in ("", "no", "false", "0", "none", "n/a", "-", "—"):
        return False
    return True


def infer_event_stage(status, target, speaker_ok, marketing_ok, slides_ok,
                      website_ok, today=TODAY, is_cancelled=False):
    """Infer 8-stage value for an event."""
    if is_cancelled or (status and "cancel" in str(status).lower()):
        return "X. Cancelled"
    if not target:
        return "1. Initiation"
    weeks_to = (target - today).days / 7
    if weeks_to < -3:
        # well past — should be closed; if close-out complete, Closed, else Day (flagged)
        if slides_ok and website_ok:
            return "8. Closed"
        return "7. Event Day"
    if weeks_to < 0:
        return "7. Event Day"
    if weeks_to <= 2:
        return "5. Two-Week Cut-Off"
    if weeks_to <= 8:
        return "4. Pre-Event Comms" if marketing_ok else "3. Marketing Activation"
    if weeks_to <= 10:
        return "3. Marketing Activation" if speaker_ok else "2. Production"
    return "1. Initiation"


def infer_content_stage(existing_status, draft, approved, live, target, today=TODAY):
    """Infer 8-stage value for content/sponsorship items."""
    s = str(existing_status or "").lower()
    if live:
        return "8. Closed"
    if approved:
        return "6. Pre-Launch"
    if draft:
        return "4. Pre-Event Comms" if s and "iqera" in s else "3. Marketing Activation"
    if "production" in s:
        return "2. Production"
    return "1. Initiation"


def compute_rag(target, stage, close_out_complete):
    """Return RAG ('Black'/'Red'/'Amber'/'Green'/'White')."""
    if stage == "X. Cancelled":
        return "White"
    if target is None:
        return "White"
    days = (target - TODAY).days
    if days < 0 and not close_out_complete:
        return "Black"
    if days < 0:
        return "White"  # past & closed = benign
    if days <= 14:
        return "Red"
    if days <= 56:
        return "Amber"
    if days <= 70:
        return "Green"
    return "White"


def extract_events(wb, sheet_name, is_past=False, is_cancelled=False):
    """Pull events from past-events / Event-Calendar-2026 / cancelled tabs.
    Columns differ slightly between past events and Event Calendar 2026.
    """
    ws = wb[sheet_name]
    rows = []
    # map column indices for each source (1-based from openpyxl)
    if sheet_name == "Event Calendar 2026":
        COL = dict(ref=2, date=3, title=4, upload_old=6, upload_new=7,
                   status=8, fmt=9, timings=10, location=11, nel=12,
                   mkt=15, delegates=16, speaker=18, speaker_fee=19,
                   speaker_exp=20, honoraria=21, slides=22, venue=23,
                   venue_status=24, ddr=25, venue_total=26,
                   sponsor=27, support=28, sponsor_rev=31,
                   invoice_no=32, gp=33, notes=34)
    else:  # past events / cancelled events (same schema)
        COL = dict(ref=2, date=3, title=4, upload_old=5, upload_new=None,
                   status=6, fmt=7, timings=8, location=9, nel=10,
                   mkt=13, delegates=14, speaker=15, speaker_fee=16,
                   speaker_exp=17, honoraria=18, slides=19, venue=20,
                   venue_status=21, ddr=22, venue_total=23,
                   sponsor=24, support=25, sponsor_rev=28,
                   invoice_no=29, gp=30, notes=31)

    for r in range(2, ws.max_row + 1):
        title = ws.cell(row=r, column=COL["title"]).value
        if not title or not str(title).strip():
            continue
        title_s = str(title).strip()
        # Skip bank holiday markers
        if title_s.upper() in ("BH", "`"):
            continue

        date = _to_date(ws.cell(row=r, column=COL["date"]).value)
        ref = ws.cell(row=r, column=COL["ref"]).value
        status = ws.cell(row=r, column=COL["status"]).value
        fmt = ws.cell(row=r, column=COL["fmt"]).value
        timings = ws.cell(row=r, column=COL["timings"]).value
        location = ws.cell(row=r, column=COL["location"]).value
        nel = ws.cell(row=r, column=COL["nel"]).value
        mkt_scheduled = _yes(ws.cell(row=r, column=COL["mkt"]).value)
        delegates = ws.cell(row=r, column=COL["delegates"]).value
        speaker_ok = _yes(ws.cell(row=r, column=COL["speaker"]).value)
        speaker_fee = ws.cell(row=r, column=COL["speaker_fee"]).value or 0
        try:
            speaker_fee = float(speaker_fee) if speaker_fee not in ("", None) else 0
        except (TypeError, ValueError):
            speaker_fee = 0
        honoraria_ok = _yes(ws.cell(row=r, column=COL["honoraria"]).value)
        slides_ok = _yes(ws.cell(row=r, column=COL["slides"]).value)
        venue = ws.cell(row=r, column=COL["venue"]).value
        venue_status = ws.cell(row=r, column=COL["venue_status"]).value
        venue_total = ws.cell(row=r, column=COL["venue_total"]).value or 0
        try:
            venue_total = float(venue_total) if venue_total not in ("", None) else 0
        except (TypeError, ValueError):
            venue_total = 0
        sponsor = ws.cell(row=r, column=COL["sponsor"]).value
        support = ws.cell(row=r, column=COL["support"]).value
        revenue = ws.cell(row=r, column=COL["sponsor_rev"]).value or 0
        try:
            revenue = float(revenue) if revenue not in ("", None) else 0
        except (TypeError, ValueError):
            revenue = 0
        invoice_no = ws.cell(row=r, column=COL["invoice_no"]).value
        notes = ws.cell(row=r, column=COL["notes"]).value

        # Is it a non-event marker (holidays, blocker)?
        is_marker = (
            ref in (None, "-", "") and
            (fmt in (None, "") and location in (None, ""))
        )
        item_type = "Marker" if is_marker else "Event"

        website_ok = _yes(ws.cell(row=r, column=COL["upload_old"]).value) or (
            COL["upload_new"] and _yes(ws.cell(row=r, column=COL["upload_new"]).value)
        )

        stage = infer_event_stage(
            status, date, speaker_ok, mkt_scheduled, slides_ok, website_ok,
            is_cancelled=is_cancelled,
        )

        close_out_complete = all([
            website_ok, slides_ok, honoraria_ok,
            (invoice_no not in (None, "")) if revenue > 0 else True,
        ]) if date and date < TODAY else False

        # Invoice status heuristic
        if revenue == 0:
            inv = "—"
        elif invoice_no:
            inv = "Paid" if (date and date < TODAY - dt.timedelta(days=30)) else "Invoiced"
        else:
            inv = "Booked"

        rag = compute_rag(date, stage, close_out_complete)

        rows.append(dict(
            ref=str(ref).strip() if ref else "",
            title=title_s,
            type=item_type,
            sponsor=str(sponsor).strip() if sponsor else "",
            format=str(fmt).strip() if fmt else "",
            location=str(location).strip() if location else "",
            lead=str(nel).strip() if nel else "",
            target=date,
            live=date if stage == "8. Closed" else None,
            stage=stage,
            rag=rag,
            speaker_ok=speaker_ok,
            mkt_scheduled=mkt_scheduled,
            slides_ok=slides_ok,
            honoraria_ok=honoraria_ok,
            website_ok=website_ok,
            venue=str(venue).strip() if venue else "",
            venue_status=str(venue_status).strip() if venue_status else "",
            delegates=delegates,
            revenue=revenue,
            spend=speaker_fee + venue_total,
            speaker_fee=speaker_fee,
            venue_total=venue_total,
            invoice_status=inv,
            invoice_no=str(invoice_no).strip() if invoice_no else "",
            support=str(support).strip() if support else "",
            close_out_complete=close_out_complete,
            notes=str(notes).strip() if notes else "",
            source=sheet_name,
        ))
    return rows


def extract_non_event(wb):
    """Pull the 14 non-event sponsorship rows."""
    ws = wb["Non Event Sponsorship"]
    rows = []
    for r in range(2, ws.max_row + 1):
        ref = ws.cell(row=r, column=1).value
        if not ref:
            continue
        company = ws.cell(row=r, column=2).value
        item_type = ws.cell(row=r, column=3).value or "Toolkit"
        status = ws.cell(row=r, column=4).value
        detail = ws.cell(row=r, column=5).value
        lead = ws.cell(row=r, column=6).value
        month = ws.cell(row=r, column=7).value
        revenue = ws.cell(row=r, column=8).value or 0
        try:
            revenue = float(revenue) if revenue not in ("", None) else 0
        except (TypeError, ValueError):
            revenue = 0
        spend = ws.cell(row=r, column=9).value or 0
        try:
            spend = float(spend) if spend not in ("", None) else 0
        except (TypeError, ValueError):
            spend = 0
        draft = _to_date(ws.cell(row=r, column=10).value) or _parse_date(ws.cell(row=r, column=10).value)
        approved = _to_date(ws.cell(row=r, column=11).value) or _parse_date(ws.cell(row=r, column=11).value)
        live = _to_date(ws.cell(row=r, column=12).value) or _parse_date(ws.cell(row=r, column=12).value)

        # Map month name to a default target date (last day of month)
        target = None
        if month:
            month_name = str(month).strip().lower()
            for mi in range(1, 13):
                if month_name == calendar.month_name[mi].lower():
                    last = calendar.monthrange(2026, mi)[1]
                    target = dt.date(2026, mi, last)
                    break

        stage = infer_content_stage(status, draft, approved, live, target)
        close_out_complete = (stage == "8. Closed")
        rag = compute_rag(target, stage, close_out_complete)

        inv = "Paid" if stage == "8. Closed" else ("Invoiced" if stage in ("6. Pre-Event Prep", "7. Event Day") else "Booked")
        if revenue == 0:
            inv = "—"

        rows.append(dict(
            ref=str(ref).strip(),
            title=str(detail or "").strip(),
            type=str(item_type).strip(),
            sponsor=str(company).strip() if company else "",
            format="",
            location="",
            lead=str(lead).strip() if lead else "",
            target=target,
            live=live,
            stage=stage,
            rag=rag,
            speaker_ok=True,  # n/a for non-event
            mkt_scheduled=bool(draft),
            slides_ok=bool(approved),
            honoraria_ok=bool(live),
            website_ok=bool(live),
            venue="",
            venue_status="",
            delegates=None,
            revenue=revenue,
            spend=spend,
            speaker_fee=0,
            venue_total=0,
            invoice_status=inv,
            invoice_no="",
            support="",
            close_out_complete=close_out_complete,
            notes="",
            source="Non Event Sponsorship",
        ))
    return rows


def _parse_date(v):
    """Parse 'dd.mm.yyyy' strings into date."""
    if v is None or isinstance(v, (dt.date, dt.datetime)):
        return _to_date(v)
    try:
        s = str(v).strip()
        if "." in s:
            d, m, y = s.split(".")
            return dt.date(int(y), int(m), int(d))
    except Exception:
        pass
    return None


def build_dataset():
    # Prefer the original source xlsx if present; otherwise read back from
    # the last-generated tracker's Master tab (which has the same schema).
    if not SRC.exists():
        print(f"Source {SRC.name} not found — reading from existing tracker Master.")
        return _load_from_existing_master()

    wb = load_workbook(SRC, data_only=True)
    rows = []
    rows += extract_events(wb, "Event Calendar 2026")
    rows += extract_events(wb, "past events", is_past=True)
    rows += extract_events(wb, "cancelled events", is_cancelled=True)
    rows += extract_non_event(wb)
    # Dedupe by ref (same event sometimes appears in multiple tabs)
    seen = {}
    out = []
    for r in rows:
        k = r["ref"] if r["ref"] else (r["title"], r["target"])
        if k in seen:
            continue
        seen[k] = True
        out.append(r)
    return out


def _load_from_existing_master():
    """Fallback: read normalized rows from the already-built tracker Master."""
    existing = OUT / "morph-events-tracker-2026.xlsx"
    wb = load_workbook(existing, data_only=True)
    ws = wb["Master"]
    rows = []
    for r in range(5, ws.max_row + 1):
        ref = ws.cell(row=r, column=1).value
        if not ref and not ws.cell(row=r, column=3).value:
            continue
        rows.append(dict(
            ref=str(ref or "").strip(),
            type=ws.cell(row=r, column=2).value or "Event",
            title=str(ws.cell(row=r, column=3).value or "").strip(),
            sponsor=str(ws.cell(row=r, column=4).value or "").strip(),
            format=str(ws.cell(row=r, column=5).value or "").strip(),
            location=str(ws.cell(row=r, column=6).value or "").strip(),
            lead=str(ws.cell(row=r, column=7).value or "").strip(),
            stage=ws.cell(row=r, column=8).value or "1. Initiation",
            rag=ws.cell(row=r, column=9).value or "White",
            target=_to_date(ws.cell(row=r, column=10).value),
            live=_to_date(ws.cell(row=r, column=11).value),
            speaker_ok=(ws.cell(row=r, column=12).value == "Yes"),
            mkt_scheduled=(ws.cell(row=r, column=13).value == "Yes"),
            slides_ok=(ws.cell(row=r, column=14).value == "Yes"),
            honoraria_ok=(ws.cell(row=r, column=15).value == "Yes"),
            website_ok=(ws.cell(row=r, column=14).value == "Yes"),
            delegates=ws.cell(row=r, column=16).value,
            revenue=float(ws.cell(row=r, column=17).value or 0),
            spend=float(ws.cell(row=r, column=18).value or 0),
            speaker_fee=0,
            venue_total=0,
            invoice_status=ws.cell(row=r, column=19).value or "—",
            invoice_no=str(ws.cell(row=r, column=20).value or "").strip(),
            notes=str(ws.cell(row=r, column=21).value or "").strip(),
            venue="",
            venue_status="",
            support="",
            close_out_complete=(ws.cell(row=r, column=8).value == "8. Closed"),
            source="existing Master",
        ))
    return rows


def extract_lookups():
    """Pull unique Sponsor / NEL / Format lists from source for dropdowns."""
    if not SRC.exists():
        # Fallback: derive from the previously-built tracker
        existing = OUT / "morph-events-tracker-2026.xlsx"
        if not existing.exists():
            return ([], [], [])
        wb = load_workbook(existing, data_only=True)
        if "Lists" not in wb.sheetnames:
            return ([], [], [])
        ws = wb["Lists"]
        sponsors, nels, formats = [], [], []
        for r in range(2, ws.max_row + 1):
            if ws.cell(row=r, column=1).value:
                sponsors.append(str(ws.cell(row=r, column=1).value).strip())
            if ws.cell(row=r, column=2).value:
                nels.append(str(ws.cell(row=r, column=2).value).strip())
            if ws.cell(row=r, column=3).value:
                formats.append(str(ws.cell(row=r, column=3).value).strip())
        return (sorted(set(sponsors)), sorted(set(nels)), sorted(set(formats)))

    wb = load_workbook(SRC, data_only=True)
    sponsors, nels, formats = set(), set(), set()

    # From Sponsor tab (authoritative sponsor list)
    if "Sponsor" in wb.sheetnames:
        sws = wb["Sponsor"]
        for r in range(2, sws.max_row + 1):
            v = sws.cell(row=r, column=1).value
            if v and str(v).strip():
                sponsors.add(str(v).strip())

    # From event tabs
    for tab in ("Event Calendar 2026", "past events", "cancelled events"):
        if tab not in wb.sheetnames:
            continue
        ws = wb[tab]
        sponsor_col = 27 if tab == "Event Calendar 2026" else 24
        fmt_col = 9 if tab == "Event Calendar 2026" else 7
        nel_col = 12 if tab == "Event Calendar 2026" else 10
        for r in range(2, ws.max_row + 1):
            s = ws.cell(row=r, column=sponsor_col).value
            f = ws.cell(row=r, column=fmt_col).value
            n = ws.cell(row=r, column=nel_col).value
            if s and str(s).strip():
                sponsors.add(str(s).strip())
            if f and str(f).strip():
                formats.add(str(f).strip())
            if n and str(n).strip() and str(n).strip() not in ("None", "0"):
                nels.add(str(n).strip())

    return (sorted(sponsors), sorted(nels), sorted(formats))


# =========================================================================
# Workbook helpers
# =========================================================================
def thin(c=GREY):
    s = Side(style="thin", color=c)
    return Border(left=s, right=s, top=s, bottom=s)


def landscape(ws):
    ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
    ws.page_setup.paperSize = ws.PAPERSIZE_A3
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins = PageMargins(left=0.3, right=0.3, top=0.4, bottom=0.4)
    ws.sheet_view.showGridLines = False


def title_block(ws, row, title, subtitle="", span=20, size=22):
    c = ws.cell(row=row, column=1, value=title)
    c.font = Font(name=FONT, size=size, bold=True, color=NAVY)
    ws.row_dimensions[row].height = max(size + 10, 30)
    ws.merge_cells(start_row=row, end_row=row, start_column=1, end_column=span)
    if subtitle:
        s = ws.cell(row=row + 1, column=1, value=subtitle)
        s.font = Font(name=FONT, size=11, italic=True, color=GREY_DARK)
        ws.merge_cells(start_row=row + 1, end_row=row + 1,
                       start_column=1, end_column=span)
    ws.cell(row=row, column=1).border = Border(
        bottom=Side(style="medium", color=MAGENTA))


def header_cells(ws, row, headers, start_col=1, fill=NAVY, text=WHITE, height=26):
    for i, h in enumerate(headers):
        c = ws.cell(row=row, column=start_col + i, value=h)
        c.font = Font(name=FONT, size=10, bold=True, color=text)
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(horizontal="left", vertical="center",
                                wrap_text=True, indent=1)
        c.border = thin(NAVY)
    ws.row_dimensions[row].height = height


def colw(ws, widths):
    for c, w in widths.items():
        ws.column_dimensions[c].width = w


def dv_list(ws, col, first, last, values):
    f = '"' + ",".join(values) + '"'
    dv = DataValidation(type="list", formula1=f, allow_blank=True)
    dv.add(f"{col}{first}:{col}{last}")
    ws.add_data_validation(dv)


def dv_named(ws, col, first, last, named_range):
    """Dropdown sourced from a named range (for long lists)."""
    dv = DataValidation(type="list", formula1=f"={named_range}", allow_blank=True)
    dv.add(f"{col}{first}:{col}{last}")
    ws.add_data_validation(dv)


def build_lists_sheet(wb, sponsors, nels, formats):
    """Hidden sheet holding long dropdown lists, with named ranges."""
    from openpyxl.workbook.defined_name import DefinedName
    ws = wb.create_sheet("Lists")
    ws.sheet_state = "hidden"
    ws.cell(row=1, column=1, value="Sponsors").font = Font(bold=True)
    ws.cell(row=1, column=2, value="NELs / Leads").font = Font(bold=True)
    ws.cell(row=1, column=3, value="Formats").font = Font(bold=True)
    for i, s in enumerate(sponsors):
        ws.cell(row=2 + i, column=1, value=s)
    for i, n in enumerate(nels):
        ws.cell(row=2 + i, column=2, value=n)
    for i, f in enumerate(formats):
        ws.cell(row=2 + i, column=3, value=f)

    # Named ranges
    def make_named(name, col_letter, count):
        if count == 0:
            return
        ref = f"Lists!${col_letter}$2:${col_letter}${1 + count}"
        wb.defined_names[name] = DefinedName(name, attr_text=ref)

    make_named("rngSponsors", "A", len(sponsors))
    make_named("rngNELs", "B", len(nels))
    make_named("rngFormats", "C", len(formats))


# =========================================================================
# How to Use (first tab)
# =========================================================================
def build_how_to_use(wb):
    ws = wb.create_sheet("How to Use", 0)
    landscape(ws)
    ws.sheet_view.showGridLines = False

    # Logo
    try:
        img = XLImage(LOGO)
        img.width, img.height = 170, 58
        ws.add_image(img, "L2")
    except Exception:
        pass

    ws.cell(row=2, column=2, value="MORPH TRACKER — GUIDE").font = Font(
        name=FONT, size=10, bold=True, color=MAGENTA)
    ws.cell(row=3, column=2, value="How to use this spreadsheet").font = Font(
        name=FONT, size=28, bold=True, color=NAVY)
    ws.row_dimensions[3].height = 40
    ws.cell(row=4, column=2,
            value="One page, plain English. Five minutes to read.").font = Font(
                name=FONT, size=11, italic=True, color=GREY_DARK)
    for col in range(2, 14):
        ws.cell(row=5, column=col).fill = PatternFill("solid", fgColor=MAGENTA)
    ws.row_dimensions[5].height = 4

    def section(row, title, colour=NAVY):
        c = ws.cell(row=row, column=2, value=title)
        c.font = Font(name=FONT, size=14, bold=True, color=colour)
        c.border = Border(bottom=Side(style="medium", color=MAGENTA))
        ws.merge_cells(start_row=row, end_row=row, start_column=2, end_column=13)
        ws.row_dimensions[row].height = 24

    def body(row, text, bold=False, colour=NAVY, size=10, indent=1):
        c = ws.cell(row=row, column=2, value=text)
        c.font = Font(name=FONT, size=size, bold=bold, color=colour)
        c.alignment = Alignment(horizontal="left", vertical="top",
                                wrap_text=True, indent=indent)
        ws.merge_cells(start_row=row, end_row=row, start_column=2, end_column=13)
        # Height scales with text length
        ws.row_dimensions[row].height = max(18, (len(text) // 100 + 1) * 16)

    def callout(row, title, text):
        for col in range(2, 14):
            ws.cell(row=row, column=col).fill = PatternFill("solid", fgColor=LIGHT_BG)
            ws.cell(row=row + 1, column=col).fill = PatternFill("solid", fgColor=LIGHT_BG)
        t = ws.cell(row=row, column=2, value=title)
        t.font = Font(name=FONT, size=10, bold=True, color=NAVY)
        ws.merge_cells(start_row=row, end_row=row, start_column=2, end_column=13)
        ws.row_dimensions[row].height = 20
        b = ws.cell(row=row + 1, column=2, value=text)
        b.font = Font(name=FONT, size=10, color=NAVY, italic=True)
        b.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=row + 1, end_row=row + 1, start_column=2, end_column=13)
        ws.row_dimensions[row + 1].height = 36

    r = 7
    section(r, "What this is")
    r += 1
    body(r, "The single place to track every MORPh event and sponsored item. "
            "Update the Master tab, and every other tab refreshes automatically — "
            "the Dashboard Amz sees, the At Risk list, the Close-out Queue, and "
            "the monthly calendar views.")
    r += 2

    section(r, "The tabs, in order")
    r += 1
    for line in [
        ("Dashboard",   "What Amz opens to. Headline numbers and priority lists."),
        ("Master",      "The table YOU edit. One row per event or sponsored item."),
        ("RAG Rules",   "Explains the colour code. Reference only — don't change."),
        ("At Risk",     "Auto-list of events in Red or Amber (inside 8 weeks)."),
        ("Close-out",   "Auto-list of past events that still need wrap-up."),
        ("Jan → Dec",   "Calendar view of what's landing on each day."),
    ]:
        tab, desc = line
        ws.cell(row=r, column=2, value=tab).font = Font(
            name=FONT, size=10, bold=True, color=NAVY)
        ws.cell(row=r, column=2).alignment = Alignment(indent=1, vertical="center")
        ws.cell(row=r, column=4, value=desc).font = Font(
            name=FONT, size=10, color=NAVY)
        ws.cell(row=r, column=4).alignment = Alignment(wrap_text=True, vertical="center")
        ws.merge_cells(start_row=r, end_row=r, start_column=4, end_column=13)
        ws.row_dimensions[r].height = 20
        r += 1
    r += 1

    section(r, "How to add a new event")
    r += 1
    for i, step in enumerate([
        "Open the Master tab.",
        "Go to the next empty row at the bottom.",
        "Fill in the columns from left to right — use the dropdown arrows where they appear.",
        "The only must-haves are: Item Ref, Type, Title, Lead Person, Event Date.",
        "Leave RAG alone — it fills in automatically based on the Event Date.",
        "Hit save. The event now appears on its month tab and on the Dashboard.",
    ], start=1):
        c = ws.cell(row=r, column=2, value=f"{i}.  {step}")
        c.font = Font(name=FONT, size=10, color=NAVY)
        c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=r, end_row=r, start_column=2, end_column=13)
        ws.row_dimensions[r].height = 20
        r += 1
    r += 1

    section(r, "How to update an event you've already added")
    r += 1
    for i, step in enumerate([
        "Find the row in Master (use Ctrl+F to search the Item Ref or title).",
        "Move the Current Stage along using the dropdown — e.g. 1. Initiation → 2. Production → 3. Marketing Activation → etc.",
        "As tasks get done, tick the Yes/No columns — Speaker Confirmed?, Marketing Sent?, Slides Received?, Honoraria Received?.",
        "When the event has happened AND all close-out tasks are Yes, set Current Stage to 8. Closed.",
        "The Dashboard, At Risk list, and Close-out queue update automatically.",
    ], start=1):
        c = ws.cell(row=r, column=2, value=f"{i}.  {step}")
        c.font = Font(name=FONT, size=10, color=NAVY)
        c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=r, end_row=r, start_column=2, end_column=13)
        ws.row_dimensions[r].height = 20
        r += 1
    r += 1

    section(r, "What the RAG colours mean")
    r += 1
    for k in RAG_ORDER:
        c = ws.cell(row=r, column=2, value=k)
        c.fill = PatternFill("solid", fgColor=RAG_FILLS[k])
        c.font = Font(name=FONT, size=10, bold=True, color=RAG_TEXT[k])
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = thin(GREY)
        ws.merge_cells(start_row=r, end_row=r, start_column=2, end_column=3)
        plain = {
            "Black": "Event has already happened but the wrap-up isn't finished. CHASE.",
            "Red":   "Event is in the next 2 weeks. Final countdown — sort delegates, dietary, speaker prep.",
            "Amber": "Event is 2–8 weeks away. Start marketing and comms.",
            "Green": "Event is 8–10 weeks away. Confirm speaker and venue.",
            "White": "More than 10 weeks out — or already closed. Nothing urgent.",
        }[k]
        b = ws.cell(row=r, column=4, value=plain)
        b.font = Font(name=FONT, size=10, color=NAVY)
        b.alignment = Alignment(wrap_text=True, vertical="center", indent=1)
        ws.merge_cells(start_row=r, end_row=r, start_column=4, end_column=13)
        ws.row_dimensions[r].height = 22
        r += 1
    r += 1

    section(r, "What the Stages mean")
    r += 1
    stage_plain = {
        "1. Initiation":           "Date pencilled in. Nothing else agreed yet.",
        "2. Production":           "Building content. Speaker and venue being confirmed.",
        "3. Marketing Activation": "Mailer out to the network. Sponsor on board.",
        "4. Pre-Event Comms":      "Engaging registered delegates. Final agenda shared.",
        "5. Two-Week Cut-Off":     "Decision point. Are delegate numbers there? Go / no-go.",
        "6. Pre-Event Prep":       "Final logistics. Dietary captured. 72-hour check-ins done.",
        "7. Event Day":            "Happening today, or happened in the last 3 days.",
        "8. Closed":               "All wrap-up tasks done: slides, honoraria, website, invoice.",
        "X. Cancelled":            "Event pulled. Sponsors notified.",
    }
    for s, desc in stage_plain.items():
        c = ws.cell(row=r, column=2, value=s)
        c.fill = PatternFill("solid", fgColor=STAGE_FILLS[s])
        c.font = Font(name=FONT, size=10, bold=True, color=STAGE_TEXT[s])
        c.alignment = Alignment(indent=1, vertical="center")
        c.border = thin(GREY)
        ws.merge_cells(start_row=r, end_row=r, start_column=2, end_column=3)
        b = ws.cell(row=r, column=4, value=desc)
        b.font = Font(name=FONT, size=10, color=NAVY)
        b.alignment = Alignment(wrap_text=True, vertical="center", indent=1)
        ws.merge_cells(start_row=r, end_row=r, start_column=4, end_column=13)
        ws.row_dimensions[r].height = 22
        r += 1
    r += 1

    section(r, "Things to avoid")
    r += 1
    for tip in [
        "Don't re-use an Item Ref. Each event or item needs its own unique code.",
        "Don't type dates as text — click the cell and use the date picker / DD/MM/YYYY format.",
        "Don't delete the header row or the RAG Rules tab. They hold the wiring.",
        "Don't edit the At Risk, Close-out, Dashboard, or month tabs directly — they're auto-generated from Master.",
        "If something looks wrong on a tab, fix it on Master, not on the tab where you see it.",
    ]:
        c = ws.cell(row=r, column=2, value="•  " + tip)
        c.font = Font(name=FONT, size=10, color=NAVY)
        c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=r, end_row=r, start_column=2, end_column=13)
        ws.row_dimensions[r].height = 20
        r += 1
    r += 1

    section(r, "Stuck? Ask.")
    r += 1
    body(r, "If the spreadsheet does something weird, if a column doesn't make sense, or if you're not sure "
            "where to log something — ask Dean or Will. Don't invent a workaround; we'd rather fix the tool than "
            "patch over it.")
    r += 2

    colw(ws, {"A": 2, "B": 22, "C": 16, "D": 18, "E": 14, "F": 14,
              "G": 14, "H": 14, "I": 14, "J": 14, "K": 14, "L": 14, "M": 14})
    ws.sheet_properties.tabColor = MAGENTA


# =========================================================================
# Dashboard
# =========================================================================
def build_dashboard(wb, rows):
    ws = wb.create_sheet("Dashboard", 0)
    landscape(ws)
    ws.sheet_view.tabSelected = True

    # Logo + header
    try:
        img = XLImage(LOGO)
        img.width, img.height = 170, 58
        ws.add_image(img, "Q2")
    except Exception:
        pass

    ws.cell(row=2, column=2, value="MORPH TRACKER").font = Font(
        name=FONT, size=10, bold=True, color=MAGENTA)
    ws.cell(row=3, column=2, value="Events & Sponsorship — 2026").font = Font(
        name=FONT, size=28, bold=True, color=NAVY)
    ws.row_dimensions[3].height = 40
    ws.cell(row=4, column=2,
            value=f"Updated {TODAY:%d %B %Y} · {len(rows)} items tracked · all figures from Master"
            ).font = Font(name=FONT, size=11, italic=True, color=GREY_DARK)
    for col in range(2, 20):
        ws.cell(row=5, column=col).fill = PatternFill("solid", fgColor=MAGENTA)
    ws.row_dimensions[5].height = 4

    # ---- RAG KPI tiles (live formulas against tblMaster) ----
    events_only = [r for r in rows if r["type"] == "Event"]
    total_items = len(rows)
    tiles = [
        ("Total Events",
         '=COUNTIF(tblMaster[Type],"Event")',
         NAVY,
         f"{total_items} items all types"),
        ("Close-out Needed",
         '=COUNTIFS(tblMaster[Type],"Event",tblMaster[RAG],"Black")',
         BLACK,
         "Past events missing sign-off"),
        ("≤ 2 weeks (Red)",
         '=COUNTIFS(tblMaster[Type],"Event",tblMaster[RAG],"Red")',
         RED,
         "2-week cut-off window"),
        ("2–8 weeks (Amber)",
         '=COUNTIFS(tblMaster[Type],"Event",tblMaster[RAG],"Amber")',
         AMBER,
         "Pre-event comms / prep"),
        ("8–10 weeks (Green)",
         '=COUNTIFS(tblMaster[Type],"Event",tblMaster[RAG],"Green")',
         GREEN,
         "Marketing activation"),
        ("Revenue Booked",
         '=SUM(tblMaster[Revenue])',
         PURPLE,
         "All rows — see Master for detail"),
    ]
    kpi_row = 7
    col = 2
    tile_w = 3
    for label, value, fill, sub in tiles:
        ws.merge_cells(start_row=kpi_row, end_row=kpi_row,
                       start_column=col, end_column=col + tile_w - 1)
        lab = ws.cell(row=kpi_row, column=col, value=label)
        lab.font = Font(name=FONT, size=10, bold=True, color=WHITE)
        lab.fill = PatternFill("solid", fgColor=fill)
        lab.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.row_dimensions[kpi_row].height = 20

        ws.merge_cells(start_row=kpi_row + 1, end_row=kpi_row + 2,
                       start_column=col, end_column=col + tile_w - 1)
        v = ws.cell(row=kpi_row + 1, column=col, value=value)
        v.font = Font(name=FONT, size=28, bold=True, color=fill)
        v.fill = PatternFill("solid", fgColor=WHITE)
        v.alignment = Alignment(horizontal="center", vertical="center")
        v.border = Border(left=Side(style="medium", color=fill),
                          right=Side(style="medium", color=fill),
                          bottom=Side(style="thin", color=fill))
        if label == "Revenue Booked":
            v.number_format = '£#,##0'
        ws.row_dimensions[kpi_row + 1].height = 28
        ws.row_dimensions[kpi_row + 2].height = 16

        ws.merge_cells(start_row=kpi_row + 3, end_row=kpi_row + 3,
                       start_column=col, end_column=col + tile_w - 1)
        s = ws.cell(row=kpi_row + 3, column=col, value=sub)
        s.font = Font(name=FONT, size=9, italic=True, color=GREY_DARK)
        s.fill = PatternFill("solid", fgColor=WHITE)
        s.alignment = Alignment(horizontal="center", vertical="center")
        s.border = Border(left=Side(style="medium", color=fill),
                          right=Side(style="medium", color=fill),
                          bottom=Side(style="medium", color=fill))
        ws.row_dimensions[kpi_row + 3].height = 16
        col += tile_w

    # ---- Events by month chart data ----
    data_start = 14
    ws.cell(row=data_start, column=2, value="Events by Month — 2026").font = Font(
        name=FONT, size=14, bold=True, color=NAVY)
    ws.cell(row=data_start, column=2).border = Border(
        bottom=Side(style="medium", color=MAGENTA))
    header_cells(ws, data_start + 1, ["Month", "Events", "Revenue"], start_col=2)
    # Live formulas: count events and sum revenue by month via COUNTIFS/SUMIFS
    for i, m in enumerate(range(1, 13)):
        row = data_start + 2 + i
        next_m_year = 2026 if m < 12 else 2027
        next_m = (m % 12) + 1
        count_f = (
            f'=COUNTIFS(tblMaster[Type],"Event",'
            f'tblMaster[Event Date],">="&DATE(2026,{m},1),'
            f'tblMaster[Event Date],"<"&DATE({next_m_year},{next_m},1))'
        )
        rev_f = (
            f'=SUMIFS(tblMaster[Revenue],tblMaster[Type],"Event",'
            f'tblMaster[Event Date],">="&DATE(2026,{m},1),'
            f'tblMaster[Event Date],"<"&DATE({next_m_year},{next_m},1))'
        )
        for c, v in enumerate([calendar.month_name[m], count_f, rev_f], start=2):
            cell = ws.cell(row=row, column=c, value=v)
            cell.font = Font(name=FONT, size=10, color=NAVY)
            cell.border = thin(GREY)
            if c == 4:
                cell.number_format = '£#,##0'
    m_last = data_start + 13
    ch = BarChart()
    ch.type = "col"
    ch.title = "Events by Month"
    ch.legend = None
    data_ref = Reference(ws, min_col=3, max_col=3,
                         min_row=data_start + 1, max_row=m_last)
    cats = Reference(ws, min_col=2, min_row=data_start + 2, max_row=m_last)
    ch.add_data(data_ref, titles_from_data=True)
    ch.set_categories(cats)
    ch.height = 8
    ch.width = 18
    for s in ch.series:
        s.graphicalProperties = GraphicalProperties(solidFill=NAVY)
    ws.add_chart(ch, "F14")

    # ---- RAG distribution pie ----
    rag_start = 29
    ws.cell(row=rag_start, column=2, value="RAG Distribution").font = Font(
        name=FONT, size=14, bold=True, color=NAVY)
    ws.cell(row=rag_start, column=2).border = Border(
        bottom=Side(style="medium", color=MAGENTA))
    header_cells(ws, rag_start + 1, ["RAG", "Meaning", "Events"], start_col=2)
    for i, k in enumerate(RAG_ORDER):
        row = rag_start + 2 + i
        cell = ws.cell(row=row, column=2, value=k)
        cell.fill = PatternFill("solid", fgColor=RAG_FILLS[k])
        cell.font = Font(name=FONT, size=10, bold=True, color=RAG_TEXT[k])
        cell.border = thin(GREY)
        c2 = ws.cell(row=row, column=3, value=RAG_LABEL[k])
        c2.font = Font(name=FONT, size=10, color=NAVY)
        c2.border = thin(GREY)
        # Live count
        c3 = ws.cell(row=row, column=4,
                     value=f'=COUNTIFS(tblMaster[Type],"Event",tblMaster[RAG],"{k}")')
        c3.font = Font(name=FONT, size=10, bold=True, color=NAVY)
        c3.border = thin(GREY)

    # ---- Close-out queue + upcoming lists ----
    list_row = 38
    # Close-out (left)
    ws.cell(row=list_row, column=2, value="Close-out Queue").font = Font(
        name=FONT, size=14, bold=True, color=RED)
    ws.cell(row=list_row, column=2).border = Border(
        bottom=Side(style="medium", color=RED))
    header_cells(ws, list_row + 1,
                 ["Date", "Ref", "Title", "NEL/Lead", "Missing"],
                 start_col=2, fill=RED)
    closeout = sorted([r for r in events_only if r["rag"] == "Black"],
                      key=lambda x: x["target"] or TODAY)
    for i, r in enumerate(closeout[:20]):
        row = list_row + 2 + i
        missing = []
        if not r["website_ok"]: missing.append("Website")
        if not r["slides_ok"]: missing.append("Slides")
        if not r["honoraria_ok"]: missing.append("Honoraria")
        if r["revenue"] > 0 and not r["invoice_no"]: missing.append("Invoice")
        vals = [r["target"], r["ref"], r["title"][:45], r["lead"],
                " / ".join(missing) if missing else "—"]
        for c, v in enumerate(vals, start=2):
            cell = ws.cell(row=row, column=c, value=v)
            cell.font = Font(name=FONT, size=9, color=NAVY)
            cell.border = thin(GREY)
            if c == 2:
                cell.number_format = "dd.mm.yyyy"
    if not closeout:
        ws.cell(row=list_row + 2, column=2,
                value="No events needing close-out — nice.").font = Font(
            name=FONT, italic=True, color=GREEN)

    # Upcoming 30 days (right)
    ws.cell(row=list_row, column=9, value="Upcoming — Next 30 Days").font = Font(
        name=FONT, size=14, bold=True, color=NAVY)
    ws.cell(row=list_row, column=9).border = Border(
        bottom=Side(style="medium", color=MAGENTA))
    header_cells(ws, list_row + 1,
                 ["Date", "Ref", "Title", "NEL/Lead", "Stage"],
                 start_col=9)
    upcoming = sorted([r for r in events_only
                       if r["target"] and TODAY <= r["target"] <= TODAY + dt.timedelta(days=30)],
                      key=lambda x: x["target"])
    for i, r in enumerate(upcoming[:25]):
        row = list_row + 2 + i
        vals = [r["target"], r["ref"], r["title"][:45], r["lead"], r["stage"]]
        for c, v in enumerate(vals, start=9):
            cell = ws.cell(row=row, column=c, value=v)
            cell.font = Font(name=FONT, size=9, color=NAVY)
            cell.border = thin(GREY)
            if c == 9:
                cell.number_format = "dd.mm.yyyy"
        st_cell = ws.cell(row=row, column=13)
        st_cell.fill = PatternFill("solid", fgColor=STAGE_FILLS[r["stage"]])
        st_cell.font = Font(name=FONT, size=9, bold=True,
                            color=STAGE_TEXT[r["stage"]])

    # Column widths
    colw(ws, {"A": 2, "B": 13, "C": 10, "D": 30, "E": 14, "F": 14, "G": 12,
              "H": 2, "I": 13, "J": 10, "K": 30, "L": 16, "M": 22, "N": 14,
              "O": 2, "P": 14, "Q": 18, "R": 14})

    # Footer note
    nrow = 70
    ws.merge_cells(start_row=nrow, end_row=nrow, start_column=2, end_column=14)
    ws.cell(row=nrow, column=2,
            value=("RAG is time-based against Target Date (see 'RAG Rules' tab). "
                   "Close-out queue = past events missing website upload, speaker slides, "
                   "honoraria form, or sponsor invoice.")).font = Font(
        name=FONT, size=9, italic=True, color=GREY_DARK)
    return ws


# =========================================================================
# Master
# =========================================================================
MASTER_COLS = [
    "Item Ref", "Type", "Title", "Sponsor", "Format", "Location",
    "Lead Person", "Current Stage", "RAG",
    "Event Date", "Date Went Live",
    "Speaker Confirmed?", "Marketing Sent?", "Slides Received?", "Honoraria Received?",
    "Delegates", "Revenue", "Spend", "Invoice Status", "Invoice No.",
    "Notes",
]

MASTER_COL_HELP = {
    "Item Ref": "Unique code for this item, e.g. F2FCAR0402 or ROSTOO01. Don't reuse.",
    "Type": "Pick from dropdown: Event, Toolkit, Blog, Newsletter, Banner, Neighbourhood Banner, or Marker (holidays/blockers).",
    "Title": "Short description of what this is — e.g. 'Cardiovascular Disease — case-based approach'.",
    "Sponsor": "Who's paying or commissioning. Leave blank if none.",
    "Format": "For events only. F2F / F2F-NEL / WEB-National / WEB-Masterclass / WEB-Bespoke / WEB-Local.",
    "Location": "City or 'UK' for webinars.",
    "Lead Person": "NEL running the event, or MORPh team member owning the deliverable.",
    "Current Stage": "Pick the stage this item is at. Drives the RAG and the dashboard.",
    "RAG": "Auto-calculated from Event Date. Don't edit unless overriding.",
    "Event Date": "The date the event runs, or the date content goes live. Use the date picker.",
    "Date Went Live": "Only fill in once the item is live or the event has run.",
    "Speaker Confirmed?": "Yes once speaker has signed up in writing (or N/A for non-events).",
    "Marketing Sent?": "Yes once the 8-week marketing mailer has gone out.",
    "Slides Received?": "Yes once speaker has handed over slides (needed to close out).",
    "Honoraria Received?": "Yes once speaker's honoraria + expenses form is signed off.",
    "Delegates": "Number of registered delegates (or expected attendees).",
    "Revenue": "Gross revenue excluding VAT. Displays as £.",
    "Spend": "Speaker fee + venue + other costs. Displays as £.",
    "Invoice Status": "Booked / Invoiced / Paid / — (if none).",
    "Invoice No.": "The sponsor's invoice number once raised.",
    "Notes": "Free text. Use for anything the columns don't cover.",
}


def rag_formula(row):
    """Live RAG formula — recalculates from Event Date and Current Stage."""
    return (
        f'=IFS('
        f'H{row}="X. Cancelled","White",'
        f'J{row}="","White",'
        f'AND(J{row}<TODAY(),H{row}<>"8. Closed"),"Black",'
        f'J{row}<TODAY(),"White",'
        f'J{row}-TODAY()<=14,"Red",'
        f'J{row}-TODAY()<=56,"Amber",'
        f'J{row}-TODAY()<=70,"Green",'
        f'TRUE,"White"'
        f')'
    )


def build_master(wb, rows):
    ws = wb.create_sheet("Master", 1)
    landscape(ws)
    title_block(ws, 1, "Master — Events & Sponsorship 2026",
                "Add / update rows here. Dashboard, At Risk, Close-out and month tabs all pull from this table.",
                span=len(MASTER_COLS))
    header_cells(ws, 4, MASTER_COLS)
    # Add hover comments on each header explaining what goes in that column
    for i, h in enumerate(MASTER_COLS):
        help_text = MASTER_COL_HELP.get(h)
        if help_text:
            ws.cell(row=4, column=i + 1).comment = Comment(help_text, "MORPh Tracker")
    first = 5
    rows_sorted = sorted(rows, key=lambda r: (r["target"] or dt.date(2100, 1, 1),
                                               r["ref"]))
    for i, r in enumerate(rows_sorted):
        row = first + i
        vals = [
            r["ref"], r["type"], r["title"], r["sponsor"], r["format"], r["location"],
            r["lead"], r["stage"],
            rag_formula(row),                  # RAG — live formula, not static
            r["target"], r["live"],
            "Yes" if r["speaker_ok"] else "No",
            "Yes" if r["mkt_scheduled"] else "No",
            "Yes" if r["slides_ok"] else "No",
            "Yes" if r["honoraria_ok"] else "No",
            r["delegates"], r["revenue"], r["spend"],
            r["invoice_status"], r["invoice_no"], r["notes"],
        ]
        for c, v in enumerate(vals, start=1):
            cell = ws.cell(row=row, column=c, value=v)
            cell.font = Font(name=FONT, size=10, color=NAVY)
            cell.border = thin(GREY)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if c in (10, 11):
                cell.number_format = "dd.mm.yyyy"
            if c in (17, 18):
                cell.number_format = '£#,##0;[Red]-£#,##0;"—"'
        ws.row_dimensions[row].height = 32
    last = first + len(rows_sorted) - 1

    # Excel Table
    ref_range = f"A4:{get_column_letter(len(MASTER_COLS))}{last}"
    tbl = Table(displayName="tblMaster", ref=ref_range)
    tbl.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2", showFirstColumn=False,
        showRowStripes=True, showColumnStripes=False)
    ws.add_table(tbl)

    colw(ws, {"A": 14, "B": 9, "C": 34, "D": 16, "E": 10, "F": 18, "G": 16,
              "H": 22, "I": 9,
              "J": 12, "K": 12,
              "L": 10, "M": 10, "N": 10, "O": 10,
              "P": 9, "Q": 12, "R": 11, "S": 12, "T": 12, "U": 40})

    # Conditional formatting
    # Stage colour on H
    rng_stage = f"H{first}:H{last}"
    for s in STAGES:
        ws.conditional_formatting.add(
            rng_stage,
            CellIsRule(operator="equal", formula=[f'"{s}"'],
                       stopIfTrue=False,
                       fill=PatternFill("solid", fgColor=STAGE_FILLS[s]),
                       font=Font(name=FONT, bold=True,
                                 color=STAGE_TEXT[s], size=10)),
        )
    # RAG colour on I and also colour the whole row fill on RAG
    for rag, fill in RAG_FILLS.items():
        ws.conditional_formatting.add(
            f"I{first}:I{last}",
            CellIsRule(operator="equal", formula=[f'"{rag}"'],
                       stopIfTrue=False,
                       fill=PatternFill("solid", fgColor=fill),
                       font=Font(name=FONT, bold=True,
                                 color=RAG_TEXT[rag], size=10)),
        )
    # Row tint on RAG Red/Amber/Black (leave Green/White alone)
    for rag, fill in (("Black", "333333"), ("Red", "FADBDB"), ("Amber", "FCEACF")):
        ws.conditional_formatting.add(
            f"A{first}:{get_column_letter(len(MASTER_COLS))}{last}",
            FormulaRule(formula=[f'$I{first}="{rag}"'],
                        stopIfTrue=False,
                        fill=PatternFill("solid", fgColor=fill)))

    # Closed — just light grey tint, readable text (no strikethrough/italic)
    ws.conditional_formatting.add(
        f"A{first}:{get_column_letter(len(MASTER_COLS))}{last}",
        FormulaRule(formula=[f'$H{first}="8. Closed"'],
                    stopIfTrue=False,
                    fill=PatternFill("solid", fgColor=LIGHT_BG)))

    # Invoice colour
    for v, c in (("Booked", AMBER), ("Invoiced", PURPLE), ("Paid", GREEN)):
        ws.conditional_formatting.add(
            f"S{first}:S{last}",
            CellIsRule(operator="equal", formula=[f'"{v}"'], stopIfTrue=False,
                       fill=PatternFill("solid", fgColor=c),
                       font=Font(name=FONT, bold=True, color=WHITE, size=10)))

    # Data validations
    dv_list(ws, "B", first, last, ALL_TYPES)                     # Type
    dv_named(ws, "D", first, last, "rngSponsors")                # Sponsor
    dv_named(ws, "E", first, last, "rngFormats")                 # Format
    dv_named(ws, "G", first, last, "rngNELs")                    # Lead Person
    dv_list(ws, "H", first, last, STAGES)                        # Current Stage
    dv_list(ws, "I", first, last, RAG_ORDER)                     # RAG
    dv_list(ws, "S", first, last, INVOICE_STATUSES)              # Invoice Status
    for col in ("L", "M", "N", "O"):                             # Yes/No flags
        dv_list(ws, col, first, last, YESNO)

    ws.freeze_panes = "C5"


# =========================================================================
# RAG Rules tab
# =========================================================================
def build_rules(wb):
    ws = wb.create_sheet("RAG Rules", 2)
    landscape(ws)
    title_block(ws, 1, "RAG Rules & Close-out Definition",
                "Thresholds aligned to Event Delivery Process — edit here to change behaviour.",
                span=6)
    header_cells(ws, 4, ["RAG", "Meaning", "Trigger", "Maps to"])
    rules = [
        ("Black", "Close-out needed",
         "Event date in the past AND close-out incomplete",
         "Event Process Stage 8 — Post-Event Close"),
        ("Red", "≤ 2 weeks to event",
         "0–14 days until Target Date",
         "Stage 5 — Two-Week Cut-Off Review"),
        ("Amber", "2–8 weeks to event",
         "15–56 days until Target Date",
         "Stage 4 — Pre-Event Comms / Stage 6 — Pre-Event Prep"),
        ("Green", "8–10 weeks to event",
         "57–70 days until Target Date",
         "Stage 3 — Marketing Activation"),
        ("White", "Out of runway",
         ">70 days until Target Date, OR past & closed",
         "Stage 1 — Initiation (or closed)"),
    ]
    for i, (rag, meaning, trig, maps) in enumerate(rules):
        r = 5 + i
        c1 = ws.cell(row=r, column=1, value=rag)
        c1.fill = PatternFill("solid", fgColor=RAG_FILLS[rag])
        c1.font = Font(name=FONT, size=11, bold=True, color=RAG_TEXT[rag])
        c1.border = thin(GREY)
        for col, v in enumerate([meaning, trig, maps], start=2):
            c = ws.cell(row=r, column=col, value=v)
            c.font = Font(name=FONT, size=10, color=NAVY)
            c.border = thin(GREY)
            c.alignment = Alignment(wrap_text=True, vertical="center")
        ws.row_dimensions[r].height = 28

    # Close-out checklist
    ws.cell(row=12, column=1, value="Close-out checklist (must ALL be Yes)"
            ).font = Font(name=FONT, size=14, bold=True, color=NAVY)
    ws.cell(row=12, column=1).border = Border(
        bottom=Side(style="medium", color=MAGENTA))
    items = [
        ("Uploaded to website", "Attendance logged + recording/resources published"),
        ("Speaker Slides received", "Speaker has handed over slides for CPD evidence"),
        ("Honoraria Form received", "Speaker fees + expenses form signed off"),
        ("Sponsor Invoice raised", "For any row with Revenue > 0"),
    ]
    header_cells(ws, 13, ["Item", "What it means"])
    for i, (a, b) in enumerate(items):
        r = 14 + i
        ws.cell(row=r, column=1, value=a).font = Font(name=FONT, size=10, bold=True, color=NAVY)
        ws.cell(row=r, column=1).border = thin(GREY)
        ws.cell(row=r, column=2, value=b).font = Font(name=FONT, size=10, color=NAVY)
        ws.cell(row=r, column=2).border = thin(GREY)

    colw(ws, {"A": 30, "B": 38, "C": 40, "D": 40})


# =========================================================================
# At Risk + Close-out tabs
# =========================================================================
def build_at_risk(wb, rows):
    ws = wb.create_sheet("At Risk", 3)
    landscape(ws)
    title_block(ws, 1, "At Risk — Red + Amber",
                "Live view — updates automatically from Master. Events in the 8-week pre-event window.",
                span=9)
    header_cells(ws, 4, ["Item Ref", "Sponsor", "Type", "Title", "Format",
                         "Location", "Lead Person", "Current Stage", "RAG",
                         "Event Date"])
    # Live dynamic-array FILTER — spills rows where Type=Event AND RAG in (Red, Amber)
    filter_formula = (
        '=FILTER(CHOOSE({1,2,3,4,5,6,7,8,9,10},'
        'tblMaster[Item Ref],'
        'tblMaster[Sponsor],'
        'tblMaster[Type],'
        'tblMaster[Title],'
        'tblMaster[Format],'
        'tblMaster[Location],'
        'tblMaster[Lead Person],'
        'tblMaster[Current Stage],'
        'tblMaster[RAG],'
        'tblMaster[Event Date]),'
        '(tblMaster[Type]="Event")*'
        '((tblMaster[RAG]="Red")+(tblMaster[RAG]="Amber")))'
    )
    cell = ws.cell(row=5, column=1, value=filter_formula)
    cell.font = Font(name=FONT, size=10, color=NAVY)
    # Stretch formatting down for the spill range (up to 100 rows)
    for r in range(5, 60):
        for c in range(1, 11):
            ws.cell(row=r, column=c).border = thin(GREY)
            ws.cell(row=r, column=c).font = Font(name=FONT, size=10, color=NAVY)
            ws.cell(row=r, column=c).alignment = Alignment(vertical="top",
                                                           wrap_text=True)
        ws.cell(row=r, column=10).number_format = "dd.mm.yyyy"

    # Conditional formatting so stage + RAG cells colour-code in the spill
    rng_all = f"A5:J60"
    for s in STAGES:
        ws.conditional_formatting.add(
            f"H5:H60",
            CellIsRule(operator="equal", formula=[f'"{s}"'], stopIfTrue=False,
                       fill=PatternFill("solid", fgColor=STAGE_FILLS[s]),
                       font=Font(name=FONT, bold=True,
                                 color=STAGE_TEXT[s], size=10)))
    for rag, fill in RAG_FILLS.items():
        ws.conditional_formatting.add(
            f"I5:I60",
            CellIsRule(operator="equal", formula=[f'"{rag}"'], stopIfTrue=False,
                       fill=PatternFill("solid", fgColor=fill),
                       font=Font(name=FONT, bold=True,
                                 color=RAG_TEXT[rag], size=10)))

    colw(ws, {"A": 13, "B": 16, "C": 10, "D": 40, "E": 10, "F": 20,
              "G": 16, "H": 22, "I": 9, "J": 12})


def build_closeout(wb, rows):
    ws = wb.create_sheet("Close-out", 4)
    landscape(ws)
    title_block(ws, 1, "Close-out Queue",
                "Live view — past events where RAG=Black (Stage is not 8. Closed). Chase slides, honoraria, invoice.",
                span=9)
    header_cells(ws, 4, ["Event Date", "Item Ref", "Sponsor", "Title",
                         "Lead Person", "Slides Received?",
                         "Honoraria Received?", "Invoice No.", "Current Stage"])
    filter_formula = (
        '=FILTER(CHOOSE({1,2,3,4,5,6,7,8,9},'
        'tblMaster[Event Date],'
        'tblMaster[Item Ref],'
        'tblMaster[Sponsor],'
        'tblMaster[Title],'
        'tblMaster[Lead Person],'
        'tblMaster[Slides Received?],'
        'tblMaster[Honoraria Received?],'
        'tblMaster[Invoice No.],'
        'tblMaster[Current Stage]),'
        '(tblMaster[Type]="Event")*(tblMaster[RAG]="Black"))'
    )
    ws.cell(row=5, column=1, value=filter_formula).font = Font(
        name=FONT, size=10, color=NAVY)
    for r in range(5, 50):
        for c in range(1, 10):
            ws.cell(row=r, column=c).border = thin(GREY)
            ws.cell(row=r, column=c).font = Font(name=FONT, size=10, color=NAVY)
            ws.cell(row=r, column=c).alignment = Alignment(vertical="top",
                                                           wrap_text=True)
        ws.cell(row=r, column=1).number_format = "dd.mm.yyyy"

    # Colour slides/honoraria cells Red when "No", Green when "Yes"
    for col in ("F", "G"):
        ws.conditional_formatting.add(
            f"{col}5:{col}50",
            CellIsRule(operator="equal", formula=['"Yes"'], stopIfTrue=False,
                       fill=PatternFill("solid", fgColor=GREEN),
                       font=Font(name=FONT, bold=True, color=WHITE, size=10)))
        ws.conditional_formatting.add(
            f"{col}5:{col}50",
            CellIsRule(operator="equal", formula=['"No"'], stopIfTrue=False,
                       fill=PatternFill("solid", fgColor=RED),
                       font=Font(name=FONT, bold=True, color=WHITE, size=10)))
    # Colour stage column
    for s in STAGES:
        ws.conditional_formatting.add(
            f"I5:I50",
            CellIsRule(operator="equal", formula=[f'"{s}"'], stopIfTrue=False,
                       fill=PatternFill("solid", fgColor=STAGE_FILLS[s]),
                       font=Font(name=FONT, bold=True,
                                 color=STAGE_TEXT[s], size=10)))

    colw(ws, {"A": 12, "B": 13, "C": 16, "D": 40, "E": 16,
              "F": 12, "G": 14, "H": 13, "I": 22})


# =========================================================================
# Month calendar tabs — events coloured by RAG
# =========================================================================
def build_month_tabs(wb, rows):
    by_date: dict[dt.date, list] = {}
    for r in rows:
        if r.get("target") and r["target"].year == 2026:
            by_date.setdefault(r["target"], []).append(r)

    cal = calendar.Calendar(firstweekday=0)
    weekday_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for month in range(1, 13):
        name = calendar.month_name[month]
        ws = wb.create_sheet(name)
        landscape(ws)
        title_block(ws, 1, f"{name} 2026",
                    "Events coloured by RAG (see key below). All data from Master.",
                    span=7)
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
            ws.row_dimensions[hdr_row].height = 18
            ws.row_dimensions[body_row].height = 70
            ws.row_dimensions[hdr_row + 2].height = 2

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
                d_cell = ws.cell(row=hdr_row, column=col, value=day)
                d_cell.font = Font(name=FONT, size=11, bold=True, color=NAVY)
                d_cell.alignment = Alignment(horizontal="right",
                                              vertical="center", indent=1)
                d_cell.fill = PatternFill("solid",
                                           fgColor=GREY_LIGHT if dow in (5, 6) else LIGHT_BG)
                d_cell.border = Border(left=Side(style="thin", color=GREY),
                                        right=Side(style="thin", color=GREY),
                                        top=Side(style="thin", color=GREY))

                body = ws.cell(row=body_row, column=col)
                body.alignment = Alignment(horizontal="left",
                                            vertical="top",
                                            wrap_text=True, indent=1)
                body.border = Border(left=Side(style="thin", color=GREY),
                                      right=Side(style="thin", color=GREY),
                                      bottom=Side(style="thin", color=GREY))

                # Live TEXTJOIN formula — pulls all items with matching Event Date.
                # Excel 365 / Excel Online evaluates the IF array inside TEXTJOIN.
                body.value = (
                    f'=IFERROR(TEXTJOIN(CHAR(10),TRUE,'
                    f'IF(tblMaster[Event Date]=DATE(2026,{month},{day}),'
                    f'tblMaster[Item Ref]&" "&tblMaster[Sponsor]&" — "'
                    f'&tblMaster[Current Stage],"")),"")'
                )
                body.font = Font(name=FONT, size=9, color=NAVY, bold=True)

                # Live cell colour via Conditional Formatting — evaluates the
                # WORST RAG present on this date in Master. Black > Red > Amber > Green.
                # If events are added/updated in Master, the cell colour updates.
                cell_ref = f"{get_column_letter(col)}{body_row}"
                for rag in ("Black", "Red", "Amber", "Green"):
                    formula = (
                        f'COUNTIFS(tblMaster[Event Date],DATE(2026,{month},{day}),'
                        f'tblMaster[RAG],"{rag}")>0'
                    )
                    ws.conditional_formatting.add(
                        cell_ref,
                        FormulaRule(formula=[formula], stopIfTrue=True,
                                    fill=PatternFill("solid",
                                                      fgColor=RAG_FILLS[rag]),
                                    font=Font(name=FONT, size=9, bold=True,
                                              color=RAG_TEXT[rag])))

                # Row height scales with current items so populated cells
                # aren't squashed on first open. Excel users can resize later.
                if items:
                    needed = max(70, 16 * (len(items) * 2 + 1))
                    if needed > ws.row_dimensions[body_row].height:
                        ws.row_dimensions[body_row].height = needed

        colw(ws, {get_column_letter(c): 22 for c in range(1, 8)})

        # RAG key
        key_row = start_row + len(month_days) * 3 + 2
        ws.cell(row=key_row, column=1, value="RAG Key").font = Font(
            name=FONT, size=10, bold=True, color=NAVY)
        for i, k in enumerate(RAG_ORDER):
            r = key_row + 1 + i
            c = ws.cell(row=r, column=1, value=f"{k}  —  {RAG_LABEL[k]}")
            c.fill = PatternFill("solid", fgColor=RAG_FILLS[k])
            c.font = Font(name=FONT, size=10, bold=True, color=RAG_TEXT[k])
            c.border = thin(GREY)
            ws.merge_cells(start_row=r, end_row=r, start_column=1, end_column=3)
        ws.sheet_properties.tabColor = NAVY


# =========================================================================
# Build
# =========================================================================
def build():
    rows = build_dataset()
    rows = [r for r in rows if r["ref"] or r["title"]]
    sponsors, nels, formats = extract_lookups()
    print(f"Loaded {len(rows)} items")
    breakdown = {}
    for r in rows:
        breakdown.setdefault(r["type"], 0)
        breakdown[r["type"]] += 1
    print("  by type:", breakdown)
    rag_count = {k: 0 for k in RAG_ORDER}
    for r in rows:
        if r["type"] == "Event":
            rag_count[r["rag"]] += 1
    print("  event RAG:", rag_count)
    print(f"  dropdown sources: {len(sponsors)} sponsors, "
          f"{len(nels)} NELs, {len(formats)} formats")

    wb = Workbook()
    wb.remove(wb.active)
    # Lists sheet FIRST so named ranges exist before other sheets use them
    build_lists_sheet(wb, sponsors, nels, formats)
    build_master(wb, rows)
    build_rules(wb)
    build_at_risk(wb, rows)
    build_closeout(wb, rows)
    build_dashboard(wb, rows)
    build_how_to_use(wb)
    build_month_tabs(wb, rows)

    # Order: How to Use first, then Dashboard, Master, reference tabs, months, Lists hidden
    order = ["How to Use", "Dashboard", "Master", "RAG Rules",
             "At Risk", "Close-out"] + [
        calendar.month_name[m] for m in range(1, 13)
    ] + ["Lists"]
    wb._sheets = [wb[n] for n in order]

    wb["How to Use"].sheet_properties.tabColor = MAGENTA
    wb["Dashboard"].sheet_properties.tabColor = PURPLE
    wb["Master"].sheet_properties.tabColor = NAVY
    wb["RAG Rules"].sheet_properties.tabColor = GREY_DARK
    wb["At Risk"].sheet_properties.tabColor = AMBER
    wb["Close-out"].sheet_properties.tabColor = RED

    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.xlsx"):
        old.unlink()
    for old in OUT.glob("*.pdf"):
        old.unlink()
    outpath = OUT / "morph-events-tracker-2026.xlsx"
    wb.save(outpath)
    print(f"Saved: {outpath}")
    return outpath


if __name__ == "__main__":
    build()
