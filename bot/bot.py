from google_sheeets_client import GoogleSheetsClient
from music import Music
from discord.ext import commands
from threading import Thread

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


@bot.event
async def on_message(message):
    author = message.author
    channel = message.channel
    server = channel.server

    if author == bot.user:
        # Don't let the bot talk to itself... it might become self-aware.
        return
    elif not sheets_client.is_command_channel(text_channel=channel.name, server_id=server.id):
        # Force users to post bot commands in the bot channel
        command_channel_id = str(sheets_client.get_command_channel_id(server_id=server.id))
        command_channel = server.get_channel(command_channel_id)

        await bot.send_message(command_channel, author.mention + " post robot commands in this channel plz")
        return

    message_string = message.content.lower()

    # Slowing down every command's processing for shitposting? You betcha.
    # If the shitposting list gets longer, we'll do this on its own thread
    if "fortnite" in message_string or "forknite" in message_string or "ree" in message_string:
        await bot.send_message(message.channel, "REEEEEEEEEEEEEEEEEEEEEEE")
    elif "nuclear" in message_string:
        await bot.send_message(message.channel, "IT'S GONNA BLOW")
    elif "penis" in message_string:
        await bot.send_message(message.channel, "You disgust me.")
    elif "country road" in message_string:
        await bot.send_message(message.channel, "WEST VIRGINIA")

    await bot.process_commands(message)


@bot.command()
async def ping():
    """Ping me and see what happens ;)"""
    await bot.say("yo yo yo")


@bot.command(pass_context=True)
async def shutdown(ctx):
    """Killswitch. Use this if the bot gains sentience."""

    await bot.send_message(ctx.message.channel, "I'll remember this, " + ctx.message.author.mention)
    print("%s killed the bot" % ctx.message.author.name)
    exit(0)


def start_bot():
    print("Connecting to Discord...")
    with open("./secret/token.txt") as token_file:
        token = token_file.readline().strip()
        bot.run(token)


# Run the bot on its own thread
thread = Thread(target=start_bot, args=())
thread.start()

sheets_client = GoogleSheetsClient()
bot.add_cog(Music(bot))
