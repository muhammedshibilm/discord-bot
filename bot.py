import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import subprocess

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(e)

@bot.tree.command(name="nmap", description="Run an Nmap scan on a given IP address")
@app_commands.describe(ip="Target IP address")
async def nmap_scan(interaction: discord.Interaction, ip: str):
    await interaction.response.send_message(f"Running nmap on `{ip}`...")
    try:
        # Run the nmap command with a timeout
        result = subprocess.run(["nmap", ip], capture_output=True, text=True, timeout=20)
        output = result.stdout[:1900]  # limiting the output to avoid exceeding Discord's message limit
        await interaction.followup.send(f"```\n{output}\n```")
    except Exception as e:
        await interaction.followup.send(f"Error: {str(e)}")

bot.run(TOKEN)
