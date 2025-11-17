import streamlit as st

# pages
about_me = st.Page(
    page = 'pages/about_me.py',
    title = 'About Me',
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
    "About Me": [about_me],
    "Projects": [senior_thesis, dashboard]
})

# run
pg.run()