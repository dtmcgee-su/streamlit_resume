import streamlit as st

# pages
resume = st.Page(
    page = 'pages/resume.py',
    title = 'Resume',
    icon = ':material/contact_page:',
    default = True
)
dashboard = st.Page(
    page = 'pages/dashboard.py',
    title = 'Dashboard',
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
    "Projects": [senior_thesis, dashboard]
})

# run
pg.run()