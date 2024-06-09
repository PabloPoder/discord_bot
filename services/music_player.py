'''
  This module contains methods to interact with youtube. 
'''
import re
from urllib import parse, request
from yt_dlp import YoutubeDL

from classes.music_player import Video
from utils.const import YTDL_OPTIONS
from utils.logger_config import logger

# region search_youtube
def search_youtube(query:str) -> list[str]:
  '''
    This function will search YouTube for the given query.

    Parameters:
    ----------
    query : 'str'
      The search query.

    Returns:
    -------
    'list': 
      A list of video IDs.
  '''
  if not query: return []
  # Encode the dictionary (query) to make it secure (correct url) and thus include it in the final url.
  # example: milky chance -> search_query=python+tutorial.
  query_string = parse.urlencode({'search_query': query})
  # Get the html content from the result page. (List of videos)
  html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
  # Extract all the URLs from the videos resulting from the HTML Content.
  search_results = re.findall(
    r'/watch\?v=(.{11})', 
    html_content.read().decode()
  )
  return search_results[0:5]
# endregion

# region get_video_info
def get_video_info(video_id:str) -> Video:
  '''
    This function will get the information of the video with the given video ID.

    Parameters:
    ----------
    video_id : 'str'
      The video ID of the video.
      
    Returns:
    -------
    `Video` or `None` 
      A `Video` object containing the information of the video.
      None if a Exception occurs 
  '''
  with YoutubeDL(YTDL_OPTIONS) as ydl:
    try:
      video_info = ydl.extract_info(video_id, download=False)
    except Exception as e:
      return None
  return Video.from_dic(data=video_info, video_id=video_id)
# endregion

# TODO: deprecated function?
# region download_audio - local file
def download_audio(video:Video):
  '''
    This function downloads the audio from the provided video,
    and save it localy

    Parameters:
    ----------
    video: `Video`
      The video object with the data.

    Returns:
    path: str
      Return the filename of the song.
  '''
  with YoutubeDL(YTDL_OPTIONS) as ydl:
    info_dict = ydl.extract_info(video.url, download=True)
    return ydl.prepare_filename(info_dict)
# endregion