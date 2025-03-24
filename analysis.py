import pandas as pd
import os
import threading

GENRE_CSV = "artist_genres.csv"

if os.path.exists(GENRE_CSV):
    genre_data = pd.read_csv(GENRE_CSV)
else:
    genre_data = pd.DataFrame(columns=["artist", "genre"])

artist_genre_dict = dict(zip(genre_data["artist"], genre_data["genre"]))

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


# Most Streamed & Top Lists


def total_listening_time(data):
    print(f"Columns in data: {data.columns}")  # Debugging step
    if "ms_played" not in data.columns:
        print("⚠️ 'ms_played' column is missing!")
        return 0  # Return 0 to prevent errors
    
    total_minutes = data["ms_played"].sum() / (1000 * 60)  # Convert to minutes
    print(f"Total minutes: {total_minutes}")  # Debugging step
    return round(total_minutes, 2)


def most_streamed_song(data):
    song_counts = data["master_metadata_track_name"].value_counts()
    top_song = song_counts.idxmax()
    song_play_count = song_counts.max()  # Get the number of times streamed
    return top_song, song_play_count


def most_streamed_artist(data):
    artist_counts = data["master_metadata_album_artist_name"].value_counts()
    top_artist = artist_counts.idxmax()
    artist_minutes = artist_counts.max()  # Get the number of times streamed
    return top_artist, artist_minutes

def most_streamed_album(data):
    return data["master_metadata_album_album_name"].value_counts().idxmax()

def most_streamed_genre(data):
    return data["genre"].value_counts().idxmax()

# Top 5 

def get_top_streamed_songs(data, n=5):
    return (
        data.groupby("master_metadata_track_name")["ms_played"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .index.tolist()
    )

def top_streamed_artists(data, n=5):
    return (
        data.groupby("master_metadata_album_artist_name")["ms_played"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .index.tolist()
    )

def top_streamed_albums(data, n=5):
    return(
        data.groupby("master_metadata_album_album_name")["ms_played"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .index.tolist()
    )

def add_genres_to_data(data, sp):
    print("🔍 [DEBUG] Started adding genres to data...")  
    data = data.copy()

    genre_cache = {}

    def safe_get_genre(artist):
        if artist in genre_cache:  # Check if genre already fetched
            print(f"✅ Using cached genre for: {artist}")
            return genre_cache[artist]
        
        print(f"🎵 Fetching genre for artist: {artist}")  
        genre_list = get_genre(artist, sp)
        genre = genre_list[0] if genre_list else "Unknown"

        genre_cache[artist] = genre  # Store in cache
        print(f"✅ Genre fetched: {genre}")  
        return genre

    data.loc[:, "genre"] = data["master_metadata_album_artist_name"].apply(safe_get_genre)
    
    print("✅ [DEBUG] Finished adding genres.")  
    return data

def top_streamed_genre(data, sp, n=5):
    if "genre" not in data.columns:
        data = add_genres_to_data(data, sp) # DEBUG

    return data["genre"].value_counts().head(n).index.tolist()

def top_listening_days(data):
    data["date"] = pd.to_datetime(data["endTime"]).dt.date 
    daily_listening = data.groupby("date")["ms_played"].sum().reset_index()  
    daily_listening = daily_listening.sort_values(by="ms_played", ascending=False)  
    return daily_listening.head(5)  

# Unique Artists and Songs

def unique_artists_count(data): 
    return data["master_metadata_album_artist_name"].nunique()

def unique_songs_count(data):
    return data["master_metadata_track_name"].nunique()


# Creating a cached CSV to store artist genres & background fetch from API to get genre 


def get_genre(artist_name, sp):

    if artist_name in artist_genre_dict:
        return artist_genre_dict[artist_name]
    
    results = sp.search(q=artist_name, type="artist", limit=1)
    if results["artists"]["items"]:
        genre = results["artists"]["items"][0]["genres"]
        genre = genre[0] if genre else "Unknown"

        artist_genre_dict[artist_name] = genre
        update_genre_dataset(artist_name, genre)
        return genre
    
    return "Unknown"

def update_genre_dataset(artist_name=None, genre=None, artist_genre_dict=None, genre_csv_path=GENRE_CSV):
    global genre_data  

    # If updating for a single artist
    if artist_name and genre:
        new_data = pd.DataFrame([[artist_name, genre]], columns=["artist", "genre"])
        genre_data = pd.concat([genre_data, new_data], ignore_index=True)
    
    # If updating from a dictionary (batch update)
    elif artist_genre_dict:
        if not isinstance(artist_genre_dict, dict):
            raise TypeError(f"Expected a dictionary, but got {type(artist_genre_dict)}")
        df = pd.DataFrame(artist_genre_dict.items(), columns=["artist", "genre"])
        genre_data = pd.concat([genre_data, df], ignore_index=True)

    # Save the updated dataset
    genre_data.to_csv(genre_csv_path, index=False)
    print("🎉 CSV saved successfully!")

def add_genres_to_data(data, sp):
    data["genre"] = data["master_metadata_album_artist_name"].apply(lambda artist: get_genre(artist, sp))
    return data

def fetch_missing_genres(artist_list): 
    def worker():
        for artist in artist_list:
            if artist not in artist_genre_dict: 
                get_genre(artist) # Update the dataset
        print("Background genre fetching completed!")

    thread = threading.Thread(target=worker)
    thread.start()

