from datetime import datetime as dt

from discord import Embed
from discord.ext import commands
import discord

from utils import nba_scores as nba


class Nba(commands.Cog, name="Nba"):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.guild is None:
            return False
        else:
            return True

    @commands.command()
    async def scores(self, ctx, date: str):
        """Shows the scores for <data>'s NBA game"""
        # initializes embed
        embd = Embed(color=0xDDDDDD,
                     timestamp=dt.utcnow())
        try:
            # getting data
            wl, scr, lead = nba.get(date)
            teams = ' vs '.join([str(ele[0][0]) for ele in wl])
            scores = ' - '.join([str(ele[1]) for ele in wl])

            # embed's fields
            embd.add_field(name=teams, value=scores, inline=False)
            embd.add_field(name="Scores", value=" - ".join(map(str, scr)), inline=False)
            embd.add_field(name="Lead", value=' | '.join(lead))

            # sets author and footer
            embd.set_author(name=f"NBA Scores on {date}",
                            icon_url=self.bot.user.avatar_url)
            embd.set_footer(text=f"Requested by {ctx.author}",
                            icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embd)
        except Exception:
            error_embd = Embed(title="Oof, Looks like there are no games scheduled today, try again with another date!",
                               color=discord.Color.red())

            await ctx.send(embed=error_embd)

    @commands.command()
    async def standings(self, ctx):
        """Shows the current NBA Standings"""
        east, west = nba.standings()  # get standings
        east_embd = Embed(timestamp=dt.utcnow())  # initialize new embed
        west_embd = Embed(timestamp=dt.utcnow())  # initialize new embed
        bot_icon = self.bot.user.avatar_url  # bot's avatar url

        # loop thru all the conferences and add a new field with each teams scores
        for team, score in east:
            east_embd.add_field(name=team, value=score)
        for team, score in west:
            west_embd.add_field(name=team, value=score)

        # setting titles for both <east_embd> and <west_embd> embeds
        east_embd.set_author(name="Eastern Conference Standings",
                             icon_url=bot_icon)
        west_embd.set_author(name="Western Conference Standings",
                             icon_url=bot_icon)

        # setting footers for both <east_embd> and <west_embd> embeds
        for embd in [west_embd, east_embd]:
            embd.set_footer(text=f"Requested by {ctx.author}",
                            icon_url=ctx.author.avatar_url)

        await ctx.send(embed=east_embd)
        await ctx.send(embed=west_embd)


def setup(bot):
    bot.add_cog(Nba(bot=bot))
