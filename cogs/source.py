import datetime as dt
from inspect import getsource as gs

from discord import Embed
from discord.ext import commands


class Source(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		if ctx.guild is None:
			return False
		else:
			return True

	@commands.command()
	async def source(self, ctx, *, name: str = None):
		error_embd = Embed(title="Command not found",
		                   color=0xE0361,
		                   timestamp=dt.datetime.utcnow())

		if name is None:
			await ctx.send(embed=error_embd)

		command = self.bot.get_command(name)

		if command is None:
			error_embd.title = f"Command `{name}` not found"
			return await ctx.send(embed=error_embd)

		try:
			source = gs(command.callback)
		except AttributeError:
			return await ctx.send(embed=error_embd)

		pages = self.to_pages(source, size=1900)

		for page in pages:
			page = page.replace("`", "`\u200b")
			await ctx.send(f"```py\n{page}```")

	@staticmethod
	def to_pages(content: str, size: int):
		pages, i = [''], 0

		for line in content.splitlines(keepends=True):
			if len(pages[i] + line) > size:
				pages.append('')
				i += 1
			pages[i] += line

		return pages


def setup(bot):
	bot.add_cog(Source(bot=bot))
