from threading import Thread
import discord

client = discord.Client()


async def get_online_users():
    voice_channel_dict = {}

    for member in client.get_all_members():
        voice_channel = member.voice.voice_channel

        if voice_channel is not None:
            if voice_channel not in voice_channel_dict:
                voice_channel_dict[voice_channel] = []

            voice_channel_dict[voice_channel].append(member.name)

    return voice_channel_dict


@client.event
async def on_ready():
    print("Success! %s is online!" % client.user.name)


@client.event
async def on_message(message):
    # Don't let the bot talk to itself... it might become self-aware.
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
        token = token_file.readline().strip()
        client.run(token)


# Run the bot on its own thread 
thread = Thread(target=start_bot, args=())
thread.start()
