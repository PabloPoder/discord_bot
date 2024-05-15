
import discord
from discord.ext import commands
from discord import Interaction

from apikeys import TEST_SERVER_ID 
from embeds.common_embeds import create_avatar_embed, create_commands_embed, create_eeorigins_embed, create_error_embed, create_weather_embed
from embeds.book_embeds import create_base_book_embed
from embeds.rocket_league_embeds import create_base_rl_embed
from services.books import get_books
from services.rocket_league import get_rocket_league_stats_data
from services.weather import get_weather_data
from ui.BooksDropdown import BooksDropdown
from ui.RLPlaylistsDropdown import RLPlaylistsDropdown

class Utilities(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # region help
  @discord.slash_command(name="commands", description="Displays all the commands", guild_ids=TEST_SERVER_ID)
  async def commands(self, interaction: Interaction):
    await interaction.response.defer()

    # Search the gif to display
    file = discord.File(f"images/blade-runner-rachael1.gif", filename=f"blade-runner-rachael1.gif")
    
    # Create the embed with the commands
    embed = create_commands_embed(image = self.bot.user.display_avatar)

    # Send the embed
    await interaction.followup.send(
      file=file, 
      embed=embed
    )
  # endregion

  # region avatar
  @discord.slash_command(name="avatar", description="Displays the avatar of an user", guild_ids=TEST_SERVER_ID)
  async def avatar(self, interaction: Interaction, user: discord.Member):
    # Defer the response to prevent timeout
    await interaction.response.defer()
    
    # Create the embed with the user's information
    embed = create_avatar_embed(user=user)

    # Send the message with the embed
    await interaction.followup.send(embed=embed)
  # endregion  

  # region eeorigins
  @discord.slash_command(name="eeorigins", description="Gives you the guide to make Origins EE", guild_ids=TEST_SERVER_ID)
  async def eeorigins(self, interaction: Interaction):
    # Defer the response to prevent timeout
    await interaction.response.defer()

    embed = create_eeorigins_embed()

    # Send the message with the embed
    await interaction.followup.send(embed=embed)
  # endregion 

  # region weather information
  @discord.slash_command(name='weather', description='Gives you the current weather by city name', guild_ids=TEST_SERVER_ID)
  async def weather(self, interaction: Interaction, city):
    ''' Get the current weather by city name

    Parameters
    ----------
    city: 'str'
        The name of the city to get the weather data from.
    '''
    # Defer the response to prevent timeout
    await interaction.response.defer()

    # Get the weather data from the city
    weather_data = await get_weather_data(city)

    # Check if the weather data was fetched
    if weather_data is None:
      embed = create_error_embed(title="Error 🤖", description="An error occurred while fetching the weather data."
      )
      await interaction.followup.send(embed=embed)
      return 
    
    # Create the embed with the weather data
    embed = create_weather_embed(weather_data=weather_data)  

    # Send the message with the embed
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
    # Defer the response to prevent timeout
    await interaction.response.defer()

    # Get the player's stats 
    player = await get_rocket_league_stats_data(nametag=nametag)

    # Check if the player exists
    if player is None:
      # Create the error embed
      embed = create_error_embed(title="That player doesn't exist! 👻", description=f"Player with nametag {nametag} not found.")
      await interaction.followup.send(embed=embed)
      return

    # Create the view with the playlist
    view = discord.ui.View()
    view.add_item(RLPlaylistsDropdown(playlists=player.playlists, player=player))

    # Create the embed with the player's stats
    embed = create_base_rl_embed(player=player)
    
    # Send the message with the embed
    await interaction.followup.send(view=view, embed=embed)
  # endregion

  # region books
  @discord.slash_command(name="books", description="Search for books that contain this text", guild_ids=TEST_SERVER_ID)
  async def books(self, interaction: Interaction, query: str):
    """Search for books that contain this text

    Parameters
    ----------
    query: str
      The text to search for in the books.
    """
    # Defer the response to prevent timeout
    await interaction.response.defer()

    # Get the books from the query text
    books = await get_books(query)

    # Check if books were found
    if not books:
      embed = create_error_embed(title="No Books Found 📚", description="No books found for your query.")
      await interaction.followup.send(embed=embed)
      return

    # Create the view with the books
    view = discord.ui.View()
    view.add_item(BooksDropdown(books=books))

    # Create the base embed with the book's template
    embed = create_base_book_embed()

    # Send the message with the view and the embed
    await interaction.followup.send(view=view, embed=embed)
  # endregion

def setup(bot):
  bot.add_cog(Utilities(bot))
