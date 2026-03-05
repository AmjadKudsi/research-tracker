# Research Coverage Tracker

> **Full-Stack Cloud Deployment** · Streamlit · Google Sheets API · gspread · GitHub CI/CD · OAuth2 Service Account

---

## Screenshot

![App UI](assets/ui.png)

---

## Overview

A persistent, cloud-hosted research paper tracking dashboard for monitoring SDLC phase coverage across 10 phases. Built with a modular Python architecture and a Google Sheets persistence layer, deployed on Streamlit Community Cloud with zero infrastructure management.

The backend was architected to be fully swappable — the UI and orchestration layers (`app.py`, `ui_components.py`) have no knowledge of the storage implementation, meaning the persistence layer was migrated from local `openpyxl`/Excel to the Google Sheets API without touching a single line of UI code.

---

## Architecture

```
research-tracker/
├── app.py              # Orchestration: load → render → write → rerun
├── config.py           # Centralised config: phases, column order, Excel path
├── excel_utils.py      # Persistence layer: Google Sheets read/write + metrics
├── ui_components.py    # All rendering: CSS injection, KPI cards, form, phase cards
├── requirements.txt    # Runtime dependencies
└── .streamlit/
    └── secrets.toml    # GCP service account + sheet URL (git-ignored)
```

---

## Features

- **Form-based paper ingestion** — title, category/phase, date, notes, URL, security flag
- **Recent additions panel** — last 10 rows appended to the sheet, displayed newest-first
- **KPI cards** — total papers tracked · phase coverage (n/10) · security-focused paper ratio
- **Phase coverage cards** — per-phase paper counts, colour-coded by threshold:
  - 🔴 0 papers · 🟠 1–3 · 🟡 4–6 · 🟢 7+
- **Dark-themed UI** — fully custom CSS injected via `st.markdown()`, Streamlit default chrome suppressed

---

## Technical Implementation

### Persistence Layer — Google Sheets API

Authentication uses a GCP service account with scoped OAuth2 credentials (`spreadsheets` + `drive.readonly`). The client is decorated with `@st.cache_resource` to prevent redundant authentication handshakes on each Streamlit rerun.

```python
@st.cache_resource
def _get_client() -> gspread.Client:
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=_SCOPES
    )
    return gspread.authorize(creds)
```

Sheet reads use `get_all_values()` rather than `get_all_records()` to handle the dynamic formula-based column header (`=COUNTA(...)`) in column A, which caused `gspread` to raise `GSpreadException`. Clean column names are applied deterministically post-read.

### Metrics Engine

All KPI values are computed in `get_metrics()` from the loaded DataFrame:
- **Phase coverage** — `value_counts()` on the Category column, matched against the 10-phase allowlist in `config.py`
- **Security ratio** — boolean mask on the Security column (`str.lower() == "yes"`), expressed as `%` of total
- **Phase gap cards** — per-phase counts passed to the renderer with threshold-based CSS class selection

### Secrets Management

Credentials are injected via Streamlit's encrypted secrets manager. The GCP private key is stored as a TOML triple-quoted block string to preserve PEM line breaks.


---

## Deployment

The app is deployed on **Streamlit Community Cloud**, connected directly to this GitHub repository. Every `git push` to `main` triggers an automatic redeploy.

### Local Setup

```bash
git clone https://github.com/AmjadKudsi/research-tracker.git
cd research-tracker
pip install -r requirements.txt

# Create secrets file
mkdir .streamlit
# Populate .streamlit/secrets.toml — see Secrets section below

streamlit run app.py
```

### Secrets format (`.streamlit/secrets.toml`)

```toml
[google_sheet]
url = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"

[gcp_service_account]
type                        = "service_account"
project_id                  = "..."
private_key_id              = "..."
private_key                 = """-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----
"""
client_email                = "...@....iam.gserviceaccount.com"
client_id                   = "..."
auth_uri                    = "https://accounts.google.com/o/oauth2/auth"
token_uri                   = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url        = "..."
universe_domain             = "googleapis.com"
```

### Google Sheet setup

1. Create a sheet with this column order in row 1:
   `Name | Date | Notes | Category | Link | Security`
   *(Column A uses the formula `="Name (count = "&COUNTA(A2:A1048576)&")"` — handled automatically)*
2. Share the sheet with the service account `client_email` as **Editor**

---

## Dependencies

```
streamlit
pandas
gspread
google-auth
```

---

## Author

**Amjad Ali**
