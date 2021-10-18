import disnake
from config import *

# instance of the client
client = disnake.Client()


# basic test commands
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


# runs the client
client.run(BOT_TOKEN)
