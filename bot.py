import discord 

TOKEN = ""

with open("token.txt") as token_file:
        TOKEN = token_file.readline().strip()

client = discord.Client()
print("Connecting to Discord...")

@client.event
async def on_ready():
    print('Success! %s is online!' % client.user.name)

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

client.run(TOKEN)
