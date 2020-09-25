import discord
from discord.ext import commands

from inspect import getsource as gs


class Source(commands.Cog, name="Source"):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.guild is None:
            return False
        else:
            return True

    @staticmethod
    def to_pages(content: str, max_size: int):
        """Converts <content> to pages"""
        pages = ['']
        i = 0
        for line in content.splitlines(keepends=True):
            if len(pages[i] + line) > max_size:
                i += 1
                pages.append('')
            pages[i] += line
        return pages

    @commands.command()
    async def source(self, ctx, *, command: str = None):
        """Source code for <command>"""
        error_embd = discord.Embed(title="Please enter a command", color=discord.Color.red())
        error_embd2 = discord.Embed(title="Can't find command", color=discord.Color.red())
        if command is None:  # if user didn't enter a command
            return await ctx.send(embed=error_embd)

        cmd = self.bot.get_command(command)

        if cmd is None:  # if there is no command named <command>
            return await ctx.send(embed=error_embd2)

        try:
            source = gs(cmd.callback)
        except AttributeError:
            return await ctx.send(embed=error_embd2)

        pages = self.to_pages(source, max_size=1950)  # converts to pages
        for page in pages:
            page = page.replace("`", "`\u200b")
            await ctx.send(f'```py\n{page}```')


def setup(bot):
    bot.add_cog(Source(bot=bot))
