'''
This cog contains a commands to interact with the Spotify API.
'''
import discord
from discord.ext import commands
from discord import Interaction

from apikeys import TEST_SERVER_ID, YOUR_USER_ID
from embeds.spotify_embeds import (
  create_playlist_created_embed,
  create_playlists_embed,
  create_tracks_embed
)
from services.spotifyclient import SpotifyClient

# region is_authorized_user
# this can be simplified by using the `commands.check` decorator directly
# and passing the predicate function as an argument
def is_authorized_user():
  '''
  Check if the user is authorized to use the Spotify commands.

  Returns:
  --------
  `commands.check`
    A check function that checks if the user is authorized to use the Spotify commands.
  '''
  def predicate(ctx):
    authorized_user_id = YOUR_USER_ID
    return ctx.author.id == authorized_user_id
  return commands.check(predicate)
# endregion

class Spotify(commands.Cog):
  '''
  A class used to represent the Spotify cog.
  '''
  def __init__(self, bot):
    self.bot = bot
    self.spotify_client = SpotifyClient()

  # region top_tracks
  @discord.slash_command(
    name="toptracks",
    description="Displays the admin user's top tracks. Needs admin verification.",
    guild_ids=TEST_SERVER_ID
  )
  @is_authorized_user()
  async def toptracks(self, interaction: Interaction, limit:int = 5):
    '''
    Display the admin user's top tracks.

    Parameters:
    -----------
    limit: `int`
      The number of top tracks to get. Default is 5.
    '''
    await interaction.response.defer()

    top_tracks = self.spotify_client.get_user_top_tracks(limit)

    if not top_tracks:
      await interaction.followup.send("No top tracks found.", ephemeral=True)
      return

    embed = create_tracks_embed(top_tracks)

    await interaction.followup.send(embed=embed)
  # endregion

  # region recommendations
  @discord.slash_command(
    name="recommendations",
    description="Displays recommendations base on the admin top tracks. Needs admin verification.",
    guild_ids=TEST_SERVER_ID
  )
  @is_authorized_user()
  async def recommendations(self, interaction: Interaction, limit:int = 5):
    '''
    Display the admin user's recommendations.

    Parameters:
    -----------
    limit: `int`
      The number of recommendations to get. Default is 5.
    '''
    await interaction.response.defer()

    recommendations = self.spotify_client.get_recommendations(limit)

    if not recommendations:
      await interaction.followup.send("No recommendations found.", ephemeral=True)
      return

    embed = create_tracks_embed(recommendations, is_recommendation=True)

    await interaction.followup.send(embed=embed)
  # endregion

  # region playlists
  @discord.slash_command(
    name="myplaylists",
    description="Displays the admin user's playlists.",
    guild_ids=TEST_SERVER_ID
  )
  async def myplaylists(self, interaction: Interaction, limit:int = 5):
    '''
    Display the admin user's playlists.

    Parameters:
    -----------
    limit: `int`
      The number of playlists to get. Default is 5.
    '''
    await interaction.response.defer()

    playlists = self.spotify_client.get_current_user_playlists(limit)

    if not playlists:
      await interaction.followup.send("No playlists found.")
      return

    embed = create_playlists_embed(playlists)

    await interaction.followup.send(embed=embed)

  @discord.slash_command(
    name="playlists",
    description="Displays the playlists of the user.",
    guild_ids=TEST_SERVER_ID
  )
  async def playlists(self, interaction: Interaction, user:str, limit:int = 5):
    '''
    Display the playlists of the user.

    Parameters:
    -----------
    user: `str`
      The user to get the playlists from.
    limit: `int`
      The number of playlists to get. Default is 5.
    '''
    await interaction.response.defer()

    playlists = self.spotify_client.get_playlist_from_user_id(user, limit)

    if not playlists:
      await interaction.followup.send("No playlists found.", ephemeral=True)
      return

    embed = create_playlists_embed(playlists)

    await interaction.followup.send(embed=embed)

  @discord.slash_command(
    name="createplaylist",
    description="Creates a playlist with the admin user's top tracks and recommendations. Needs admin verification.",
    guild_ids=TEST_SERVER_ID
  )
  @is_authorized_user()
  async def createplaylist(
    self,
    interaction: Interaction,
    name:str = "My recommended playlist",
    description:str = "A playlist with recommended songs by Rachael Nexus-7",
  ):
    '''
    Create a playlist with the admin user's top tracks and recommendations.

    Parameters:
    -----------
    name: `str`
      The name of the playlist. Default is "My recommended playlist".
    description: `str`
      The description of the playlist. Default is 
      "A playlist with recommended songs by Rachael Nexus-7".
    '''
    await interaction.response.defer()

    playlist_url = self.spotify_client.create_playlist()

    embed = create_playlist_created_embed(
      playlist_url=playlist_url,
      name=name,
      description=description
    )

    if not playlist_url:
      await interaction.followup.send("Failed to create playlist.", ephemeral=True)
      return

    await interaction.followup.send(embed=embed)
    await interaction.followup.send(playlist_url)
  # endregion

def setup(bot):
  '''
    the Spotify cog to the bot.
  '''
  bot.add_cog(Spotify(bot))
