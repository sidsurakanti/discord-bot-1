import os
from datetime import datetime as dt

import discord
from discord import Spotify
from discord.ext import commands

from utils import spoti

class Commands(commands.Cog, name="Commands"):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.guild is None:
            return False
        else:
            return True

    @commands.command(hidden=True, aliases=['reload', 'reload_cogs'])
    @commands.has_permissions(administrator=True)
    async def _reload(self, ctx):
        """Reloads all cogs"""
        cogs_folder = "./cogs"

        # looping thru all the cogs in the cogs folder
        for cog in os.listdir(cogs_folder):
            if (cog.endswith(".py")):  # if cog is a python file
                try:
                    self.bot.unload_extension(f"cogs.{cog[:-3]}")  # unloading cog
                    self.bot.load_extension(f"cogs.{cog[:-3]}")  # loading cog

                except Exception as e:  # if there's an error while loading cogs
                    print(e)
                    await ctx.send(embed=discord.Embed(title="***Error while loading cogs.***",
                                                       color=discord.Color.red()))
                    break

        else:  # if all cogs were loaded successfully
            print('Reloaded cogs successfully')
            await ctx.send(embed=discord.Embed(title="***Reloaded all cogs successfully***",
                                               color=discord.Color.green()))

    @commands.command(aliases=['av', 'pfp'])
    async def avatar(self, ctx, *, member: discord.Member = None):
        """Returns the profile picture of <member>"""
        member = member or ctx.author  # sets member to <ctx.author> if <member> is None

        # initializing new embed
        embd = discord.Embed(title=member.display_name,
                             color=discord.Color.dark_magenta(),
                             timestamp=dt.utcnow())

        embd.set_image(url=member.avatar_url)  # setting image
        embd.set_footer(text=f"Requested by {member.display_name}")  # setting footer

        await ctx.send(embed=embd)

    @commands.command(aliases=['whois'])
    async def info(self, ctx, *, member: discord.Member = None):
        """Returns the discord info of <member>"""
        # defining values
        member = member or ctx.author  # sets member to <ctx.author> if <member> is None
        joined_on = member.joined_at.strftime("%a, %b, %Y  %I:%M %p")  # the time when <member> joined the server
        created_at = member.created_at.strftime("%a, %b, %Y  %I:%M %p")  # the time when <member>'s account was created
        member_roles = [role for role in member.roles if role.name != '@everyone']  # roles <member> has except @everyone role

        # Embed
        # initializing new embed
        embd = discord.Embed(color=discord.Color.dark_blue(),
                             timestamp=dt.utcnow())

        embd.set_author(name=member.display_name, icon_url=member.avatar_url)  # setting author
        embd.set_thumbnail(url=member.avatar_url)  # setting thumbnail
        embd.set_footer(text=f"Requested by {ctx.author}")  # setting footer
        embd.add_field(name="Joined on", value=joined_on)  # new field
        embd.add_field(name="Registered on", value=created_at)  # new field

        if member_roles:  # if member has roles
            embd.add_field(name=f"Roles [{len(member_roles)}]", value=" ".join([role.mention for role in member_roles]), inline=False)
        else:  # if member doesn't have any roles
            embd.add_field(name=f"Roles [0]", value="None", inline=False)

        await ctx.send(embed=embd)

    @commands.command()
    async def spotify(self, ctx, *args):
        """Returns the name and duration of the song <member> is listening to"""
        member = ctx.author  # sets member to <ctx.author> if <member> is None
        if args:
            embd = discord.Embed(title="Invalid Argument(s)",
                                 color=discord.Color.red(),
                                 timestamp=dt.utcnow())

            embd.set_footer(text=f"Requested by {member}")  # setting footer
            return await ctx.send(embed=embd)

        # looping thru all of <members> activities
        for activity in member.activities:
            if isinstance(activity, Spotify):  # if <activity> is of type Spotify
                mins, secs = divmod(activity.duration.seconds, 60)  # getting the duration of <activity> in MM:SS format
                if secs < 10:  # adds a zero before <secs> so it's fits MM:SS format
                    secs = f"0{secs}"

                # initializing new embed
                embd = discord.Embed(color=discord.Color.green(),
                                     timestamp=dt.utcnow())

                embd.set_author(name=f"{member.display_name}", icon_url=member.avatar_url)  # setting author
                embd.set_footer(text=f"Requested by {member}")
                embd.set_image(url=activity.album_cover_url)  # setting image as album cover for <activity>

                # new field
                embd.add_field(name=f"**{activity.title}**",
                               value=f"*{activity.artist}*")
                # new field
                embd.add_field(name="Song Duration",
                               value=f"{mins}:{secs}",
                               inline=False)
                # new field
                try:
                    link = spoti.get_track(activity.track_id)
                    embd.add_field(name="Song link",
                                   value=link,
                                   inline=False)
                except Exception:
                    pass

                await ctx.send(embed=embd)
                break

        else:
            # initializing new embed
            embd = discord.Embed(title=f"You are not listening to anything at the moment",  # title for the embed
                                 color=discord.Color.dark_purple(),  # color for the embed
                                 timestamp=dt.utcnow())

            await ctx.send(embed=embd)

    @commands.command(aliases=['embed'])
    async def embedify(self, ctx, title, *, desc):
        """Creates an embed with title: <title> and description: <desc>"""
        # initializing new embed
        embd = discord.Embed(title=title, description=desc,
                             color=discord.Color.blue(),
                             timestamp=dt.utcnow())
        embd.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)  # setting footer

        await ctx.message.delete()  # deleting command invocation message
        await ctx.send(embed=embd)

    @commands.command(aliases=['member_count'])
    async def members(self, ctx):
        """Returns the number of members in the guild"""
        members = [member for member in self.bot.guild.members if not member.bot]  # list of all the members in the server
        # initializing embed
        embd = discord.Embed(title=f"Members: {len(members)}",
                                   color=discord.Color.dark_magenta())
        await ctx.send(embed=embd)


def setup(bot):
    bot.add_cog(Commands(bot=bot))
