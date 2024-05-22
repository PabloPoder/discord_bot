'''
This module contains the commands for the youtube player music cog. 
The yt_music cog contains commands that provide a music player.
'''

import asyncio
import discord
import yt_dlp
from discord.ext import commands
from discord import Interaction

from services.music_player import ffmpeg_options, download_song, play_next

from apikeys import TEST_SERVER_ID

class MusicPlayer(commands.Cog):
  '''
  A class used to represent the Music player cog.
  '''
  def __init__(self, bot):
    self.bot = bot
    self.voice_clients = {}
    self.queues = []

  # region play
  @discord.slash_command(
    name="play",
    description="Plays a song from YouTube",
    guild_ids=TEST_SERVER_ID
  )
  async def play(self, interaction: Interaction, url: str):
    '''
    Plays a song from YouTube

    Parameters
    ----------
    url : str
      The URL of the song to play
    '''
    await interaction.response.defer()

    # 1. Check if the user is in a voice channel
    if interaction.user.voice is None:
      await interaction.followup.send(
        "You must be in a voice channel to use this command.",
        ephemeral=True,
      )
      return

    # 2. Check if the bot is already playing music
    if self.bot.user.voice is not None:
      await interaction.followup.send(
        "I am already playing music in another place.",
        ephemeral=True,
      )
      return

    # 3. Connect to the voice channel
    voice_client = await interaction.user.voice.channel.connect()

    # 4. Download the song
    song_url, song_title, song_thumbnail = await download_song(url)

    if song_url is None:
      await interaction.followup.send(
        "An error occurred: Unable to download the song.",
        ephemeral=True
      )
      return

    # 5. Play the song
    try:
      # create a player object from the song_url
      player = discord.FFmpegPCMAudio(song_url, **ffmpeg_options)
      # Add the player to the queue
      if interaction.guild.id not in self.queues:
          self.queues[interaction.guild.id] = self.queues.pop()
      self.queues[interaction.guild.id].append(player)

      # If not already playing, start playing
      if not voice_client.is_playing():
        play_next(interaction.guild.id, voice_client)

      await interaction.followup.send(f"Playing {song_title}", ephemeral=True)

    except yt_dlp.DownloadError as e:
      await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)

def setup(bot):
  '''
  Add the Utilities cog to the bot.
  '''
  bot.add_cog(MusicPlayer(bot))
