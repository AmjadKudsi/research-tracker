import streamlit as st
from excel_utils import load_sheet, get_metrics, append_row_to_excel
from ui_components import render_header, render_form, render_phase_gap_cards

def main():
    st.set_page_config(page_title="Research Tracker", layout="wide")

    df = load_sheet()
    metrics = get_metrics(df)

    # 1. Header and latest additions
    render_header(df, metrics)

    # 2. Form (in between header & coverage section)
    new_entry = render_form()
    if new_entry:
        try:
            append_row_to_excel(new_entry)
            df = load_sheet() # Reload to reflect new data
            st.success("Paper added successfully.")
            st.rerun()
        except PermissionError:
            st.error("Close the Excel file before adding a new entry.")


    # 3. Bottom section
    render_phase_gap_cards(metrics)

if __name__ == "__main__":
    main()
