from bot import *
from config import TOKEN, GUILD_ID

# Declare intents
intents = discord.Intents.all()

# Instance of your Discord bot in your server
bot = DuckShotBot("!", intents, GUILD_ID)

# Run the bot
bot.run(TOKEN)
