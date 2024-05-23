'''
This file contains the Track class, which is used to represent a track of Spotify.
'''

from typing import List

class Track:
  '''
  A class used to represent a track of Spotify.
  '''
  def __init__(self,
    track_id:str,
    name:str,
    artists:List[str],
    album:str,
    images:str,
    uri:str
  ):
    self.track_id = track_id
    self.name = name
    self.artists = artists
    self.album = album
    self.images = images
    self.uri = uri

  def __str__(self):
    artist_names = ', '.join([artist['name'] for artist in self.artists])
    return f"{self.name} by {artist_names} from {self.album} ({self.uri})"

  @classmethod
  def from_dict(cls, data:dict):
    '''
    Create a Track object from a dictionary.
    
    Parameters:
    ----------
    data : dict
      The dictionary with the track data.

    Returns:
    -------
    `Track`
      The Track object created from the dictionary.
    '''
    return cls(
      track_id=data.get('id', ""),
      name=data.get('name', ""),
      # artist is a list of dictionaries, so we get the name of each artist and the id
      artists = [
        {
          'name': artist.get('name', ""),
          'id': artist.get('id', ""),
        } for artist in data['artists']
      ],
      album=data.get('album', {}).get('name', ""),
      images=data.get('album', {}).get('images', [{}])[0].get('url', ""), # get the first image
      uri=data.get('external_urls', {}).get('spotify', "")
    )

class Playlist:
  '''
  A class used to represent a playlist of Spotify.
  '''
  def __init__(self,
    playlist_id:str,
    name:str,
    description:str,
    images:str,
    uri:str
  ):
    self.playlist_id = playlist_id
    self.name = name
    self.description = description
    self.images = images
    self.uri = uri

  def __str__(self):
    return f"{self.name} - {self.description} ({self.uri})"

  @classmethod
  def from_dict(cls, data:dict):
    '''
    Create a Playlist object from a dictionary.
    
    Parameters:
    ----------
    data : dict
      The dictionary with the playlist data.

    Returns:
    -------
    `Playlist`
      The Playlist object created from the dictionary.
    '''
    return cls(
      playlist_id=data.get('id', ""),
      name=data.get('name', ""),
      description=data.get('description', ""),
      images=data.get('images', [{}])[0].get('url', ""), # get the first image
      uri=data.get('external_urls', {}).get('spotify', "")
    )