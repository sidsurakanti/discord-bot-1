import datetime as dt
import random

import discord
from discord import Embed
from discord.ext import commands

from config import *
from .utils import reddit, gipfy


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		if ctx.guild is None:
			return False
		else:
			return True

	@commands.command()
	async def meme(self, ctx):
		"""Shows a random anime meme"""
		post_title, post_url = reddit.generate(REDDIT_ID, REDDIT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD)
		color = random.choice([0x6CA1F0, 0x2CDB92, 0x9627DB, 0xCFFF87, 0xFFC20B, 0x6BF0D9])
		embd = Embed(color=color,
		             timestamp=dt.datetime.utcnow())
		embd.set_author(name=post_title)
		embd.set_image(url=post_url)
		embd.set_footer(text="Powered by Reddit", icon_url=ctx.author.avatar_url)
		embd.description = f"Image not loading? [**Link**]({post_url})"
		await ctx.send(embed=embd)

	@commands.command()
	async def gif(self, ctx):
		"""Shows a random anime gif"""
		gif_url, bitly_url = gipfy.get_gif(GIFPY_API_KEY)
		color = random.choice([0x6CA1F0, 0x2CDB92, 0x9627DB, 0xCFFF87, 0xFFC20B, 0x6BF0D9])
		embd = Embed(color=color,
		             timestamp=dt.datetime.utcnow())
		embd.set_image(url=f"{gif_url}")
		embd.set_footer(text="Powered by Gifpy", icon_url=ctx.author.avatar_url)
		embd.description = f"Gif not loading? [**Link**]({bitly_url})"
		await ctx.send(embed=embd)

	@commands.command()
	async def say(self, ctx, channel: discord.TextChannel, *, text):
		"""Sends specified text in specified channel"""
		embd = Embed(description=f'Sent "{text}" in {channel.mention}',
		             color=ctx.author.color,
		             timestamp=dt.datetime.utcnow())
		await channel.send(text)
		await ctx.send(embed=embd)


def setup(bot):
	bot.add_cog(Fun(bot=bot))
