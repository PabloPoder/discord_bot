'''
This module contains the commands for the utilities cog. 
The utilities cog contains commands that provide information about the bot, 
the user, and other utilities like weather, books, and rocket league stats.
'''
import discord
from discord.ext import commands
from discord import Interaction

from utils.apikeys import TEST_SERVER_ID
from embeds.common_embeds import (
  create_avatar_embed,
  create_commands_embed,
  create_eeorigins_embed,
  create_error_embed,
  create_weather_embed
)
from embeds.book_embeds import create_base_book_embed
from embeds.rocket_league_embeds import create_base_rl_embed
from services.books import get_books
from services.rocket_league import get_rocket_league_stats_data
from services.weather import get_weather_data
from ui.books_dropdown import BooksDropdown
from ui.rocketleague_playlists_dropdown import RLPlaylistsDropdown

from utils.logger_config import logger

class Utilities(commands.Cog):
  '''
  A class used to represent the utilities cog.
  '''
  def __init__(self, bot):
    self.bot = bot

  # region help
  @discord.slash_command(
    name="commands",
    description="Displays all the commands",
    guild_ids=TEST_SERVER_ID
  )
  async def commands(self, interaction: Interaction):
    ''' 
    Displays all the commands available
    '''
    await interaction.response.defer()

    file = discord.File("images/blade-runner-rachael1.gif", filename="blade-runner-rachael1.gif")

    embed = create_commands_embed(image = self.bot.user.display_avatar)

    await interaction.followup.send(
      file=file,
      embed=embed
    )
  # endregion

  # region ping
  @discord.slash_command(
    name="ping",
    description="Check if the bot is online",
    guild_ids=TEST_SERVER_ID,
  )
  async def ping(self, interaction: Interaction):
    '''
    This function is called when the user sends the `/ping` command.
    It sends a message to the user with the latency of the bot.
    '''
    logger.info(f"Received ping request from {interaction.user.name}")
    latency = f"{round(self.bot.latency *1000)}ms"
    
    await interaction.send(f"Pong! {latency}")
    logger.info(f"Sent pong request from {interaction.user.name} with latency {latency}")
  # endregion


  # region avatar
  @discord.slash_command(
    name="avatar",
    description="Displays the avatar of an user",
    guild_ids=TEST_SERVER_ID
  )
  async def avatar(self, interaction: Interaction, user: discord.Member):
    '''
    Displays the avatar of an user.
    '''
    await interaction.response.defer()

    embed = create_avatar_embed(user=user)

    await interaction.followup.send(embed=embed)
  # endregion

  # region eeorigins
  @discord.slash_command(
    name="eeorigins",
    description="Gives you the guide to make Origins EE",
    guild_ids=TEST_SERVER_ID
  )
  async def eeorigins(self, interaction: Interaction):
    '''
    Gives you the guide to make Origins EE
    '''
    await interaction.response.defer()

    embed = create_eeorigins_embed()

    await interaction.followup.send(embed=embed)
  # endregion

  # region weather information
  @discord.slash_command(
    name='weather',
    description='Gives you the current weather by city name',
    guild_ids=TEST_SERVER_ID
  )
  async def weather(self, interaction: Interaction, city):
    ''' Get the current weather by city name

    Parameters
    ----------
    city: 'str'
        The name of the city to get the weather data from.
    '''
    await interaction.response.defer()

    weather_data = await get_weather_data(city)

    if weather_data is None:
      embed = create_error_embed(
        title="Error 🤖",
        description="An error occurred while fetching the weather data."
      )
      await interaction.followup.send(embed=embed)
      return

    embed = create_weather_embed(weather_data=weather_data)

    await interaction.followup.send(embed=embed)
  # endregion

  # region rocket league stats
  @discord.slash_command(name='rlrank', description=' Get the stats from a player of Rocket League',
    guild_ids=TEST_SERVER_ID,
  )
  async def rlrank(self, interaction: Interaction, nametag:str):
    ''' Get the stats from a player of Rocket League

    Parameters
    ----------
    nametag: str
        The name of the player to get the stats from.
    '''
    await interaction.response.defer()

    player = await get_rocket_league_stats_data(nametag=nametag)

    if player is None:
      embed = create_error_embed(
        title="That player doesn't exist! 👻",
        description=f"Player with nametag {nametag} not found."
      )
      await interaction.followup.send(embed=embed)
      return

    view = discord.ui.View()
    view.add_item(RLPlaylistsDropdown(playlists=player.playlists, player=player))

    embed = create_base_rl_embed(player=player)

    await interaction.followup.send(view=view, embed=embed)
  # endregion

  # region books
  @discord.slash_command(
    name="books",
    description="Search for books that contain this text",
    guild_ids=TEST_SERVER_ID
  )
  async def books(self, interaction: Interaction, query: str):
    """Search for books that contain this text

    Parameters
    ----------
    query: str
      The text to search for in the books.
    """
    await interaction.response.defer()

    books = await get_books(query)

    if not books:
      embed = create_error_embed(
        title="No Books Found 📚",
        description="No books found for your query."
      )
      await interaction.followup.send(embed=embed)
      return

    view = discord.ui.View()
    view.add_item(BooksDropdown(books=books))

    embed = create_base_book_embed()

    await interaction.followup.send(view=view, embed=embed)
  # endregion

def setup(bot):
  '''
  Add the Utilities cog to the bot.
  '''
  bot.add_cog(Utilities(bot))
