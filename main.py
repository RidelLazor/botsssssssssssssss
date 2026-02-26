import os
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class RidelLazor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="announce", description="Send a RidelLazor announcement")
    @app_commands.describe(title="Announcement title", message="Announcement message", ping="Ping everyone")
    async def announce(self, interaction: discord.Interaction, title: str, message: str, ping: bool = False):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You must be an administrator to use this command.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"📢 {title}",
            description=message,
            color=0x00BFFF
        )
        embed.set_footer(text="RidelLazor Announcements")
        embed.timestamp = discord.utils.utcnow()

        content = "@everyone" if ping else None

        await interaction.response.send_message(content=content, embed=embed)

    async def cog_load(self):
        await self.bot.tree.sync()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def main():
    async with bot:
        await bot.add_cog(RidelLazor(bot))
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())
