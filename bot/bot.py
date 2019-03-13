from google_sheeets_client import GoogleSheetsClient
from google_vision_client import GoogleVisionClient
from music import Music
from discord.ext import commands
from threading import Thread
import os
import signal
import sys
import requests
# TODO make separate image downloader

bot = commands.Bot(command_prefix=".", description="yo yo yo\n\nHere's what I know how to do:")

vision_client = None

# TODO: Make Google Sheets optional by using command-line argument
if "vision" in sys.argv:
    print("Connecting to Google Vision...")
    vision_client = GoogleVisionClient()

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


async def process_attachments(channel, attachments):
    print("process attachments")
    if attachments is None or vision_client is None or len(attachments) < 1:
        return

    print("looking at attachments")

    image_url = attachments[0]["url"]
    print("url: '%s'" % image_url)

    #TODO try just using the url
    f = open('discord-recent-attachment.jpg', 'wb')
    f.write(requests.get(image_url).content)
    f.close()

    is_bad = vision_client.detect_safe_search('./discord-recent-attachment.jpg')
    print(is_bad)

    if is_bad:
        await bot.send_message(channel, "Unsafe image detected!")
        return

@bot.event
async def on_message(message):
    author = message.author
    channel = message.channel
    server = channel.server
    message_string = message.content.lower()


    # TODO: DON'T BLOCK ON THIS! IT'LL MAKE THE WHOLE BOT SLOW!
    attachments_response = await process_attachments(channel, message.attachments)
    if attachments_response is not None:
        # await bot.send_message(channel, attachments_response)
        return

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
