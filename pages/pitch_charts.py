import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="2026 Pitch Charts", layout="wide")
@st.cache_data
def load_data():
    df = pd.read_parquet("data/statcast_2026.parquet")
    df = df.dropna(subset=["plate_x", "plate_z"]).copy()

    if "game_date" in df.columns:
        df["game_date"] = pd.to_datetime(df["game_date"])

    if "pitch_name" not in df.columns:
        df["pitch_name"] = df["pitch_type"] if "pitch_type" in df.columns else "Unknown"
    df["pitch_name"] = df["pitch_name"].fillna("Unknown")

    if "type" not in df.columns:
        df["type"] = "Unknown"
    df["type"] = df["type"].fillna("Unknown")

    if "description" not in df.columns:
        df["description"] = ""
    if "events" not in df.columns:
        df["events"] = pd.NA

    df["in_play"] = (
        df["description"].fillna("").str.contains("hit_into_play")
        | df["type"].eq("X")
        | df["events"].notna()
    )

    return df


def add_strike_zone(fig, sz_top=3.5, sz_bot=1.5):
    left = -0.83
    right = 0.83

    fig.add_shape(type="rect", x0=left, x1=right, y0=sz_bot, y1=sz_top, line=dict(width=1.5, color="gray"))
    fig.add_shape(type="line", x0=-3.4, x1=3.4, y0=sz_top, y1=sz_top, line=dict(color="gray", width=1))
    fig.add_shape(type="line", x0=-3.4, x1=3.4, y0=sz_bot, y1=sz_bot, line=dict(color="gray", width=1))
    fig.add_shape(type="line", x0=left, x1=left, y0=-1.0, y1=6.0, line=dict(color="gray", width=1))
    fig.add_shape(type="line", x0=right, x1=right, y0=-1.0, y1=6.0, line=dict(color="gray", width=1))

    fig.add_annotation(x=-3.0, y=sz_top + 0.05, text="TopZone", showarrow=False)
    fig.add_annotation(x=-3.0, y=sz_bot + 0.05, text="BottomZone", showarrow=False)
    fig.add_annotation(x=left + 0.05, y=-0.85, text="LeftZone", showarrow=False)
    fig.add_annotation(x=right + 0.45, y=-0.85, text="RightZone", showarrow=False)

    return fig


df = load_data()

st.title("2026 Strike Zone Pitch Charts")
st.text("Data source: Statcast (3/25 - 3/30)")

chart_col, filter_col = st.columns([4, 1])

with filter_col:
    st.markdown("### Filters")

    player_options = sorted(df["player_name"].dropna().unique())
    selected_player = st.selectbox("Player Name", player_options)

    player_df = df[df["player_name"] == selected_player].copy()

    pitch_options = sorted(player_df["pitch_name"].dropna().unique())
    selected_pitches = st.multiselect("Pitch Name", pitch_options, default=pitch_options)

    # ball_options = sorted(player_df["balls"].dropna().unique())
    # selected_balls = st.multiselect("Balls", ball_options, default=ball_options)

    # strike_options = sorted(player_df["strikes"].dropna().unique())
    # selected_strikes = st.multiselect("Strikes", strike_options, default=strike_options)

    type_options = [x for x in ["B", "S", "X"] if x in player_df["type"].unique()]
    selected_types = st.multiselect("Pitch Result (ball, strike, contact)", type_options, default=type_options)

    in_play_choice = st.radio("In Play", ["All", "In Play Only", "Exclude In Play"])

    vmin = float(player_df["release_speed"].min())
    vmax = float(player_df["release_speed"].max())

    selected_vel = st.slider(
        "Velocity",
        min_value=float(round(vmin, 1)),
        max_value=float(round(vmax, 1)),
        value=(float(round(vmin, 1)), float(round(vmax, 1))),
        step=0.1
    )

filtered = player_df[
    player_df["pitch_name"].isin(selected_pitches)
    # & player_df["balls"].isin(selected_balls)
    # & player_df["strikes"].isin(selected_strikes)
    & player_df["type"].isin(selected_types)
    & player_df["release_speed"].between(selected_vel[0], selected_vel[1])
].copy()

if in_play_choice == "In Play Only":
    filtered = filtered[filtered["in_play"]]
elif in_play_choice == "Exclude In Play":
    filtered = filtered[~filtered["in_play"]]

type_color_map = {
    "B": "#4C78A8",
    "S": "#F28E2B",
    "X": "#E15759",
}

fig = px.scatter(
    filtered,
    x="plate_x",
    y="plate_z",
    color="type",
    symbol="pitch_name",
    # color_discrete_map=type_color_map,
    hover_data=[
        "game_date",
        "pitch_name",
        "release_speed",
        "balls",
        "strikes",
        "description",
        "events",
    ],
)

fig.update_traces(
    marker=dict(size=7, opacity=0.8, line=dict(width=0.4, color="rgba(0,0,0,0.25)"))
)

fig.update_layout(
    width=760,
    height=560,
    margin=dict(l=40, r=40, t=40, b=40),
)

fig.update_xaxes(title="Plate X", range=[-3, 3], zeroline=False, dtick=1)
fig.update_yaxes(title="Plate Z", range=[-1.2, 6.0], zeroline=False, dtick=1, scaleanchor="x", scaleratio=1)

fig = add_strike_zone(fig)

with chart_col:
    st.plotly_chart(fig, use_container_width=False)
    st.caption(f"{len(filtered):,} pitches shown")
    st.dataframe(filtered[["game_date", "pitch_name", "release_speed", "balls", "strikes", "description", "events"]])