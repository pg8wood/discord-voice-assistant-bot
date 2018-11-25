from asyncio import Queue, Event

import datetime

from discord import ChannelType
from discord.ext import commands
from discord.voice_client import ProcessPlayer

import util

class Music:
    """
    A simple music player. Supports YouTube links and search.

    Attributes:
        bot (discord.ext.commands.Bot) the bot that will play all this fancy music
    """

    def __init__(self, bot):
        self.bot = bot
        self.current_song = None
        self.advance_queue_event = Event()
        self.queue = Queue()
        self.playlist_task_loop = self.bot.loop.create_task(self.playlist_task())
        # self.playlist_task_loop = None

    # @property
    # def audio_player(self):
    #     return self.current_song.player()

    def set_next_song_ready(self):
        """
        Tells the queue the next song is ready to be played by setting the advance queue event's internal flag
        """
        self.bot.loop.call_soon_threadsafe(self.advance_queue_event.set)

    async def playlist_task(self):
        print("Started audio player task loop. Waiting on songs...")
        """
        Plays songs from the queue. Should be run as a coroutine as it is blocking
        """
        while True:
            self.advance_queue_event.clear()
            self.current_song = await self.queue.get()

            # TODO figure out why this line causes a hang
            # await self.bot.say("Now playing %s" % self.current_song.title)

            self.current_song.start()
            await self.advance_queue_event.wait()

    def is_playing(self):
        return self.current_song is not None and not self.current_song.is_done()

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

        voice_channel = self.bot.voice_client_in(server) if self.bot.is_voice_connected(
            server) else await self.bot.join_voice_channel(user_channel)

        # All ytdl options are available here: https://github.com/rg3/youtube-dl/blob/master/README.md
        ytdl_options = {
            "default_search": "auto",  # Search for video title if url is invalid
            "format": "bestaudio/best",
            "quiet": True
        }

        new_song_player = await voice_channel.create_ytdl_player(url, ytdl_options=ytdl_options,
                                                                 after=self.set_next_song_ready)
        new_song_player.volume = 0.05
        duration = util.time_string(new_song_player.duration)
        await self.bot.say("'%s' -- %s was added to the queue." % (new_song_player.title, duration))
        await self.queue.put(new_song_player)

    @commands.command(pass_context=True)
    async def skip(self, ctx):
        """
        Skips the current song
        """
        if not self.is_playing():
            await self.bot.say("Nothing's playing right now. 💩")
        else:
            await self.bot.say("Skipped '%s'" % self.current_song.title)
            self.current_song.stop()

    @commands.command(pass_context=True)
    async def volume(self, ctx, volume):
        """<0 - 200> Sets the volume of the bot. Changes volume for ALL users, so use this command with caution."""
        try:
            volume = int(volume)
        except ValueError:
            await self.bot.say("Usage: %svolume <integer in range 0 - 200>. Changes volume for ALL users, so use this "
                               "command with caution." % self.bot.command_prefix)

        if volume < 0:
            await self.bot.say("What would negative volume even be?")
        elif volume > 200:
            await self.bot.say("IT'S TOO LOUD")
        elif isinstance(self.current_song, ProcessPlayer):
            self.current_song.volume = volume / 100.0
        else:
            await self.bot.say("Nothing's playing right now. 💩")

    @commands.command(pass_context=True)
    async def stop(self):
        """STOP THE MUSIC"""
        await self.bot.say("Player stopped.")

        if not self.current_song.is_done:
            self.current_song.stop()

        try:
            self.playlist_task.cancel()
        except:
            pass  # shameless
