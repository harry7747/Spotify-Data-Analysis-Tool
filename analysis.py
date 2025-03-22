import pandas as pd

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
    return data["ms_played"].sum() / (1000 * 60)

def most_streamed_song(data):
    return data["master_metadata_track_name"].value_counts().idxmax()

def most_streamed_artist(data):
    return data["master_metadata_album_artist_name"].value_counts().idxmax()

def most_streamed_albums(data):
    return data["master_metadata_album_album_name"].value_counts().idxmax()

# Fetching genre using Spotify's API 

def get_genre(artist_name):
    results = sp.search(q=artist_name, type='artist', limit=1)
    if results["artists"]["items"]:  
        return results["artists"]["items"][0]["genres"]  
    return ["Unknown"]  

def add_genres_to_data(data):
    data["genre"] = data["master_metadata_album_artist_name"].apply(lambda artist: get_genre(artist)[0])
    return data

def most_streamed_genre(data):
    return data["genre"].value_counts().idxmax()

# Top 5 

def top_streamed_songs(data, n=5):
    return data.groupby("master_metadata_track_name")["ms_played"].sum().sort_values(ascending=False).head(n)

def top_streamed_artists(data, n=5):
    return data.groupby("master_metadata_album_artist_name")["ms_played"].sum().sort_values(ascending=False).head(n)

def top_streamed_albums(data, n=5):
    return data.groupby("master_metadata_album_album_name")["ms_played"].sum().sort_values(ascending=False).head(n)

def top_streamed_genre(data, n=5):
    return data.groupby("genre")["ms_played"].sum().sort_values(ascending=False).head(n)

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

