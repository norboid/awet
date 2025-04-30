import discord
from discord.ext import commands
from discord import app_commands
import os
import requests

class Hypixel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("HYPIXEL_API_KEY")  # Make sure to set this environment variable

    @app_commands.command(name="stats", description="Fetches and displays stats for the given Minecraft username")
    @app_commands.guilds(123456789012345678)  # Replace with your Discord server's ID (optional)
    async def stats(self, interaction: discord.Interaction, minecraft_username: str):
        """Fetches and displays stats for the given Minecraft username"""
        if not self.api_key:
            await interaction.response.send_message("API key not set. Please check the environment variables.")
            return
        
        # Make a request to the Hypixel API to get the player's stats
        url = f"https://api.hypixel.net/player?key={self.api_key}&name={minecraft_username}"
        response = requests.get(url)
        data = response.json()

        if not data['success']:
            await interaction.response.send_message(f"Could not find stats for {minecraft_username}. Please check the username.")
            return
        
        player_data = data['player']
        
        # You can customize the stats you want to show here
        stats_embed = discord.Embed(
            title=f"Stats for {minecraft_username}",
            color=discord.Color.blue()
        )

        # Example: Displaying some basic stats like level and karma
        stats_embed.add_field(name="Level", value=player_data.get('level', 'N/A'), inline=True)
        stats_embed.add_field(name="Karma", value=player_data.get('karma', 'N/A'), inline=True)

        # If you want to display more detailed stats, you can pull them from the player data
        if 'stats' in player_data:
            stats = player_data['stats']
            # Example: Displaying some game stats (e.g., BedWars)
            bedwars_stats = stats.get('Bedwars', {})
            if bedwars_stats:
                stats_embed.add_field(name="BedWars Wins", value=bedwars_stats.get('wins_bedwars', 'N/A'), inline=True)
                stats_embed.add_field(name="BedWars Kills", value=bedwars_stats.get('kills_bedwars', 'N/A'), inline=True)

        await interaction.response.send_message(embed=stats_embed)

# Setup function for loading this cog
async def setup(bot):
    await bot.add_cog(Hypixel(bot))
    await bot.tree.sync()  # Ensure slash commands are synced with Discord
