import itertools
from datetime import datetime as dt

import discord
from discord.ext import commands


class Help(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(verify_checks=True, **options)

    def embedify(self, title: str, description: str) -> discord.Embed:
        """Returns an embed with title <title> and description: <desc>"""
        embed = discord.Embed(title=title,
                              description=description,
                              color=discord.Color.dark_teal(),
                              timestamp=dt.utcnow())
        embed.set_author(name=self.context.bot.user, icon_url=self.context.bot.user.avatar_url)
        embed.set_footer(icon_url=self.context.author.avatar_url, text=f'Requested by: {self.context.author}')

        return embed

    def command_not_found(self, string) -> str:
        """Returns command not found string"""
        ret = "```Command or Category not {self.clean_prefix}{string} found```"
        return ret

    def subcommand_not_found(self, command, string) -> str:
        """Return subcommand not found string"""
        ret = f'```Subcommand "{self.context.prefix}{command.qualified_name}" has no subcommands```'
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return ret[:-2] + f' named {string}'

        return ret

    @staticmethod
    def no_category() -> str:
        """Returns no category string"""
        string = "Category not found"
        return string

    def get_opening_note(self) -> str:
        ret = f"""Izzy's discord bot.
                  Use prefix "**{self.clean_prefix}**"
                  Use **`{self.clean_prefix}help <command name>`** for more info on a command
                  You can also use **`{self.clean_prefix}help <category name>`** for more info on a category
               """

        return ret

    @staticmethod
    def command_or_group(*obj) -> list:
        names = []
        for command in obj:
            if isinstance(command, commands.Group):
                names.append(f"Groups: {command.name}")
            else:
                names.append(f'{command.name}')

        return names

    def full_cog_path(self, command, include_prefix: bool = False) -> str:
        """Returns cog/group path"""
        string = f"`{command.qualified_name} {command.signature}`"

        if any(command.aliases):
            string += ' | Aliases: '
            string += ', '.join(f'{alias}' for alias in command.aliases)

        if include_prefix:
            string = f"`{self.clean_prefix}`" + string

        return string

    def full_command_path(self, command, include_prefix: bool = False) -> str:
        """Returns command path"""
        string = f"{command.qualified_name} {command.signature}`"

        if any(command.aliases):
            string += ' | Aliases: '
            string += ', '.join(f'{alias}' for alias in command.aliases)

        if include_prefix:
            string = f"`{self.clean_prefix}" + string

        return string

    async def send_bot_help(self, mapping):
        """Main help command"""
        title = f"**{self.context.bot.user.name} Help**"
        desc = self.get_opening_note()
        embed = self.embedify(title=title, description=desc)

        no_category = f"\u200b{self.no_category()}"

        def get_category(command, *, no_cat=no_category):
            """Returns the category of <command>"""
            cog = command.cog
            return (no_cat if cog is None else cog.qualified_name)

        filtered = await self.filter_commands(self.context.bot.commands, sort=True, key=get_category)
        for category, cmds in itertools.groupby(filtered, key=get_category):
            if cmds:
                name = f"**{category}**"
                value = f"```fix\n{', '.join(self.command_or_group(*cmds))}```"
                embed.add_field(name=name, value=value, inline=False)

        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        """Help command for a group"""
        title = self.full_cog_path(group)
        desc = (group.short_doc) or ("```No specified command description.```")
        embed = self.embedify(title=title, description=desc)

        filtered = await self.filter_commands(group.commands, sort=True, key=lambda c: c.name)
        if filtered:
            for command in filtered:
                name = self.full_cog_path(command)
                if isinstance(command, commands.Group):
                    name = 'Group: ' + name

                value = (f"```fix\n{command.help}```") or ("*No specified command description.*")
                embed.add_field(name=name, value=value, inline=False)

        if len(embed.fields) == 0:
            embed.add_field(name='No commands', value='This group has no commands')

        await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        """Help command for a cog"""
        title = cog.qualified_name
        desc = (f"```fix\n{cog.description}```") or ("```No specified command description.```")
        embed = self.embedify(title=title, description=desc)

        filtered = await self.filter_commands(cog.get_commands())
        if filtered:
            for command in filtered:
                name = self.full_cog_path(command)
                if isinstance(command, commands.Group):
                    name = f"Group: {name}"

                value = (f"```fix\n{command.help}```") or ("```No specified command description```")
                embed.add_field(name=name, value=value, inline=False)

        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        """Help command for a command"""
        title = self.full_command_path(command, include_prefix=True)
        desc = (f"```fix\n{command.help}```") or ("```No specified command description```")
        embed = self.embedify(title=title, description=desc)

        await self.context.send(embed=embed)

    @staticmethod
    def list_to_string(lst) -> str:
        """Converts from list to string"""
        return ', '.join([obj.name if isinstance(obj, discord.Role) else str(obj).replace('_', ' ') for obj in lst])


class NewHelp(commands.Cog, name="Help Command"):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        self.bot = bot
        bot.help_command = Help()
        bot.help_command.cog = self
        bot.get_command('help').hidden = True

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot):
    bot.add_cog(NewHelp(bot))
