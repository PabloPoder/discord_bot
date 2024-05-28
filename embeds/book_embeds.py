'''
This module contains the functions to create the embeds for the books.
'''
import random
import discord
from discord import Embed

from utils.const import MOTIVATIONAL_QUOTES
from services.books import Book

def get_random_color() -> int:
  '''Get a random color for the embed

  return: `int`
      The random color for the embed.
  '''
  return random.randint(0, 0xFFFFFF)

def create_book_embed(book: Book) -> Embed:
  '''Create an embed with the book's information

  Parameters
  ----------
  book: :class:`Book`
      The book to create the embed from.
  return: :class:`Embed`
      The embed with the book's information.
  '''
  embed:Embed = Embed(
    color=discord.Color.blurple(),
    title=book.name,
    description=book.description[:200] + "...",
    url=book.url,
  )
  embed.set_thumbnail(book.thumbnail)
  embed.set_image(book.thumbnail)
  embed.set_author(icon_url=book.thumbnail, name=book.authors)
  embed.add_field(name="📖 Page Count:", value=book.page_count)
  embed.add_field(name="📅 Published Date:", value=book.published_date)
  embed.add_field(name="⭐ Average Rating:", value=book.average_rating)
  embed.add_field(name="🗣️ Language:", value=book.language)
  embed.add_field(name="🗃️ Categories:", value=book.categories)
  embed.add_field(name="📚 Publisher:", value=book.publisher)
  embed.set_footer(text="🧙‍♂️" + random.choice(MOTIVATIONAL_QUOTES))

  return embed

def create_base_book_embed() -> Embed:
  '''Create a base embed with the book's template

  return: :class:`Embed`
      The embed with the book's template.
  '''

  embed:Embed = Embed(
    title="Book",
    description="Select a book to view its details...",
    color=discord.Color.blurple()
  )
  embed.add_field(name="📖 Page Count:", value="0")
  embed.add_field(name="📅 Published Date:", value=" -/-/-")
  embed.add_field(name="⭐ Average Rating:", value="0")
  embed.add_field(name="🗣️ Language:", value=" - ")
  embed.add_field(name="🗃️ Categories:", value=" - ")
  embed.add_field(name="📚 Publisher:", value=" - ")

  return embed
