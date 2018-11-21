from threading import Thread

import discord
from discord import ChannelType
from discord.ext import commands

bot = commands.Bot(command_prefix=".")


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
    await bot.say("yo yo yo")


@bot.command(pass_context=True)
async def play(ctx, url):
    author = ctx.message.author
    user_channel = author.voice_channel

    if user_channel.type is not ChannelType.voice:
        await bot.say("You must join a voice channel before using this command. I'm not listening to your "
                      "shitty music alone.")
        return

    voice_channel = await bot.join_voice_channel(user_channel)
    player = await voice_channel.create_ytdl_player(url)

    await bot.say("Now playing %s" % player.title)
    player_thread = Thread(target=player.start(), args=())
    player_thread.start()


def start_bot():
    print("Connecting to Discord...")
    with open("./secret/token.txt") as token_file:
        token = token_file.readline().strip()
        bot.run(token)


# Run the bot on its own thread
thread = Thread(target=start_bot, args=())
thread.start()
