import aiohttp

from classes.Weather import WeatherData

from apikeys import WEATHER_ENDPOINT, WEATHER_TOKEN

async def get_weather_data(city:str):
  '''Get the weather data from the OpenWeatherMap API

  Parameters
  ----------
  city: str
      The name of the city to get the weather data from.
  return: :class:`WeatherData` | `None`
      The weather data from the OpenWeatherMap API.
  '''
  # Set the parameters for the request
  weather_params = {
      "q": city,
      "appid": WEATHER_TOKEN,
      "units": 'metric'
  }

  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(WEATHER_ENDPOINT, params=weather_params) as response:
        response.raise_for_status()  # Raise an exception for 4XX or 5XX errors
        data = await response.json()

        if data is None:
          return None

        # Create a WeatherData object with the fetched data
        weather_data = WeatherData.from_dict(data)

        return weather_data
  
  except Exception as e:
    return None
