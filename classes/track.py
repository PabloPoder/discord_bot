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

  def from_dict(self, data:dict):
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
    return Track(
      track_id=data['id'],
      name=data['name'],
      # artist is a list of dictionaries, so we get the name of each artist and the id
      artists = [
        {
          'name': artist['name'], 
          'id': artist['id']
        } for artist in data['artists']
      ],
      album=data['album']['name'],
      images=data['album']['images'][0],
      uri=data['uri']
    )
