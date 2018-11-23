from threading import Thread

import discord
from discord import ChannelType
from discord.ext import commands

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
            self.player = await voice_channel.create_ytdl_player(url)
            await bot.say("Now playing %s" % self.player.title)
            player_thread = Thread(target=self.player.start(), args=())
            player_thread.start()
        else:
            await bot.say("Something's already playing. Hold up. I don't know how to queue music yet.")

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
