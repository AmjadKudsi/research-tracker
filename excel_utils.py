"""
excel_utils.py  (Google Sheets backend)
Drop-in replacement for the original openpyxl version.
All public function signatures are identical so app.py needs no changes.

Setup
-----
1. Create a Google Sheet with this header row in Sheet1:
   Name | Category | Date | Notes | Link | Security

2. Share the sheet with your service-account e-mail (Editor access).

3. Add credentials to .streamlit/secrets.toml (local) or
   Streamlit Cloud → App settings → Secrets (deployed).
   See README for the exact format.
"""

import pandas as pd
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# ── auth ──────────────────────────────────────────────────────────────────────

_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
]

@st.cache_resource
def _get_client() -> gspread.Client:
    """Authenticate once and reuse the client across reruns."""
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=_SCOPES,
    )
    return gspread.authorize(creds)


def _get_worksheet() -> gspread.Worksheet:
    client = _get_client()
    sheet_url = st.secrets["google_sheet"]["url"]
    spreadsheet = client.open_by_url(sheet_url)
    return spreadsheet.sheet1


# ── public API (identical to the original excel_utils) ────────────────────────

def load_sheet() -> pd.DataFrame:
    """
    Return the Google Sheet as a DataFrame.
    Row 1 is treated as the header row.
    """
    ws = _get_worksheet()
    records = ws.get_all_records(expected_headers=["Name", "Category", "Date", "Notes", "Link", "Security"])
    df = pd.DataFrame(records)
    return df


def append_row_to_excel(entry: dict):
    """
    Append a new paper row to the bottom of the sheet.
    Parameter name kept as-is so app.py needs no changes.
    """
    ws = _get_worksheet()
    ws.append_row(
        [
            entry.get("Name", ""),
            entry.get("Category", ""),
            entry.get("Date", ""),
            entry.get("Notes", ""),
            entry.get("Link", ""),
            entry.get("Security", "No"),
        ],
        value_input_option="USER_ENTERED",
    )


def get_metrics(df: pd.DataFrame) -> dict:
    """
    Values for the KPI cards.
    Identical logic to the original; no changes needed here.
    """
    df_clean = df.dropna(how="all")
    total_papers = len(df_clean)

    if "Category" in df_clean.columns:
        phase_counts = (
            df_clean["Category"]
            .value_counts(dropna=True)
            .to_dict()
        )
    else:
        phase_counts = {}

    all_phases = [
        "Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5",
        "Phase 6", "Phase 7", "Phase 8", "Phase 9", "Phase 10",
    ]

    covered = [p for p in all_phases if phase_counts.get(p, 0) > 0]
    coverage_text = f"{len(covered)} / {len(all_phases)} phases covered"

    if "Security" in df_clean.columns:
        security_mask = df_clean["Security"].astype(str).str.strip().str.lower() == "yes"
        security_papers = int(security_mask.sum())
    else:
        security_papers = 0

    if total_papers > 0:
        pct = round((security_papers / total_papers) * 100)
        security_ratio_pct = f"{pct}% of total"
    else:
        security_ratio_pct = "0% of total"

    phase_gap_info = [
        {"phase": phase, "count": phase_counts.get(phase, 0)}
        for phase in all_phases
    ]

    return {
        "total_papers": total_papers,
        "phase_coverage_text": coverage_text,
        "phase_gap_info": phase_gap_info,
        "security_papers": security_papers,
        "security_ratio_pct": security_ratio_pct,
    }
