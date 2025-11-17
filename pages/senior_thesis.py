import streamlit as st

st.title('Senior Thesis')

with open('media/pdf/dylan_mcgee_senior_thesis_literature_review.pdf', "rb") as f:
    pdf_data = f.read()

st.download_button(
    label="📄 Download Literature Review",
    data=pdf_data,
    file_name="media/pdf/dylan_mcgee_senior_thesis_literature_review.pdf",
    mime="application/pdf"
)

with open('media/pdf/dylan_mcgee_senior_thesis_poster.pdf', "rb") as f:
    pdf_data = f.read()

st.download_button(
    label="📄 Download PDF",
    data=pdf_data,
    file_name="media/pdf/dylan_mcgee_senior_thesis_poster.pdf",
    mime="application/pdf"
)





st.image('./media/images/dylan_mcgee_senior_thesis.png',  use_container_width="always")

