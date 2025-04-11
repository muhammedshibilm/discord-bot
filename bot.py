import discord
from discord.ext import commands
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command()
async def nmap(ctx, ip: str):
    try:
        await ctx.send(f"Running Nmap on `{ip}`...")
        result = subprocess.run(["nmap", ip], capture_output=True, text=True)
        await ctx.send(f"**Nmap Results for `{ip}`:**\n```{result.stdout[:1900]}```")
    except Exception as e:
        await ctx.send(f"Error: {e}")

bot.run(TOKEN)
