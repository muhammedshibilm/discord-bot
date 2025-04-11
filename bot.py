import os
import subprocess
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Load token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # Replace with your bot token if not using .env

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # For app_commands

# Nmap command
@tree.command(name="nmap", description="Run Nmap scan on a public IP or host")
@app_commands.describe(flags="Nmap flags (like -sV)", target="Target IP or domain")
async def nmap(interaction: discord.Interaction, flags: str, target: str):
    await interaction.response.defer()  # Acknowledge interaction
    try:
        # Run Nmap command
        result = subprocess.run(["nmap", *flags.split(), target], capture_output=True, text=True, timeout=30)
        output = result.stdout[:1900]  # Discord message limit
        await interaction.followup.send(f"```{output}```")
    except subprocess.TimeoutExpired:
        await interaction.followup.send("⏱️ Scan timed out.")
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await tree.sync()
        print(f"🔁 Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

bot.run(TOKEN)
