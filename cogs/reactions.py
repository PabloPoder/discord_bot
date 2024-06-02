'''
This file contains the code for the reactions cog.
'''
import discord
from discord.ext import commands

from utils.const import WORDS_TO_REACT
from utils.logger_config import logger

class Reactions (commands.Cog):
    '''
    This class contains the reactions cog.
    '''
    def __init__ (self, bot):
        self.bot = bot

    # region Commands
    @commands.Cog.listener()
    async def on_message (self, message: discord.Message):
        '''
        This function is called whenever a message is sent in a channel 
        that the bot has access to.
        '''
        if message.author == self.bot.user:
            return

        # Baldwin IV of Jerusalem Reaction
        if message.content.lower() in [word for word in WORDS_TO_REACT]:
            await message.add_reaction('✋🏻')
            await message.add_reaction('😔')
            await message.channel.send("https://media1.tenor.com/m/mBywuwFuhvMAAAAd/king-baldwin.gif")
            logger.info(f"Added reactions to message from {message.author.name}")
        # endregion

def setup (bot):
    '''
    This function sets up the reactions cog.
    '''
    bot.add_cog(Reactions(bot))
