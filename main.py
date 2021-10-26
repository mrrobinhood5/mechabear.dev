import disnake
import logging
from disnake.ext import commands
import motor.motor_asyncio
from config import *


# discord intents
intents = disnake.Intents(
    guilds=True, members=True, messages=True, reactions=True,
    bans=False, emojis=False, integrations=False, webhooks=True, invites=False, voice_states=False, presences=False,
    typing=False
)

# instance of the client
# client = disnake.Client()

# instance of the bot
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, test_guilds=TEST_GUILDS)

# instance of the database
db = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_URL}")
bot.__setattr__("db", db.Mecha)

# logger setup
logger = logging.getLogger('disnake')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='disnake.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# bot output
@bot.event
async def on_ready():
    print(f'I\'m in as {bot.user} with a "{bot.command_prefix}" prefix')

# TODO: add an after loop event to load all the quests names and put them as an attribute on the bot.

# loads the cogs
for cog in cogs:
    bot.load_extension(f'cogs.{cog[:-3]}')
    # bot.load_extension(cog)

# runs the client
# client.run(BOT_TOKEN)
bot.run(BOT_TOKEN)
