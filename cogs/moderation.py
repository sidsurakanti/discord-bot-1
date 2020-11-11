import datetime as dt
import os

from discord import Embed
from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded, ExtensionAlreadyLoaded


class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		if ctx.guild is None:
			return False
		else:
			return True

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def reload(self, ctx):
		"""Reloads all extensions/cogs"""
		for cog in os.listdir("cogs"):
			if cog.endswith(".py"):
				try:
					self.bot.reload_extension(f"cogs.{cog[:-3]}")
				except ExtensionNotLoaded:
					self.bot.load_extension(f"cogs.{cog[:-3]}")

		embd = Embed(title="Reloaded Cogs",
		             color=0xFFC087,
		             timestamp=dt.datetime.utcnow())
		embd.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embd)

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def unload(self, ctx, name):
		"""Unloads specified extension/cog"""
		color = 0xFFC087

		for cog in os.listdir("cogs"):
			if cog.endswith(".py") and cog.startswith(name):
				try:
					self.bot.unload_extension(f"cogs.{cog[:-3]}")
					title = f"Unloaded `{name.title()}` cog"
					break
				except ExtensionNotLoaded:
					title = "Extension was already unloaded"
					break
		else:
			title = "Extension not found"
			color = 0xFF564D

		embd = Embed(title=title,
		             color=color,
		             timestamp=dt.datetime.utcnow())
		embd.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embd)

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def load(self, ctx, name):
		"""Loads specified extension/cog"""
		color = 0xFFC087

		for cog in os.listdir("cogs"):
			if cog.endswith(".py") and cog.startswith(name):
				try:
					self.bot.load_extension(f"cogs.{cog[:-3]}")
					title = f"Loaded `{name.title()}`"
					break
				except ExtensionAlreadyLoaded:
					title = f"Extension was already loaded"
					break
		else:
			title = "Extension not found"
			color = 0xFF564D

		embd = Embed(title=title,
		             color=color,
		             timestamp=dt.datetime.utcnow())
		embd.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embd)


def setup(bot):
	bot.add_cog(Moderation(bot=bot))
