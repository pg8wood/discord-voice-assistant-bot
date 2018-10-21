import discord 

TOKEN = ""

with open("token.txt") as token_file:
        TOKEN = token_file.readline().strip()

client = discord.Client()
print("Connecting to Discord...")


def process_online_users():
    users_in_voice_count = 0
    for member in client.get_all_members():
        member_voice_channel = member.voice.voice_channel

        if member_voice_channel is not None:
            print("%s is in %s" % (member.name, member.voice.voice_channel))
            users_in_voice_count += 1

    if users_in_voice_count == 0:
        print("Looks like all the voice channels are empty.")


@client.event
async def on_ready():
    print("Success! %s is online!" % client.user.name)
    process_online_users()


@client.event
async def on_message(message):
    # Talking to yourself may be good for you, but not if you're a bot.
    if message.author == client.user:
        return

    if message.content.startswith("!online"):
       process_online_users()

    elif message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

client.run(TOKEN)
