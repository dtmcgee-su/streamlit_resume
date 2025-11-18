import streamlit as st 
import pandas as pd
import plotly.express as px
from utils.streamlit_components import pitch_movement_chart


st.html("""
    <style>
        .stMainBlockContainer {
            max-width:70rem;
        }
    </style>
    """
)

df = pd.read_csv('./data/pitch_movement.csv')
df = df.dropna()

st.title('Identifying Undervalued Free Agents Using PFX Data')
st.write(
    """
    The secret to winning in modern baseball is discovering talent before they become expensive stars. 
    This project aims to do just that for pitchers. Instead of relying on traditional stats like Wins or ERA, 
    we dive deep into pitch design—the unique way a pitcher's ball moves through the air. \n
    In this project, I analyze the induced vertical break and horizontal break across every pitch type for every pitcher in the dataset.
    By defining and quantifying "elite pitch design" based on outliers in movement and efficiency (e.g., a four-seam fastball with 
    exceptional rise or a slider with unique sweep), we move past simple velocity and usage rates. The goal is to surface pitchers 
    whose superior, unique movement profiles suggest high effectiveness, thereby identifying undervalued free-agent arms that could 
    offer significant, cost-controlled production to a major league front office.
    """
)
st.divider()
# NOTE: add a table for column definitions? 

boxplot_col1, boxplot_col2 = st.columns([1,3], gap='small', vertical_alignment='top', border=True)
with boxplot_col1:
    st.write(
        """
        Lets start by looking at the data. I used Statcast PFX data from Baseball Savant, which tracks the movement of every pitch thrown in MLB since 2008.
        After familiarizing myself with the data and cleaning any issues, I began graphing some basic distributions to get a better sense of the data.
        """
    )
with boxplot_col2:
    velo_order = df.groupby('pitch_type_name')['avg_speed'].mean().sort_values(ascending=False).index.to_list()
    fig = px.box(df, x='pitch_type_name', y='avg_speed', title='Average Speed by Pitch Type', category_orders={'pitch_type_name': velo_order})
    # fig.show()
    st.plotly_chart(fig, use_container_width=True)


# customizable pitch movement scatter plot
pitch_movement_chart()


