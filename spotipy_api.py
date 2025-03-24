import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = "163ab0a7ce0a444db7007c38cae05a0e", client_secret="967e59606b274e81b13d2b00ccbf1ef1"))


def get_artist_image(artist_name):
    result = sp.search(q=artist_name, type="artist", limit=1)
    if result["artists"]["items"]:
        return result["artists"]["items"][0]["images"][0]["url"]
    return None 

def get_album_cover(album_name):
    result = sp.search(q=album_name, type='album', limit=1)
    if result["albums"]["items"]:
        return result["albums"]["items"][0]["images"][0]["url"]
    return None

def get_track_thumbnail(track_name):
    result = sp.search(q=track_name, type='track', limit=1)
    if result["tracks"]["items"]:
        return result["tracks"]["items"][0]["album"]["images"][0]["url"]
    return None
