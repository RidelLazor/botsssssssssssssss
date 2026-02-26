import os
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread

# --- SETUP FLASK (Agar Render tetap menyala) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- SETUP BOT DISCORD ---
TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class RidelLazor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="announce", description="Send a RidelLazor announcement")
    async def announce(self, interaction: discord.Interaction, title: str, message: str, ping: bool = False):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You must be an administrator to use this command.", ephemeral=True)
            return

        embed = discord.Embed(title=f"📢 {title}", description=message, color=0x00BFFF)
        embed.set_footer(text="RidelLazor Announcements")
        embed.timestamp = discord.utils.utcnow()
        content = "@everyone" if ping else None
        await interaction.response.send_message(content=content, embed=embed)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()

async def main():
    keep_alive() # Memulai server web
    async with bot:
        await bot.add_cog(RidelLazor(bot))
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
