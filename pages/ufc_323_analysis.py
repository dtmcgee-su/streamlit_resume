##### Imports #####
import streamlit as st
import pandas as pd
from plotly import graph_objects as go


st.html("""
    <style>
        .stMainBlockContainer {
            max-width:90rem;
        }
    </style>
    """
)

st.markdown("""
    <style>
    .centered-subheader {
        text-align: center;
    }
    .small-font {
    font-size: 12px !important;      
    </style>
    """, unsafe_allow_html=True
)





##### Introduction #####
st.title("UFC 323 Matchip Analysis")

st.write(
    """
        This page gives you a detailed look at the upcoming matchups for *UFC 323: Dvalishvili vs. Yan 2* by pulling together each fighter’s metrics. \n
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

row = df.loc[match]

# Fighter dictionaries
red = {k.replace("red_", ""): v for k, v in row.items() if k.startswith("red_")}
blue = {k.replace("blue_", ""): v for k, v in row.items() if k.startswith("blue_")}



##### Matchup Details #####
st.subheader(f"Matchup: {df.loc[match, 'fighter_red']} vs. {df.loc[match, 'fighter_blue']}")

col1, col2 = st.columns(2, border=True)


def gauge_chart(title, value):
    fig = go.Figure(go.Indicator(
        mode='gauge+number',
        value=float(value.replace('%', '')),
        title={'text': title, 'font': {'size': 18}},
        gauge={
            'axis': {'range': [0, 100]},
            'steps' : [
                {'range': [0, 33], 'color': "red"},
                {'range': [33, 66], 'color': "yellow"},
                {'range': [66, 100], 'color': "green"}
            ],
            'bar': {'color': "black"},
        },
        
    ))
    fig.update_layout(height=250)
    return fig


with col1:
    st.markdown(f"### {df.loc[match, 'fighter_red']}")
    st.markdown(f"*{df.loc[match, 'red_nickname']}*")
    
    sub_col1, sub_col2 = st.columns([3,2])
    with sub_col1:
        st.image(df.loc[match, 'red_image'], use_container_width=True)
    with sub_col2:
        st.markdown(f"**Height:** {df.loc[match, 'red_height']}")
        st.markdown(f"**Weight:** {df.loc[match, 'red_weight']}")
        st.markdown(f"**Reach:** {df.loc[match, 'red_reach']}")
        st.markdown(f"**Stance:** {df.loc[match, 'red_stance']}")
        st.markdown(f"**DOB:** {df.loc[match, 'red_dob']}")
    

    
    g1, g2 = st.columns(2)
    with g1:
        st.plotly_chart(gauge_chart("Striking Accuracy", red["str_acc"]), use_container_width=True, key="str_acc_red")
    with g2:
        st.plotly_chart(gauge_chart("Striking Defense", red["str_def"]), use_container_width=True, key="str_def_red")
    g3, g4 = st.columns(2)
    with g3:
        st.plotly_chart(gauge_chart("Takedown Accuracy", red["td_acc"]), use_container_width=True, key="td_acc_red")
    with g4:
        st.plotly_chart(gauge_chart("Takedown Defense", red["td_def"]), use_container_width=True, key="td_def_red")


with col2:
    st.markdown(f"### {df.loc[match, 'fighter_blue']}")
    st.markdown(f"*{df.loc[match, 'blue_nickname']}*")

    sub_col1, sub_col2 = st.columns([3,2])
    with sub_col1:
        st.image(df.loc[match, 'blue_image'], use_container_width=True)
    with sub_col2:
        st.markdown(f"**Height:** {df.loc[match, 'blue_height']}")
        st.markdown(f"**Weight:** {df.loc[match, 'blue_weight']}")
        st.markdown(f"**Reach:** {df.loc[match, 'blue_reach']}")
        st.markdown(f"**Stance:** {df.loc[match, 'blue_stance']}")
        st.markdown(f"**DOB:** {df.loc[match, 'blue_dob']}")

    g5, g6 = st.columns(2)
    with g5:
        st.plotly_chart(gauge_chart("Striking Accuracy", blue["str_acc"]), use_container_width=True, key="str_acc_blue")
    with g6:
        st.plotly_chart(gauge_chart("Striking Defense", blue["str_def"]), use_container_width=True, key="str_def_blue")
    g7, g8 = st.columns(2)
    with g7:
        st.plotly_chart(gauge_chart("Takedown Accuracy", blue["td_acc"]), use_container_width=True, key="td_acc_blue")
    with g8:
        st.plotly_chart(gauge_chart("Takedown Defense", blue["td_def"]), use_container_width=True, key="td_def_blue")



def radar_chart(f1, f2, name1, name2):
    categories = [
        "Strikes Landed per Min", 
        "Strikes Absorbed per Min (lower is better)", 
        "Striking Accuracy", 
        "Striking Defense",
        "Takedown Avg", 
        "Takedown Accuracy", 
        "Takedown Defense", 
        "Submission Avg"]
    

    f1_vals = [
        float(f1['slpm'] or 0),
        10 - float(f1['sapm'] or 0),  # invert because lower is better
        float(f1['str_acc'].replace('%','')) / 10 if f1['str_acc'] else 0,
        float(f1['str_def'].replace('%','')) / 10 if f1['str_def'] else 0,
        float(f1['td_avg'] or 0),
        float(f1['td_acc'].replace('%','')) / 10 if f1['td_acc'] else 0,
        float(f1['td_def'].replace('%','')) / 10 if f1['td_def'] else 0,
        float(f1['sub_avg'] or 0)
    ]

    f2_vals = [
        float(f2['slpm'] or 0),
        10 - float(f2['sapm'] or 0),
        float(f2['str_acc'].replace('%','')) / 10 if f2['str_acc'] else 0,
        float(f2['str_def'].replace('%','')) / 10 if f2['str_def'] else 0,
        float(f2['td_avg'] or 0),
        float(f2['td_acc'].replace('%','')) / 10 if f2['td_acc'] else 0,
        float(f2['td_def'].replace('%','')) / 10 if f2['td_def'] else 0,
        float(f2['sub_avg'] or 0)
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=f1_vals,
        theta=categories,
        fill='toself',
        name=name1,
        line_color='blue',
        showlegend=True,
    ))

    fig.add_trace(go.Scatterpolar(
        r=f2_vals,
        theta=categories,
        fill='toself',
        name=name2,
        line_color='red',
        showlegend=True
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True)
        ),
        showlegend=True,
        height=600,

    )

    return fig

radar_fig = radar_chart(red, blue, df.loc[match, 'fighter_red'], df.loc[match, 'fighter_blue'])
st.plotly_chart(radar_fig, use_container_width=True)




# st.plotly_chart(gauge_chart("Str Acc", red["str_acc"]), title=f"{df.loc[match, 'fighter_red']} Striking Accuracy")