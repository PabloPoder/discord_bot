'''
This module contains the commands that only the administrator can use.
'''
import discord
from discord.ext import commands
from discord import Interaction

from utils.apikeys import TEST_SERVER_ID

from utils.logger_config import logger

class Admin(commands.Cog):
  ''' A class representing the admin functionality of the bot. '''

  def __init__(self, bot):
    self.bot = bot

  # TODO: Fix the clear command - can't 'followup.send' because the interaction is deleted
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
    logger.info("Clearing messages...")

    await interaction.response.defer()

    try:
      await interaction.channel.purge(limit=amount)
      await interaction.followup.send(f"{amount} messages were deleted!", ephemeral=True)
      logger.info(f"{amount} messages were deleted!")
    except Exception as e:
      logger.error(f"Failed to clear messages. Error: {e}")
      await interaction.followup.send(f"Failed to clear messages. Error: {e}", ephemeral=True)
      return
  # endregion

def setup(bot):
  '''
  Add the Admin cog to the bot.
  '''
  bot.add_cog(Admin(bot))
