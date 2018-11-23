from threading import Thread

from discord.ext import commands

from music import Music

bot = commands.Bot(command_prefix=".", description="yo yo yo\n\nHere's what I know how to do:")
bot.add_cog(Music(bot))


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


def start_bot():
    print("Connecting to Discord...")
    with open("./secret/token.txt") as token_file:
        token = token_file.readline().strip()
        bot.run(token)


if __name__ == '__main__':
    # Run the bot on its own thread
    thread = Thread(target=start_bot, args=())
    thread.start()

