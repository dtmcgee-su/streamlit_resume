import streamlit as st

# pages
resume = st.Page(
    page = 'pages/resume.py',
    title = 'Resume',
    icon = ':material/contact_page:',
    default = True
)
pfx_analysis = st.Page(
    page = 'pages/2025_pfx_analysis.py',
    title = '2025 MLB PFX Analysis',
    icon = ':material/analytics:',
)
senior_thesis = st.Page(
    page = 'pages/senior_thesis.py',
    title = 'Senior Thesis',
    icon = ':material/insert_chart:'
)


# link pages to site
pg = st.navigation({
    "About Me": [resume],
    "Projects": [senior_thesis, pfx_analysis]
})

# run
pg.run()