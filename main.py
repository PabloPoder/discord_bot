import os

import discord 
from discord.ext import commands

from apikeys import BOT_TOKEN

intents = discord.Intents.all()
intents.members = True

description = '''An example bot to showcase the disxord.ext.commands extension module.
There are a number of utility commands bein showcased here'''

bot = commands.Bot(command_prefix='/', intents=intents)

# region on_readey event
@bot.event
async def on_ready():
  await bot.change_presence(
    activity=discord.Activity(
      type=discord.ActivityType.listening,
      name=f"`/`",
      state=f"Ready to serve {len(bot.users)} users!" ,
    )
  )

  print(f"{bot.user.name} is ready!")
  print("------")
# endregion

# # region commands
# @bot.slash_command(name="hello", description="Say hi to Rachael")
# async def hello(interaction: Interaction):
#   await interaction.send("Hello, I am Rachael!")
# # endregion

# region load_extensions
# Load all the extensions in the cogs folder
def load_extensions():
  initial_extensions = []

  for filename in os.listdir("./cogs"):
    if(filename.endswith(".py")):
      initial_extensions.append("cogs." + filename[:-3])

  if __name__ == "__main__":
    for extension in initial_extensions:
      bot.load_extension(extension)
# endregion

load_extensions()
bot.run(BOT_TOKEN)