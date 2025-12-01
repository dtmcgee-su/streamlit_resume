##### Imports #####
import streamlit as st
from plotly import graph_objects as go


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