import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def get_track(track_id: str = None):
    """Get spotify link of track with id <track_id>"""
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    results = spotify.track(track_id=track_id)
    return results['external_urls']['spotify']






