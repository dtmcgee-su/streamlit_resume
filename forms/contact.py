import streamlit as st
import re
import requests

WEBHOOK_URL = st.secrets['WEBHOOK_URL']

def is_valid_email(email):
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-.]+$"
    return re.match(email_pattern, email) is not None


def contact_form():
    with st.form('contact_form'):
        first_name = st.text_input('First Name')
        email = st.text_input('Email Address')
        message = st.text_input('Your Message')
        submit_button = st.form_submit_button('Submit')

        if submit_button:
            if not WEBHOOK_URL:
                st.error('Error with the email service. Try again later.')
                st.stop()

            if not first_name: 
                st.error('Please provide your name.')
            
            if not email: 
                st.error('Please provide your email address.')
                         
            if not is_valid_email(email): 
                st.error('Please provide a valid email address.')
                         
            if not message: 
                st.error('Please provide a message.')
                st.stop()

            data = {
                'email': email,
                'name': first_name,
                'message': message
            }
            response = requests.post(WEBHOOK_URL, json=data)

            if response.status_code == 200:
                st.success('Your message has been sent successfully!')
            else:
                st.error('There was an error sending your message.')