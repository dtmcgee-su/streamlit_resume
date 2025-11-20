##### Imports #####
import streamlit as st 
import pandas as pd
import plotly.express as px
from utils.streamlit_components import pitch_movement_chart, pitch_performance_vs_usage
import json
from plotly.io import from_json


st.html("""
    <style>
        .stMainBlockContainer {
            max-width:70rem;
        }
    </style>
    """
)

##### Intro ######
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

##### Plot 1: Box Plot #####
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


##### Plot 2: Usage vs Performance #####
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


##### Plot 3: Pitch Movement Scatter #####
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

##### Modeling #####
st.subheader("Modeling 'Elite' Pitch Design")
st.write(
    """
    To quantify "elite" pitch design, I built a classification model to predict whether a given pitch is "elite" based on its movement and performance metrics. \n
    For the purpose of this exercise, I classified any pitch in the top 25th percentile of Whiff Percentage as "elite," forming the target variable for the model.
    After cleaning, I merged pitch movement and performance data together to create a dataset ready for modeling. \n
    The features used in the model are described in the table below:

    """
)
df_features = pd.DataFrame({

    'Feature': [
                'pitch_per', 
                'pitcher_break_z_induced', 
                'pitcher_break_x', 
                'avg_speed', 
                'est_ba', 
                'est_slg', 
                'est_woba', 
                'hard_hit_percent',
                'pitch_hand'
    ],
    'Description': [
                    'Percentage of times the pitch is thrown by the a given pitcher',
                    'The vertical movement of the pitch caused by spin, measured in inches',
                    'The horizontal movement of the pitch caused by spin, measured in inches',
                    'The average speed of the pitch, measured in MPH',
                    'Expected batting average against the pitch',
                    'Expected slugging percentage against the pitch',
                    'Expected weighted on-base average against the pitch',
                    'Percentage of batted balls against the pitch that are classified as hard-hit (exit velocity >= 95 MPH)',
                    'The handedness of the pitcher (L or R)'

    ]
   
})
st.dataframe(df_features, hide_index=True)

st.write(
    """
        I decided to use a Random Forest Classifier for this task, as it is known to handle non-linear relationships and interactions between features well.
        The output of the model is a classification whether a pitch is "elite" at swinging and missing based on its pitch design and previous performance metrics. \n
    """
)
try:
    with open('media/model_results/feature_importance.json', 'r') as f:
        json_str = json.load(f)
        fig_fi = from_json(json_str)

    st.plotly_chart(fig_fi, use_container_width=True)
except FileNotFoundError:
    st.warning('Feature importance file not found.')

st.write(
    """
        The feature importance chart above shows what the model believes were the most important facotrs in predicting an elite pitch.
        The model is telling us that performance metrics like xSLG and xWOBA are the most important features, which makes sense.
        However, I was expecting pitch movement to weigh more. 
        It's not a surprise that veritcal movement is a better predictor than horizontal when it comes to swing-and-miss pitches.
    """
)

try:
    with open('media/model_results/roc_curve_fig.json', 'r') as f:
        fig_json_string = json.load(f)
        fig_roc = from_json(fig_json_string)
        
    st.plotly_chart(fig_roc, use_container_width=True) 
    
except FileNotFoundError:
    st.warning("ROC Curve figure not found.")

st.write(
    """
        Above is the ROC curve from the model.
        The Receiver Operating Characteristic (ROC) curve is a graph that shows the performance of a classification model.
        It plots the True Positive Rate (TPR) against the False Positive Rate (FPR).
        A perfect model would have an ROC curve that is a right angle.
        The model achieved an **Area Under the Curve (AUC)** of **0.9418** which is considered very strong.
    """
)


st.divider()
##### Findings #####
st.subheader("Findings")
st.write(
    """
    After analyzing/visualizing pitch movement, I identified a couple pitches with unique movement profiles with low usage percentages that could be resulting in undervalued talent.
    Any pitch included was predicted as elite based on my model. \n
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

st.divider()
##### Improvements #####
st.subheader("Findings")
st.write(
    """
    No project is perfect, below are the list of changes I would like to make that could make this project stronger: \n
    - Incorporate pitch command
    - Experiment with other modeling techniques
    - Use data from multiple seasons
    - Validate findings with actual game footage
    """
)