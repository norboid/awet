import discord
from discord.ext import commands
import os
import requests

class Hypixel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("HYPIXEL_API_KEY")  # Make sure to set this environment variable

    @commands.command(name="stats")
    async def stats(self, ctx, minecraft_username: str):
        """Fetches and displays stats for the given Minecraft username"""
        if not self.api_key:
            await ctx.send("API key not set. Please check the environment variables.")
            return
        
        # Make a request to the Hypixel API to get the player's stats
        url = f"https://api.hypixel.net/player?key={self.api_key}&name={minecraft_username}"
        response = requests.get(url)
        data = response.json()

        if not data['success']:
            await ctx.send(f"Could not find stats for {minecraft_username}. Please check the username.")
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

        await ctx.send(embed=stats_embed)

# Setup function for loading this cog
def setup(bot):
    bot.add_cog(Hypixel(bot))
