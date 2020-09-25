import asyncio
import os

import discord
import jishaku
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingPermissions, MissingRole, MissingRequiredArgument, BadArgument
from discord import Embed

from config import *


class Izzy(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=kwargs.pop('command_prefix', ('.')),
                         case_insensitive=True, **kwargs)

    # when the bot is logged in
    async def on_ready(self):
        """When bot is ready/logged on"""
        await self.wait_until_ready()

        self.guild = self.get_guild(756911551528829078)
        self.welcomes = self.guild.get_channel(758812190354178088)

        # changes status of the bot
        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Activity(type=discord.ActivityType.playing, name='Use prefix "."'))

        # loads cogs/extensions
        for cog in os.listdir('cogs'):
            if cog.endswith('.py'):
                self.load_extension(f"cogs.{cog[:-3]}")

        self.load_extension("jishaku")  # loads the jsk cog

        print(f"{self.user.name} is ready!")

    # every time a message is sent in a guild
    async def on_message(self, message):
        if message.author.bot:  # if <message> was from a bot
            return

        await self.process_commands(message)

    async def process_commands(self, message):
        if message.author.bot:
            return

        ctx = await self.get_context(message=message)

        await self.invoke(ctx)

    # If there's a error while trying to run a command
    async def on_command_error(self, ctx, error):
        """Command errors"""
        if isinstance(error, CommandNotFound):  # if someone invokes a command that isn't there
            return await ctx.send(embed=Embed(title="Command Not Found",
                                              color=discord.Color.red()))

        elif isinstance(error, MissingPermissions):  # if someone invokes a command that needs perms that the person doesn't have
            return await ctx.send(embed=Embed(title="Missing perms",
                                              color=discord.Color.red()))

        elif isinstance(error, MissingRole):  # if someone invokes a command that needs a specific role that the person doesn't have
            return await ctx.send(embed=Embed(title="Missing role",
                                              color=discord.Color.red()))

        elif isinstance(error, MissingRequiredArgument):  # if someone invokes a command without the required arguments
            return await ctx.send(embed=Embed(title="Missing required parameter",
                                              color=discord.Color.red()))

        elif isinstance(error, BadArgument):  # if someone invokes a command with a bad argument
            return await ctx.send(embed=Embed(title="Argument is invalid, please try again",
                                              color=discord.Color.red()))

        else:
            raise error

    @classmethod
    async def setup(cls):
        bot = cls()
        try:  # runs the bot with <TOKEN>
            await bot.start(TOKEN)
        except KeyboardInterrupt:
            await bot.close()


# Starting the bot
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Izzy.setup())
