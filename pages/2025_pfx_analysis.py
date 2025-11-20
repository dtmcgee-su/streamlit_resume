import streamlit as st 
import pandas as pd
import plotly.express as px
from utils.streamlit_components import pitch_movement_chart, pitch_performance_vs_usage


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
        Lets start by looking at the data. \n
        I used Statcast PFX data from Baseball Savant, which tracks the movement of every pitch thrown in MLB since 2008.
        After familiarizing myself with the data and cleaning any issues, I began graphing some basic distributions to get a better sense of the data. \n
        Here is an example boxplot showing the average speed distribution for each pitch type.
        """
    )
with boxplot_col2:
    velo_order = df.groupby('pitch_type_name')['avg_speed'].mean().sort_values(ascending=False).index.to_list()
    fig = px.box(df, x='pitch_type_name', y='avg_speed', title='Average Speed by Pitch Type', category_orders={'pitch_type_name': velo_order})
    # fig.show()
    st.plotly_chart(fig, use_container_width=True)


st.subheader('Are The Best Performing Pitches Thrown The Most?')
st.write(
    """
        In order to idenify undervalued pitches, we first need to confirm whether or not the best performing pitches are being thrown the most. \n
        Looking at the graph below, it's clear that there is not a strong correlation between pitch percentage and success. 
        This is likely due to the wide variety of factors that go into pitch selection, such as game situation, batter tendencies, and pitcher strategy.
        It's also impotant to note that command for a given pitch is not factored in this analysis.
        Nevertheless, this chart shows there are likely many pitches that are not being utilized to their full potential. \n
        I included the average xSLG on the graph. I will spend a majority of my analysis focused on quadrant 3 (low usage, low xSLG) to find pitches that could be undervalued.
    """
)
pitch_performance_vs_usage()

st.divider()


# customizable pitch movement scatter plot
st.subheader("Exploring Pitch Movement Data")
st.write(
    """
        Now that we have a basic understanding of the data, let's dive deeper. \n
        If the goal is to find underutilized pitches with unique movement profiles, we need to be able to visualize pitch movement effectively. \n
        The following graph displays the horizontal and vertical break of pitches, allowing us to begin to see how different pitch type clusters and outliers could show exceptional pitches. \n 
        The data is grouped by pitcher and pitch type, with each point representing the average movement for that pitch type from that pitcher. \n
        Use the filters on the left to customize the pitch movement scatter plot.
    """
)
pitch_movement_chart()



st.divider()
st.subheader("Findings")
st.write(
    """
    After analyzing/visualizing pitch movement, I identified several pitches with unique movement profiles with low usage percentages that could be resulting in undervalued talent. \n
    """
)

findings_col1, findings_col2 = st.columns([2,2], gap='small', border=True)
with findings_col1:
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image('media/images/chirs_bassitt_headshot.png', use_container_width=True)
    st.image('media/images/chris_bassitt_curveball_movement.png', caption='Figure 1')
with findings_col2:
    st.markdown(
        """
        **Chris Bassitt** \n
        If you look at Figure 1, you'll see a curveball that's in the upper quartile for both horizontal and induced vertical break.
        That pitch belongs to Chris Bassitt, who surprisingly used it only **16%** of the time. 
        With that much movement, plus factoring in the **71.3** average velocity (20 MPH slower than his fastball), the makings of this pitch look very promising.
        However, just because the metrics look good, doesn't mean the pitch was effective.
         \n
        Taking a look at his pitch tracking data from last season, his curveball was his most effective pitch last year by a wide margin. (https://baseballsavant.mlb.com/savant-player/greg-weissert-669711?stats=statcast-r-pitching-mlb) \n
        **It was among his top two pitch types in xBA. xSLG, xWOBA, exit velocity, and Whiff%.**
        Batters hit a measly 0.182 xBA against it, along with a 36.4% Whiff rate.
       

        \n
        Bassitt is known for throwing many different pitches. Having a wide arsenal, giving him the ability to vary his pitch mix, could've been part of the reason why his curveball was so successful last year. 
        Regardless, I believe increasing his curveball usage could result in a better overall season.
        """
    )