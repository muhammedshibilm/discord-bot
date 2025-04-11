import os
import subprocess
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # Ensure this key is set in your Railway environment

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Create the bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# When the bot is ready, sync the app commands (slash commands)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Define the slash command
@bot.tree.command(name="nmap", description="Run an Nmap scan on a target")
@app_commands.describe(flag="Nmap flag (e.g., -sV)", ip="Target IP address or domain")
async def nmap(interaction: discord.Interaction, flag: str, ip: str):
    # Acknowledge the interaction immediately
    await interaction.response.defer()
    try:
        # Optionally, add -Pn flag if not provided
        flags_list = flag.split()
        if "-Pn" not in flags_list:
            flags_list.append("-Pn")
        
        # Execute the Nmap command; adjust timeout as needed
        result = subprocess.run(['nmap', "--unprivileged", *flags_list, ip],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                timeout=60)
        # Combine stdout and stderr output
        output = result.stdout + result.stderr
        if not output.strip():
            output = "No output received."
        # Truncate output if too long for Discord (max ~2000 characters)
        if len(output) > 1900:
            output = output[:1900] + "\n...Output truncated."
        await interaction.followup.send(f"```{output}```")
    except subprocess.TimeoutExpired:
        await interaction.followup.send("Nmap scan timed out.")
    except Exception as e:
        await interaction.followup.send(f"Error running scan: {str(e)}")

bot.run(TOKEN)
