'''
This file contains the embeds for the music player.
'''

import discord
from discord import Embed

from classes.music_player import Video

def now_playing_embed(video_song: Video) -> Embed:
  '''
    This function will return an embed with the currently playing song.

    Parameters:
    ----------
    video_song: `Video`
      The song object with the data.
  '''
  if not video_song:
    return discord.Embed(
      title = 'Nothing is playing!',
      color = discord.Color.blurple()
    )
  
  embed = discord.Embed(
    title = 'Now Playing',
    description = f'[{video_song.title}]({video_song.url})',
    color = discord.Color.blurple()
  )

  embed.set_image(url = video_song.thumbnail)
  embed.add_field(name = 'Duration', value = video_song.duration, inline = False)
  return embed