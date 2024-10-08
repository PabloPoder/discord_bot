'''
This module contains the API keys for the bot. 
The keys are loaded from the .env file using the `dotenv` library.
'''
import os
from dotenv import load_dotenv


# Load the environment variables from the .env file
load_dotenv()

# Get the API keys
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')
# TODO: remove this when we finish the bot creation
TEST_SERVER_ID = [
    os.getenv('TEST_SERVER_ID_1'),
    os.getenv('TEST_SERVER_ID_2'),
    os.getenv('TEST_SERVER_ID_3')
]

# Endpoints
WEATHER_ENDPOINT = os.getenv('WEATHER_ENDPOINT')
ROCKET_LEAGUE_ENDPOINT = os.getenv('ROCKET_LEAGUE_ENDPOINT')
GOOGLE_BOOKS_ENDPOINT = os.getenv('GOOGLE_BOOKS_ENDPOINT')

# Spotify API
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
# Discord id of the user who is authorized to use the Spotify commands
YOUR_USER_ID = os.getenv('YOUR_USER_ID')
