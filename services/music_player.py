'''
This module is responsible for playing music.
'''
import asyncio
from discord import Interaction
import yt_dlp

yt_dl_options = {
  "format": "bestaudio/best",
  "postprocessors": [{
    "key": "FFmpegExtractAudio",
    "preferredcodec": "mp3",
    "preferredquality": "192",
  }],
}

ytdl = yt_dlp.YoutubeDL(yt_dl_options)
ffmpeg_options = {"options": "-vn"}


async def download_song(url:str):
  '''
  Download a song from YouTube.
  
  Parameters
  ----------
  url : str
    The URL of the song to download.

  Returns
  -------
  str
    The URL of the song.
  str
    The title of the song.
  str
    The thumbnail of the song.
  '''
  # Download the song. This is a blocking operation, so we run it in a separate thread
  loop = asyncio.get_event_loop()
  data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

  if data is None:
    return None, None, None

  return data["url"], data["title"], data["thumbnail"]

def play_next(self, guild_id, voice_client):
  '''
  Play the next song in the queue.

  Parameters
  ----------
  guild_id : int
    The ID of the guild.
  voice_client : `discord.VoiceClient`
    The voice client object.
  Returns
  -------
  None
  '''
  if guild_id in self.queues and len(self.queues[guild_id]) > 0:
    player = self.queues[guild_id].pop()
    voice_client.play(
      player,
      after=lambda e:
        asyncio.run_coroutine_threadsafe(
          self.play_next(guild_id, voice_client),
          self.bot.loop
        ) if e is None else None)