import spotipy
import json
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, render_template
from flask import jsonify
from data_processing import load_data, preprocess_data
from analysis import most_streamed_artist, most_streamed_song, most_streamed_album, most_streamed_genre, get_top_streamed_songs, top_streamed_artists, top_streamed_albums, top_streamed_genre, top_listening_days
from analysis import top_artists_each_year_with_counts, top_song_each_month_with_counts, top_songs_each_year_with_counts, total_listening_time, unique_artists_count, unique_songs_count
from analysis import get_listening_time_by_day_of_week, get_change_in_listening_time_by_year, get_listening_time_by_year, add_genres_to_data
from analysis import get_daily_listening_time, get_most_listened_day, get_hourly_listening_time_for_day, get_listening_time_by_day_of_week, get_listening_streaks


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = "163ab0a7ce0a444db7007c38cae05a0e", client_secret="967e59606b274e81b13d2b00ccbf1ef1"))


app = Flask(__name__)


file_path = "combined_spotify_data.csv"
data = load_data(file_path)
data = preprocess_data(data)


@app.route("/get_data")
def get_data():
    data = preprocess_data(data)

    print(json.dumps(data.to_dict(orient="records"), indent=2))

    return json.dumps(data.to_dict(orient="records"))


@app.route("/")
def home():
    # Get analytics data
    top_artist, artist_minutes = most_streamed_artist(data)
    top_song, song_minutes = most_streamed_song(data)
    total_minutes = total_listening_time(data)
    formatted_total_minutes = "{:,.2f}".format(total_minutes)
    formatted_artist_minutes = "{:,.2f}".format(artist_minutes)
    formatted_song_minutes = "{:,.2f}".format(song_minutes)
    top_albums = top_streamed_albums(data)
    top_songs = get_top_streamed_songs(data)
    top_genre = top_streamed_genre(data, sp)
    unique_artists = unique_artists_count(data)
    unique_songs = unique_songs_count(data)
    listening_streaks = get_listening_streaks(data)


    print("DEBUG: Type of top_streamed_songs ->", type(top_songs))
    print("DEBUG: Content of top_streamed_songs ->", top_songs)


    # Pass data to the HTML template
    return render_template ("index.html",
    top_artist=top_artist, artist_minutes=artist_minutes,
    top_song=top_song, song_minutes=song_minutes,
    total_minutes=total_minutes,
    formatted_total_minutes=formatted_total_minutes,  # <-- Pass formatted_total_minutes
    top_streamed_albums=top_albums,
    top_streamed_songs = top_songs,
    top_streamed_genre=top_genre,
    unique_artists_count=unique_artists,
    unique_songs_count=unique_songs,
    listening_streaks=listening_streaks
    )



if __name__ == "__main__":
    app.run(debug=True)

