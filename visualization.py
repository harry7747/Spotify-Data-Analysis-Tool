import pandas as pd
import os
import spotipy
import IPython.display as ipd
import matplotlib as plt
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from IPython.display import display, HTML
from analysis import most_streamed_artist, most_streamed_song, most_streamed_albums, most_streamed_genre, top_streamed_songs, top_streamed_artists, top_streamed_albums, top_streamed_genre, top_listening_days
from analysis import top_artists_each_year_with_counts, top_song_each_month_with_counts, top_songs_each_year_with_counts, total_listening_time, unique_artists_count, unique_songs_count
from analysis import get_listening_time_by_day_of_week, get_change_in_listening_time_by_year, get_listening_time_by_year
from analysis import get_daily_listening_time, get_most_listened_day, get_hourly_listening_time_for_day, get_listening_time_by_day_of_week, get_listening_streaks


# Structure Code

def display_most_streamed_item(title, name, cover_url=None):
    """Displays the most streamed item (song, artist, album) with optional cover image."""
    html = f"""
    <div style='border: 2px solid #333; padding: 10px; margin: 10px 0; border-radius: 10px; display: flex; align-items: center;'>
        {'<img src="' + cover_url + '" style="width: 50px; height: 50px; margin-right: 10px; border-radius: 5px;">' if cover_url else ''}
        <strong>{title}: </strong> {name}
    </div>
    """
    display(HTML(html))

def display_stat(title, value):
    html = f"""
    <div style='border-left: 5px solid #007bff; padding: 8px; margin: 5px 0;'>
        <strong>{title}: </strong> {value}
    </div>
    """
    display(HTML(html))

# Fetching data from Spotipy API 

def get_artist_image(artist_name, sp):
    result = sp.search(q=artist_name, type="artist", limit=1)
    if result["artists"]["items"]:
        return result["artists"]["items"][0]["images"][0]["url"]
    return None 

def get_album_cover(album_name, sp):
    result = sp.search(q=album_name, type='album', limit=1)
    if result["albums"]["items"]:
        return result["albums"]["items"][0]["images"][0]["url"]
    return None

def get_track_thumbnail(track_name, sp):
    result = sp.search(q=track_name, type='track', limit=1)
    if result["tracks"]["items"]:
        return result["tracks"]["items"][0]["album"]["images"][0]["url"]
    return None

# Displaying the data

def display_most_streamed_artist(data, sp):
    most_streamed_artist = most_streamed_artist(data)  

    results = sp.search(q=most_streamed_artist, type="artist", limit=1)
    artist = results["artists"]["items"][0] if results["artists"]["items"] else None
    artist_image_url = artist["images"][0]["url"] if artist else None

    display_html = f"""
    <div style="text-align: center;">
        <h2 style="font-family: Arial, sans-serif;">🎤 Most Streamed Artist</h2>
        <h3 style="color: #1DB954;">{most_streamed_artist}</h3>
        {'<img src="' + artist_image_url + '" width="200">' if artist_image_url else '<p>Image not available</p>'}
    </div>
    """
    display(HTML(display_html))

def display_most_streamed_song(data, sp):
    most_streamed_song = most_streamed_song(data)  

    results = sp.search(q=most_streamed_song, type="track", limit=1)
    track = results["tracks"]["items"][0] if results["tracks"]["items"] else None
    song_image_url = track["album"]["images"][0]["url"] if track else None
    artist_name = track["artists"][0]["name"] if track else "Unknown Artist"

    display_html = f"""
    <div style="text-align: center;">
        <h2 style="font-family: Arial, sans-serif;">🎵 Most Streamed Song</h2>
        <h3 style="color: #1DB954;">{most_streamed_song} - {artist_name}</h3>
        {'<img src="' + song_image_url + '" width="200">' if song_image_url else '<p>Image not available</p>'}
    </div>
    """

    display(HTML(display_html))

def display_most_streamed_album(data, sp):
    most_streamed_album = most_streamed_album(data) 

    results = sp.search(q=most_streamed_album, type="album", limit=1)
    album = results["albums"]["items"][0] if results["albums"]["items"] else None
    album_image_url = album["images"][0]["url"] if album else None
    album_artist = album["artists"][0]["name"] if album else "Unknown Artist"

    display_html = f"""
    <div style="text-align: center;">
        <h2 style="font-family: Arial, sans-serif;">💿 Most Streamed Album</h2>
        <h3 style="color: #1DB954;">{most_streamed_album} - {album_artist}</h3>
        {'<img src="' + album_image_url + '" width="200">' if album_image_url else '<p>Image not available</p>'}
    </div>
    """

    display(HTML(display_html))

def display_most_streamed_genre(data):
    most_streamed_genre = most_streamed_genre(data)

    display_html = f"""
    <div style="text-align: center;">
        <h2 style="font-family: Arial, sans-serif;">🎶 Most Streamed Genre</h2>
        <h3 style="color: #1DB954;">{most_streamed_genre}</h3>
        <p style="font-style: italic; color: grey;">Music style that defined your listening</p>
    </div>
    """

    display(HTML(display_html))


def display_top_5_songs(data, sp):
    top_songs = top_streamed_songs(data) 

    html_content = "<div style='text-align: center;'><h2>🎵 Top 5 Most Streamed Songs</h2>"

    for song in top_songs.index:
        result = sp.search(q=song, limit=1, type="track")
        if result["tracks"]["items"]:
            album_cover = result["tracks"]["items"][0]["album"]["images"][0]["url"]
        else:
            album_cover = "https://via.placeholder.com/150"

        html_content += f"""
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
            <img src="{album_cover}" width="100" height="100" style="border-radius: 10px; margin-right: 10px;">
            <h3>{song}</h3>
        </div>
        """

    html_content += "</div>"

    display(HTML(html_content))

def display_top_5_artists(data, sp):
    top_artists = top_streamed_artists(data)

    html_content = "<div style='text-align: center;'><h2>🎤 Top 5 Most Streamed Artists</h2>"

    for artist in top_artists.index:
        result = sp.search(q=artist, limit=1, type="artist")
        if result["artists"]["items"]:
            artist_image = result["artists"]["items"][0]["images"][0]["url"]
        else:
            artist_image = "https://via.placeholder.com/150" 

        html_content += f"""
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
            <img src="{artist_image}" width="100" height="100" style="border-radius: 50%; margin-right: 10px;">
            <h3>{artist}</h3>
        </div>
        """

    html_content += "</div>"

    display(HTML(html_content))

def display_top_5_albums(data, sp):
    top_albums = top_streamed_albums(data)

    html_content = "<div style='text-align: center;'><h2>📀 Top 5 Most Streamed Albums</h2>"

    for album in top_albums.index:
        result = sp.search(q=album, limit=1, type="album")
        if result["albums"]["items"]:
            album_cover = result["albums"]["items"][0]["images"][0]["url"]
        else:
            album_cover = "https://via.placeholder.com/150"

        html_content += f"""
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
            <img src="{album_cover}" width="100" height="100" style="border-radius: 10px; margin-right: 10px;">
            <h3>{album}</h3>
        </div>
        """

    html_content += "</div>"

    display(HTML(html_content))

def display_total_listening_time(data):
    total_ms = data["ms_played"].sum()
    total_hours = total_ms / (1000 * 60 * 60)
    total_minutes = total_ms / (1000 * 60)  

    listening_text = f"<h2>Total Listening Time</h2>"
    listening_text += f"<p><b>{total_hours:.2f} hours</b> ({total_minutes:.0f} minutes) of music played.</p>"

    # Enhancement: Fun equivalent comparisons
    if total_hours >= 24:
        listening_text += f"<p>That’s like listening to music non-stop for <b>{total_hours / 24:.1f} days</b>!</p>"

    return display(HTML(listening_text))

def display_yearly_listening_time(data):
    data["year"] = pd.to_datetime(data["endTime"]).dt.year
    yearly_listening = data.groupby("year")["ms_played"].sum() / (1000 * 60 * 60) 

    listening_text = "<h2>📅 Total Listening Time (Year-on-Year)</h2><ul>"
    prev_year_hours = None

    for year, hours in yearly_listening.items():
        listening_text += f"<li><b>{year}:</b> {hours:.1f} hours"
        
        if prev_year_hours is not None:
            change = ((hours - prev_year_hours) / prev_year_hours) * 100
            arrow = "⬆️" if change > 0 else "⬇️"
            listening_text += f" ({arrow} {abs(change):.1f}% change)"
        
        listening_text += "</li>"
        prev_year_hours = hours

    listening_text += "</ul>"
    
    return display(HTML(listening_text))

def display_most_streamed_day(data):
    most_streamed_day, most_streamed_time_ms = most_streamed_day(data)  
    most_streamed_time = most_streamed_time_ms / (1000 * 60 * 60)

    listening_text = f"""
    <h2>📅 Your Most Streamed Day</h2>
    <p><b>{most_streamed_day}</b> was your most music-filled day!</p>
    <p>You listened for a total of <b>{most_streamed_time:.1f} hours</b>.</p>
    """

    if most_streamed_time >= 10:
        listening_text += "<p>Whoa! That’s almost half a day of music! 🎵</p>"
    elif most_streamed_time >= 5:
        listening_text += "<p>Seems like a long session—were you on a road trip or deep focus mode? 🚗💼</p>"
    else:
        listening_text += "<p>A solid listening day, but you’ve had even bigger ones before!</p>"

    return display(HTML(listening_text))

def display_top_5_listening_days(data):
    top_5_days = top_listening_days(data) 
    top_5_days["Hours Played"] = top_5_days["ms_played"] / (1000 * 60 * 60)  

    listening_text = "<h2>📅 Your Top 5 Listening Days</h2><ul>"
    
    for index, row in top_5_days.iterrows():
        listening_text += f"<li><b>{row['date']}</b>: {row['Hours Played']:.1f} hours</li>"

    listening_text += "</ul>"

    max_hours = top_5_days["Hours Played"].max()
    min_hours = top_5_days["Hours Played"].min()

    if max_hours >= 10:
        listening_text += "<p>Your biggest day was an absolute music marathon! 🏆🎶</p>"
    elif max_hours - min_hours > 5:
        listening_text += "<p>Your top day had way more music than others—was it a special occasion? 🎉</p>"

    for i, row in top_5_days.iterrows():
        listening_percentage = (row["hours_played"] / 24) * 100 
        if i == 0:
            display_html += f"<li><b>🔥 {row['date']}: {row['hours_played']} hours</b> ({listening_percentage:.1f}% of the day!)</li>"
        else:
            display_html += f"<li>{row['date']}: {row['hours_played']} hours</li>"

    display_html += "</ul>"

    return display(HTML(listening_text))

def plot_yearly_listening_time(data):
    data["year"] = pd.to_datetime(data["endTime"]).dt.year
    yearly_listening = data.groupby("year")["ms_played"].sum() / (1000 * 60 * 60)

    plt.figure(figsize=(10, 5))
    yearly_listening.plot(kind="bar", color="skyblue", edgecolor="black")

    plt.xlabel("Year")
    plt.ylabel("Total Listening Time (Hours)")
    plt.title("Total Listening Time Year-on-Year")
    plt.xticks(rotation=45)
    
    for i, (year, hours) in enumerate(yearly_listening.items()):
        if i > 0:
            prev_year = list(yearly_listening.keys())[i - 1]
            growth = ((hours - yearly_listening[prev_year]) / yearly_listening[prev_year]) * 100
            plt.text(i, hours + 10, f"{growth:.1f}%", ha="center", fontsize=10, color="green")

    plt.show()

def plot_listening_diversity(data, time_period="year", show_graph=False):
    """
    Visualizes listening diversity over time as text (default) or as a graph (toggleable).
    
    Parameters:
    - data: DataFrame containing Spotify listening history
    - time_period: "year" (default) or "month" to change granularity
    - show_graph: Boolean flag to toggle graph visualization
    """

    data["date"] = pd.to_datetime(data["endTime"])
    data["year"] = data["date"].dt.year
    data["month"] = data["date"].dt.to_period("M") 
    
    if time_period == "year":
        diversity_data = data.groupby("year")["master_metadata_album_artist_name"].nunique()
        label = "Year"
    else:
        diversity_data = data.groupby("month")["master_metadata_album_artist_name"].nunique()
        label = "Month"

    latest_year = diversity_data.index.max()
    latest_count = diversity_data.loc[latest_year]
    
    text_summary = f"""
    <h2>🎵 Listening Diversity Over Time</h2>
    <p>In <b>{latest_year}</b>, you discovered <b>{latest_count} unique artists</b>!</p>
    """
    
    display(HTML(text_summary))
    
    if show_graph:
        plt.figure(figsize=(10, 5))
        plt.plot(diversity_data.index.astype(str), diversity_data, marker="o", linestyle="-", color="purple")
        plt.xlabel(label)
        plt.ylabel("Unique Artists Count")
        plt.title(f"🎶 Unique Artists Over Time ({label}-wise)")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.show()
