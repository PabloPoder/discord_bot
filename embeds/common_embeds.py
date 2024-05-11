from discord import Embed, Member

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
    color=0x02DCFF, 
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
    color=0x02DCFF,
    title=f"{weather_data.name}, {weather_data.country}"
  )

  embed.set_author(icon_url=weather_data.icon, name=weather_data.main)
  embed.set_thumbnail(url=weather_data.icon)

  embed.add_field(name='Temperature', value=f"{weather_data.temp} °C")
  embed.add_field(name='Feels Like', value=weather_data.feels_like, inline=True)
  embed.add_field(name='Sky Condition', value=weather_data.description, inline=True)
  embed.add_field(name='Wind Speed', value=weather_data.speed)
  embed.add_field(name='Humidity', value=weather_data.humidity, inline=True)
  embed.add_field(name='Coulds', value=f"{weather_data.clouds} %", inline=True)

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
    color=0xe74c3c, 
    title=title, 
    description=description
  )

  return embed