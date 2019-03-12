from google_sheeets_client import GoogleSheetsClient
from music import Music
from discord.ext import commands
from threading import Thread
import os
import signal

import itertools
import inspect
from discord.ext.commands import Command, Paginator

class NewHelpFormatter(commands.HelpFormatter):

	def get_max_alias_length(self):
		"""Returns the longest list of aliases possible for formatting purposes.
		
		Most of this code is lifted directly from format() in formatter.py (found in https://github.com/Rapptz/discord.py). The only reason this code has been copy-pasted is because the original method did most of what was needed already; it simply needed to be slightly tweaked for my purposes.
		"""
		max_len = 0
		
		def category(tup):
			cog = tup[1].cog_name
			# we insert the zero width space there to give it approximate
			# last place sorting position.
			return cog + ':' if cog is not None else '\u200bUncategorized:'
		
		if self.is_bot():
			data = sorted(self.filter_command_list(), key=category)
			for category, commands in itertools.groupby(data, key=category):
				# there simply is no prettier way of doing this.
				commands = list(commands)
				if len(commands) > 0:
					for name, command in commands:
						aliases = '|'.join(command.aliases)
						if len(aliases) > max_len:
							max_len = len(aliases)
		
		return(max_len)

	def _add_subcommands_to_page(self, max_width, max_alias_width, commands):
		"""An overridden function that changes up the formatting of commands that are to be added to a paginator.
		
		Most of this code is lifted directly from _add_subcommands_to_page() in formatter.py (found in https://github.com/Rapptz/discord.py). The only reason this code has been copy-pasted is because the original method did most of what was needed already; it simply needed to be slightly tweaked for my purposes.
		"""
		for name, command in commands:
			if name in command.aliases:
				# skip aliases
				continue
			
			aliases = '|'.join(command.aliases)
			
			if len(aliases) > 0:
				entry = '  {0:<{width}} [{2:<{alias_width}} {1}'.format(name, command.short_doc, aliases + "]", width = max_width, alias_width = max_alias_width + 3)
			else:
				entry = '  {0:<{width}} {2:<{alias_width}} {1}'.format(name, command.short_doc, " ", width = max_width, alias_width = max_alias_width + 4)
			
			shortened = self.shorten(entry)
			self._paginator.add_line(shortened)

	def format(self):
		"""An overridden function that adds a few little aesthetic changes to the default help command.
		
		Most of this code is lifted directly from format() in formatter.py (found in https://github.com/Rapptz/discord.py). The only reason this code has been copy-pasted is because the original method did most of what was needed already; it simply needed to be slightly tweaked for my purposes.
		"""
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
		
		key_line = '  {0:<{width}} {2:<{alias_width}} {1}'.format("Command", "Description", "Aliases", width = max_width, alias_width = max_alias_length + 4)
		self._paginator.add_line(key_line)
		bar_line = '{0:-<{key_line_len}}'.format("", key_line_len = self.width)
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



new_help_formatter = NewHelpFormatter()
new_help_formatter.width = 100

bot = commands.Bot(command_prefix=".", formatter=new_help_formatter, description="yo yo yo\n\nHere's what I can do, fam:")

# Configure cogs
sheets_client = GoogleSheetsClient()
music_client = Music(bot)
bot.add_cog(music_client)


def start_bot():
    print("Connecting to Discord...")
    with open("./secret/token.txt") as token_file:
        token = token_file.readline().strip()
        bot.run(token)


# Run the bot on its own thread
thread = Thread(target=start_bot, args=())
thread.start()


# discord.py commands and events

@bot.event
async def on_ready():
	print("Success! %s is online!" % bot.user.name)
	
	##Send a message to each server's command channel notifying users that the bot is ready to accept commands
	servers = bot.servers
	for server in servers:
		command_channel_id = str(sheets_client.get_command_channel_id(server_id=server.id))
		command_channel = server.get_channel(command_channel_id)
		
		await bot.send_message(command_channel, "Success! %s is online!" % bot.user.name)


@bot.event
async def on_message(message):
    author = message.author
    channel = message.channel
    server = channel.server
    message_string = message.content.lower()

    if author == bot.user:
        # Don't let the bot talk to itself... it might become self-aware.
        return
    elif message_string.startswith(bot.command_prefix) and not sheets_client.is_command_channel(text_channel=channel.name, server_id=server.id):
        # Force users to post bot commands in the bot channel
        command_channel_id = str(sheets_client.get_command_channel_id(server_id=server.id))
        command_channel = server.get_channel(command_channel_id)

        await bot.send_message(command_channel, author.mention + " post robot commands in this channel plz")
        await bot.delete_message(message)
        return

    custom_response = sheets_client.get_custom_response(message_string) if not message_string.startswith(bot.command_prefix) else None

    # Process custom responses
    if custom_response is not None:
        """
        Unfortunately, yt_dl doesn't provide a mechanism to discern which services are supported shy of "just trying it 
        out" and catching errors (from their docs). Instead, we'll limit which media sites are supported here to avoid 
        catching errors frequently as control flow since this is both slow and an anti-pattern.
        """
        supported_audio_sites = ("youtube", "soundcloud")
        for site in supported_audio_sites:
            if site in custom_response:  # ♫ Audio response!
                await music_client.audio_response(message, custom_response)
                return
        else:  # Textual audio response
            await bot.send_message(message.channel, custom_response)
        return

    await bot.process_commands(message)


@bot.command()
async def ping():
    """Ping me and see what happens ;)"""
    await bot.say("yo yo yo")


@bot.command(pass_context=True, aliases=["kill", "ded", "die"])
async def shutdown(ctx):
    """Kill switch. Use this if the bot gains sentience. You CANNOT restart the bot after using this command."""

    await bot.send_message(ctx.message.channel, "I'll remember this, " + ctx.message.author.mention)
    print("%s killed the bot" % ctx.message.author.name)
    exit(0)

@bot.command(pass_context=True, aliases=["toot", "doot"])
async def test(ctx):
	"""Test command"""
	await bot.send_message(ctx.message.channel, "HLERP")

@bot.command(pass_context=True, aliases=["reboot", "reload"])
async def restart(ctx):
    """Restarts the bot."""

    await bot.send_message(ctx.message.channel, "https://i.ytimg.com/vi/Zxo0V6x3GBE/maxresdefault.jpg")  # We'll be right back
    print("%s restarted the bot" % ctx.message.author.name)
    os.kill(os.getpid(), signal.SIGTERM)


# Dialogflow G Suite fulfillment functions

async def get_online_users():
    voice_channel_dict = {}

    for member in bot.get_all_members():
        voice_channel = member.voice.voice_channel

        if voice_channel is not None:
            if voice_channel not in voice_channel_dict:
                voice_channel_dict[voice_channel] = []

            voice_channel_dict[voice_channel].append(member.name)

    return voice_channel_dict
