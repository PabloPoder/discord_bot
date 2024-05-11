from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

# Get the API keys
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')
# TODO: remove this when we finish the bot creation
TEST_SERVER_ID = [os.getenv('TEST_SERVER_ID_1'), os.getenv('TEST_SERVER_ID_2'), os.getenv('TEST_SERVER_ID_3')]

# Endpoints
WEATHER_ENDPOINT = os.getenv('WEATHER_ENDPOINT')
ROCKET_LEAGUE_ENDPOINT = os.getenv('ROCKET_LEAGUE_ENDPOINT')
GOOGLE_BOOKS_ENDPOINT = os.getenv('GOOGLE_BOOKS_ENDPOINT')