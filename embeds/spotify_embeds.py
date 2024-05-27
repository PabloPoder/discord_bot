'''
This file contains the embeds for the Spotify commands.
'''

from typing import List
import discord
from discord import Embed

from classes.spotify import Playlist, Track
from const import SPOTIFY_LOGO

def create_tracks_embed(top_tracks:List[Track], is_recommendation: bool = False) -> Embed:
  '''Create an embed with the user's top tracks

  Parameters
  ----------
  top_tracks: `list`
      The list of the user's top tracks.
  is_recommendation: `bool`
      A boolean to check if the tracks are recommendations.

  Returns
  -------
  :class:`Embed`
      The embed with the user's top tracks.
  '''
  embed:Embed = Embed(
    title= "Top Tracks" if not is_recommendation else "Recommendations",
    description="Here are your top tracks!"
      if not is_recommendation else "Here are some recommendations for you!",
    color=discord.Color.blurple()
  )

  embed.set_thumbnail(url=top_tracks[0].images)

  embed.set_footer(text="Powered by Spotify", icon_url=SPOTIFY_LOGO)

  for index, track in enumerate(top_tracks):
    embed.add_field(
      name=f"{index + 1}. {track.name}",
      value=f"{track.artists[0]['name']}\n[Listen on Spotify]({track.uri})",
      inline=False
    )

  return embed

def create_playlists_embed(playlists:List[Playlist]) -> Embed:
  '''Create an embed with the user's playlists

  Parameters
  ----------
  playlists: `list`
      The list of the user's playlists.

  Returns
  -------
  :class:`Embed`
      The embed with the user's playlists.
  '''
  embed:Embed = Embed(
    title="Playlists",
    description="Here are your playlists!",
    color=discord.Color.blurple()
  )

  embed.set_author(name=playlists[0].owner.display_name, icon_url=playlists[0].owner.images)
  embed.set_thumbnail(url=playlists[0].images)

  embed.set_footer(text="Powered by Spotify", icon_url=SPOTIFY_LOGO)

  for index, playlist in enumerate(playlists):
    embed.add_field(
      name=f"{index + 1}. {playlist.name}",
      value=f"{playlist.description}\n[Listen on Spotify]({playlist.uri})",
      inline=False
    )

  return embed

def create_playlist_created_embed(playlist_url:str, name:str, description:str) -> Embed:
  '''Create an embed with the created playlist

  Parameters
  ----------
  playlist_url: `str`
      The url of the created playlist.
  name: `str`
      The name of the playlist. 
  description: `str`
      The description of the playlist.

  Returns
  -------
  :class:`Embed`
      The embed with the created playlist.
  '''
  embed:Embed = Embed(
    title=name,
    url=playlist_url,
    description="Your playlist has been created!",
    color=discord.Color.blurple()
  )

  embed.set_thumbnail(url=SPOTIFY_LOGO)

  embed.add_field(
    name="Playlist's description",
    value=description,
    inline=False
  )

  return embed
