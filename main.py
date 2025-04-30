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

    # Sync slash commands with Discord
    try:
        await bot.tree.sync()
        logging.info("Slash commands synced successfully")
    except Exception as e:
        logging.error(f"Error syncing slash commands: {e}")

    # Load extensions dynamically after the bot is ready
    await load_extensions()

async def load_extensions():
    """Load extensions (cogs) dynamically"""
    cog_files = [f for f in os.listdir("cogs") if f.endswith(".py")]
    for cog in cog_files:
        try:
            # Properly await within an async function
            await bot.load_extension(f"cogs.{cog[:-3]}")  # Ensure this is inside an async function
            logging.info(f"✅ Loaded cog: {cog}")
        except Exception as e:
            logging.error(f"Failed to load cog {cog}: {e}")

# Error handling for commands
@bot.event
async def on_command_error(ctx, error):
    logging.error(f"Error: {error}")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I don't recognize that command.")
    else:
        await ctx.send("An error occurred. Please try again later.")

# Make sure the Discord token is set
token = os.getenv("DISCORD_TOKEN")
if token is None:
    logging.error("DISCORD_TOKEN is not set in the environment variables.")
else:
    bot.run(token)
