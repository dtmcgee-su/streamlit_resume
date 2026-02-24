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
fantasy_baseball_draft_analysis = st.Page(
    page = 'pages/fantasy_baseball_draft_analysis.py',
    title = 'Fantasy Baseball Draft Tool (MVP)',
    icon = ':material/sports_baseball:',
)

# link pages to site
pg = st.navigation({
    "About Me": [resume],
    "Projects": [senior_thesis, pfx_analysis, ufc_323_analysis],
})

# run
pg.run()