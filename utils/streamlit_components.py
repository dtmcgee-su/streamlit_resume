import streamlit as st
import pandas as pd
import plotly.express as px

def pitch_movement_chart():
    # Load Data
    df = pd.read_csv('./data/pitch_movement.csv')
    df=df.dropna()
    df=df.rename(columns={'last_name, first_name': 'pitcher_name'})

    # Create Columns
    col1, col2 = st.columns([1, 3], border=True)  # Left column is 1/4 width, right column 3/4

    # Left Column: Filters
    with col1:

        # Pitch Type
        pitch_types = st.multiselect(
            "Pitch Type",
            options=sorted(df['pitch_type_name'].unique()),
            default=df['pitch_type_name'].unique(),
            help="Select one or more pitch types to display"
        )
        st.write("")

        # Pitcher Name
        pitchers = st.multiselect(
            "Pitcher Name",
            options=sorted(df['pitcher_name'].unique()),
            default=[],
            help="Start typing to search"
        )
        st.write("")
        
        # Pitch Hand
        pitch_hand = st.multiselect(
            "Pitch Hand",
            options=['L', 'R'],
            default=['L', 'R']
        )
        st.write("")

        # Average Speed Slider
        min_speed, max_speed = int(df['avg_speed'].min()), int(df['avg_speed'].max())
        speed_range = st.slider(
            "Average Speed (mph)",
            min_value=min_speed,
            max_value=max_speed,
            value=(min_speed, max_speed)
        )

    # Right Column: Plot + Table
    with col2:
        # Filter the dataframe
        filtered_df = df[
            df['pitch_type_name'].isin(pitch_types) &
            df['pitch_hand'].isin(pitch_hand) &
            (df['avg_speed'] >= speed_range[0]) &
            (df['avg_speed'] <= speed_range[1])
        ]
        if pitchers:
            filtered_df = filtered_df[filtered_df['pitcher_name'].isin(pitchers)]

        # Plotly scatter
        fig = px.scatter(
            filtered_df,
            x='pitcher_break_x',
            y='pitcher_break_z_induced',
            color='pitch_type_name',
            hover_data=['pitcher_name', 'avg_speed', 'pitches_thrown', 'pitch_per'],
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)


