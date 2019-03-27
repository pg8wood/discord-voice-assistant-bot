import itertools
import inspect
from discord.ext import commands
from discord.ext.commands import Command, Paginator


class NewHelpFormatter(commands.HelpFormatter):
    """
    Much of the code in the following functions has been taken from https://github.com/Rapptz/discord.py and modified to suit the purposes of this bot.
    """

    def get_max_alias_length(self):
        """Returns the longest list of aliases possible for formatting purposes."""
        max_len = 0

        def category(tup):
            cog = tup[1].cog_name
            # we insert the zero width space there to give it approximate
            # last place sorting position.
            return cog + ':' if cog is not None else '\u200bUncategorized:'

        if self.is_bot():
            data = sorted(self.filter_command_list(), key=category)
            for category, commands in itertools.groupby(data, key=category):
                commands = list(commands)
                if len(commands) > 0:
                    for name, command in commands:
                        aliases = '|'.join(command.aliases)
                        if len(aliases) > max_len:
                            max_len = len(aliases)

        return (max_len)

    def _add_subcommands_to_page(self, max_width, max_alias_width, commands):
        """An overridden function that changes up the formatting of commands that are to be added to a paginator."""
        for name, command in commands:
            if name in command.aliases:
                # skip aliases
                continue

            aliases = '|'.join(command.aliases)

            if len(aliases) > 0:
                entry = '  {0:<{width}} [{2:<{alias_width}} {1}'.format(name, command.short_doc, aliases + "]",
                                                                        width=max_width,
                                                                        alias_width=max_alias_width + 3)
            else:
                entry = '  {0:<{width}} {2:<{alias_width}} {1}'.format(name, command.short_doc, " ", width=max_width,
                                                                       alias_width=max_alias_width + 4)

            shortened = self.shorten(entry)
            self._paginator.add_line(shortened)

    def format(self):
        """An overridden function that adds a few little aesthetic changes to the default help commands"""
        self._paginator = Paginator()

        description = self.command.description if not self.is_cog() else inspect.getdoc(self.command)

        if description:
            # <description> portion
            self._paginator.add_line(description, empty=True)

        if isinstance(self.command, Command):
            # <signature portion>
            signature = self.get_command_signature()
            self._paginator.add_line(signature, empty=True)

            # <long doc> section
            if self.command.help:
                self._paginator.add_line(self.command.help, empty=True)

            # end it here if it's just a regular command
            if not self.has_subcommands():
                self._paginator.close_page()
                return self._paginator.pages

        max_width = self.max_name_size

        def category(tup):
            cog = tup[1].cog_name
            # we insert the zero width space there to give it approximate
            # last place sorting position.
            return cog + ':' if cog is not None else '\u200bUncategorized:'

        max_alias_length = self.get_max_alias_length()

        key_line = '  {0:<{width}} {2:<{alias_width}} {1}'.format("Command", "Description", "Aliases", width=max_width,
                                                                  alias_width=max_alias_length + 4)
        self._paginator.add_line(key_line)
        bar_line = '{0:-<{key_line_len}}'.format("", key_line_len=self.width)
        self._paginator.add_line(bar_line)

        if self.is_bot():
            data = sorted(self.filter_command_list(), key=category)
            for category, commands in itertools.groupby(data, key=category):
                # there simply is no prettier way of doing this.
                commands = list(commands)
                if len(commands) > 0:
                    self._paginator.add_line(category)

                self._add_subcommands_to_page(max_width, max_alias_length, commands)
        else:
            self._paginator.add_line('Commands:')
            self._add_subcommands_to_page(max_width, self.filter_command_list())

            # add the ending note
        self._paginator.add_line()
        ending_note = self.get_ending_note()
        self._paginator.add_line(ending_note)
        return self._paginator.pages