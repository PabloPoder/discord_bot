'''
This module contains the commands that only the administrator can use.
'''
import discord
from discord.ext import commands
from discord import Interaction

from apikeys import TEST_SERVER_ID


class Admin(commands.Cog):
  """A class representing the admin functionality of the bot."""

  def __init__(self, bot):
    self.bot = bot

  # region clear messages only administrator
  @discord.slash_command(
    name="clear",
    description="Clears an amount of messages",
    guild_ids=TEST_SERVER_ID
  )
  @commands.has_permissions(administrator=True)
  async def clear(self, interaction: Interaction, amount: int):
    '''Clears an amount of messages

    Parameters
    ----------
    amount : `int`, optional
        The amount of messages to clear.
    '''
    # Defer the response to prevent timeout
    await interaction.response.defer()

    # Delete the messages
    await interaction.channel.purge(limit=amount)

    # Send the message with the amount of messages deleted
    await interaction.followup.send(f"{amount} messages were deleted!", ephemeral=True)


def setup(bot):
  '''
  Add the Admin cog to the bot.
  '''
  bot.add_cog(Admin(bot))
