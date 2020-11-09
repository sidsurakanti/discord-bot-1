import os
import asyncio
import datetime as dt

import discord
from discord.ext import commands
from discord import Embed
from discord.ext.commands import MemberNotFound

from config import *


intents = discord.Intents.default()
intents.members = True


class Cloud(commands.Bot):
	def __init__(self, **kwargs): 
		super().__init__(command_prefix=kwargs.pop("command_prefix", ("-")),
										 case_insensitive=True, intents=intents, **kwargs)

	async def on_ready(self):
		"""after bot is logged on"""
		await self.wait_until_ready()
		await self.change_presence(status=discord.Status.idle,
                               activity=discord.Activity(type=discord.ActivityType.playing, name=f'{self.command_prefix}help'))

		# loads cogs
		for cog in os.listdir("cogs"):
			if cog.endswith(".py"):
				self.load_extension(f"cogs.{cog[:-3]}")

		self.load_extension("jishaku") 
		print(f"{self.user.name} is ready!")

	async def on_message(self, message):
		if message.author.bot: 
			return

		command_prefix = f"`{self.command_prefix}`"
		if isinstance(self.command_prefix, tuple):
			command_prefix = ", ".join([f"`{i}`" for i in self.command_prefix])

		if f"<@!{self.user.id}>" == message.content:
			embd = Embed(color=0xFF9D8C,
									 timestamp=dt.datetime.utcnow())
			embd.add_field(name="Name", value=f"{self.user.name} (`{self.user}`)", inline=False)
			embd.add_field(name="Details", value=f'Prefix(s): {command_prefix}\nAuthor: `izzy#2859`')
			embd.add_field(name="\u200b",
										 value=f"[**Invite Link**]({discord.utils.oauth_url(self.user.id, permissions=discord.Permissions(administrator=True))})",
										 inline=False)
			embd.set_thumbnail(url=self.user.avatar_url)
			await message.channel.send(embed=embd)

		await self.process_commands(message)

	async def process_commands(self, message):
		if message.author.bot:
			return

		ctx = await self.get_context(message=message)
		await self.invoke(ctx)

	async def on_command_error(self, ctx, exception):
		await self.wait_until_ready()

		error = getattr(exception, 'original', exception)
		embd = Embed(title="Error",
								 color=0xDB594E,
								 timestamp=dt.datetime.utcnow())

		if isinstance(error, MemberNotFound):
			embd.description = "Member not found"
			embd.set_footer(icon_url=self.user.avatar_url)
			await ctx.send(embed=embd)

		print(exception)

	@classmethod 
	async def setup(cls): 
		bot = cls()
		try: 
			await bot.start(BOT_TOKEN)
		except KeyboardInterrupt:
			await bot.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Cloud.setup())
