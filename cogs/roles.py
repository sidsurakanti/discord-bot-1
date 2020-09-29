import discord
from discord.ext import commands
from discord.utils import get


class Roles(commands.Cog, name="Roles"):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.guild is None:
            return False
        else:
            return True

    @commands.command(aliases=['cr'], hidden=True)
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, name):
        """Create a new role"""
        embd = discord.Embed(
            title=f"Created a new role called `{name}`")  # initializing embed and setting a title
        await self.bot.guild.create_role(
            name=name)  # creating a new role with name <name>
        await ctx.send(embed=embd)

    @commands.command(aliases=['dr', 'delrole'], hidden=True)
    @commands.has_permissions(manage_roles=True)
    async def deleterole(self, ctx, role: discord.Role, *, reason=None):
        """Deletes a role"""
        try:
            await role.delete(reason=reason)
            await ctx.send(embed=discord.Embed(title=f"Deleted role `{role}`",
                                               color=discord.Color.green()))
        except Exception:
            await ctx.send(embed=discord.Embed(title=f"Error deleting role `{role}`",
                                               color=discord.Color.red()))

    @commands.command(hidden=True)
    @commands.has_permissions(manage_roles=True)
    async def bind(self, ctx, name, member: discord.Member = None):
        """Add a role to a user"""
        member = member or ctx.author  # sets member to <ctx.author> if <member> is None
        role = get(ctx.guild.roles, name=name)  # gets role object from guild

        if role:  # if there's already a role called <name>
            await member.add_roles(role)  # adds <role> to <member>
            await ctx.send(embed=discord.Embed(title=f"Added `{role}` role to {member}",
                                               color=discord.Color.green()))
        else:  # if there isn't already a role called <name>
            await self.bot.guild.create_role(
                name=name)  # creates a new role with the name of <name>
            role = get(ctx.guild.roles,
                       name=name)  # gets the role object for the newly created role with the name of <name>
            await member.add_roles(role)  # adds <role> to <member>
            embd = discord.Embed(title=f"Created and added `{role}` to {member}",
                                 color=discord.Color.green())  # defining a new embed and adding a title and color
            await ctx.send(embed=embd)

    @commands.command(hidden=True)
    @commands.has_permissions(manage_roles=True)
    async def unbind(self, ctx, name, member: discord.Member = None, *, reason=None):
        """Removes a role from user"""
        member = member or ctx.author  # sets member to <ctx.author> if <member> is None
        role = get(ctx.guild.roles, name=name)  # get role object with the the name <name>
        embd = discord.Embed(title=f"Removed role `{role}` from `{member}`")
        await member.remove_roles(role,
                                  reason=reason)  # removes the role object from guild
        await ctx.send(embed=embd)


def setup(bot):
    bot.add_cog(Roles(bot=bot))
