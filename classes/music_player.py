'''
 This module contains the classes to representes util data of youtube.
'''

class Video:
  '''
    Video Class
  '''
  def __init__(
    self,
    title,
    description,
    duration,
    source,
    url,
    thumbnail
  ):
    self.title = title
    self.description = description
    self.duration = duration
    self.source = source
    self.url = url
    self.thumbnail = thumbnail

  def __str__(self):
    return f"{self.title} - {self.description} - {self.duration} - [source]({self.source}) - [url]({self.url}) - [thumbnail]({self.thumbnail})"
  
  @classmethod
  def from_dic(cls, data: dict, video_id):
    '''
      Creates a new instance of a video from the data provided in the dictionary.

      Parameters:
      ----------
      data: `dict`
        The dictionary with the data.
      
      Returns:
      --------
      return: :class:`Video`
    '''
    
    # Source: 
    # data['url']: Use this if you only need to play the audio on Discord without specific format preferences.
    # data['formats'][n]['url']: Use this if you have preferences for the audio format, such as Opus or MP3, 
    # or if you need to adjust the audio quality.
    return cls(
      title=data.get('title', ""),
      description=data.get('description', ""),
      duration=data.get('duration', ""),
      source=data.get('url', ""),
      url="https://www.youtube.com/watch?v=" + video_id,
      thumbnail="https://i.ytimg.com/vi/" + video_id + "/hqdefault.jpg",
    )