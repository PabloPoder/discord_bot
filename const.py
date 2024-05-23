'''
This module contains constants related to motivational quotes, Rocket League ranks, and YouTube.

Motivational quotes:
- MOTIVATIONAL_QUOTES: A list of motivational quotes.

Rocket League:
- RL_RANK_COLORS: A dictionary mapping Rocket League ranks to their corresponding colors.
- UNRANKED_ICON: A string representing the URL of the unranked icon.
- NOOBIES: A list of usernames representing new players.

YouTube:
- (No constants defined yet)
'''
# region books
MOTIVATIONAL_QUOTES = [
    "Every page is a step closer to greatness.",
    "Books are the food for the soul.",
    "Reading is traveling without moving.",
    "In every book, a fresh start awaits.",
    "Words have the power to change the world.",
    "Reading opens doors to imagination.",
    "A book is a friend that never fails you.",
    "Books are the best gift you can give yourself.",
    "Reading is the master key to knowledge.",
    "The magic of reading never ends."
]
# endregion

# region rocket league
RL_RANK_COLORS = {
  "Un": 0x000000, # unranked
  "Br": 0xAD5F20, # bronze
  "Si": 0xA7A7A7, # silver
  "Go": 0xCEAF18, # gold
  "Pl": 0x7BCCCB, # platinum
  "Di": 0x0859BC, # diamond
  "Ch": 0x7108BC, # champion
  "Gr": 0xBC0839, # grand champion
  "Su":0xBC08B7,  # supersonic legend
}

UNRANKED_ICON = "https://www.brandoncruoff.com/pictures/rocket_league/unranked_icon.png"

NOOBIES = [
  "VDeshens",
  "ZOMB_-Frank",
  "Milurk",
  "Amnessia"
]
# endregion

# region youtube
YT_DL_OPTIONS = {"format": "bestaudio/best"}
# endregion

# region spotify
SPOTIFY_LOGO = "https://cdn.iconscout.com/icon/free/png-256/spotify-11-432546.png"
SPOTIFY_SCOPE = "user-top-read user-library-read playlist-modify-public playlist-modify-private"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/"
# endregion
