'''
This file contains the methods interact with the Spotify API.
'''
from typing import List
import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from apikeys import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from classes.spotify import Track, Playlist
from const import SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE


class SpotifyClient:
  '''
  A class used to interact with the Spotify API.
  '''
  def __init__(self):
    try:
      self.sp:Spotify = self.create_spotify_object()
    except spotipy.SpotifyException as e:
      raise spotipy.SpotifyException(
        msg=f"Failed to create Spotify object: {e}",
        http_status=e.http_status,
        code=e.code
      )

    self.top_tracks:List[Track] = []
    self.recommendations:List[Track] = []

  # region create_spotify_object
  def create_spotify_object(self):
    '''
    Create the Spotify object to interact with the Spotify API.

    Returns:
    -------
    `spotipy.Spotify`
      The Spotify object to interact with the Spotify API.
    '''

    # Create the spotify oauth object
    oauth = SpotifyOAuth(
      client_id=SPOTIFY_CLIENT_ID,
      client_secret=SPOTIFY_CLIENT_SECRET,
      redirect_uri=SPOTIFY_REDIRECT_URI,
      scope=SPOTIFY_SCOPE,
    )

    if oauth.is_token_expired(oauth.get_cached_token()):
      oauth.refresh_access_token(oauth.get_cached_token()['refresh_token'])

    # Get the token
    token = oauth.get_access_token(as_dict=False)

    # Create the Spotify object with the token and return it
    return spotipy.Spotify(auth=token)
  # endregion

  # region get_user_top_tracks
  def get_user_top_tracks(self, limit:int = 5) -> list[Track]:
    '''
    Get the user's top tracks from the Spotify API.
    This method set the top_tracks attribute with the top tracks.

    Parameters:
    ----------
    limit: `int`
      The number of top tracks to get. Default is 5.
    Returns:
    -------
    `list`: `List[Track]` or `[]`
      The top tracks from the Spotify API.
    '''
    # If the Spotify object is not created, return None
    if not self.sp:
      return None

    self.top_tracks = []

    try:
      tracks = self.sp.current_user_top_tracks(limit=limit)["items"]

      for track in tracks:
        temp_track = Track.from_dict(data = track)
        self.top_tracks.append(temp_track)

    except spotipy.SpotifyException as e:
      print(f"Failed to get top tracks: {e}")
      self.top_tracks = []

    return self.top_tracks
  # endregion

  # region get_recommendations
  def get_recommendations(self, limit:int = 5) -> list[Track]:
    '''
    Get recommendations from the Spotify API.
    This method set the recommendations attribute with the recommendations.

    Parameters:
    ----------
    limit: `int`
      The number of recommendations to get. Default is 5.
    Returns:
    -------
    `list`: `dict` or `None`
      The recommendations from the Spotify API.
      Or None if there was an error.
    '''
    if not self.sp:
      return None

    if self.top_tracks == []:
      try:
        self.top_tracks = self.get_user_top_tracks()
      except spotipy.SpotifyException as e:
        print(f"Failed to get top tracks: {e}")
        self.top_tracks = []

    # Get seeds to get recommendations
    seed_tracks = []
    seed_artists = []
    try:
      seed_genres = self.sp.artist(self.top_tracks[0].artists[0]['id'])['genres']

    except spotipy.SpotifyException as e:
      print(f"Failed to get seed genres: {e}")
      seed_genres = []

    for track in self.top_tracks:
      seed_artists.append(track.artists[0]['id'])
      seed_tracks.append(track.track_id)

    # Get recommendations
    try:
      new_recommendations = self.sp.recommendations(
        seed_genres=seed_genres,
        seed_tracks=seed_tracks[:2],
        seed_artists=seed_artists[:2],
        limit=limit
      )['tracks']

      # Convert the recommendations to Track objects
      for track in new_recommendations:
        temp_track = Track.from_dict(data = track)
        self.recommendations.append(temp_track)

    except spotipy.SpotifyException as e:
      print(f"Failed to get recommendations: {e}")
      self.recommendations = []

    return self.recommendations
  # endregion

  # region create_playlist
  def create_playlist(self,
    name="My recommended playlist",
    description="A playlist with recommended songs by Rachael Nexus-7",
    ) -> str:
    '''
    Create a playlist in the user's Spotify account based on the recommendations and
    top user's tracks.

    Parameters:
    ----------
    name: `str`
      The name of the playlist.
    description: `str`
      The description of the playlist.

    Returns:
    -------
    `str`
      The url of the created playlist.
    '''
    if not self.sp:
      return None

    # Create the playlist and get the id of it
    try:
      playlist_id = self.sp.user_playlist_create(
        user=self.sp.me()['id'],
        name=name,
        description=description,
        public=True
      )['id']
    except spotipy.SpotifyException as e:
      print(f"Failed to create playlist: {e}")
      return None

    # If there isn't recommendations, get them (in process, get the top tracks too)
    if not self.recommendations:
      try:
        self.get_recommendations()
      except spotipy.SpotifyException as e:
        print(f"Failed to get recommendations: {e}")
        self.recommendations = []

    #  Use the helper method to add tracks to the playlist
    try:
      self.add_tracks_to_playlist(playlist_id, self.recommendations)
      self.add_tracks_to_playlist(playlist_id, self.top_tracks)
    except spotipy.SpotifyException as e:
      print(f"Failed to add tracks to playlist: {e}")

    return self.sp.playlist(playlist_id=playlist_id)['external_urls']['spotify']
  # endregion

  # region add_tracks_to_playlist
  def add_tracks_to_playlist(self, playlist_id: str, tracks: list) -> None:
    '''Add a list of tracks to a playlist.

    Parameters:
    ----------
    playlist_id: `str`
      The id of the playlist.
    tracks: `list`
      The list of tracks to add to the playlist.
    '''
    track_ids = [track.track_id for track in tracks]

    try:
      self.sp.playlist_add_items(playlist_id, track_ids)
    except spotipy.SpotifyException as e:
      print(f"Failed to add tracks to playlist: {e}")
  # endregion

  # region clear_recommendations and clear_top_tracks
  def clear_recommendations(self):
    '''
    Clear the recommendations attribute.
    '''
    self.recommendations = []

  def clear_top_tracks(self):
    '''
    Clear the top_tracks attribute.
    '''
    self.top_tracks = []
  # endregion

  # region get_current_user_playlists
  def get_current_user_playlists(self, limit: int = 5) -> list:
    '''
    Get the user's playlists.

    Parameters:
    ----------
    limit: `int`
      The number of playlists to get. Default is 5.

    Returns:
    -------
    `list`
      The user's playlists.
    '''
    if not self.sp:
      return None

    try:
      playlists:List[Playlist] = [
        Playlist.from_dict(item) for item in
        self.sp.current_user_playlists(limit=limit)['items']
      ]
      # return self.sp.current_user_playlists(limit=limit)['items']
      return playlists

    except spotipy.SpotifyException as e:
      print(f"Failed to get playlists: {e}")
      return []
  # endregion
