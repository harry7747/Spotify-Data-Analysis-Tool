import pandas as pd
import os
import spotipy
import IPython.display as ipd
import matplotlib as plt
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from IPython.display import display, HTML
from data_processing import load_data, preprocess_data, save_data
from analysis import most_streamed_artist, most_streamed_song, most_streamed_album, most_streamed_genre, get_top_streamed_songs, top_streamed_artists, top_streamed_albums, top_streamed_genre, top_listening_days
from analysis import top_artists_each_year_with_counts, top_song_each_month_with_counts, top_songs_each_year_with_counts, total_listening_time, unique_artists_count, unique_songs_count
from analysis import get_listening_time_by_day_of_week, get_change_in_listening_time_by_year, get_listening_time_by_year
from analysis import get_daily_listening_time, get_most_listened_day, get_hourly_listening_time_for_day, get_listening_time_by_day_of_week, get_listening_streaks
from visualization import display_most_streamed_artist, display_most_streamed_song, display_most_streamed_album, display_most_streamed_genre
from visualization import display_top_5_songs, display_most_streamed_artist, display_top_5_albums
from visualization import display_total_listening_time, display_yearly_listening_time, display_most_streamed_day, display_top_5_listening_days
from visualization import plot_yearly_listening_time, plot_listening_diversity
from spotipy_api import get_artist_image, get_album_cover, get_track_thumbnail

df = pd.read_csv("combined_spotify_data.csv") # DEBUG
df.columns = df.columns.str.strip()

# Authentication with Spotipy

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = "163ab0a7ce0a444db7007c38cae05a0e", client_secret="967e59606b274e81b13d2b00ccbf1ef1"))

# Specifying folder path

folder_path = r"C:\Users\Muhammad Hassan\Documents\GitHub\Spotify-Data-Analysis-Tool/combined_spotify_data.csv"

# Load and process data
raw_data = load_data(folder_path)
processed_data = preprocess_data(raw_data)

# Save processed data
save_data(processed_data)

# Load processed data for analysis
data = pd.read_csv("combined_spotify_data.csv")

del sp # Delete the Spotify object before python shuts down

# DEBUGGING

print(list(df.columns))

