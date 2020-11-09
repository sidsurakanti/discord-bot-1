import datetime as dt

import discord
from discord.ext import commands
from discord import Embed


class Commands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	def cog_check(self, ctx):
		if ctx.guild is None:
			return False
		else:
			return True
	
	@commands.command()
	async def ping(self, ctx):
		"""Shows the latency of the bot"""
		embd = Embed(title=f"Pong! {round(self.bot.latency * 1000)}ms",
					 			 color=0xFF96BD,
					 			 timestamp=dt.datetime.utcnow())
		embd.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embd)

	@commands.command(aliases=["av"])
	async def avatar(self, ctx, member: discord.Member = None):
		"""Shows a bigger picture of your or the specified user's avatar"""
		user = member or ctx.author
		embd = Embed(color=0x8CC6FF,
								 timestamp=dt.datetime.utcnow())
		embd.set_image(url=user.avatar_url)
		embd.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embd)
	
	@commands.command()
	async def info(self, ctx, member: discord.Member = None):
		"""Shows info about you or the given user"""
		user = member or ctx.author
		roles = user.roles
		joined_at, created_at = user.joined_at, user.created_at
		embd = Embed(color=user.color,
								 timestamp=dt.datetime.utcnow())
		embd.add_field(name="Joined At", value=joined_at.strftime('%a, %b %d, %Y at %I:%M %p %z'))
		embd.add_field(name="Registered At", value=created_at.strftime('%a, %b %d, %Y at %I:%M %p %z'))
		embd.add_field(name="Roles", value=f"{' '.join([role.mention for role in roles if role.name != '@everyone'])}", inline=False)
		embd.set_thumbnail(url=user.avatar_url)
		embd.set_author(name=user, icon_url=user.avatar_url)
		await ctx.send(embed=embd)

	@commands.command()
	async def members(self, ctx):
		"""Shows the number of members in the server"""
		count = len([member for member in self.bot.get_all_members() if not member.bot])
		embd = Embed(title=f"Members: {count}",
								 timestamp=dt.datetime.utcnow(),
								 color=0xABEB96)
		embd.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embd)

	@commands.command()
	async def invite(self, ctx):
		"""Gives you the invite link for the bot"""
		link = discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions(administrator=True))
		embd = Embed(description=f"[**Invite Link**]({link})", 
								 color=0x78C7DB)
		await ctx.send(embed=embd)


def setup(bot):
    bot.add_cog(Commands(bot=bot))
