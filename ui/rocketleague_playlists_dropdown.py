'''
 This module contains the dropdown for the Rocket League playlists.
'''
from typing import List

from discord.ui import Select
from discord import Interaction, SelectOption

from embeds.rocket_league_embeds import create_rl_embed
from services.rocket_league import Playlist, RocketLeaguePlayer

class RLPlaylistsDropdown(Select):
  '''
  A dropdown for Rocket League playlists.
  '''
  def __init__(self,
    playlists: List[Playlist] = None,
    player: RocketLeaguePlayer = None
  ):
    self.playlists = playlists
    self.player = player
    options = [
      SelectOption(
        label=playlist.name,
        value=playlist.name
      ) for playlist in self.playlists]

    super().__init__(options=options, placeholder="Select a playlist to view its details...")

  async def callback(self, interaction: Interaction):
    # Get the selected book
    playlist = next(playlist for playlist in self.playlists
      if playlist.name == interaction.data["values"][0]
    )

    # if the selected book is not found in the list then return
    if not playlist:
      await interaction.followup.send("Playlist not found!")

    # Create an embed with the book's information
    embed = create_rl_embed(playlist=playlist, player=self.player)

    # Edit the original message with the embed containing the book's information
    await interaction.response.edit_message(embed=embed)
