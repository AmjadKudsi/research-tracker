"""
config.py
Centralized configuration for the research tracker app.
"""

# Path to your Excel workbook
EXCEL_PATH = "Research.xlsx"

# All SDLC / research phases you're tracking.
# These strings are used only for coverage stats in the dashboard.
ALL_PHASES = [
    "Phase 1",
    "Phase 2",
    "Phase 3",
    "Phase 4",
    "Phase 5",
    "Phase 6",
    "Phase 7",
    "Phase 8",
    "Phase 9",
    "Phase 10",
]

# Columns (for clarity / future-proofing)
COLUMN_ORDER = ["Name", "Category", "Date", "Notes", "Link"]
COLUMN_LETTERS = {
    "Name": "A",
    "Category": "B",
    "Date": "C",
    "Notes": "D",
    "Link": "E",
}
