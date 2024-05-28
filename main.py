'''
This module is the main entry point for the bot. It initializes 
the bot and loads all the extensions in the cogs folder.
'''
import os

import discord
from discord.ext import commands
from utils.logger_config import logger

from utils.apikeys import BOT_TOKEN, TEST_SERVER_ID

intents = discord.Intents.all()

# bot = commands.Bot(command_prefix='/', intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents)

# region on_ready event
@bot.event
async def on_ready():
  '''
  This event is called when the bot is ready to start sending requests to Discord.
  '''
  await bot.change_presence(
    activity=discord.Activity(
      type=discord.ActivityType.listening,
      name="`/`",
      state=f"Ready to serve {len(bot.users)} users!" ,
    )
  )
  logger.info(f"{bot.user.name} is ready!")
  print("------")
# endregion


bot.slash_command(
  name="ping",
  description="Check if the bot is online",
  guild_ids=[TEST_SERVER_ID],
)
async def ping(interaction= discord.Interaction):
  '''
  This function is called when the user sends the `/ping` command.
  It sends a message to the user with the latency of the bot.
  '''
  await interaction.send(f"Pong! {round(bot.latency * 1000)}ms")

# region load_extensions
def load_extensions():
  ''' 
  Load all the extensions in the cogs folder.

  Parameters
----------
  None
  '''
  initial_extensions = []

  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      initial_extensions.append("cogs." + filename[:-3])

  if __name__ == "__main__":
    for extension in initial_extensions:
      bot.load_extension(extension) 
# endregion


load_extensions()
bot.run(BOT_TOKEN)
