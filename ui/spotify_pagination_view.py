'''
This file contains the SpotifyPaginationView class.
'''

import math
import discord

from typing import List
from discord import Embed, Interaction, Button
from discord.ui import View
from classes.spotify import Playlist, Track
from embeds.spotify_embeds import create_playlists_embed, create_tracks_embed

class SpotifyPaginationView(View):
  ''' A class used to represent the SpotifyPaginationView. 
  
  Attributes:
  -----------
  data: `List[Track]` or `List[Playlist]`
    The data to display.
  is_recommendation: `bool` or `None`
    True if the data is `recommendation`, false if the dat is `top tracks`.
    None if the data is `playlist`.
  '''
  def __init__(
    self,
    data: List[Track] | List[Playlist],
    is_recommendation: bool | None = False
  ):
    super().__init__(timeout=180)
    self.data = data
    self.sep = 5
    self.current_page = 1
    self.interaction = None
    self.is_recommendation = is_recommendation

  # region send_view_and_embed
  async def send_view_and_embed(self, interaction: Interaction):
    '''
    Save the current message to edit it later, and send the view to the interaction.

    Parameters:
    -----------
    interaction: `Interaction`
      The interaction object.
    '''
    # Send the view, save the message to edit it later
    self.interaction = await interaction.send(view=self)

    await self.update_message(self.data[:self.sep])
  # endregion

  #region update_message
  async def update_message(self, data):
    '''
    Update the message with the new data.

    Parameters:
    -----------
    data: `List[Track]` or `List[Playlist]`
      The data to update the message with.    
    '''
    # Update the buttons based on the current page
    self.update_buttons()

    embed: Embed = None

    if isinstance(data[0], Track):
      embed = create_tracks_embed(
        tracks=data,
        is_recommendation=self.is_recommendation,
        page=self.current_page
      )
    else:
      embed = create_playlists_embed(playlists=data, page=self.current_page)
    
    # Update the previous embed with the new data
    await self.interaction.edit(embed=embed, view=self)
  # endregion

  # region update_buttons
  def update_button(self, button: Button, disabled: bool, style: discord.ButtonStyle):
    '''
    Update the button with the new style and disabled status.

    Parameters:
    -----------
    button: `Button`
      The button to update.
    disabled: `bool`
      True if button is disabled.
    style: `discord.ButtonStyle`
      The style of the button.
    '''
    button.disabled = disabled # True if button is disabled
    button.style = style
  
  def update_buttons(self):
    '''Update the buttons based on the current page.'''
    is_more_data = len(self.data) <= self.sep
    is_first_page = self.current_page == 1
    is_last_page = self.current_page == math.ceil(len(self.data) / self.sep)

    self.update_button(
      self.first_page_button,
      is_first_page, # True if button is disabled
      discord.ButtonStyle.grey if is_first_page 
      else discord.ButtonStyle.green
    )
    self.update_button(
      self.prev_button,
      is_first_page,
      discord.ButtonStyle.grey if is_first_page 
      else discord.ButtonStyle.blurple
    )
    self.update_button(
      self.next_button,
      is_more_data or is_last_page,
      discord.ButtonStyle.grey if is_last_page or 
      is_more_data else discord.ButtonStyle.blurple
    )
    self.update_button(
      self.last_page_button,
      is_last_page or is_more_data,
      discord.ButtonStyle.grey if is_last_page 
      or is_more_data else discord.ButtonStyle.green
    )
  # endregion

  # region get_current_page_data
  def get_current_page_data(self):
    '''
    Get the current page data.

    Returns:
    --------
    `List[Track]` or `List[Playlist]`
      The current page data.
    '''
    # Get the first and last item based on the current page
    last_item = self.current_page * self.sep
    first_item = last_item - self.sep

    # If the current page is the last page, set the first and last item
    if self.current_page == math.ceil(len(self.data) / self.sep):
      first_item = self.current_page * self.sep - self.sep
      last_item = len(self.data)
    
    return self.data[first_item:last_item]
  # endregion

  # region buttons
  @discord.ui.button(label="🤛🏻", style=discord.ButtonStyle.green)
  async def first_page_button(
    self,
    button: discord.ui.Button,
    interaction:discord.Interaction
  ):
    await interaction.response.defer()
    self.current_page = 1
    await self.update_message(self.get_current_page_data())

  @discord.ui.button(label="👈🏻", style=discord.ButtonStyle.blurple)
  async def prev_button(
    self,
    button: Button,
    interaction: Interaction
  ):
    await interaction.response.defer()
    self.current_page -= 1
    await self.update_message(self.get_current_page_data())

  @discord.ui.button(label="👉🏻", style=discord.ButtonStyle.blurple)
  async def next_button(
    self,
    button: Button,
    interaction: Interaction
  ):
    await interaction.response.defer()
    self.current_page += 1
    await self.update_message(self.get_current_page_data())

  @discord.ui.button(label="🤜🏻", style=discord.ButtonStyle.green)
  async def last_page_button(
    self, 
    button: discord.ui.Button,
    interaction:discord.Interaction
  ):
    await interaction.response.defer()
    self.current_page = math.ceil(len(self.data) / self.sep)
    await self.update_message(self.get_current_page_data())
  # endregion
