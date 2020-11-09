import datetime as dt
import itertools

import discord
from discord import embeds
from discord.ext import commands
from discord import Embed


class Help(commands.HelpCommand):
  def __init__(self, **options):
    super().__init__(verify_checks=True, **options)
  
  def embedify(self, title: str, desc: str = None) -> Embed:
    embd = Embed(description=desc, 
                 color=0xFF9D8C,
                 timestamp=dt.datetime.utcnow())
    embd.set_author(name=title, icon_url=self.context.bot.user.avatar_url)
    embd.set_footer(text=f"Requested by {self.context.author}", icon_url=self.context.author.avatar_url)
    return embd

  @staticmethod
  def command_or_group(*obj):
    names = []

    for cmd in obj:
      try:
        names.append(f"`{cmd.name}`")
      except AttributeError:
        pass
    
    return names

  async def command_not_found(self, string):
    embd = self.embedify("Command not found", f"Couldn't find a command named `{string}`")
    await self.context.send(embed=embd)
  
  async def send_bot_help(self, mapping):
    embd = self.embedify(f"Bot Help")

    def get_category(cmd, *, no_category=f"\u200bNo Category"):
      cog = cmd.cog
      return cog.qualified_name if cog is not None else no_category

    filtered = await self.filter_commands(self.context.bot.commands, sort=True, key=get_category)

    for category, cmds in itertools.groupby(filtered, key=get_category):
      if cmds:
        embd.add_field(name=f"**{category}**",
                       value=', '.join(self.command_or_group(*cmds)),
                       inline=False)

    embd.add_field(name="\u200b", value=f"Use `{self.clean_prefix}help <command>` or `{self.clean_prefix}help <cog>` for more info on a command or cog")
    await self.context.send(embed=embd)

  async def send_cog_help(self, cog):
    embd = self.embedify(cog.qualified_name)
    filtered = await self.filter_commands(cog.get_commands())
    
    if filtered:
      for command in filtered:
        name = f"`{command.name}`"
        embd.add_field(name=name,
                       value=command.help or "**No specified command description**",
                       inline=False)
    
    embd.add_field(name="\u200b", value=f"Use `{self.clean_prefix}help <command>` for more info on a command")
    await self.context.send(embed=embd)

  async def send_command_help(self, command):
    embd = self.embedify(command.name,
                         command.help or "**No specified command description**")
                         
    if command.aliases:
      embd.add_field(name="Aliases", value=', '.join(f'`{alias}`' for alias in command.aliases))

    string =  f"`{self.clean_prefix}{command.qualified_name} {command.signature}`" if command.signature else f"`{command.qualified_name}`"
    embd.add_field(name="Usage",
                   value=string,
                   inline=False)

    try:
      await command.can_run(self.context)
    except Exception as error:
      err_embd = self.embedify("You're missing permissions to run this command")
      return await self.context.send(embed=err_embd)

    await self.context.send(embed=embd)


class HelpCommand(commands.Cog, name="Help"):
  def __init__(self, bot):
    self._old_help_command = bot.help_command
    bot.help_command = Help()
    bot.help_command.cog = self
    bot.get_command('help').hidden = True
    self.bot = bot
  
  def cog_unload(self):
    self.bot.help_command = self._old_help_command


def setup(bot):
  bot.add_cog(HelpCommand(bot))



