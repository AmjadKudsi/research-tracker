import streamlit as st
import pandas as pd
import streamlit.components.v1 as components  # you already import this


def _inject_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #000000;
            color: #FFFFFF;
        }

        /* Hide Streamlit top header bar */
        header[data-testid="stHeader"] {
            display: none !important;
        }

        /* Remove default top gap left by header */
        main.block-container {
            padding-top: 1rem !important;
            padding-bottom: 4rem;
        }

        /* Top title bar for the page */
        .main-title-block {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: flex-end;
            padding-top: 1rem;
            padding-bottom: 1rem;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid #333333;
        }

        .main-title-left {
            font-size: 2.3rem;
            line-height: 1.2rem;
            font-weight: 900;
            color: #FFFFFF;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
        }

        .main-title-right {
            font-size: 1.5rem;
            line-height: 1rem;
            font-weight: 500;
            color: #888888;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
        }

        /* Section header (Most recent 10 additions, Coverage status by phase, etc.) */
        .section-header {
            background-color: #111111;
            color: #FFFFFF;
            font-size: 0.8rem;
            font-weight: 500;
            padding: 0.4rem 0.6rem;
            border: 1px solid #333333;
            border-radius: 4px;
            margin-bottom: 0.5rem;
        }

        .metric-card {
            background-color: #111111;
            border: 1px solid #333333;
            border-radius: 6px;
            padding: 0.8rem 1rem;
            min-height: 4.5rem;
        }
        .metric-label {
            font-size: 0.7rem;
            font-weight: 500;
            color: #AAAAAA;
            margin-bottom: 0.4rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .metric-value {
            font-size: 1.2rem;
            font-weight: 600;
            color: #FFFFFF;
            line-height: 1.2rem;
        }

        .gap-card {
            background-color: #111111;
            border: 1px solid #333333;
            border-radius: 6px;
            padding: 0.8rem 1rem;
            min-height: 4.5rem;
        }
        .gap-phase {
            font-size: 0.8rem;
            font-weight: 500;
            color: #FFFFFF;
            margin-bottom: 0.4rem;
        }
        .gap-count-0 {
            font-size: 0.75rem;
            color: #ff5252;
        }
        .gap-count-low {
            font-size: 0.75rem;
            color: #ff9100;
        }
        .gap-count-mid {
            font-size: 0.75rem;
            color: #ffea00;
        }
        .gap-count-high {
            font-size: 0.75rem;
            color: #00c853;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_page_header():
    """Top title bar with page name on the left and owner on the right."""
    st.markdown(
        """
        <div class="main-title-block">
            <div class="main-title-left">Research Tracker</div>
            <div class="main-title-right">Amjad Ali</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_metric_cards(metrics: dict):
    """
    Renders the 3 KPI cards in one row:
    1. Total papers tracked
    2. SDLC coverage
    3. Security focus
    """

    total_papers = metrics.get("total_papers", 0)
    coverage_text = metrics.get("phase_coverage_text", "")

    security_papers = metrics.get("security_papers", 0)
    security_ratio_pct = metrics.get("security_ratio_pct", "0% of total")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total papers tracked</div>
                <div class="metric-value">{total_papers}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Phase coverage</div>
                <div class="metric-value">{coverage_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Security focus</div>
                <div class="metric-value">{security_papers} papers <span style="font-size:0.8rem; color:#AAAAAA;">({security_ratio_pct})</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_header(df: pd.DataFrame, metrics: dict):
    """
    Renders:
    1. CSS
    2. Title + KPI cards
    3. Last 10 appended entries from Excel (not sorted by date)
       Showing only Name / Category / Notes.
    """

    _inject_css()

    # page header bar
    render_page_header()

    # KPI cards row
    render_metric_cards(metrics)

    # section label
    st.markdown(
        '<div class="section-header">Most recent 10 additions</div>',
        unsafe_allow_html=True,
    )

    # work on a copy so we do not mutate df
    df_local = df.copy()

    # drop any fully empty rows that pandas pulled in from the sheet
    df_local = df_local.dropna(how="all")

    # figure out the Excel first column header
    # this is something like "Name (count = 5)"
    title_col = df_local.columns[0] if len(df_local.columns) > 0 else None

    # take the LAST 10 rows as written in Excel
    # tail(10) gives you the bottom 10 rows, which are the newest appends
    last10 = df_local.tail(10)

    # reverse them so newest appears first in the preview
    last10 = last10.iloc[::-1].reset_index(drop=True)

    # choose columns to show: Name col, Category, Notes
    cols_for_display = []
    if title_col and title_col in last10.columns:
        cols_for_display.append(title_col)
    if "Category" in last10.columns:
        cols_for_display.append("Category")
    if "Notes" in last10.columns:
        cols_for_display.append("Notes")

    st.dataframe(
        last10[cols_for_display],
        use_container_width=True,
        hide_index=True,
    )


def render_form():
    """Form to add a new paper row to Excel."""
    st.markdown(
        '<div class="section-header">Add a new paper</div>',
        unsafe_allow_html=True,
    )

    name = st.text_input("Paper title")
    category = st.text_input("Category / Phase (e.g. Phase 1)")
    date = st.text_input("Published date (e.g. Sep-25)")
    notes = st.text_area("Notes (bullets allowed)")
    link = st.text_input("Link to paper (URL)")
    security_flag = st.checkbox("Security relevant (vulns / threat / mitigation / secure code etc.)", value=False)

    submitted = st.button("Submit", use_container_width=True)

    if submitted:
        if not name.strip():
            st.warning("Please provide a paper title.")
            return None

        return {
            "Name": name.strip(),
            "Category": category.strip(),
            "Date": date.strip(),
            "Notes": notes.strip(),
            "Link": link.strip(),
            "Security": "Yes" if security_flag else "No",
        }

    return None


def render_phase_gap_cards(metrics: dict):
    """
    Show coverage cards for Phase 1 ... Phase 10.
    Color encodes coverage:
      0 -> red
      1-3 -> orange
      4-6 -> yellow
      7+ -> green
    """

    phase_list = metrics.get("phase_gap_info", [])

    st.markdown(
        '<div class="section-header" style="margin-top:2rem;">Coverage status by phase</div>',
        unsafe_allow_html=True,
    )

    chunk_size = 5
    for i in range(0, len(phase_list), chunk_size):
        row = phase_list[i:i + chunk_size]
        cols = st.columns(len(row))
        for (info, col) in zip(row, cols):
            phase = info.get("phase", "Phase ?")
            count = info.get("count", 0)

            # choose css class based on count
            if count == 0:
                cls = "gap-count-0"
            elif count <= 3:
                cls = "gap-count-low"
            elif count <= 6:
                cls = "gap-count-mid"
            else:
                cls = "gap-count-high"

            with col:
                st.markdown(
                    f"""
                    <div class="gap-card">
                        <div class="gap-phase">{phase}</div>
                        <div class="{cls}">
                            {count} papers
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )



def render_gaps_section(metrics: dict):
    """
    Keep this around if you still want the old monolithic block
    somewhere else. Otherwise you can delete this after you switch
    app.py to render_phase_gap_cards().
    """
    gap_lines = metrics.get("gap_lines", [])
    if not gap_lines:
        return

    block_html_lines = []
    for line in gap_lines:
        if "under-covered" in line:
            block_html_lines.append(f'<div class="gap-line-warn">{line}</div>')
        else:
            block_html_lines.append(f'<div class="gap-line-ok">{line}</div>')

    joined = "\n".join(block_html_lines)
    st.markdown(
        f'<div class="gaps-block">{joined}</div>',
        unsafe_allow_html=True,
    )
