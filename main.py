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

print(data.head())
print(data.info())
print(data.describe())

# Converting data to specific format

data["endTime"] = pd.to_datetime(data["ts"])

# Converting total play time to minutes 

def get_total_play_time_minutes(data):
    return data["ms_played"].sum() / (1000 * 60)

# Functions

# Calclate total listening time 

def calculate_total_listening_time(data):
    return data["ms_played"].sum() / (1000 * 60) # Convert ms to minutes

# Find top items 

def find_top_items(df, column, n=5):
    return df[column].value_counts().head(n)

# Find day with most listening 

def most_listened_day(df):
    df['date'] = pd.to_datetime(df['endTime']).dt.date
    return df.groupby('daet')['ms_played'].sum().idxmax()

