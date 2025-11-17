import streamlit as st 
from forms.contact import contact_form


st.html("""
    <style>
        .stMainBlockContainer {
            max-width:70rem;
        }
    </style>
    """
)

@st.dialog('Contact Me')
def show_contact_form():
    contact_form()

main_col1, main_col2 = st.columns([4,1], gap='small', vertical_alignment='top', border=True)
with main_col1:


    
    sub_col1, sub_col2 = st.columns([1,2], gap='small', vertical_alignment='center')
    with sub_col1: 
        st.image('./media/images/dylan_mcgee_profile_photo_cropped.png', width = 250)
    with sub_col2:
        st.title('Dylan McGee')
        st.write('Data Scientist with 5 years of experience converting data into actionable insights across sports ticketing and brand sponsorship.')
        btn1, btn2 = st.columns(2, gap='small', vertical_alignment='center')
        with btn1:
            if st.button('Contact Me'):
                show_contact_form()
        with btn2:
            with open('media/pdf/dylan_mcgee_resume.pdf', "rb") as f:
                pdf_data = f.read()
            st.download_button(
                label="Download Resume",
                data=pdf_data,
                file_name="dylan_mcgee_resume.pdf",
                mime="application/pdf"
)


    # experience
    st.write("\n")
    st.subheader('Experience', anchor=False, divider = 'gray')
    st.badge('Eventellect')
    st.write(
        f"""
        Data Scientist | Houston, TX | 05/2024 - 11/2025
        - Designed, built, and optimized statistical and machine learning models, improving predictive accuracy and driving measurable business outcomes.
        - Led end-to-end model development lifecycle, including feature engineering, model selection, hyperparameter tuning, and performance monitoring.
        - Developed automated data pipelines to ingest, clean, transform, and store data, reducing manual workload and increasing reliability.
        - Communicated with internal stakeholders on how to use data science products to drive value. 
        ---
        """
    )
    st.badge('MVPIndex')
    st.write(
        """
        Data Scientist | Austin, TX (Remote) | 11/2021 – 05/2024 

        - Led algorithm selection and optimization, utilizing machine learning, statistical modeling, and decision  theory to control data-driven decision making. 
        - Managed production, maintenance, and versioning of 75+ computer vision models, reducing production costs by  80% and improving data quality. 
        - Oversaw a team creating labeled datasets, resulting in a $1,000,000.00 deal with the National Hockey League. 
        - Automated data delivery to clients using jobs/workflows in Databricks, enhancing accessibility and efficiency with  Python, SQL, AWS, and an internal API. 
        - Processed and analyzed big data, optimizing data pulls for 5x faster execution times via Spark and delta tables. 
        - Integrated APIs (Sportradar, Sieve, X, Meta and more) into various data pipelines within the data science department. 
        ---
    
        """
    )
    st.badge('Major League Baseball')
    st.write(
        """
        IT Intern | New York, NY | 06/2019 - 09/2019
        - Provided desktop application support to MLB, MLBAM, and club employees. 
        - Upgraded, repaired, replaced, and imaged MAC and Windows computers as needed. 
        - Problem solved issues regarding hardware, software, licenses, drives, and the cloud.  
        """
        )

with main_col2:
    # contact info 
    st.subheader('Contact Information', anchor=False, divider='gray')
    st.write(
        """
        - :material/mark_email_read: dylan.mcgee2036@gmail.com 
        - (315) 882-6357
        - https://www.linkedin.com/in/dmcgee20/
        - https://github.com/dtmcgee-su
        \n
        """
    )


    # skills
    st.subheader('Skills', anchor=False, divider='gray')
    st.badge('Programming', color='green')
    st.write(
        """
        - Python 
        - R
        - SQL
        """
    )
    st.badge('Tools', color='green')
    st.write(
            """
            - Git/GitHub 
            - UV
            - Streamlit
            """
        )
    st.badge('Data Management', color='green')
    st.write(
        """
        - AWS 
        - Snowflake
        - Databricks
        - Azure
        \n \n \n
        """
    )

    # education
    st.subheader('Education', anchor=False, divider = 'gray')
    st.write(
        """
        Syracuse University \n
        Major: Sport Analytics \n
        Minor: Information Management and Technology \n
        Graduated: Spring 2021
        """
    )


   