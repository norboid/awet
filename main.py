import discord
from discord.ext import commands
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Ensure the bot has the necessary intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logging.info(f"✅ Logged in as {bot.user}")
    try:
        # Sync slash commands with Discord
        await bot.tree.sync()
        logging.info("Slash commands synced successfully")
    except Exception as e:
        logging.error(f"Error syncing slash commands: {e}")

# Error handling for commands
@bot.event
async def on_command_error(ctx, error):
    logging.error(f"Error: {error}")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I don't recognize that command.")
    else:
        await ctx.send("An error occurred. Please try again later.")

# Load cogs dynamically from the 'cogs' folder
cog_files = [f for f in os.listdir("cogs") if f.endswith(".py")]
for cog in cog_files:
    try:
        await bot.load_extension(f"cogs.{cog[:-3]}")  # Awaiting the load_extension call
        logging.info(f"✅ Loaded cog: {cog}")
    except Exception as e:
        logging.error(f"Failed to load cog {cog}: {e}")

# Make sure the Discord token and Hypixel API key are set
token = os.getenv("DISCORD_TOKEN")
if token is None:
    logging.error("DISCORD_TOKEN is not set in the environment variables.")
else:
    bot.run(token)
