import os
import subprocess
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")  # Set this as an environment variable

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Remove default help command
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user.name}')

@bot.command(name="help")
async def custom_help(ctx):
    help_text = """
**🛠️ Available Commands:**

`/nmap -flag IP`  
‣ Run an Nmap scan with a specified flag and IP.  
‣ Example: `/nmap -sV 1.2.3.4`

`/help`  
‣ Show this help message.
"""
    await ctx.send(help_text)

@bot.event
async def on_message(message):
    await bot.process_commands(message)  # Let commands work

    if message.author.bot:
        return

    if message.content.startswith('/nmap'):
        parts = message.content.split()
        if len(parts) < 3:
            await message.channel.send("Usage: `/nmap -flag IP` (e.g., `/nmap -sV 1.2.3.4`)")
            return

        flag = parts[1]
        ip = parts[2]

        # Basic validation
        if not flag.startswith('-') or any(c in flag for c in ';|&$`'):
            await message.channel.send("Invalid flag.")
            return
        if any(c in ip for c in ';|&$`') or len(ip) > 50:
            await message.channel.send("Invalid IP.")
            return

        await message.channel.send(f"🔍 Running `nmap {flag} {ip}`...")

        try:
            result = subprocess.run(
                ['nmap', flag, ip],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )

            output = result.stdout + result.stderr
            if not output.strip():
                output = "No output received. The host might be down or blocked the scan."
            if len(output) > 1900:
                output = output[:1900] + "\n...Output truncated."

            await message.channel.send(f"```\n{output}\n```")

        except subprocess.TimeoutExpired:
            await message.channel.send("❌ Nmap scan timed out.")
        except Exception as e:
            await message.channel.send(f"⚠️ Error: {str(e)}")

bot.run(TOKEN)
