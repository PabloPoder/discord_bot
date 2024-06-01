'''
This module contains the commands that only the administrator can use.
'''
import discord
from discord.ext import commands
from discord import Interaction

from embeds.common_embeds import create_clear_embed
from utils.apikeys import TEST_SERVER_ID

from utils.logger_config import logger

class Admin(commands.Cog):
  ''' A class representing the admin functionality of the bot. '''

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
    logger.info("Clearing messages...")
    await interaction.response.defer()

    # Get the interaction where the command was called cause the interaction can be deleted
    channel = interaction.channel
    embed = create_clear_embed(amount=amount)

    try:
      await channel.purge(limit=amount)
      await channel.send(embed=embed, delete_after=5)
      logger.info(f"{amount} messages were deleted!")
    except Exception as e:
      logger.error(f"Failed to clear messages. Error: {e}")
      await channel.send(f"Failed to clear messages. Error: {e}", delete_after=5)
      return
  # endregion

def setup(bot):
  '''
  Add the Admin cog to the bot.
  '''
  bot.add_cog(Admin(bot))
