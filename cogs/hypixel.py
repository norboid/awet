import discord
from discord.ext import commands
from discord import option
import requests
import os

class Hypixel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="stats", description="Get Hypixel stats by Minecraft username")
    @option("username", description="Minecraft username")
    async def stats(self, ctx, username: str):
        await ctx.defer()

        # Get UUID from Mojang
        uuid_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        uuid_res = requests.get(uuid_url)
        if uuid_res.status_code != 200:
            await ctx.respond(f"❌ Could not find Minecraft user `{username}`.")
            return
        uuid = uuid_res.json()["id"]

        # Get Hypixel stats
        api_key = os.getenv("HYPIXEL_API_KEY")
        hypixel_url = f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}"
        response = requests.get(hypixel_url)
        data = response.json()

        if not data.get("success") or not data.get("player"):
            await ctx.respond(f"❌ Could not retrieve stats for `{username}`.")
            return

        player = data["player"]
        displayname = player.get("displayname", username)
        level = int((player.get("networkExp", 0)) ** 0.5)  # rough estimate
        karma = player.get("karma", 0)

        embed = discord.Embed(title=f"{displayname}'s Hypixel Stats", color=0x00ff00)
        embed.add_field(name="Network Level", value=level, inline=True)
        embed.add_field(name="Karma", value=karma, inline=True)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Hypixel(bot))
