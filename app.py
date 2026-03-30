import streamlit as st

# pages
resume = st.Page(
    page = 'pages/resume.py',
    title = 'Resume',
    icon = ':material/contact_page:',
    default = True
)
pfx_analysis = st.Page(
    page = 'pages/pfx_analysis.py',
    title = '2025 MLB PFX Analysis',
    icon = ':material/analytics:',
)
senior_thesis = st.Page(
    page = 'pages/senior_thesis.py',
    title = 'Senior Thesis',
    icon = ':material/insert_chart:'
)
ufc_323_analysis = st.Page(
    page = 'pages/ufc_323_analysis.py',
    title = 'UFC 323 Analysis',
    icon = ':material/sports_mma:'
)
pitch_charts = st.Page(
    page = 'pages/pitch_charts.py',
    title = '2026 MLB Pitch Charts',
    icon = ':material/sports_baseball:',
)

# link pages to site
pg = st.navigation({
    "About Me": [resume],
    "Projects": [senior_thesis, pfx_analysis, ufc_323_analysis, pitch_charts],
})

# run
pg.run()