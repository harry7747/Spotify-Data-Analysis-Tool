import pandas as pd
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

# Cleaning and combining JSON files

folder_path = r"C:\Users\Muhammad Hassan\Downloads\my_spotify_data\Spotify Extended Streaming History"

dataframes = []

# Loop through all JSON files in one folder

for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)

        df = pd.read_json(file_path)
        dataframes.append(df)


# Combine all dataframes into one

combined_data = pd.concat(dataframes, ignore_index=True)

# Save to a CSV

combined_data.to_csv("combined_spotify_data.csv", index=False)

print("combined_data.head()")

# Specfying the columns to read

columns_to_read = ("ts", "ms_played", "master_metadata_track_name", "master_metadata_album_artist_name", "master_metadata_album_album_name")

data = pd.read_csv("combined_spotify_data.csv", usecols=columns_to_read, low_memory=False)

# Converting data to specific format

data["endTime"] = pd.to_datetime(data["ts"])

# Converting total play time to minutes 

def get_total_play_time_minutes(data):
    return data["ms_played"].sum() / (1000 * 60)

# Functions written categorically

# Daily 

def get_daily_listening_time(data):
    data["date"] = pd.to_datetime(data["endTime"]).dt.date
    return data.groupby("date")["ms_played"].sum()

def get_most_listened_day(data):
    daily_listening = get_daily_listening_time(data)
    return daily_listening.idxmax()

def get_hourly_listening_time_for_day(data, selected_date):
    data["date"] = pd.to_datetime(data["endTime"]).dt.date
    data["hour"] = pd.to_datetime(data["endTime"]).dt.hour
    
    # Filter data for the selected date
    filtered_data = data[data["date"] == selected_date]

    return data.groupby("hour")["ms_played"].sum()

def get_listening_time_by_day_of_week(data):
    data["date"] = pd.to_datetime(data["endTime"]).dt.date
    data["day_of_week"] = pd.to_datetime(data["endTime"]).dt.dayofweek
    return data.groupby("day_of_week")["ms_played"].sum()

def get_listening_streaks(data):
    data["date"] = pd.to_datetime(data["endTime"]).dt.date
    data["date_diff"] = data["date"].diff().dt.days.fillna(0)
    
    streaks = []
    streak_length = 0
    
    for date_diff in data["date_diff"]:
        if date_diff == 1:
            streak_length += 1
        else:
            streaks.append(streak_length + 1)
            streak_length = 0

    streaks.append(streak_length + 1)
    return max(streaks)


# Yearly


def get_listening_time_by_year(data):
    data["year"] = pd.to_datetime(data["endTime"]).dt.year
    return data.groupby("year")["ms_played"].sum()

def get_change_in_listening_time_by_year(data):
    yearly_listening = get_listening_time_by_year(data)
    return yearly_listening.pct_change()

def top_artists_each_month_with_counts(data, year):
    data["year"] = pd.to_datetime(data["endTime"]).dt.year
    data["month"] = pd.to_datetime(data["endTime"]).dt.month

    filtered_data = data[data["year"] == year]

    top_artist_per_month = (
        filtered_data.groupby("month")["master_metadata_album_artist_name"]
        .apply(lambda x: x.value_counts().head(1))
    )

    return top_artist_per_month

def top_artists_each_year_with_counts(data):
    data["year"] = pd.to_datetime(data["endTime"]).dt.year

    top_artist_per_year = (
        data.groupby("year")["master_metadata_album_artist_name"]
        .apply(lambda x: x.value_counts().head(1))
    )

    return top_artist_per_year

def top_song_each_month_with_counts(data,year):
    data["year"] = pd.to_datetime(data["endTime"]).dt.year
    data["month"] = pd.to_datetime(data["endTime"]).dt.month

    filtered_data = data[data["year"] == year]

    top_songs_per_month = (
        filtered_data.groupby("month")["master_metadata_track_name"]
        .apply(lambda x: x.value_counts().head(1))
    )

    return top_songs_per_month

def top_songs_each_year_with_counts(data):
    data["year"] = pd.to_datetime(data["endTime"]).dt.year

    top_songs_per_year = (
        data.groupby("year")["master_metadata_track_name"]
        .apply(lambda x: x.value_counts().head(1))
    )

    return top_songs_per_year


