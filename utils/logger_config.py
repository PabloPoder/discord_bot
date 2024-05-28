'''
This file contains the settings for the logging. It creates a logger for each level.
'''
import logging

# Create a logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)  # Set the lowest level to register all

handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8',
    mode='w'
)

handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
)

logger.addHandler(handler)
