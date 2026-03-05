# Research Tracker

A lightweight Streamlit dashboard for tracking research papers across SDLC phases. Log papers, flag security relevance, and monitor phase coverage — all backed by a local Excel file.

---

## Features

- **Add papers** via a simple form (title, category/phase, date, notes, link, security flag)
- **Recent additions** panel showing the last 10 entries
- **KPI cards** for total papers tracked, phase coverage, and security-focused papers
- **Phase coverage cards** (Phases 1–10) with colour-coded status:
  - 🔴 0 papers · 🟠 1–3 · 🟡 4–6 · 🟢 7+
- Dark-themed UI

---

## Project Structure

```
├── app.py              # Main Streamlit entry point
├── config.py           # Excel path, phase list, column config
├── excel_utils.py      # Read / write helpers for the Excel workbook
├── ui_components.py    # All rendering functions (header, form, cards)
├── requirements.txt    # Python dependencies
└── Research.xlsx       # Your data file (not committed — see below)
```

---

## Setup (Local)

### Prerequisites
- Python 3.9+
- `pip`

### Install & run

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/research-tracker.git
cd research-tracker

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Excel file
# Place your Research.xlsx in the project root.
# The expected columns are: Name, Category, Date, Notes, Link, Security

# 4. Run the app
streamlit run app.py
```

---

## Configuration

Edit `config.py` to customise the app:

| Setting | Description |
|---|---|
| `EXCEL_PATH` | Path to the Excel workbook (default: `Research.xlsx`) |
| `ALL_PHASES` | List of SDLC phases to track coverage for |
| `COLUMN_ORDER` | Column names expected in the workbook |

---

## Dependencies

```
streamlit
pandas
openpyxl
```

---

## Author

**Amjad Ali**
