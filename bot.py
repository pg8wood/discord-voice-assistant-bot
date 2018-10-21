from threading import Thread
import discord

client = discord.Client()


async def get_online_users():
    users_in_voice_channels = []

    for member in client.get_all_members():
        member_voice_channel = member.voice.voice_channel

        if member_voice_channel is not None:
            users_in_voice_channels.append("%s is in %s" % (member.name, member.voice.voice_channel))

    return users_in_voice_channels


@client.event
async def on_ready():
    print("Success! %s is online!" % client.user.name)
    users = await get_online_users()
    print(users)


@client.event
async def on_message(message):
    # Talking to yourself may be good for you, but not if you're a bot.
    if message.author == client.user:
        return

    if message.content.startswith("!online"):
        users = await get_online_users()
        await client.send_message(message.channel, users)

    elif message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)


def start_bot():
    print("Connecting to Discord...")
    with open("./secret/token.txt") as token_file:
        TOKEN = token_file.readline().strip()
        client.run(TOKEN)


thread = Thread(target=start_bot, args=())
thread.start()
