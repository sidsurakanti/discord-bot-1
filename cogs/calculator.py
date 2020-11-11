import datetime as dt
import random

import discord
from discord import Embed
from discord.ext import commands

from .utils.calc import main as cl


class Calculator(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		if ctx.guild is None:
			return False
		else:
			return True

	@commands.command()
	async def calc(self, ctx, *, expr):
		"""Calculates things"""
		result = cl.calc(expr)
		embd = Embed(color=discord.Color.dark_blue(),
		             timestamp=dt.datetime.utcnow())
		embd.set_author(name="Result")
		embd.set_footer(text=f"Requested by {ctx.author}")
		embd.title = f"`{result}`"
		await ctx.send(embed=embd)


def setup(bot):
	bot.add_cog(Calculator(bot=bot))
