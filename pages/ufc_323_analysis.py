##### Imports #####
import streamlit as st
import pandas as pd
from plotly import graph_objects as go


st.html("""
    <style>
        .stMainBlockContainer {
            max-width:70rem;
        }
    </style>
    """
)

st.markdown("""
    <style>
    .centered-subheader {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True
)





##### Introduction #####
st.title("UFC 323 Matchip Analysis")

st.write(
    """
        This page gives you a detailed look at the upcoming matchups for UFC 323: Dvalishvili vs. Yan 2 by pulling together each fighter’s metrics. \n
        The data is sourced from UFC Stats and includes striking and grappling statistics. 
        With this tool, you can see the differences instantly through the radar chart, efficiency gauges, and side-by-side comparisons. 
        It’s a simple way to understand where each fighter has strengths and weaknesses.
        Select a matchup from the dropdown below to get started!
    """
)
st.divider()


##### Load Data #####
df = pd.read_csv('data/ufc_323_fighter_stats.csv')

match = st.selectbox(
    'Choose a Matchup',
    options=df.index,
    format_func=lambda i: f"{df.loc[i, 'fighter_red']} vs. {df.loc[i, 'fighter_blue']}"
)

# row = df.loc[match]



##### Basic Matchup Details #####
st.subheader(f"Matchup: {df.loc[match, 'fighter_red']} vs. {df.loc[match, 'fighter_blue']}")

col1, col2 = st.columns(2, border=True)

with col1:
    st.markdown(f"### {df.loc[match, 'fighter_red']}")
    st.markdown(f"*{df.loc[match, 'red_nickname']}*")
    st.markdown(f"**Height:** {df.loc[match, 'red_height']}")
    st.markdown(f"**Weight:** {df.loc[match, 'red_weight']}")
    st.markdown(f"**Reach:** {df.loc[match, 'red_reach']}")
    st.markdown(f"**Stance:** {df.loc[match, 'red_stance']}")
    st.markdown(f"**DOB:** {df.loc[match, 'red_dob']}")


with col2:
    st.markdown(f"### {df.loc[match, 'fighter_blue']}")
    st.markdown(f"*{df.loc[match, 'blue_nickname']}*")
    st.markdown(f"**Height:** {df.loc[match, 'blue_height']}")
    st.markdown(f"**Weight:** {df.loc[match, 'blue_weight']}")
    st.markdown(f"**Reach:** {df.loc[match, 'blue_reach']}")
    st.markdown(f"**Stance:** {df.loc[match, 'blue_stance']}")
    st.markdown(f"**DOB:** {df.loc[match, 'blue_dob']}")