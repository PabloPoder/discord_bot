'''
This file contains the SpotifyPaginationView class.
'''

import discord

from typing import List
from discord import Interaction, Button
from discord.ui import View
from classes.spotify import Track
from embeds.spotify_embeds import create_tracks_embed

class SpotifyPaginationView(View):
  ''' A class used to represent the SpotifyPaginationView. '''
  def __init__(self, data: List[Track]):
    super().__init__()
    self.data = data
    self.sep = 5
    self.current_page = 1

    # Add buttons
    self.add_item(
      Button(style=discord.ButtonStyle.blurple ,label="Previous", custom_id="previous")
    )
    self.add_item(
      Button(style=discord.ButtonStyle.blurple, label="Next", custom_id="next")
    )

  async def send_view_and_embed(self, interaction: Interaction):
    # send the view, save the message to edit it later
    self.message = await interaction.response.send_message(view=self)
    
    # update the message with the first page data
    await self.update_message(self.data[:self.sep])

  async def update_message(self, data):
    embed = create_tracks_embed(data, is_recommendation=True)
    # update the message with the new data
    await self.message.edit(embed=embed, view=self)

  @discord.ui.button(label="Previous", custom_id="previous")
  async def previous_button(self, button: Button, interaction: Interaction):
    if self.current_page > 1:
      self.current_page -= 1
      start = (self.current_page - 1) * self.sep
      end = start + self.sep
      await self.update_message(self.data[start:end])

  @discord.ui.button(label="Next", custom_id="next")
  async def next_button(self, button: Button, interaction: Interaction):
    if self.current_page * self.sep < len(self.data):
      self.current_page += 1
      start = (self.current_page - 1) * self.sep
      end = start + self.sep
      await self.update_message(self.data[start:end])

  # TODO: Test