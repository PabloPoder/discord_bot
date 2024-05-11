class WeatherData:
  def __init__(self, name, country, icon, description, temp, feels_like, speed, humidity, clouds, main):
    self.name = name
    self.country = country
    self.main = main
    self.icon = f"http://openweathermap.org/img/w/{icon}.png"
    self.description = description
    self.temp = temp
    self.feels_like=  f"{feels_like} °C"
    self.humidity = f"{humidity} %"
    self.speed = f"{speed} m/seg"
    self.clouds = clouds
  
  @classmethod
  def from_dict(cls, data):
    ''' Construct a new instance from a dictionary
    
    Parameters
    ----------
    data: `dict`
        The dictionary to construct the new instance from.
    return: :class:`WeatherData`
    '''
    return cls(
      name=data.get('name', "Weather"),
      country=data.get('sys', {}).get('country'),
      main=data.get('weather', [{}])[0].get('main'),
      icon=data.get('weather', [{}])[0].get('icon'),
      description=data.get('weather', [{}])[0].get('description'),
      temp=data.get('main', {}).get('temp'),
      feels_like=data.get('main', {}).get('feels_like'),
      speed=data.get('wind', {}).get('speed'),
      humidity=data.get('main', {}).get('humidity'),
      clouds=data.get('clouds', {}).get('all')
    )