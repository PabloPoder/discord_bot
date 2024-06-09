'''
  This file contains the code for the music player cog.
'''
import re
import discord
from asyncio import run_coroutine_threadsafe
from discord.ext import commands
from discord import Interaction
from classes.music_player import Video
from utils.apikeys import TEST_SERVER_ID
from utils.const import FFMPEG_OPTIONS
from utils.logger_config import logger
from services.music_player import get_video_info, search_youtube

from yt_dlp import YoutubeDL

from embeds.music_player_embeds import now_playing_embed

class MusicPlayer(commands.Cog):
  '''
    This class is the music player cog.
  '''
  def __init__(self, bot):
    self.bot = bot
    # This dictionary will store the voice clients for each guild (server).
    self.is_playing = {}
    self.is_paused = {}
    self.music_queue = {}
    self.queue_index = {}
    self.voice_channel = {}
    
  @commands.Cog.listener()
  async def on_ready(self):
    '''
      This function is called when the bot is ready.
    '''
    logger.debug('Music Player cog is ready.')
    for guild in self.bot.guilds:
      id = int(guild.id)
      self.is_playing[id] = self.is_paused[id] = False
      self.music_queue[id] = []
      self.queue_index[id] = 0
      self.voice_channel[id] = None

  # region utils methods
  async def join_voice_channel(self, interaction: Interaction, channel):
    '''
      This function will join the voice channel of the user.
    '''
    id = int(interaction.guild.id)
    if self.voice_channel[id] == None or not self.voice_channel[id].is_connected():
      self.voice_channel[id] = await channel.connect()
      
      if self.voice_channel[id] == None:
        await interaction.followup.send('Failed to join voice channel.')
        return
      
    # If the bot is already in a voice channel, move it to the new channel.
    else:
      await self.voice_channel[id].move_to(channel)
  
  async def play_next(self, interaction: Interaction):
    '''
      This function will play the next song in the queue.

      Parameters:
      ----------
      interaction : 'discord.Interaction'
        The context object.
    '''
    id = int(interaction.guild.id)

    if not self.is_playing[id]:
      return
    # If the queue is not empty, play the next song.
    if self.queue_index[id] + 1 < len(self.music_queue[id]):
      self.is_playing[id] = True
      self.queue_index[id] += 1
      
      # Get the song to play.
      video_song: Video = self.music_queue[id][self.queue_index[id]][0]

      # Send a message to the channel.
      message = now_playing_embed(self, interaction, video_song)
      coro = interaction.followup.send(embed=message)

      # Run the coroutine in the event loop.
      fut = run_coroutine_threadsafe(coro, self.bot.loop)
      try:
        fut.result()
      except Exception as e:
        pass
      
      # Play the song.
      self.voice_channel[id].play(
        discord.FFmpegPCMAudio(
          video_song.source, 
          **FFMPEG_OPTIONS
        ), after=lambda e: self.play_next(interaction=interaction)
      )
      logger.info(f"Playing song: [{video_song.title}]({video_song.source})")
    else:
      self.queue_index[id] += 1
      self.is_playing[id] = False

  async def play_music(self, interaction: Interaction):
    '''
      This function will play the music fromt the music_queue.

      Parameters:
      ----------
      interaction : 'discord.Interaction'
        The context object.
    '''
    id = int(interaction.guild.id)

    if self.queue_index[id] < len(self.music_queue[id]):
      self.is_playing[id] = True
      self.is_paused[id] = False

      await self.join_voice_channel(interaction, self.music_queue[id][self.queue_index[id]][1])
      video_song: Video = self.music_queue[id][self.queue_index[id]][0]

      message = now_playing_embed(video_song)
      await interaction.followup.send(embed=message)
      
      try:
        self.voice_channel[id].play(
          discord.FFmpegPCMAudio(
            video_song.source,
            **FFMPEG_OPTIONS
          ), after=lambda e: self.play_next(interaction=interaction)
        )
        logger.info(f"Playing song: [{video_song.title}]({video_song.source})")
      except Exception as e:
        logger.error(f'Error playing song: {e}')
    else:
      await interaction.followup.send('Queue is empty.')
      self.queue_index[id] += 1
      self.is_playing[id] = False
  # endregion

  # region on_voice_state_update
  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    '''
      This function is called when a member's voice state is updated.
    '''
    id = int(member.guild.id)

    if member.id != self.bot.user.id and before.channel != None and after.channel != before.channel:
      remaining_channel_members = before.channel.members

      # If the bot is the only member in the voice channel, disconnect it.
      if len(remaining_channel_members) == 1 and remaining_channel_members[0].id == self.bot.user.id and self.voice_channel[id].is_connected():
        self.is_playing[id] = self.is_paused[id] = False
        self.music_queue[id] = []
        self.queue_index[id] = 0
        await self.voice_channel[id].disconnect()
        logger.info('Left the voice channel.')
  # endregion

  # region join
  @discord.slash_command(
    name="join",
    description="Music Player: Join the voice channel.",
    guild_ids=TEST_SERVER_ID
  )
  async def join(self, interaction: Interaction):
    '''
      This command will make the bot join the voice channel of the user.
    '''
    await interaction.response.defer()
    if interaction.user.voice:
      channel = interaction.user.voice.channel
      await self.join_voice_channel(interaction, channel)
      await interaction.followup.send(f'Joined {channel}.')
      logger.info(f'Music Player: Joined "{channel}" voice channel.')
    else:
      await interaction.followup.send('You are not in a voice channel.')
  # endregion

  # region slashcommand leave
  @discord.slash_command(
    name="leave",
    description="Music Player: Leave the voice channel.",
    guild_ids=TEST_SERVER_ID
  )
  async def leave(self, interaction: Interaction):
    '''
      This command will make the bot leave the voice channel.
    '''
    await interaction.response.defer()
    # Get the guild ID.
    id = int(interaction.guild.id)
    self.is_playing[id] = self.is_paused[id] = False
    self.music_queue[id] = []
    self.queue_index[id] = 0

    if self.voice_channel[id] != None:
      await interaction.followup.send('Music Player left the voice channel.')

      await self.voice_channel[id].disconnect()
      logger.info('Music Player left the voice channel.')
    else:
      await interaction.followup.send('Not in a voice channel.')
  # endregion

  # region slashcommand play
  @discord.slash_command(
    name="play",
    description="Music Player: Play a song.",
    guild_ids=TEST_SERVER_ID,
  )
  async def play(self, interaction: Interaction, query: str = ""):
    '''
      This command will play the song with the given query.
    '''
    await interaction.response.defer()

    id = int(interaction.guild.id)

    # Get the channel where the user is.
    try:
      user_channel = interaction.user.voice.channel
    except:
      await interaction.followup.send('You are not in a voice channel.', ephemeral=True)
      return
    
    # If the query is empty, play the next song in the queue.
    if query == "" or len(query) == 0:
      # If the queue is empty, return.
      if len(self.music_queue[id]) == 0:
        await interaction.followup.send('Queue is empty.', ephemeral=True)
        return
      # If the bot is not playing, play the next song.
      elif not self.is_playing[id]:
        # If the music queue is empty or the bot is not in a voice channel then play_music (join an play).
        if self.music_queue[id] == None or self.voice_channel[id] == None:
          await self.play_music(interaction)
        else:
          self.is_paused[id] = False
          self.is_playing[id] = True
          self.voice_channel[id].resume()
      else:
        return
    else:
      video_song = get_video_info(search_youtube(query=query)[0])

      # If the song is not found, return.
      if type(video_song) == type(True):
        await interaction.followup.send('Failed to get video information. Try something different', ephemeral=True)
        logger.error('Failed to get video information.')
        return
      
      # If the song is found, add it to the queue.
      else:
        self.music_queue[id].append([video_song, user_channel])
        
        if not self.is_playing[id]:
          await self.play_music(interaction)
        else:
          await interaction.followup.send(f'Added {video_song.title} to the queue.', ephemeral=True)
  # endregion

def setup(bot):
  '''
    This function will add the Music Player cog to the bot.
  '''
  bot.add_cog(MusicPlayer(bot))