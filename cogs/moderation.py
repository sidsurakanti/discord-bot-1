import discord
from discord.ext import commands
from discord.utils import get
from discord import Embed
from discord import Permissions


class Moderation(commands.Cog, name="Moderation"):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.guild is None:
            return False
        else:
            return True

    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, num: int = 5):
        """Purge's last <num> messages"""
        num = 100 if num > 100 else num  # sets <num> to 100 if <num> is greater than 100
        await ctx.message.delete()  # deletes command invocation message
        await ctx.channel.purge(limit=num)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason: str = None):
        """Mutes <member>"""
        role = get(ctx.guild.roles, name="Muted")  # gets role called 'Muted' in guild
        embd = Embed(title=f":white_check_mark:  **Muted {member}**", color=discord.Color.green())  # initializes new embed and sets title

        if role is None:  # creates a new role called 'Muted' and sets <role> to the new role if there isn't already a role called 'Muted'
            role = await ctx.guild.create_role(name="Muted", permissions=Permissions.general())

        # loops thru all the channels in the guild and sets send_message permission for <role> to False
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False, read_messages=True, read_message_history=True)

        await ctx.message.delete()  # deletes the command invocation message
        await member.add_roles(role, reason=reason)  # adds <role> to <member>
        await ctx.send(embed=embd)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        """Unmutes <member> """
        role = get(member.guild.roles, name='Muted')  # gets the role object for the role with the name of 'Muted'
        await member.remove_roles(role, reason=reason)  # removes the 'Muted' role from user
        embd = Embed(title=f":white_check_mark:  Unmuted {member} ",
                     color=discord.Color.green())  # initializes new embed and sets title
        await ctx.message.delete()  # deletes command invocation message
        await ctx.send(embed=embd)

    @commands.command(hidden=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Moderation(bot=bot))
