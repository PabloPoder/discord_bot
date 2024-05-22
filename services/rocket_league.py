'''
This module contains the methods to fetch and process 
Rocket League player data from the Rocket League API.
'''
import aiohttp

from apikeys import ROCKET_LEAGUE_ENDPOINT
from classes.rocket_league import Playlist, RocketLeaguePlayer

async def fetch_player_data(nametag:str):
  ''' Fetch the player data from the Rocket League API

  Parameters
  ----------
  nametag : `str`
      The name of the player to get the stats from.
  headers : `dict`
      The headers to use for the request.
  
  Returns
  -------
  dict
      The player data from the Rocket League API.
  '''
  # Set the headers for the request, simulate the request from a browser
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "+
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  }
  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(ROCKET_LEAGUE_ENDPOINT+nametag, headers=headers) as response:
        response.raise_for_status()
        return await response.json()
  except aiohttp.ClientError as err:
    print("An error occurred while fetching the player data:")
    print(f"Player: {nametag}, Error: {err}")
  return None

def is_ranked_playlist(playlist):
  ''' Check if the playlist is a ranked playlist 

  Parameters
  ----------
  playlist: dict
      The playlist to check if it is a ranked playlist.
  return: bool
      True if the playlist is a ranked playlist, False otherwise. 
      Playlists are considered to be ranked if their name is "Ranked Duel 1v1", 
      "Ranked Doubles 2v2" or "Ranked Standard 3v3"
  '''
  return playlist.get("metadata", {}).get("name") in [
    "Ranked Duel 1v1", "Ranked Doubles 2v2", "Ranked Standard 3v3", "Tournament Matches"]

def is_playlist_type(playlist):
  ''' Check if the playlist is a ranked playlist
  
  Parameters
  ----------
  playlist: dict
      The playlist to check if it is a ranked playlist.
  return: bool
      True if the playlist is a ranked playlist, False otherwise.
      Playlists are considered to be ranked if their type is "playlist"
  '''
  return playlist.get("type", {}) == "playlist"

async def get_rocket_league_stats_data(nametag:str):
  ''' Get statistics from a Rocket League player

  This methods makes a request and transform the data into a :class:`RocketLeaguePlayer` object

  Parameters
  ----------
  nametag: str
      The name of the player to get the stats from.
  return: :class:`RocketLeaguePlayer`
  '''
  # Retrieve player data from the Rocket League API
  data = await fetch_player_data(nametag)
  # If no data is returned, exit the function
  if data is None:
    return None

  # Extract all playlists from the retrieved player data
  playlists = data.get("data", {}).get("segments", [])

  # Filter out playlists to include only 'ranked' type and exclude new types
  # like 'peak-rating' and 'playlistAverage'
  filtered_playlists = [
    playlist for playlist in playlists if is_ranked_playlist(playlist)
      and is_playlist_type(playlist)
  ]

  # Transform each filtered playlist into a Playlist object and store them in a list
  playlists_data = [Playlist.from_dict(playlist) for playlist in filtered_playlists]

  # Extract the 'Lifetime' playlist from the list of playlists
  lifetime_playlist = [playlist for playlist in playlists
    if playlist.get("metadata", {}).get("name") == "Lifetime"]

  # Construct a RocketLeaguePlayer object using the retrieved data,
  # playlist data, and lifetime playlist
  player =  RocketLeaguePlayer.from_data(data, playlists_data, lifetime_playlist)

  # Return the constructed RocketLeaguePlayer object
  return player
   