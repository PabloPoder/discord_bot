
from typing import List

import discord
from services.books import Book

from discord.ui import Select
from discord import Button, ButtonStyle, Interaction, SelectOption 

from embeds.book_embeds import create_book_embed

class BooksDropdown(Select):
  def __init__(self, books: List[Book] = None):
    self.books = books
    options = [SelectOption(label=book.name, value=book.id) for book in self.books]

    super().__init__(options=options, placeholder="Select a book to view its details...")

  async def callback(self, interaction: Interaction):
    # Get the selected book
    book = next((book for book in self.books if book.id == interaction.data["values"][0]), None)

    # if the selected book is not found in the list then return 
    if not book:
      await interaction.followup.send("Book not found!")
      return

    # Create an embed with the book's information
    embed = create_book_embed(book=book)

    # Create save button and add it to the view
    self._add_save_button_to_view(embed)

    # Edit the original message with the embed containing the book's information
    await interaction.response.edit_message(embed=embed, view=self.view)


  def _add_save_button_to_view(self, embed):
      # Create save button
      saveButton = discord.ui.Button(
        label="Save book", emoji="💾", style=ButtonStyle.green,
      )

      async def button_callback(interaction: Interaction):
        # send dm with the name of the book
        await interaction.user.send(embed=embed)

      saveButton.callback = button_callback

      # Remove all buttons from the view
      self._remove_all_buttons_from_view()

      self.view.add_item(saveButton)

  def _remove_all_buttons_from_view(self):
      for item in self.view.children:
        if isinstance(item, discord.ui.Button):
          self.view.remove_item(item)