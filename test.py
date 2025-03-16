import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


# Sample Spotify-like Data

sample_data = [
    {"endTime": "2021-07-01 00:00:00.000Z", "artistName": "Travis Scott", "trackName": "HOUSTONFORNICATION", "msPlayed": 30000},
    {"endTime": "2021-07-03 00:00:00.000Z", "artistName": "Travis Scott", "trackName": "BUTTERFLY EFFECT", "msPlayed": 18000},
    {"endTime": "2021-07-02 00:00:00.000Z", "artistName": "Billie Eilish", "trackName": "BIRDS OF A FEATHER", "msPlayed": 20000},
    {"endTime": "2021-07-03 00:00:00.000Z", "artistName": "The Weeknd", "trackName": "TAKE ME BACK TO LA", "msPlayed": 15000},
    {"endTime": "2021-07-02 00:00:00.000Z", "artistName": "The Weeknd", "trackName": "TIMELESS", "msPlayed": 32000},
]

# Convert to a Dataframe

data = pd.DataFrame(sample_data)

print(data)



# Funtions 



# Function to calculate total listening time

def calculate_total_listening_time(data):
    return data["msPlayed"].sum() / (1000 * 60) # Convert ms to minutes


# Function to find top items  

def find_top_items(df, column, n=5):
    return df[column].value_counts().head(n)


# Function to get the day with the most listening 

def most_listened_day(df):
    df['date'] = pd.to_datetime(df['endTime']).dt.date
    return df.groupby('date')['msPlayed'].sum().idxmax()


# Example usage 


total_time = calculate_total_listening_time(data)
print(f"Total listening time: {total_time:.2f} minutes")

top_artist = find_top_items(data, "artistName", n=3)
print("Top Artist:", top_artist)

most_day = most_listened_day(data)
print(f"Day with the most listening: {most_day}")



# Visualizing the data



# Visualize top 3 artists

top_3_artists = data['artistName'].value_counts().head(3)
sns.barplot(x=top_3_artists.values, y=top_3_artists.index)
plt.title('Top 3 Artists')
plt.xlabel('Play Count')
plt.show()

# Visualize listening over days

data['date'] = pd.to_datetime(data['endTime']).dt.date
daily_listening = data.groupby('date')['msPlayed'].sum()
daily_listening.plot(kind='line', title='Daily Listening Time', figsize=(10,5))
plt.ylabel('Listening Time (ms)')
plt.show()



# Set up Spotipy credentials



client_id = "163ab0a7ce0a444db7007c38cae05a0e"
client_secret = "967e59606b274e81b13d2b00ccbf1ef1"

sp = Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))

# Example: Get metedata for a song

track = sp.search(q='Song1', type='track', limit=1)
print(track['tracks']['items'][0]['name'])

# Example: Get genre for an artist

artist = sp.search(q="Artist A", type="artist", limit=1)
print(artist['artists']['items'][0]['genres'])

