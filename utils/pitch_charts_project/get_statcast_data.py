import pybaseball
import pandas as pd 

def get_statcast_data(start_date: str, end_date: str, filename: str):
    """
    Get Statcast data for a given date range and save it to a parquet file.

    Args:
        start_date (str): The start date in 'YYYY-MM-DD'
        end_date (str): The end date in 'YYYY-MM-DD'
        filename (str): The name of the output parquet file
    """
    
    df = pybaseball.statcast(start_date, end_date)

    cols = [
        "game_date", "pitcher", "player_name", "batter", "pitch_type",
        "release_speed", "plate_x", "plate_z", "description", "events",
        "balls", "strikes", "outs_when_up", "stand", "p_throws",
        "inning", "home_team", "away_team", "sz_top", "sz_bot"
    ]

    df = df[cols].copy()
    # remove missing values
    df = df.dropna(subset=['plate_x', 'plate_z'])
    df['game_date'] = pd.to_datetime(df['game_date'])
    if filename.endswith('.csv'):
        df.to_csv(filename, index=False)
    elif filename.endswith('.parquet'): 
        df.to_parquet(filename, index=False)
    return df


# pulling data in week long increment to avoid timeouts
if __name__ == "__main__":
    start_date = "2026-03-25"
    end_date = "2026-03-29"
    filename = "data/statcast_2026.parquet"
    df = get_statcast_data(start_date, end_date, filename)