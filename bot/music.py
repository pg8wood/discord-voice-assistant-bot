from asyncio import Queue, Event

import discord
from discord import ChannelType
from discord.ext import commands
from discord.voice_client import ProcessPlayer

import util
import validators


class Music:
    """
    A simple music player. Supports audio links like YouTube and SoundCloud.
    Supports a single Discord guild at a time.

    Attributes:
        bot (discord.ext.commands.Bot) the bot that will play all this fancy music
    """

    def __init__(self, bot):
        self.bot = bot
        self.voice_channel = self.bot.voice_clients[0] if len(self.bot.voice_clients) > 0 else None
        self.current_song = None
        self.advance_queue_event = Event()
        self.queue = Queue()
        self.playlist_task_loop = self.bot.loop.create_task(self.playlist_task())

    def set_next_song_ready(self):
        """
        Tells the queue the next song is ready to be played by setting the advance queue event's internal flag
        """
        self.bot.loop.call_soon_threadsafe(self.advance_queue_event.set)

    async def playlist_task(self):
        """
        Plays songs from the queue. Should be run as a coroutine as it is blocking
        """
        print("Started audio player task loop. Waiting on songs...")
        while True:
            self.advance_queue_event.clear()

            if self.queue.qsize() == 0 and self.voice_channel is not None:
                await self.bot.change_presence(game=None)
                await self.voice_channel.disconnect()

            self.current_song = await self.queue.get()

            # TODO figure out why this line causes a hang
            # await self.bot.say("Now playing %s" % self.current_song.title)

            self.current_song.start()
            await self.bot.change_presence(game=discord.Game(name=self.current_song.title))
            await self.advance_queue_event.wait()

    def is_playing(self):
        return self.current_song is not None and not self.current_song.is_done()

    @commands.command(pass_context=True)
    async def play(self, ctx, url=""):
        """
        Play audio from YouTube

        usage:
        .play <url> play url from YouTube
        .play resume the current music player, if one exists
        """
        await self.queue_track(ctx.message, url)

    async def audio_response(self, message, url):
        """
        Plays an audio track as an audio response to a message if no tracks are playing
        """
        if not (self.is_playing() and self.queue.qsize() == 0):
            await self.queue_track(message, url, False)

    async def queue_track(self, message, url, announce=True):
        """ 
        Helper function to allow play functionality to be invoked internally
        """
        author = message.author
        server = message.server
        user_channel = author.voice_channel

        if user_channel is None or user_channel.type is not ChannelType.voice:
            await self.bot.say("You must join a voice channel before using this command. I'm not listening to your "
                               "shitty music alone.")
            return

        if url == "":
            await self.resume.invoke(ctx)
            return
        elif not validators.url(url):
            await self.bot.send_message(message.channel, "That doesn't look like a valid url...")
            return

        self.voice_channel = self.bot.voice_client_in(server) if self.bot.is_voice_connected(
            server) else await self.bot.join_voice_channel(user_channel)

        # All ytdl options are available here: https://github.com/rg3/youtube-dl/blob/master/README.md
        ytdl_options = {
            "default_search": "auto",  # Search for video title if url is invalid
            "format": "bestaudio/best",
            "quiet": True
        }

        new_song_player = await self.voice_channel.create_ytdl_player(url, ytdl_options=ytdl_options,
                                                                      after=self.set_next_song_ready)
        new_song_player.volume = 0.50
        duration = util.time_string(new_song_player.duration)
        await self.queue.put(new_song_player)

        if announce:
            await self.bot.send_message(message.channel,
                                        "'%s' -- %s was added to the queue." % (new_song_player.title, duration))

    @commands.command(pass_context=True, aliases=["playing", "nowplaying"])
    async def np(self, ctx):
        """Gets the currently-playing song"""
        now_playing_message = "Nothing is playing." if self.current_song is None else self.current_song.title
        await self.bot.say(now_playing_message)

    @commands.command(pass_context=True)
    async def skip(self, ctx):
        """
        Skips the current song
        """
        if not self.is_playing():
            await self.bot.say("Nothing's playing right now. ¯\_(ツ)_/¯")
        else:
            await self.bot.say("Skipped '%s'" % self.current_song.title)
            self.current_song.stop()

            # Skipped the last song in the queue
            if self.queue.qsize() == 0:
                self.current_song = None
                await self.bot.change_presence(game=None)

    @commands.command(pass_context=True, aliases=["vol"])
    async def volume(self, ctx, volume):
        """<0 - 200> Sets the volume of the bot. Changes volume for EVERYONE."""
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
            await self.bot.say("Nothing's playing right now. ¯\_(ツ)_/¯")

    @commands.command(pass_context=True)
    async def pause(self):
        """Pause the current track"""
        if self.is_playing():
            self.current_song.pause()
            await self.bot.change_presence(game=discord.Game(name="Paused - " + self.current_song.title))
        else:
            await self.bot.say("Nothing's playing right now. ¯\_(ツ)_/¯")

    @commands.command(pass_context=True)
    async def resume(self):
        """Resume the current track"""
        if self.is_playing():
            self.current_song.resume()
            await self.bot.change_presence(game=discord.Game(name=self.current_song.title))
        else:
            await self.bot.say("There's nothing to resume ¯\_(ツ)_/¯")

    @commands.command(pass_context=True)
    async def stop(self):
        """STOP THE MUSIC"""
        try:
            self.current_song.stop()
            self.current_song = None
            await self.bot.say("Player stopped and queue emptied.")
            await self.bot.change_presence(game=None)
        except:
            await self.bot.say("I CAN'T STOP IT")
