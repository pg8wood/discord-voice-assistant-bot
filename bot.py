from threading import Thread

from discord import ChannelType
from discord.ext import commands
from discord.voice_client import ProcessPlayer

bot = commands.Bot(command_prefix=".", description="yo yo yo\n\nHere's what I know how to do:")


async def get_online_users():
    voice_channel_dict = {}

    for member in bot.get_all_members():
        voice_channel = member.voice.voice_channel

        if voice_channel is not None:
            if voice_channel not in voice_channel_dict:
                voice_channel_dict[voice_channel] = []

            voice_channel_dict[voice_channel].append(member.name)

    return voice_channel_dict


@bot.event
async def on_ready():
    print("Success! %s is online!" % bot.user.name)


@bot.command()
async def ping():
    """Ping me and see what happens ;)"""
    await bot.say("yo yo yo")


class Music:
    player = None

    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        """<url> Play audio from YouTube"""
        author = ctx.message.author
        server = ctx.message.server
        user_channel = author.voice_channel

        if user_channel is None or user_channel.type is not ChannelType.voice:
            await bot.say("You must join a voice channel before using this command. I'm not listening to your "
                          "shitty music alone.")
            return

        voice_channel = bot.voice_client_in(server) if bot.is_voice_connected(server) else await bot.join_voice_channel(user_channel)

        if self.player is None:
            # All ytdl options are available here: https://github.com/rg3/youtube-dl/blob/master/README.md
            ytdl_options = {
                "default_search": "auto",  # Search for video title if url is invalid
                "format": "bestaudio/best",
                "quiet": True
            }

            self.player = await voice_channel.create_ytdl_player(url, ytdl_options=ytdl_options)
            self.player.volume = 0.05
            await bot.say("Now playing %s" % self.player.title)
            player_thread = Thread(target=self.player.start(), args=())
            player_thread.start()
        else:
            await bot.say("Something's already playing. Hold up. I don't know how to queue music yet.")

    @commands.command(pass_context=True)
    async def volume(self, ctx, volume):
        """<0 - 200> Sets the volume of the bot. Changes volume for ALL users, so use this command with caution."""
        try:
            volume = int(volume)
        except ValueError:
            await(bot.say("Usage: %svolume <integer in range 0 - 200>. Changes volume for ALL users, so use this "
                          "command with caution." % bot.command_prefix))

        if volume < 0:
            await(bot.say("What would negative volume even be?"))
        elif volume > 200:
            await(bot.say("IT'S TOO LOUD"))
        elif isinstance(self.player, ProcessPlayer):
            self.player.volume = volume / 100.0
            await bot.add_reaction(ctx.message, '👍')
        else:
            await(bot.say("Nothing's playing right now. 💩"))

    @commands.command(pass_context=True)
    async def stop(self):
        """STOP THE MUSIC"""
        await bot.say("Player stopped.")
        self.player.stop()


def start_bot():
    print("Connecting to Discord...")
    with open("./secret/token.txt") as token_file:
        token = token_file.readline().strip()
        bot.run(token)


bot.add_cog(Music())

# Run the bot on its own thread
thread = Thread(target=start_bot, args=())
thread.start()
