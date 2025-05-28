'''
This module contains the functions to create the embeds for the the Rocket League commands.
'''
from discord import Embed
from utils.const import NOOBIES, RL_RANK_COLORS, UNRANKED_ICON
from services.rocket_league import Playlist, RocketLeaguePlayer


def create_base_rl_embed(player: RocketLeaguePlayer) -> Embed:
    ''' Create the base embed for the player's Rocket League stats

    Parameters
    ----------
    player: :class:`RocketLeaguePlayer`
        The player object with the Rocket League stats.
    return: :class:`discord.Embed`
    '''
    # Create the base embed
    embed: Embed = Embed(
        color=RL_RANK_COLORS["Un"],
        title="Select a playlist to view the stats! 🚀"
    )
    embed.set_author(icon_url=UNRANKED_ICON, name=player.name)
    embed.set_thumbnail(url=UNRANKED_ICON)
    embed.add_field(name='🎯 MMR', value=" - ")
    embed.add_field(name='🏆 Wins', value=player.wins)
    embed.add_field(name='🥅 Goals', value=player.goals)
    embed.add_field(name='🚀 Peak MMR', value=" - ")
    embed.add_field(name='🪽 Saves', value=player.saves)
    embed.add_field(name='🤝 Assists', value=player.assists)
    embed.add_field(name='🥇 Streak', value=" - ")
    embed.add_field(name='⚽ Goals Shot Ratio', value=player.goals_shot_ratio)
    embed.add_field(name='⭐ TRN Rating', value=player.trn_rating)

    embed.set_footer(
        text="Rocket League",
        icon_url="https://cdn2.steamgriddb.com/icon/d538fafd2c832e8cb5d424d68dc7f8af.png"
    )

    return embed


def create_rl_embed(playlist: Playlist, player: RocketLeaguePlayer):
    ''' Create the embed for the player's Rocket League stats

    Parameters
    ----------
    player: :class:`RocketLeaguePlayer`
        The player object with the Rocket League stats.
    return: :class:`discord.Embed`
    '''
    # Create the embed
    embed = Embed(
        color=RL_RANK_COLORS[playlist.tier[:2]],
        title=f"{playlist.tier} {playlist.division}"
    )
    embed.set_author(icon_url=playlist.tier_icon, name=player.name)
    embed.set_thumbnail(url=playlist.tier_icon)
    embed.add_field(name='🎯 MMR', value=playlist.mmr)
    embed.add_field(name='🏆 Wins', value=player.wins)
    embed.add_field(name='🥅 Goals', value=player.goals)
    embed.add_field(name='🚀 Peak MMR', value=playlist.peak_mmr)
    embed.add_field(name='🪽 Saves', value=player.saves)
    embed.add_field(name='🤝 Assists', value=player.assists)
    embed.add_field(name='🥇 Streak', value=playlist.win_streak)
    embed.add_field(name='⚽ Goals Shot Ratio', value=player.goals_shot_ratio)
    embed.add_field(name='⭐ TRN Rating', value=player.trn_rating)

    # If the player is a noobie, add a special message
    if player.name in NOOBIES and "Diamond" in playlist.tier:
        embed.add_field(name='💎 Hardstuck player alert',
                        value="This player is a noobie! 🤣")

    embed.set_footer(
        text=playlist.name,
        icon_url="https://cdn2.steamgriddb.com/icon/d538fafd2c832e8cb5d424d68dc7f8af.png"
    )

    return embed
