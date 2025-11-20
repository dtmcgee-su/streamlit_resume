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
############################################################################

# Do the best performing pitches get thrown the most? 
df_pitch_movement = pd.read_csv('./data/pitch_movement.csv')
df_pitch_stats = pd.read_csv('./data/pitch_arsenal_stats.csv')

df_pitch_movement['pitcherId_pitchType'] = df_pitch_movement['pitcher_id'].astype(str) + '_' + df_pitch_movement['pitch_type']
df_pitch_stats['pitcherId_pitchType'] = df_pitch_stats['player_id'].astype(str) + '_' + df_pitch_stats['pitch_type']

# filter data for relevant columns
df_pitch_movement = df_pitch_movement[[
    'last_name, first_name',	
    'pitcher_id',	
    'team_name_abbrev',	
    'pitch_hand',	
    'pitch_type',
    'pitch_type_name',
    'avg_speed',
    'pitches_thrown',
    'total_pitches',
    'pitch_break_z',
    'pitch_break_z_induced',
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

px.scatter(
    filtered_df,
    x='pitcher_break_x',
    y='pitcher_break_z_induced',
    color='pitch_type_name',
    hover_data=['pitcher_name', 'avg_speed', 'pitches_thrown', 'pitch_per'],
    height=600
)


