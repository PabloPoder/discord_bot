import discord
from discord.ext import commands
from discord import Interaction

from apikeys import TEST_SERVER_ID

class Admin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # region clear messages only administrator
  @discord.slash_command(name="clear", description="Clears an ammount of messages", guild_ids=TEST_SERVER_ID)
  @commands.has_permissions(administrator=True)
  async def clear(self, interaction: Interaction, ammount: int):
    '''Clears an ammount of messages

    Parameters
    ----------
    ammount : `int`, optional
        The ammount of messages to clear.
    '''
    # Defer the response to prevent timeout
    await interaction.response.defer()  

    # Delete the messages
    await interaction.channel.purge(limit=ammount)

    # Send the message with the ammount of messages deleted
    await interaction.followup.send(f"{ammount} messages were deleted!", ephemeral=True)


def setup(bot):
  bot.add_cog(Admin(bot))
