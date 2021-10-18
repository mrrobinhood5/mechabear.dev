import os

# discord CONSTANTS
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_PREFIX = "."
TEST_GUILDS = [435645321029353472, 899695318772383794]

# mongo CONSTANTS
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = os.getenv("DB_URL")

# cogs
cogs = os.listdir("./cogs")
cogs.remove("__pycache__") if "__pycache__" in cogs else 0
