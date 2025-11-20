import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels

def pitch_movement_chart():
    # Load Data
    df = pd.read_csv('./data/pitch_movement.csv')
    df=df.dropna()
    df=df.rename(columns={'last_name, first_name': 'pitcher_name'})

    # Create Columns
    col1, col2 = st.columns([1, 3], border=True) 

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
############################################################################

def pitch_performance_vs_usage():
    # Do the best performing pitches get thrown the most? 
    df_pitch_movement = pd.read_csv('./data/pitch_movement.csv')
    df_pitch_stats = pd.read_csv('./data/pitch-arsenal-stats.csv')

    df_pitch_movement['pitcherId_pitchType'] = df_pitch_movement['pitcher_id'].astype(str) + '_' + df_pitch_movement['pitch_type']
    df_pitch_stats['pitcherId_pitchType'] = df_pitch_stats['player_id'].astype(str) + '_' + df_pitch_stats['pitch_type']
    df_pitch_movement = df_pitch_movement.dropna()
    df_pitch_movement.rename(columns={'last_name, first_name': 'pitcher_name'}, inplace=True)

    # filter data for relevant columns
    df_pitch_movement = df_pitch_movement[[
        'pitcher_name',	
        'pitcher_id',	
        'team_name_abbrev',	
        'pitch_hand',
        'pitch_type',
        'pitch_type_name',
        'avg_speed',
        'pitches_thrown',
        'total_pitches',
        'pitch_per',
        'pitcher_break_z',
        'pitcher_break_z_induced',
        'pitcher_break_x',
        'pitcherId_pitchType'
    ]]

    df_pitch_stats = df_pitch_stats[[
        'ba',	
        'slg',	
        'woba',	
        'whiff_percent',	
        'k_percent',	
        'put_away',	
        'est_ba',	
        'est_slg',	
        'est_woba',	
        'hard_hit_percent',
        'pitcherId_pitchType'
    ]]


    # left join on movement
    df_merged = df_pitch_movement.merge(df_pitch_stats, on='pitcherId_pitchType', how='left', suffixes=('_movement', '_stats'))
    
    
    
    col1, col2 = st.columns([1,3], border=True)
    with col1:
        # Pitch Type
        pitch_types = st.multiselect(
            "Pitch Type",
            options=sorted(df_merged['pitch_type_name'].unique()),
            default=df_merged['pitch_type_name'].unique(),
            help="Select one or more pitch types to display",
            key='pitch_type_perf_usage'
        )
        st.write("")
    with col2:

        # Filter the dataframe
        filtered_df = df_merged[
            df_merged['pitch_type_name'].isin(pitch_types)
            # df_merged['pitch_hand'].isin(pitch_hand) &
            # (df_merged['avg_speed'] >= speed_range[0]) &
            # (df_merged['avg_speed'] <= speed_range[1])
        ]
        # if pitchers:
        #     filtered_df = filtered_df[filtered_df['pitcher_name'].isin(pitchers)]






        fig = px.scatter(
            filtered_df,
            x='est_slg',
            y='pitch_per',
            color='whiff_percent',
            hover_data=['pitcher_name', 'pitch_type', 'est_ba', 'est_woba', 'hard_hit_percent'],
            height=600,
            trendline='ols',
            title='Pitch Usage vs Estimated Slugging Percentage (xSLG)'
        )
        fig.add_vline(
            x=0.42, 
            line_width=2, 
            line_dash="dash", 
            line_color="red", 
            annotation_text="MLB Average xSLG",
            annotation_font_size=14,
            annotation_font_color='red')
        st.plotly_chart(fig, use_container_width=True)


