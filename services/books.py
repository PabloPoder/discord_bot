'''
This file contains the functions to get the books from the Google Books API.
'''
from typing import List
import logging
import aiohttp
from utils.logger_config import logger
from utils.apikeys import GOOGLE_BOOKS_ENDPOINT

from classes.Book import Book

# region get_books - get books from google books api
async def fetch_books(query:str):
  '''
  Asynchronously fetch the books from the Google Books API from a query string.
  This is an asynchronous function and should be called with 'await'.

  Parameters
  ----------
  query: `str`
      The query string to search for the books.
  
  return: `dict` or `None`
  '''
  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(GOOGLE_BOOKS_ENDPOINT+query) as response:
        response.raise_for_status()
        return await response.json()
  except aiohttp.ClientError as err:
    # logger.exception("An error occurred while fetching the book data:")
    logger.error(f"Book: {query}, Error: {err}")
    return None

# TODO: Check return with q: "el imperio final"
async def get_books(query: str):
  '''Asynchronously get the books from the Google Books API from a query string
  This is an asynchronous function and should be called with 'await'.

  Parameters
  ----------
  query: `str`
      The query string to search for the books.
  
  return: `List[Book]` or `None`
  '''
  # Log the query
  logger.info("Get books from Google Books API with query: %s", query)

  # Get the books from the Google Books API
  data = await fetch_books(query)

  if data is None:
    return None

  # Get the first 5 books from the data, checking for KeyError
  raw_books = data.get("items", [])[:5]

  # Create a list of books
  books:List[Book] = []

  # Loop through the raw_books and create a Book object
  for item in raw_books:
    volume_info = item.get("volumeInfo", {})

    if not volume_info:
      logging.error("No volumeInfo in item %s", item)
      continue

    temp_book = Book.from_dict(item, volume_info)
    books.append(temp_book)

  logger.info("Books found: %s", books)
  return books
# endregion
