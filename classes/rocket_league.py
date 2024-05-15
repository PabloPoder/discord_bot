'''
  This file contains the classes used to represent the data of a Rocket League player.
'''
from typing import List


class Playlist():
  '''
  Represents a rocket league playlist.
  '''
  def __init__(self, name, tier, tier_icon, division, mmr, peak_mmr, win_streak):
    self.name = name
    self.tier = tier
    self.tier_icon = tier_icon
    self.division = division
    self.mmr = mmr
    self.peak_mmr = peak_mmr
    self.win_streak = win_streak

  def __str__(self):
    return f"{self.name} - {self.tier} - {self.division} - {self.mmr} - {self.peak_mmr} - {self.win_streak}"

  @classmethod
  def from_dict(cls, playlist_dict):
    ''' Creates a new instance of a playlist from the data provided in the dictionary.

    Parameters
    ----------
    playlist_dict: dict
        The dictionary containing the data of the playlist.
    return: :class:`Playlist`
    '''
    metadata = playlist_dict.get("metadata", {})
    stats = playlist_dict.get("stats", {})
    tier = stats.get("tier", {}).get("metadata", {})
    division = stats.get("division", {}).get("metadata", {})
    return cls(
      name=metadata.get("name", ""),
      tier=tier.get("name", ""),
      tier_icon=tier.get("iconUrl", ""),
      division=division.get("name", ""),
      mmr=stats.get("rating", {}).get("value", 0),
      peak_mmr=stats.get("peakRating", {}).get("value", 0),
      win_streak=stats.get("winStreak", {}).get("displayValue", ""),
    )

class RocketLeaguePlayer():
  '''
  Represents a Rocket League player.
  '''
  def __init__(self,
    name,
    playlists:List[Playlist],
    wins,
    goals,
    saves,
    assists,
    goals_shot_ratio,
    trn_rating
  ):
    self.name = name
    self.playlists = playlists
    self.wins = wins
    self.goals = goals
    self.saves = saves
    self.assists = assists
    self.goals_shot_ratio = goals_shot_ratio
    self.trn_rating = trn_rating

  def __str__(self):
    return f"{self.name} - {self.playlists} - {self.wins} - {self.goals} - {self.saves} - {self.assists} - {self.goals_shot_ratio} - {self.trn_rating}"

  @classmethod
  def from_data(cls, data, playlists_data, lifetime_playlist):
    '''
    Creates a new instance of a Rocket League player from the data provided in the dictionary.
    '''
    name = data["data"]["platformInfo"]["platformUserIdentifier"]

    if lifetime_playlist is None:
      stats = {
        "wins": "-",
        "goals": "-",
        "saves": "-",
        "assists": "-",
        "goalShotRatio": "-",
        "tRNRating": "-"
      }
    else:
      stats = lifetime_playlist[0]["stats"]

    return cls(
      name = name,
      playlists = playlists_data,
      wins = stats["wins"]["displayValue"],
      goals = stats["goals"]["displayValue"],
      saves = stats["saves"]["displayValue"],
      assists = stats["assists"]["displayValue"],
      goals_shot_ratio = stats["goalShotRatio"]["displayValue"],
      trn_rating = stats["tRNRating"]["displayValue"]
    )
