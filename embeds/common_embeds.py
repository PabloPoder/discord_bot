'''
This module contains the functions to create the embeds of the bot.
'''
import discord
from discord import Asset, Embed, Member

from services.weather import WeatherData

def create_avatar_embed(user: Member):
  '''Create an embed with the user's information

  Parameters
  ----------
  user: :class:`discord.Member`
    The user to create the embed from.
  return: :class:`Embed`
    The embed with the user's information.
  '''
  # Get the user's date information and format it
  created_at = user.created_at.strftime("%b %d, %Y")
  joined_at = user.joined_at.strftime("%b %d, %Y") if user.joined_at else " _ "

  # Create the embed with the user's information
  embed: Embed = Embed(
    color = user.color,
    title = f"{user.top_role}",
    description = f"{created_at} · {joined_at}"
  )
  embed.set_image(url=user.avatar)
  embed.set_author(icon_url=user.avatar, name=user.name)

  return embed

def create_eeorigins_embed():
  ''' Create an embed with the guide to make Origins EE

  return: :class:`Embed`  
  '''
  # Create an embed with the guide to make Origins EE
  embed: Embed = Embed(
    color=discord.Color.blurple(),
    title="Origins Easter Egg Guide",
    description="'Every story has a beginning... and an end.'\n— 'Origins' trailer"
  )
  embed.set_image("https://i.imgur.com/GMtg61Q.jpeg")
  embed.set_footer(text="Good Luck!")

  return embed

def create_weather_embed(weather_data: WeatherData):
  '''Create an embed with the weather data

  Parameters
  ----------
  weather_data: :class:`WeatherData`
    The weather data to create the embed from.
  return: :class:`Embed`
    The embed with the weather data.
  '''
  # Create the embed with the weather data
  embed: Embed = Embed(
    color=discord.Color.blurple(),
    title=f"{weather_data.name}, {weather_data.country}"
  )

  embed.set_author(icon_url=weather_data.icon, name=weather_data.main)
  embed.set_thumbnail(url=weather_data.icon)

  embed.add_field(name='Temperature', value=f"{weather_data.temp} °C")
  embed.add_field(name='Feels Like', value=weather_data.feels_like, inline=True)
  embed.add_field(name='Sky Condition', value=weather_data.description, inline=True)
  embed.add_field(name='Wind Speed', value=weather_data.speed)
  embed.add_field(name='Humidity', value=weather_data.humidity, inline=True)
  embed.add_field(name='Clouds', value=f"{weather_data.clouds} %", inline=True)

  # Add a footer to the embed if the weather is cold or cloudy
  if int(weather_data.clouds) >= 70 or int(weather_data.temp) <= 12:
    embed.set_footer(
      text="Perfect time to play Skyrim!",
      # skyrim logo:
      icon_url="https://images.uesp.net/6/6b/SR-icon-logo.jpg"
    )

  return embed

def create_error_embed(title: str, description: str):
  '''Create an embed with the error message

  Parameters
  ----------
  title: `str`
    The title of the embed.
  description: `str`
    The description of the embed.
  return: :class:`Embed`
    The embed with the error message.
  '''
  # Create the embed with the error message
  embed: Embed = Embed(
    color=discord.Color.red(),
    title=title,
    description=description
  )

  return embed

def create_commands_embed(image: Asset):
  '''Create an embed with all the commands of the bot

  Parameters
  ----------
  image: `Asset`
    The image of the bot.
  return: :class:`Embed`
    The embed with all the commands of the bot.
  '''
  # Create an embed with all the commands of the bot
  # Create embed with all the commands of my bot
  embed = discord.Embed(
    title="Commands",
    description="Here are all my commands ",
    color=discord.Color.blurple()
  )

  embed.set_thumbnail(url=image)

  embed.add_field(name="`/avatar`", value="Displays the avatar of an user.", inline=False)
  embed.add_field(name="`/eeorigins`", value="Gives you the guide to make Origins EE", inline=False)
  embed.add_field(
    name="`/weather`",
    value="Gives you the current weather by city name",
    inline=False
  )
  embed.add_field(
    name="`/rlrank`",
    value="Get the stats from a player of Rocket League",
  )
  embed.add_field(
    name="`/books`",
    value="Search for books that contain this text",
    inline=False
  )
  embed.add_field(
    name="`/toptracks`",
    value="Get the top tracks of the admin's spotify account",
  )
  embed.add_field(
    name="`/recommendations`",
    value="Get the recommendations base on the admin's spotify account",
    inline=False
  )
  embed.add_field(
    name="`/myplaylists`",
    value="Get the playlists of the admin's spotify account",
  )
  embed.add_field(
    name="`/commands`",
    value="Displays this message",
    inline=False
  )
  embed.add_field(name="`Creator:`", value="@ZOMB_-Frank", inline=False)

  embed.set_author(name="Rachael Nexus-7 🤖🕵️🦄", icon_url=image)
  embed.set_footer(
    text="Tyrell Corporation ",
    icon_url="https://res.cloudinary.com/teepublic/image/private/s--JL6qhWBz--/c_crop,x_10,y_10/c_fit,h_830/c_crop,g_north_west,h_1038,w_1038,x_-104,y_-104/l_upload:v1565806151:production:blanks:vdbwo35fw6qtflw9kezw/fl_layer_apply,g_north_west,x_-215,y_-215/b_rgb:000000/c_limit,f_auto,h_630,q_auto:good:420,w_630/v1663152101/production/designs/34889022_0.jpg"
  )

  return embed

def create_clear_embed(amount: int):
  '''
  Create an embed to show when the messages were cleared.

  Returns
  -------
  :class:`Embed`
    The embed with the message that the messages were cleared.
  '''
  embed = discord.Embed(
    title="Messages Cleared",
    description=f"{amount} messages were cleared successfully!",
    color=discord.Color.red()
  )

  return embed

