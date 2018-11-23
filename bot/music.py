from threading import Thread

from discord import ChannelType
from discord.ext import commands
from discord.voice_client import ProcessPlayer


class Music:
    """
    A simple music player. Supports YouTube links and search.

    Attributes:
        bot (discord.ext.commands.Bot) the bot that will play all this fancy music
    """

    def __init__(self, bot):
        self.bot = bot
        self.player = None

    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        """<url> Play audio from YouTube"""
        author = ctx.message.author
        server = ctx.message.server
        user_channel = author.voice_channel

        if user_channel is None or user_channel.type is not ChannelType.voice:
            await self.bot.say("You must join a voice channel before using this command. I'm not listening to your "
                          "shitty music alone.")
            return

        voice_channel = self.bot.voice_client_in(server) if self.bot.is_voice_connected(server) else await self.bot.join_voice_channel(user_channel)

        if self.player is None:
            # All ytdl options are available here: https://github.com/rg3/youtube-dl/blob/master/README.md
            ytdl_options = {
                "default_search": "auto",  # Search for video title if url is invalid
                "format": "bestaudio/best",
                "quiet": True
            }

            self.player = await voice_channel.create_ytdl_player(url, ytdl_options=ytdl_options)
            self.player.volume = 0.05
            await self.bot.say("Now playing %s" % self.player.title)
            player_thread = Thread(target=self.player.start(), args=())
            player_thread.start()
        else:
            await self.bot.say("Something's already playing. Hold up. I don't know how to queue music yet.")

    @commands.command(pass_context=True)
    async def volume(self, ctx, volume):
        """<0 - 200> Sets the volume of the bot. Changes volume for ALL users, so use this command with caution."""
        try:
            volume = int(volume)
        except ValueError:
            await(self.bot.say("Usage: %svolume <integer in range 0 - 200>. Changes volume for ALL users, so use this "
                          "command with caution." % self.bot.command_prefix))

        if volume < 0:
            await(self.bot.say("What would negative volume even be?"))
        elif volume > 200:
            await(self.bot.say("IT'S TOO LOUD"))
        elif isinstance(self.player, ProcessPlayer):
            self.player.volume = volume / 100.0
            await self.bot.add_reaction(ctx.message, '👍')
        else:
            await(self.bot.say("Nothing's playing right now. 💩"))

    @commands.command(pass_context=True)
    async def stop(self):
        """STOP THE MUSIC"""
        await self.bot.say("Player stopped.")
        self.player.stop()
