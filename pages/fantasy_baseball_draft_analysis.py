# init
# app.py
# Step 1 (MVP): Upload a CSV and display it in Streamlit.
#
# Run:
#   pip install streamlit pandas
#   streamlit run app.py

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Fantasy Draft Tool (MVP)", layout="wide")

st.title("Fantasy Baseball Draft Tool — MVP")
st.caption("Step 1: Upload a hitters projections CSV and display it.")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is None:
    st.info("Upload a CSV to get started.")
    st.stop()

# Read the CSV
try:
    df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"Could not read that CSV: {e}")
    st.stop()

# Basic summary
st.subheader("Preview")
c1, c2, c3 = st.columns(3)
c1.metric("Rows", f"{len(df):,}")
c2.metric("Columns", f"{df.shape[1]:,}")
c3.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")

# Controls
with st.expander("Display options", expanded=False):
    show_cols = st.multiselect("Columns to show", options=df.columns.tolist(), default=df.columns.tolist())
    max_rows = st.slider("Max rows to display", min_value=25, max_value=500, value=200, step=25)

# Display dataframe
st.dataframe(df[show_cols].head(max_rows), use_container_width=True)

# Optional: download back (useful to confirm ingest)
st.download_button(
    "Download the uploaded CSV (as-is)",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="uploaded.csv",
    mime="text/csv",
)